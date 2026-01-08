# ATA 21-60 — Temperature Control

## Overview

This section contains documentation for the **Temperature Control** subsystem of the ATA 21 Air Conditioning system.

## Structure

```text
21-60-temperature-control/
├── SSOT/                    # Single Source of Truth
└── PUB/                     # Publication views
    ├── AMM/                 # Aircraft Maintenance Manual
    │   ├── CSDB/            # Common Source Database
    │   │   ├── DM/          # Data Modules
    │   │   ├── PM/          # Publication Modules
    │   │   ├── DML/         # Data Module Lists
    │   │   ├── ICN/         # Illustrations/Graphics
    │   │   ├── BREX/        # Business Rules Exchange
    │   │   ├── COMMON/      # Common information sets
    │   │   └── APPLICABILITY/ # Applicability statements
    │   ├── EXPORT/          # Export outputs
    │   ├── bindings.csv     # Publication bindings
    │   └── csdb.profile.yaml # CSDB profile configuration
    └── IPC/                 # Illustrated Parts Catalog
        └── (same structure as AMM)
```

## Document Control

- **ATA Section**: 21-60
- **System**: Temperature Control
- **Standard**: ATA iSpec 2200 SNS / S1000D
- **Status**: Active
- **Last Updated**: 2026-01-08
