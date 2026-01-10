# Teknia Token (TT) — Rules & Spec v3.14

**Teknia Token (TT)** is the native accounting unit for IDEALE/ASI-T2 interactions.  
It supports verifiable incentives for knowledge exchange and a deterministic, integer-only ledger.

---

## Objectives

- Incentivize **Context eXchange Profile (CXP)** publishing and consumption with a repo-scoped budget (TT).
- Track costs/rewards in a verifiable **append-only** ledger with cryptographic integrity.

---

## Roles & Accounts

**Human & org roles**
- `treasury` — repository budget holder
- `user/<github-username>` — individual contributors
- `domain/<DDD>` — domain budgets (e.g., `domain/AAA`) *(future/optional)*
- `sink:<event>` — cost sinks (e.g., `sink:consume`)

**System accounts**
- `TREASURY` — main treasury (receives genesis minus founder allocation)
- `FOUNDER` — founder allocation
- `VAULT_SUSTAIN` — accumulates sustainability fees

> You can use either the lowercase “Rules” style (e.g., `treasury`) in docs or the uppercase system accounts in the CLI; both map cleanly in the tooling.

---

## Token Specifications (v3.14)

- **Symbol**: TT  
- **Genesis Supply**: **2,000,000,000 TT**  
- **Divisibility**: `1 TT = 360 deg` (integer **deg** only; no fractions)  
- **Founder Allocation**: **5%** (100M TT / 36B deg) at genesis  
- **Treasury at Genesis**: **95%** (1.9B TT / 684B deg)  
- **Minimum Transfer Quantum**: **2,592 deg** (**7.2 TT**) — **transfers only**  
- **Sustain Fees**: π-tier schedule on transfers; base 0.5% on reward/consume  
- **Policy Immutability**: SHA-256 of policy stored in ledger and checked by `verify`

### Divisibility & Precision

All arithmetic uses **integer deg**:
```

1 TT = 360 deg
0.5 TT = 180 deg  ✓
0.25 TT = 90 deg  ✓
0.01 TT = 3.6 deg ✗ (not integer → invalid)

````

### Minimum Transfer Quantum (Δθmin)

- **min_transfer_deg** = **2,592 deg** = **7.2 TT**  
- Applies to **transfer** only (configurable).  
- **reward/consume** have **no quantum restriction** (still integer deg).

Valid transfer examples:
- ✓ 2,592 deg (7.2 TT)
- ✓ 25,920 deg (72 TT)
- ✗ 360 deg (1 TT) — not a multiple of 2,592

### Sustain Fee Mechanism (π-tiers for transfers)

| Amount (TT) | Amount (deg) | Tier BPS | Fee %  | Notes                |
|-------------|---------------|----------|--------|----------------------|
| ≥ 7,200     | ≥ 2,592,000   | 314      | 3.14%  | 1000× Δθmin          |
| ≥ 720       | ≥ 259,200     | 99       | 0.99%  | 100× Δθmin           |
| ≥ 72        | ≥ 25,920      | 31.4     | 0.314% | 10× Δθmin            |
| < 72        | < 25,920      | 50       | 0.5%   | Base transfer tier   |

**Fee calculation**: `(amount_deg × tier_bps) // 10000` (integer floor division)  
**Reward/Consume fee**: fixed **0.5%** (`50 bps`) → `(amount_deg × 50) // 10000`  
**Fee sink**: all fees credit **`VAULT_SUSTAIN`** and are **paid by sender**.

---

## Economics: Events & Pricing (CXP)

Automatable pricing hooks aligned to repo workflows:

- **CXP Publish** → *reward* `+ prices.cxp_publish_reward` TT to `user/<actor>` (from `treasury`) **iff** `auto.reward_on_publish = true`.
- **CXP Consume** → *charge* `− prices.cxp_consume_cost` TT from `treasury` to `sink:consume` **iff** `auto.charge_on_consume = true`.

See configuration in `finance/teknia.tokenomics.json` (or `teknia.tokenomics.nofee.json`).

---

## Configuration Files

- **Tokenomics**: `finance/teknia.tokenomics.json`  
  - `deg_per_tt: 360`
  - `min_transfer_deg: 2592`
  - `sustain_fee_tiers` as above
  - policy hashing & validation rules

- **Ledger (balances + tx + policy hash)**: `finance/ledger.json`
- **Transaction log (append-only)**: `finance/txlog.jsonl`
- **Head pointer**: `finance/txhead.json`
- **Badge output (example)**: `badges/tt-verified.svg` *(via CLI)*

---

## CLI — `tools/tek_tokens.py` (v3.14)

> Python 3.8+. Integer-only arithmetic in **deg**, policy hashing, π-tier fees, min transfer quantum.

### Init

```bash
# default config (π-tier fees)
python tools/tek_tokens.py init

# use alternate config (no-fee)
python tools/tek_tokens.py --config finance/teknia.tokenomics.nofee.json init
````

Creates:

* `TREASURY`: 684,000,000,000 deg (1.9B TT)
* `FOUNDER`: 36,000,000,000 deg (100M TT)
* `VAULT_SUSTAIN`: 0 deg

### Balances

```bash
python tools/tek_tokens.py balance
python tools/tek_tokens.py balance --account TREASURY
python tools/tek_tokens.py --eur-per-tt 0.10 balance
```

### Transfers (π-tiers, **must** be multiple of 7.2 TT)

```bash
python tools/tek_tokens.py transfer --from TREASURY --to alice --tt 7.2
python tools/tek_tokens.py transfer --from TREASURY --to bob   --tt 72
```

### Rewards & Consume (base 0.5% fee, **no** min quantum)

```bash
python tools/tek_tokens.py reward  --to alice       --tt 3
python tools/tek_tokens.py consume --from user/bob  --tt 2
```

### Quotes (no mutation)

```bash
python tools/tek_tokens.py quote --op transfer --tt 720
python tools/tek_tokens.py quote --op reward   --tt 72
```

### Verify & Badge

```bash
python tools/tek_tokens.py verify
python tools/tek_tokens.py badge --out badges/tt-verified.svg
```

---

## Automation Hooks (CXP)

Typical GitHub Actions integration:

```bash
# On CXP Publish
python tools/tek_tokens.py auto \
  --event cxp-publish \
  --actor github_username \
  --run-id 12345

# On CXP Consume
python tools/tek_tokens.py auto \
  --event cxp-consume \
  --actor github_username \
  --run-id 12346
```

Toggle behavior via `auto.*` flags in tokenomics config.

---

## Validation Rules

1. Amounts must resolve to **integer deg**.
2. **Transfer** amounts must be **multiples of 2,592 deg** (7.2 TT).
3. Source account must exist and have sufficient balance.
4. No negative balances; sum of balances equals **genesis supply deg**.
5. `verify` checks policy hash, chain consistency, and supply invariants.

Example check function (conceptual):

```python
def is_valid_transfer_deg(amount_deg: int) -> bool:
    return amount_deg > 0 and (amount_deg % 2592 == 0)
```

---

## Ledger Model

* **Format**: `finance/ledger.json` (balances + policy + metadata), `finance/txlog.jsonl` (append-only tx), `finance/txhead.json` (chain head).
* **Immutability**: each tx links prior hash; `verify` recomputes and checks chain & policy hash.
* **Corrections**: via compensating transactions only (no in-place edits).

**Illustrative transaction entry**:

```json
{
  "tx_id": "TX-000123",
  "type": "transfer",
  "timestamp": "2025-10-04T12:00:00Z",
  "from": "TREASURY",
  "to": "alice",
  "amount_deg": 25920,
  "fee_deg": 81,
  "policy_hash": "sha256:...",
  "prev": "TX-000122",
  "hash": "sha256:..."
}
```

---

## Domain Allocation (Optional)

Initial ideas for distributing TT from treasury:

1. **Equal split** across domains (`AAA..PPP`)
2. **Activity-based** by contribution metrics
3. **Project-based** by portfolio priorities

> Implement with `TRANSFER` transactions from `TREASURY` to `domain/<DDD>`.

---

## Security & Governance

* **Append-only** ledger with hash chaining
* **Policy immutability** via stored SHA-256
* **PR-gated** changes; CI verifies `balance` + `verify`
* **Exportable** badges and reports for transparency

---

## Badge Endpoint (Shields)

(Optional) Shields endpoint JSON:

```json
{
  "schemaVersion": 1,
  "label": "Teknia TT",
  "message": "10000 TT",
  "color": "blue"
}
```

Embed in README:

```markdown
![Teknia TT](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/<org>/<repo>/main/finance/badges/tt-balance.json)
```

---

## KNU (Knowledge Unit) Reward Distribution

**KNU Distribution System** extends TT v3.14 to allocate rewards based on effort and impact metrics within Knowledge Network Operational Tasks (KNOTs).

### Distribution Formula

Token allocation uses a weighted combination of normalized effort and impact:

```
w_i = α·Ê_i + (1-α)·Î_i
T_i = P_k · w_i
```

**Components:**

- **P_k** — Prize pool in TT for the KNOT (e.g., 150 TT for K06)
- **E_i** — Predicted effort for KNU i (story points or hours)
- **Ê_i** — Normalized effort: `E_i / Σ E_i` across all KNUs
- **I_i** — Effective impact: `ΔR_k,i + λ·S_i`
- **Î_i** — Normalized impact: `I_i / Σ I_i` across all KNUs
- **ΔR_k,i** — Direct residue reduction (uncertainty resolved, 0-100)
- **S_i** — Spillover impact from adjacent KNOTs: `Σ(a_k→j · ΔR_j,i)`
- **a_k→j** — Adjacency weight between KNOT k and j (0-1)
- **w_i** — Final weight for KNU i (weights sum to 1.0)
- **T_i** — Token allocation for KNU i

**Default Parameters:**

- **α = 0.30** → 30% effort weight, 70% impact weight
- **λ = 0.50** → spillover worth 50% of direct impact

### Example Calculation

Given KNOT K06 with pool = 150 TT and 3 KNUs:

| KNU | Owner | E_pred | ΔR_primary | ΔR_adj | Status |
|-----|-------|--------|------------|--------|--------|
| KNU-K06-00-001 | alice | 5.0 | 30.0 | 10.0 | merged |
| KNU-K06-00-002 | bob | 3.0 | 15.0 | 5.0 | merged |
| KNU-K06-00-003 | charlie | 2.0 | 5.0 | 0.0 | merged |

**Step 1: Normalize effort**

- Total effort: 5 + 3 + 2 = 10
- Ê_alice = 5/10 = 0.50
- Ê_bob = 3/10 = 0.30
- Ê_charlie = 2/10 = 0.20

**Step 2: Calculate effective impact (λ = 0.50)**

- I_alice = 30 + 0.50×10 = 35
- I_bob = 15 + 0.50×5 = 17.5
- I_charlie = 5 + 0.50×0 = 5

**Step 3: Normalize impact**

- Total impact: 35 + 17.5 + 5 = 57.5
- Î_alice = 35/57.5 = 0.609
- Î_bob = 17.5/57.5 = 0.304
- Î_charlie = 5/57.5 = 0.087

**Step 4: Calculate weights (α = 0.30)**

- w_alice = 0.30×0.50 + 0.70×0.609 = 0.576
- w_bob = 0.30×0.30 + 0.70×0.304 = 0.303
- w_charlie = 0.30×0.20 + 0.70×0.087 = 0.121

**Step 5: Allocate tokens**

- T_alice = 150 × 0.576 = 86.4 TT (31,104 deg)
- T_bob = 150 × 0.303 = 45.5 TT (16,380 deg)
- T_charlie = 150 × 0.121 = 18.1 TT (6,516 deg)

### Spillover Mechanism

Spillover captures cross-KNOT impact via adjacency weights. For example, if:

- KNOT K06 is adjacent to K01, K04, K05, K07
- A KNU in K06 resolves uncertainty that benefits K01 (adjacency weight = 0.4)
- The spillover contribution is: `S_i += 0.4 × ΔR_K01,i`

**Adjacency graph** (excerpt):

```json
{
  "K06": {
    "K01": 0.4,
    "K04": 0.3,
    "K05": 0.3,
    "K07": 0.4
  }
}
```

Spillover rewards work that benefits multiple KNOTs, promoting cross-functional collaboration.

### Eligibility Rules

For a KNU to be eligible for distribution:

1. **Status**: Must be `accepted` or `merged` (not `pending` or `rejected`)
2. **Artifacts**: Must include evidence links (documents, PRs, commits)
3. **Validation**: Must be validated by KNOT owner with timestamp

**Validation fields:**

```json
{
  "validated_by": "knot_owner_username",
  "validated_at": "2026-01-10T00:00:00Z"
}
```

### CLI Usage

#### Distribute Rewards

```bash
# Full distribution with TT rewards
python tools/knu_distribution.py distribute --knot K06 --input knus.json

# Dry-run (calculate without executing)
python tools/knu_distribution.py distribute --knot K06 --input knus.json --dry-run
```

#### Calculate Weights

```bash
# Preview weight calculation
python tools/knu_distribution.py calculate --knot K06 --input knus.json
```

**Output:**

```
============================================================
Weight Calculation: K06
Pool: 150.0 TT
α (effort weight): 0.3
λ (spillover factor): 0.5
============================================================

KNU-K06-00-001       alice           w=0.5761 →    86.41 TT
KNU-K06-00-002       bob             w=0.3030 →    45.46 TT
KNU-K06-00-003       charlie         w=0.1209 →    18.13 TT

============================================================
Total weight: 1.000000 (should be 1.0)
============================================================
```

#### Validate Eligibility

```bash
# Check KNU eligibility
python tools/knu_distribution.py validate --input knus.json
```

#### Generate Report

```bash
# JSON report
python tools/knu_distribution.py report --knot K06 --input knus.json --output report.json
```

### KNU Input Format

KNU entries are provided in JSON format:

```json
{
  "knus": [
    {
      "knu_id": "KNU-K06-00-001",
      "knot_id": "K06",
      "owner": "alice",
      "E_pred": 5.0,
      "dR_primary": 30.0,
      "dR_adj_sum": 10.0,
      "status": "merged",
      "artifacts": ["evidence/k06-001.md", "https://github.com/.../pull/123"],
      "validated_by": "knot_owner",
      "validated_at": "2026-01-10T00:00:00Z"
    }
  ]
}
```

**Field descriptions:**

- `knu_id` — Unique identifier (format: `KNU-<KNOT>-<SEQ>-<ID>`)
- `knot_id` — Parent KNOT (K01-K14)
- `owner` — GitHub username or account to receive tokens
- `E_pred` — Predicted effort (story points, hours, or normalized units)
- `dR_primary` — Direct residue reduction (0-100, uncertainty resolved)
- `dR_adj_sum` — Pre-calculated spillover from adjacent KNOTs
- `status` — Lifecycle status (`pending`, `accepted`, `merged`, `rejected`)
- `artifacts` — Evidence links (documents, PRs, commits, issues)
- `validated_by` — KNOT owner username who validated
- `validated_at` — Validation timestamp (ISO 8601)

### KNOT Pool Allocations

Current pool allocations (total: 1,590 TT):

| KNOT | Pool (TT) | Description |
|------|-----------|-------------|
| K01  | 100       | Certification authority basis |
| K02  | 100       | ConOps command authority readiness |
| K03  | 120       | Hazard management cryogenic/fire |
| K04  | 100       | Interfaces geometry ICDs datums |
| K05  | 150       | Model fidelity uncertainty budgets |
| K06  | 150       | Data governance SSOT schemas |
| K07  | 200       | AI autonomy assurance monitoring |
| K08  | 100       | Cybersecurity threat mitigation |
| K09  | 100       | Test verification qualification |
| K10  | 100       | Industrial readiness supply chain |
| K11  | 100       | Human factors training readiness |
| K12  | 120       | Spaceport ground infrastructure |
| K13  | 150       | MRO PHM health monitoring |
| K14  | 100       | Regulatory evolution compliance |

**Total allocated:** 1,590 TT across 14 KNOTs

### Integration with TT System

KNU distribution integrates with TT v3.14 reward mechanism:

1. **Calculate weights** using effort + impact formula
2. **Convert to deg** (1 TT = 360 deg) for integer arithmetic
3. **Execute rewards** via `tek_tokens.py reward --to <owner> --tt <amount>`
4. **Apply 0.5% fee** (base rate, not π-tier) on each reward
5. **Log transaction** to `finance/txlog.jsonl` with hash chain
6. **Record distribution** to `finance/knu_ledger.csv`

**Transaction flow:**

```
KNU Input → Validate → Calculate Weights → Execute Rewards → Update Ledgers
    ↓           ↓             ↓                   ↓                ↓
knus.json   eligibility   w_i = α·Ê + (1-α)·Î   tek_tokens.py   txlog.jsonl
                                                                 knu_ledger.csv
```

### Distribution Ledger

All KNU distributions are logged to `finance/knu_ledger.csv`:

```csv
timestamp,knot_id,knu_id,owner,E_pred,dR_primary,dR_adj_sum,weight,tokens_tt,tokens_deg,tx_id,validated_by
2026-01-10T12:00:00Z,K06,KNU-K06-00-001,alice,5.0,30.0,10.0,0.5761,86.41,31108,TX-000123,knot_owner
2026-01-10T12:00:01Z,K06,KNU-K06-00-002,bob,3.0,15.0,5.0,0.3030,45.46,16364,TX-000124,knot_owner
```

This provides an auditable record of all distributions with full traceability to TT transactions.

### Configuration Files

- **Pool config**: `finance/knu_pools.json` — KNOT pools, α, λ parameters
- **Adjacency graph**: `finance/knu_adjacency.json` — Cross-KNOT weights
- **Distribution ledger**: `finance/knu_ledger.csv` — Distribution records

All configurations are committed to git for transparency and versioning.

---

## Roadmap

1. **Label-driven rewards** (`tt:reward-<n>` on PRs)
2. **Signatures** for tx (GPG/OIDC job claims)
3. **Domain budgets** with scheduled top-ups
4. **Folder-based attribution** of costs/rewards
5. **Quoting in EUR** via energy/price models
6. **Automated KNU distribution** via GitHub Actions on milestone completion

---

## See Also

* Tokenomics config — `finance/teknia.tokenomics.json`
* Optional no-fee config — `finance/teknia.tokenomics.nofee.json`
* KNU pools config — `finance/knu_pools.json`
* KNU adjacency graph — `finance/knu_adjacency.json`
* TT CLI — `tools/tek_tokens.py`
* KNU distribution CLI — `tools/knu_distribution.py`
* Repo README — `README.md`

```

