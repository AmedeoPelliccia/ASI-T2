# KNU Distribution Example Workflow

This example demonstrates a complete workflow for distributing Teknia Tokens (TT) to Knowledge Units (KNUs) within KNOT K06.

## Scenario

KNOT K06 ("Data governance SSOT schemas") has a prize pool of **150 TT** to distribute among 3 KNUs:

1. **alice** - High effort, high impact with spillover
2. **bob** - Medium effort, medium impact  
3. **charlie** - Lower effort, lower impact

## Prerequisites

```bash
# Initialize TT ledger (if not already done)
cd /path/to/ASI-T2
python tools/tek_tokens.py init

# Check initial balances
python tools/tek_tokens.py balance
```

## Step 1: Prepare KNU Data

Create `examples/knus_k06.json`:

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
      "artifacts": [
        "docs/data-governance/schema-v2.md",
        "https://github.com/org/repo/pull/123"
      ],
      "validated_by": "knot_owner",
      "validated_at": "2026-01-10T12:00:00Z"
    },
    {
      "knu_id": "KNU-K06-00-002",
      "knot_id": "K06",
      "owner": "bob",
      "E_pred": 3.0,
      "dR_primary": 15.0,
      "dR_adj_sum": 5.0,
      "status": "merged",
      "artifacts": [
        "docs/data-governance/ssot-implementation.md"
      ],
      "validated_by": "knot_owner",
      "validated_at": "2026-01-10T12:30:00Z"
    },
    {
      "knu_id": "KNU-K06-00-003",
      "knot_id": "K06",
      "owner": "charlie",
      "E_pred": 2.0,
      "dR_primary": 5.0,
      "dR_adj_sum": 0.0,
      "status": "merged",
      "artifacts": [
        "docs/data-governance/glossary.md"
      ],
      "validated_by": "knot_owner",
      "validated_at": "2026-01-10T13:00:00Z"
    }
  ]
}
```

## Step 2: Validate Eligibility

Verify all KNUs meet eligibility requirements:

```bash
python tools/knu_distribution.py validate --input examples/knus_k06.json
```

**Expected output:**

```
============================================================
KNU Eligibility Validation
============================================================

✓ KNU-K06-00-001       alice           VALID
✓ KNU-K06-00-002       bob             VALID
✓ KNU-K06-00-003       charlie         VALID

============================================================
Valid: 3, Invalid: 0
============================================================
```

## Step 3: Calculate Weights

Preview the distribution calculation:

```bash
python tools/knu_distribution.py calculate --knot K06 --input examples/knus_k06.json
```

**Expected output:**

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

### Weight Calculation Breakdown

**For alice (KNU-K06-00-001):**

1. **Effort contribution**: E = 5.0, Ê = 5.0/(5.0+3.0+2.0) = 0.50
2. **Impact calculation**: I = 30.0 + 0.5×10.0 = 35.0
3. **Impact contribution**: Î = 35.0/(35.0+17.5+5.0) = 0.609
4. **Final weight**: w = 0.3×0.50 + 0.7×0.609 = **0.5761**
5. **Token allocation**: 150 TT × 0.5761 = **86.41 TT** (31,108 deg)

## Step 4: Generate Report

Create a detailed JSON report:

```bash
python tools/knu_distribution.py report --knot K06 --input examples/knus_k06.json --output examples/k06_report.json
```

**Report contents** (`examples/k06_report.json`):

```json
{
  "knot_id": "K06",
  "pool_tt": 150.0,
  "pool_description": "Data governance SSOT schemas",
  "parameters": {
    "alpha": 0.3,
    "lambda_spillover": 0.5
  },
  "distributions": [
    {
      "knu_id": "KNU-K06-00-001",
      "owner": "alice",
      "effort": 5.0,
      "impact_primary": 30.0,
      "impact_spillover": 10.0,
      "weight": 0.5761,
      "tokens_tt": 86.41,
      "tokens_deg": 31108
    },
    {
      "knu_id": "KNU-K06-00-002",
      "owner": "bob",
      "effort": 3.0,
      "impact_primary": 15.0,
      "impact_spillover": 5.0,
      "weight": 0.3030,
      "tokens_tt": 45.46,
      "tokens_deg": 16364
    },
    {
      "knu_id": "KNU-K06-00-003",
      "owner": "charlie",
      "effort": 2.0,
      "impact_primary": 5.0,
      "impact_spillover": 0.0,
      "weight": 0.1209,
      "tokens_tt": 18.13,
      "tokens_deg": 6528
    }
  ],
  "summary": {
    "total_knus": 3,
    "total_weight": 1.0,
    "total_tt": 150.0
  }
}
```

## Step 5: Dry-Run Distribution

Test the distribution without executing rewards:

```bash
python tools/knu_distribution.py distribute --knot K06 --input examples/knus_k06.json --dry-run
```

**Expected output:**

```
============================================================
KNU Distribution: K06
============================================================

[DRY-RUN] KNU-K06-00-001 → alice: 86.41 TT (31,108 deg)
[DRY-RUN] KNU-K06-00-002 → bob: 45.46 TT (16,364 deg)
[DRY-RUN] KNU-K06-00-003 → charlie: 18.13 TT (6,528 deg)

============================================================
Distribution Complete
============================================================
KNOT: K06
KNUs distributed: 3
Total allocated: 150.00 TT (54,000 deg)
============================================================
```

## Step 6: Execute Distribution

Execute the actual token distribution:

```bash
python tools/knu_distribution.py distribute --knot K06 --input examples/knus_k06.json
```

**Expected output:**

```
============================================================
KNU Distribution: K06
============================================================

✓ KNU-K06-00-001 → alice: 86.41 TT (31,108 deg) [TX-000123]
✓ KNU-K06-00-002 → bob: 45.46 TT (16,364 deg) [TX-000124]
✓ KNU-K06-00-003 → charlie: 18.13 TT (6,528 deg) [TX-000125]

============================================================
Distribution Complete
============================================================
KNOT: K06
KNUs distributed: 3
Total allocated: 150.00 TT (54,000 deg)
============================================================
```

## Step 7: Verify Results

### Check TT Balances

```bash
# Check individual balances
python tools/tek_tokens.py balance --account alice
python tools/tek_tokens.py balance --account bob
python tools/tek_tokens.py balance --account charlie
```

**Expected output (for alice):**

```
Account: alice
  Balance: 30,978 deg = 86.05 TT
```

*Note: Actual balance is slightly less due to 0.5% reward fee (129 deg)*

### Check Distribution Ledger

```bash
cat finance/knu_ledger.csv
```

**Expected output:**

```csv
timestamp,knot_id,knu_id,owner,E_pred,dR_primary,dR_adj_sum,weight,tokens_tt,tokens_deg,tx_id,validated_by
2026-01-10T14:30:00Z,K06,KNU-K06-00-001,alice,5.0,30.0,10.0,0.5761,86.41,31108,TX-000123,knot_owner
2026-01-10T14:30:01Z,K06,KNU-K06-00-002,bob,3.0,15.0,5.0,0.3030,45.46,16364,TX-000124,knot_owner
2026-01-10T14:30:02Z,K06,KNU-K06-00-003,charlie,2.0,5.0,0.0,0.1209,18.13,6528,TX-000125,knot_owner
```

### Check Transaction Log

```bash
tail -n 3 finance/txlog.jsonl | python -m json.tool
```

**Expected output:**

```json
{
  "tx_id": "TX-000123",
  "type": "reward",
  "timestamp": "2026-01-10T14:30:00Z",
  "from": "TREASURY",
  "to": "alice",
  "amount_deg": 31108,
  "amount_tt": 86.41,
  "fee_deg": 129,
  "fee_tt": 0.36
}
```

### Verify Ledger Integrity

```bash
python tools/tek_tokens.py verify
```

**Expected output:**

```
✓ Verification PASSED
✓ Policy hash: a1b2c3d4e5f6...
✓ Total supply: 720,000,000,000 deg
✓ Accounts: 7
✓ Transactions: 125
```

## Summary

This workflow demonstrates:

1. ✅ **Eligibility validation** - All KNUs meet requirements
2. ✅ **Weight calculation** - Using effort (30%) and impact (70%) with spillover
3. ✅ **Report generation** - Detailed JSON output for auditing
4. ✅ **Dry-run testing** - Preview before execution
5. ✅ **Token distribution** - Execute via tek_tokens.py reward
6. ✅ **Traceability** - Full audit trail in CSV and JSONL logs
7. ✅ **Verification** - Ledger integrity maintained

## Formula Recap

The distribution uses:

```
w_i = α·Ê_i + (1-α)·Î_i
T_i = P_k · w_i
```

Where:
- **α = 0.30** (30% effort, 70% impact)
- **λ = 0.50** (spillover worth 50% of direct impact)
- **P_k = 150 TT** (K06 pool)

This balances:
- **Effort recognition** - Rewards predicted work investment
- **Impact weighting** - Prioritizes uncertainty reduction
- **Spillover bonus** - Incentivizes cross-KNOT collaboration

## Next Steps

- Configure additional KNOT pools (K01-K14)
- Automate KNU data collection from GitHub milestones
- Integrate with GitHub Actions for milestone-based distribution
- Expand adjacency graph as KNOTs evolve
- Monitor distribution patterns and adjust α/λ parameters if needed
