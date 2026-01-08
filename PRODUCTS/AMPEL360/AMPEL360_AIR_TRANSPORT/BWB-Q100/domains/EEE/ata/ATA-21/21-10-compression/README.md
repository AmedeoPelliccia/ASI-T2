# ATA 21-10 — Compression Systems

## Overview

This section contains documentation for the **Compression Systems** subsystem of the ATA 21 Air Conditioning system.

## Structure

```text
21-10-compression/
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

- **ATA Section**: 21-10
- **System**: Compression Systems
- **Standard**: ATA iSpec 2200 SNS / S1000D
- **Status**: Active
- **Last Updated**: 2026-01-08
