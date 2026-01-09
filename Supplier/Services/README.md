# Supplier / Services / Domains

This directory contains domain mirrors for **supplier alignment and handoff**.

## Purpose

The structures here mirror the canonical domains from `PRODUCTS/**/domains/<CODE>/` to provide:
- Clear supplier interfaces for each engineering domain
- Standardized handoff structures for service deliverables
- Traceability paths for IEF/UTCS evidence and SBOMs

## Structure

Each domain under `domains/` follows the standard structure:

```
<DOMAIN_CODE>/
├── DELs/           # Deliveries/releases for this domain
├── PAx/            # Packaging (On-Board/Off-Board)
├── PLM/            # CAx++ stack
│   ├── CAO/        # Computer-Aided Optimization
│   ├── CAD/        # Computer-Aided Design
│   ├── CAE/        # Computer-Aided Engineering
│   ├── CAM/        # Computer-Aided Manufacturing
│   ├── CAV/        # Computer-Aided Verification
│   ├── CAI/        # Computer-Aided Integration
│   ├── CAS/        # Computer-Aided Simulation
│   ├── CAP/        # Computer-Aided Planning
│   └── CMP/        # Computer-Aided Maintenance & Production
├── QUANTUM_OA/     # Quantum/heuristics portfolio
│   ├── QOX/        # Quantum-Optimized X (general)
│   ├── MILP/       # Mixed-Integer Linear Programming
│   ├── LP/         # Linear Programming
│   ├── QP/         # Quadratic Programming
│   ├── QUBO/       # Quadratic Unconstrained Binary Optimization
│   ├── QAOA/       # Quantum Approximate Optimization Algorithm
│   ├── SA/         # Simulated Annealing
│   └── GA/         # Genetic Algorithms
├── policy/         # Linters, rules (naming, Schematron, etc.)
├── tests/          # pytest suites / conformance cases
└── README.md       # Domain-specific documentation
```

## Canonical Domains

The following 15 canonical domains are mirrored here:

- **AAA** — Aerodynamics
- **AAP** — Aerodynamics & Propulsion
- **CCC** — Communications, Command & Control
- **CQH** — Cybersecurity, Quantum & Hybrid systems
- **DDD** — Data, Diagnostics & Decision systems
- **EDI** — Environmental, Design & Integration
- **EEE** — Electrical, Electronics & Energy
- **EER** — Energy, Environment & Resources
- **IIF** — Integration, Interfaces & Frameworks
- **IIS** — Information, Integration & Systems
- **LCC** — Lifecycle, Certification & Compliance
- **LIB** — Libraries & reusable components
- **MEC** — Mechanical systems
- **OOO** — OS, Ontologies & Office interfaces
- **PPP** — Propulsion systems

## Source of Truth

The **source of truth** for each domain remains in the product roots:
- `PRODUCTS/**/domains/<CODE>/`

This directory structure is synchronized from product domains using:
```bash
python tools/sync_domains_suppliers_vendors.py
```

## CI Guard

The GitHub Actions workflow `.github/workflows/supplier-vendor-domains-check.yml` ensures that:
1. All 15 canonical domains exist
2. Each domain has the complete required structure
3. All PLM and QUANTUM_OA subdirectories are present

## Evidence & Traceability

- Evidence lives with artifacts in the product roots
- SBOMs should be linked from `sbom/` when packaging
- IEF/UTCS metadata and provenance are maintained at artifact level

## Maintenance

This structure is idempotent. Re-running the sync script is safe and will only:
- Create missing directories with `.gitkeep` files
- Add README stubs for new domains (won't overwrite existing)

---

**Last scaffolded:** 2025-10-05  
**Scaffold tool:** `tools/sync_domains_suppliers_vendors.py`  
**CI guard:** `.github/workflows/supplier-vendor-domains-check.yml`
