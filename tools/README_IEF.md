# IEF · HUELLΔ Tools

This directory contains tools for managing the IEF (IDEALE Evidence Framework) HUELLΔ system for traceability, material passports, and lifecycle event tracking.

## Overview

The HUELLΔ system provides:
- **Event capture** with templates for rapid data collection
- **Badge generation** from verification results (Shields.io-compatible)
- **Material passport assembly** per asset with aggregated metrics
- **Traceability tracking** across lifecycle stages

## Tools

### 1. `ief_badges.py` - Badge Generator

Generates Shields.io-compatible badge JSON endpoints from verification results.

**Features:**
- Aggregates events by asset UID
- Calculates traceability coverage by lifecycle stages
- Extracts and aggregates metrics (energy, CO₂, risk, quality)
- Outputs badges: trace, risk, quality, impact

**Usage:**

```bash
# Generate badges for all assets
python tools/ief_badges.py \
    --verify verification/verify-results.json \
    --root . \
    --out badges/

# Generate badges for specific asset
python tools/ief_badges.py \
    --verify verification/verify-results.json \
    --asset "urn:ideale:component:AAA:BWQ1:FWD-SPAR:SN-000123" \
    --root . \
    --out badges/
```

**Output Structure:**
```
badges/
└── <DOMAIN>/
    └── <SERIAL>/
        ├── trace.json          # Traceability coverage
        ├── risk.json           # Risk level (max)
        ├── quality.json        # Quality score (min)
        ├── impact_energy.json  # Energy consumption
        └── impact_co2.json     # CO₂ emissions
```

**Badge Schema (Shields.io):**
```json
{
  "schemaVersion": 1,
  "label": "Risk",
  "message": "low · 0.10",
  "color": "success"
}
```

**Target Lifecycle Stages:**
- `assemble` - Assembly/manufacturing
- `service` - Service/maintenance
- `transport` - Transportation
- `handoff` - Transfer of custody

**Color Coding:**
- **Traceability**: brightgreen (complete) → green (75%) → yellow (50%) → orange (<50%)
- **Risk**: success (≤0.20) → yellow (≤0.50) → orange (≤0.80) → red (>0.80)
- **Quality**: brightgreen (≥0.98) → green (≥0.95) → yellow (≥0.90) → orange (<0.90)
- **Energy**: brightgreen (≤1 kWh) → green (≤10) → yellow (≤50) → orange (>50)

### 2. `ief_assemble_passport.py` - Passport Assembler

Assembles material passports per asset from verified events.

**Features:**
- Loads verified events for specific asset UID
- Aggregates lifecycle metrics across all events
- Generates passport JSON with metadata and badge links
- Outputs to `evidence/passports/<DOMAIN>/<SERIAL>.json`

**Usage:**

```bash
python tools/ief_assemble_passport.py \
    --verify verification/verify-results.json \
    --asset "urn:ideale:component:AAA:BWQ1:FWD-SPAR:SN-000123" \
    --family AMPEL360 \
    --model BWB \
    --variant Q100 \
    --domain AAA \
    --ata ATA-57 \
    --sbom sbom/AMPEL360-BWQ1.spdx.json \
    --policy-sha sha256:...pinned... \
    --root . \
    --out-root evidence/passports \
    --badges-root badges
```

**Output Structure:**
```
evidence/
└── passports/
    └── <DOMAIN>/
        └── <SERIAL>.json
```

**Passport Schema:**
```json
{
  "passport_version": "0.1",
  "ief_version": "0.1",
  "generated_at": "2025-10-05T16:30:00Z",
  "asset": {
    "uid": "urn:ideale:component:...",
    "family": "AMPEL360",
    "model": "BWB",
    "variant": "Q100",
    "domain": "AAA",
    "ata": "ATA-57"
  },
  "lifecycle": {
    "design_ref": null,
    "manufacture_ref": null,
    "service_state": "unknown"
  },
  "events": [...],
  "calculations": {
    "energy_kwh_total_est": 0.045,
    "co2e_kg_total_est": 0.011,
    "quality_min": 0.97,
    "risk_max": 0.10,
    "coverage": {
      "assemble": true,
      "service": true,
      "transport": true,
      "handoff": false
    }
  },
  "badges": [...],
  "evidence": {...},
  "privacy": {...}
}
```

### 3. Event Templates (`templates/`)

Ready-to-use JSON templates for rapid event capture.

**Available Templates:**
- `event-inspect.json` - Inspection events
- `event-transport.json` - Transport events
- `event-assemble.json` - Assembly events

**Event Schema (IEF v0.1):**
```json
{
  "ief_version": "0.1",
  "event_type": "inspect|transport|assemble|service|handoff",
  "ts": "2025-10-05T12:00:00Z",
  "actor": { "id": "", "role": "", "auth": "" },
  "asset": {
    "uid": "urn:ideale:component:...",
    "passport_ref": "evidence/passports/..."
  },
  "context": {
    "loc_geohash": "ezjnn",
    "env": "HANGAR",
    "temp_c": 21.0,
    "vibe": "low"
  },
  "inputs": [...],
  "signatures": {
    "sigstore_bundle": "signatures/.../evt.bundle.json",
    "policy_hash": "sha256:..."
  },
  "calc": {
    "energy_kwh_est": 0.002,
    "co2e_kg_est": 0.001,
    "quality_score": 0.99,
    "risk_score": 0.05,
    "conformance": ["IEF-0.1", "TFA-ATA-57"],
    "reputation_weight": 0.92
  }
}
```

## CI Integration Example

Add to your `.github/workflows/` after verification:

```yaml
- name: Build badges from events
  run: |
    python tools/ief_badges.py \
      --verify verification/verify-results.json \
      --root . \
      --out badges/

- name: Assemble material passport (example asset)
  run: |
    python tools/ief_assemble_passport.py \
      --verify verification/verify-results.json \
      --asset "urn:ideale:component:AAA:BWQ1:FWD-SPAR:SN-000123" \
      --family AMPEL360 --model BWB --variant Q100 \
      --domain AAA --ata ATA-57 \
      --sbom sbom/AMPEL360-BWQ1.spdx.json \
      --policy-sha $(cat policies/POLICY.SHA256) \
      --root . \
      --out-root evidence/passports \
      --badges-root badges
```

## Design Principles

### "El evento sin firma no existe"
Events without signatures/bundles are not verified. The verification system enforces signature requirements.

### "Bloquea con elegancia"
Risk badges turn red/blocked when `risk_max > 0.8`, enabling graceful blocking of unsafe shipments.

### "Cada badge es una flor digital"
Badge endpoints live in `badges/.../*.json`, ready for Shields.io display in READMEs or portals.

## Dependencies

**None!** All tools use only Python standard library:
- `argparse` - CLI argument parsing
- `json` - JSON handling
- `pathlib` - Path operations
- `datetime` - Timestamp handling
- `sys` - System exit codes

## File Locations

**Configuration:**
- Event templates: `templates/event-*.json`
- Verification input: `verification/verify-results.json` (generated by verification tool)

**Outputs (git-ignored):**
- Badges: `badges/<DOMAIN>/<SERIAL>/*.json`
- Passports: `evidence/passports/<DOMAIN>/<SERIAL>.json`

**SBOM Reference:**
- `sbom/*.spdx.json` - Software Bill of Materials

## Version History

- **v0.1** - Initial release
  - Badge generator with 5 badge types
  - Passport assembler with full metadata
  - Three event templates (inspect, transport, assemble)
  - IEF v0.1 schema support

## Related Documentation

- [TOKENS.md](../docs/TOKENS.md) - Teknia Token system
- [UTCS Whitepaper](../WHITEPAPERS/MASTER_WHITEPAPER_3_UTCS.md) - Evidence framework
- [Copilot Instructions](../.github/copilot-instructions.md) - Development guidelines

## License

See [LICENSES/](../LICENSES/) for licensing information.
