---
id: ATA-21-OV-0001
project: PRODUCTS/AMPEL360/BWB-Q100
artifact: /home/runner/work/ASI-T2/ASI-T2/PRODUCTS/AMPEL360/BWB-Q100/domains/EEE/ata/21/README.md
llc: SYSTEMS
classification: INTERNAL–EVIDENCE-REQUIRED
version: 1.0.0
release_date: 2026-01-08
maintainer: "ASI-T Architecture Team"
bridge: "CB→QB→UE→FE→FWD→QS"
ethics_guard: MAL-EEM
utcs_mi: v5.0
canonical_hash: "TBD"
---
# ATA 21 — Air Conditioning (ATA iSpec 2200 SNS Structure)

## Overview

This directory contains the **ATA 21 Air Conditioning/Pressurization** system documentation structured according to the **ATA iSpec 2200 Standard Numbering System (SNS)** with S1000D CSDB publication management.

## Purpose

The ATA SNS structure enables:
- Compliance with ATA iSpec 2200 standard
- S1000D-based technical publication management
- Industry-standard maintenance manual organization
- Illustrated parts catalog structuring
- Integration with existing aviation documentation systems

## Directory Structure

The structure follows the **ATA SNS subject-level (21-xx-yy)** format where:
- `xx` = **Section** (3rd–4th digits)
- `yy` = **Subject** (5th–6th digits)

### Sections

```text
ATA-21-air-conditioning/
├── 21-00-air-conditioning-general/          # General information
├── 21-10-compression/                       # Compression systems
├── 21-20-distribution/                      # Distribution systems
├── 21-30-pressurization-control/            # Pressurization control
├── 21-40-heating/                           # Heating systems
├── 21-50-cooling/                           # Cooling systems
├── 21-60-temperature-control/               # Temperature control
└── 21-70-moisture-air-contaminant-control/  # Moisture/air contaminant control
```

### Subject Structure

Each section contains subjects following the pattern `21-xx-yy-<subject-name>/`:
- `21-xx-00-<section-name>/` — General subject for each section
- `21-xx-YY-<subject-name>/` — Additional subjects as defined by ATA SNS extract

### SSOT and PUB Structure

Each subject directory contains:

```text
21-xx-yy-<subject-name>/
├── SSOT/                           # Single Source of Truth
└── PUB/                            # Publication views
    ├── AMM/                        # Aircraft Maintenance Manual
    │   ├── CSDB/                   # Common Source Database
    │   │   ├── DM/                 # Data Modules
    │   │   ├── PM/                 # Publication Modules
    │   │   ├── DML/                # Data Module Lists
    │   │   ├── ICN/                # Illustrations/Graphics
    │   │   ├── BREX/               # Business Rules Exchange
    │   │   ├── COMMON/             # Common information sets
    │   │   └── APPLICABILITY/      # Applicability statements
    │   ├── EXPORT/                 # Export outputs
    │   ├── bindings.csv            # Publication bindings
    │   └── csdb.profile.yaml       # CSDB profile configuration
    └── IPC/                        # Illustrated Parts Catalog
        └── (same structure as AMM)
```


## S1000D CSDB Structure

The **CSDB (Common Source Database)** follows the S1000D standard and contains:

- **DM** (Data Modules): Individual documentation units
- **PM** (Publication Modules): Publication structure definitions
- **DML** (Data Module Lists): Lists referencing data modules
- **ICN** (Illustrations): Graphics, diagrams, and illustrations
- **BREX** (Business Rules Exchange): Validation rules and constraints
- **COMMON** (Common Information Sets): Reusable content
- **APPLICABILITY** (Applicability Statements): Product/variant applicability

## Publication Views

Each subject can have multiple publication views (SUB_ID):
- **AMM**: Aircraft Maintenance Manual
- **IPC**: Illustrated Parts Catalog
- Additional publications can be added as needed (e.g., WDM, CMM, FIM, SRM)

## Usage Guidelines

1. **For Certification Documentation**: Use this ATA SNS structure
2. **For Development/Lifecycle**: Use the parent OPT-IN Framework structure
3. **Cross-Reference**: Maintain traceability between both structures

## References

- [ATA iSpec 2200 Extract: ATA Standard Numbering System](https://publications.airlines.org/products/ispec-2200-extract-ata-standard-numbering-system-revision-2024-1)
- [ATA Chapters and Sub-chapters Reference](https://toddheffley.com/wordpress/?p=5760)
- S1000D Specification (International specification for technical publications)

## Notes

- Each `21-xx-00-*` directory serves as the "general" subject for its section
- Additional subjects `21-xx-YY-*` should only be added when defined in your ATA SNS extract
- The `PUB/<SUB_ID>/CSDB` structure is self-contained for S1000D publishing
- Configuration files (`bindings.csv`, `csdb.profile.yaml`) should be populated according to project requirements

## Document Control

- **ATA Chapter**: 21
- **Structure Version**: 1.0
- **Standard**: ATA iSpec 2200 SNS / S1000D
- **Status**: Active
- **Repository**: AMPEL360-AIR-T
- **Location**: Integrated with OPT-IN Framework
- **Last Updated**: 2026-01-08
