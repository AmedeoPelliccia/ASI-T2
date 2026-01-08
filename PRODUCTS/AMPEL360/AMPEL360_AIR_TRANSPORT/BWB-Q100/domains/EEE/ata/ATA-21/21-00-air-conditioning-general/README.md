# ATA 21-00 — Air Conditioning - General

## Overview

This section contains documentation for the **Air Conditioning - General** subsystem of the ATA 21 Air Conditioning system.

## Structure

```text
21-00-air-conditioning-general/
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

- **ATA Section**: 21-00
- **System**: Air Conditioning - General
- **Standard**: ATA iSpec 2200 SNS / S1000D
- **Status**: Active
- **Last Updated**: 2026-01-08
