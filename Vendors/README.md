# Vendors

This directory tree provides **vendor-facing views** of the IDEALE.eu engineering domains.

## Structure

```
Vendors/
└── Components/
    ├── domains/        # Engineering domain mirrors (15 canonical domains)
    │   ├── AAA/
    │   ├── AAP/
    │   ├── ...
    │   └── PPP/
    └── README.md       # Components-level documentation
```

## Purpose

The `Vendors/Components/` tree mirrors the canonical domain structure to provide:
- Clear interfaces for vendor/component collaboration
- Standardized handoff structures for component deliverables
- Domain-specific organization for vendor-provided artifacts
- Traceability paths linking to product roots

## Getting Started

1. See `Components/README.md` for the complete structure and domain list
2. Each domain under `Components/domains/<CODE>/` contains:
   - Standard subtrees: DELs, PAx, PLM, QUANTUM_OA, policy, tests
   - Domain-specific README with scope and alignment notes

## Maintenance

The structure is synchronized using:
```bash
python tools/sync_domains_suppliers_vendors.py
```

CI enforcement via: `.github/workflows/supplier-vendor-domains-check.yml`

---

**Canonical domains:** 15 (AAA through PPP)  
**Source of truth:** `PRODUCTS/**/domains/<CODE>/`  
**Last scaffolded:** 2025-10-05
