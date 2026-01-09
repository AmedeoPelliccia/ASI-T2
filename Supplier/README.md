# Supplier

This directory tree provides **supplier-facing views** of the IDEALE.eu engineering domains.

## Structure

```
Supplier/
└── Services/
    ├── domains/        # Engineering domain mirrors (15 canonical domains)
    │   ├── AAA/
    │   ├── AAP/
    │   ├── ...
    │   └── PPP/
    └── README.md       # Services-level documentation
```

## Purpose

The `Supplier/Services/` tree mirrors the canonical domain structure to provide:
- Clear interfaces for supplier collaboration
- Standardized handoff structures for service deliverables
- Domain-specific organization for supplier-provided artifacts
- Traceability paths linking to product roots

## Getting Started

1. See `Services/README.md` for the complete structure and domain list
2. Each domain under `Services/domains/<CODE>/` contains:
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
