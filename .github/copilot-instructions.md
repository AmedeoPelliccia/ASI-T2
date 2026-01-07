# Copilot Instructions for ASI-T2

> Purpose: Make Copilot's suggestions, reviews, and codegen **consistent with this repo's rules**, especially the Teknia Token (TT) system **v3.14** (π-tier hybrid tokenomics) and our CI/legal/compliance expectations.

---

## Repository Context (must know)

- **Language/Stack:** Python 3.11+, Markdown, YAML, SVG.  
- **Token System:** Teknia Token (TT) v3.14  
  - **Divisibility:** `1 TT = 360 deg` (integer `deg` only, no fractions)  
  - **Genesis:** `2B TT = 720B deg`  
  - **Founder:** 5% @ genesis → `FOUNDER`  
  - **Fees:** π-tier for **transfers** only; **reward/consume always 0.5%**  
    - Tiers (by **deg**, multiples of Δθmin=2592 deg = 7.2 TT):
      - `≥ 25920 deg (72 TT)` → **31.4 bps** (0.314%)
      - `≥ 259200 deg (720 TT)` → **99 bps** (0.99%)
      - `≥ 2592000 deg (7,200 TT)` → **314 bps** (3.14%)
      - `< 72 TT` → base **50 bps** (0.5%)
  - **Δθmin:** `2592 deg` (7.2 TT) **applies to transfers only**
  - **Auditability:** SHA-256 **hash-chain** (`finance/txlog.jsonl`, `finance/txhead.json`)
  - **Policy integrity:** policy sanity checks in `verify`; config in `finance/teknia.tokenomics.json`
- **Generated & ignored:** `finance/ledger.json`, `finance/txlog.jsonl`, `finance/txhead.json`, `badges/*.svg`

---

## Golden Rules (apply to all suggestions)

1. **Integer math only** for ledger amounts (`deg`). Reject/flag floats; convert `TT` via exact rational → integer `deg` only if it divides cleanly.
2. **Respect Δθmin scope**: enforce multiple of `2592 deg` **for transfers only**; do **not** enforce for reward/consume.
3. **Fee correctness**:
   - Transfers: apply π-tier **based on amount in `deg`** using floor division.
   - Reward/Consume: **always 0.5%** (50 bps), no tiering.
4. **No silent policy drift**: Never change policy semantics in code without updating config/docs/tests and verifying.
5. **Hash-chain integrity**: Any mutation to tx append code must keep `prev → hash(payload)` chain logic and `TXHEAD` sync.
6. **I/O determinism**: Use UTF-8, `newline="
"`, stable JSON canon (`sort_keys=True`, compact separators) for reproducibility.
7. **Security hygiene**:
   - Escape text in **SVG** (`html.escape`, `quote=False`) before injecting into text nodes.
   - Treat all dynamic strings as untrusted; avoid templating into HTML/SVG attributes unescaped.
8. **Tests over examples**: Prefer adding/expanding tests in `tools/test_tek_tokens_v314.py` to lock behavior.
9. **Don't invent files**: Respect `.gitignore` and generated artifacts; do not suggest committing runtime state.
10. **Clarity over cleverness**: Small, auditable diffs; explicit arithmetic; no magic constants—reference Δθmin and tier thresholds symbolically from config when possible.

---

## Style & Formatting

- **Python**: 3.11+, standard library first; no heavy deps in CLI.  
- **JSON**: Canonicalization helpers (stable sort + separators); no trailing commas.  
- **CLI UX**: Helpful error messages; `--json` emits machine-friendly output; human output concise and exact.

---

## Common Pitfalls to Avoid

- ❌ Applying Δθmin to `reward`/`consume`.  
- ❌ Using floats for fees; must be floor of integer arithmetic.  
- ❌ Forgetting to update `verify/replay` paths when fee logic changes.  
- ❌ Outputting locale-dependent numbers in tests (commas/spaces). Normalize or assert numerically.  
- ❌ Writing SVG with unescaped dynamic content.  
- ❌ Modifying generated files in PRs.

---

## Review Checklists

### Token Ops (transfer/reward/consume)
- [ ] Amount parsed → exact integer `deg` (TT → Fraction → `deg`, denominator==1)
- [ ] **Transfer**: `deg % 2592 == 0` enforced
- [ ] Correct fee chosen (π-tier for transfer; 0.5% for reward/consume)
- [ ] Fee computed as `floor(deg * bps / 10000)` using integer math
- [ ] Sender has balance ≥ `(net + fee)`; balances updated atomically
- [ ] Fee credited to `VAULT_SUSTAIN` if enabled
- [ ] TX appended with SHA-256 chain; `TXHEAD` updated
- [ ] `verify` and `replay` still pass locally

### Badge / Output Artifacts
- [ ] Escaped strings in SVG/JSON (`html.escape` for SVG text)
- [ ] File written with `encoding='utf-8', newline='
'`
- [ ] No sensitive or user-controlled attributes added

### Tests
- [ ] π-tier thresholds covered (≥10×, ≥100×, ≥1000× Δθmin + base)
- [ ] Δθmin scope tests (transfer rejects non-multiple; reward/consume allow)
- [ ] `verify` and `replay` invariants stay green
- [ ] Numeric assertions resilient to thousands separators

---

## Preferred Code Patterns

**Canonical JSON write**
```python
json.dump(obj, f, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
```

**SVG text escaping**

```python
import html
def _svg_escape(s: str) -> str:
    return html.escape(str(s), quote=False)
```

**Fee computation (tiers aware)**

```python
fee = (amount_deg * bps_fraction.numerator) // (10000 * bps_fraction.denominator)
net = amount_deg - fee
```

**TX append (hash-chain)**

```python
entry["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
entry["prev"] = prev_hash
entry["hash"] = sha256(prev_hash + canon(entry_without_hash))
```

---

## Commit & PR Guidance

* **Commit messages:** `tools: enforce SVG escaping in badge`, `finance: add π-tier thresholds to config`, `tests: add v3.14 tier coverage`
* **PR description should include:**
  * What changed and why (link to v3.14 rule if relevant)
  * Effects on fees/Δθmin scope/replay/verify
  * Test coverage summary
* **Do not** include generated artifacts in PRs.

---

## Examples of Good Copilot Behavior

* Propose a minimal diff to fix fee rounding to integer floor with tiers, and add a unit test in `tools/test_tek_tokens_v314.py`.
* Replace raw SVG f-strings with escaped helpers and deterministic file writes.
* Normalize number formatting in tests by parsing JSON output (`--json`) or stripping separators.

---

## When Unsure

Prefer:

1. Ask for the relevant config value (Δθmin, tiers) from `finance/teknia.tokenomics.json`.
2. Add/adjust tests to pin intended behavior.
3. Keep changes small and auditable.

*Thank you! This guidance helps align Copilot's suggestions with our transparency, legality, sustainability, meritocracy, accessibility, equity, and fairness principles.*
