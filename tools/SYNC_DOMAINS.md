# Domain Synchronization Tool

Tool for scaffolding Supplier/Services and Vendors/Components domain structures.

## Purpose

`sync_domains_suppliers_vendors.py` creates and maintains mirrored domain structures for supplier and vendor alignment. It ensures consistency across the 15 canonical engineering domains.

## Usage

```bash
python tools/sync_domains_suppliers_vendors.py
```

The script is **idempotent** — safe to run multiple times. It will:
- Create missing directories
- Add `.gitkeep` files to maintain empty folders in git
- Generate README stubs for new domains (won't overwrite existing)

## What It Does

Creates the following structure:

```
Supplier/Services/domains/<CODE>/
Vendors/Components/domains/<CODE>/
    ├── DELs/           # Deliveries/releases
    ├── PAx/            # Packaging (On-Board/Off-Board)
    ├── PLM/            # CAx++ stack (9 subdirs)
    │   ├── CAO/ CAD/ CAE/ CAM/ CAV/ CAI/ CAS/ CAP/ CMP/
    ├── QUANTUM_OA/     # Quantum/heuristics (8 subdirs)
    │   ├── QOX/ MILP/ LP/ QP/ QUBO/ QAOA/ SA/ GA/
    ├── policy/         # Linters, rules
    ├── tests/          # Test suites
    └── README.md       # Domain documentation
```

## Canonical Domains

The script scaffolds exactly **15 canonical domains**:

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

## Output

```
✓ Scaffolded 15 canonical domains into Supplier/Services and Vendors/Components.
```

## Subdirectory Breakdown

### PLM (Product Lifecycle Management)
9 Computer-Aided X (CAx++) subdirectories:
- **CAO** — Computer-Aided Optimization
- **CAD** — Computer-Aided Design
- **CAE** — Computer-Aided Engineering
- **CAM** — Computer-Aided Manufacturing
- **CAV** — Computer-Aided Verification
- **CAI** — Computer-Aided Integration
- **CAS** — Computer-Aided Simulation
- **CAP** — Computer-Aided Planning
- **CMP** — Computer-Aided Maintenance & Production

### QUANTUM_OA (Quantum & Optimization Algorithms)
8 quantum/heuristics subdirectories:
- **QOX** — Quantum-Optimized X (general)
- **MILP** — Mixed-Integer Linear Programming
- **LP** — Linear Programming
- **QP** — Quadratic Programming
- **QUBO** — Quadratic Unconstrained Binary Optimization
- **QAOA** — Quantum Approximate Optimization Algorithm
- **SA** — Simulated Annealing
- **GA** — Genetic Algorithms

## File Counts

Per domain: 23 directories (6 top-level + 9 PLM + 8 QUANTUM_OA)  
Per tree: 15 domains × 23 directories = 345 directories  
Total: 690 directories across both Supplier and Vendors trees

Each directory contains a `.gitkeep` file (690 total across both trees).

## CI Integration

The structure is enforced by GitHub Actions workflow:
`.github/workflows/supplier-vendor-domains-check.yml`

The CI check:
1. Validates all 15 canonical domains exist
2. Verifies complete structure for each domain
3. Checks all PLM and QUANTUM_OA subdirectories

## Source of Truth

The canonical domains are defined in:
- **Script:** `tools/sync_domains_suppliers_vendors.py` (`CANONICAL_DOMAINS` list)
- **CI:** `.github/workflows/supplier-vendor-domains-check.yml` (`CANONICAL_DOMAINS` list)

Both must be kept in sync.

The **product-level source of truth** for domain content remains:
- `PRODUCTS/**/domains/<CODE>/`

## Maintenance

To add a new canonical domain:
1. Update `CANONICAL_DOMAINS` in `tools/sync_domains_suppliers_vendors.py`
2. Update `CANONICAL_DOMAINS` in `.github/workflows/supplier-vendor-domains-check.yml`
3. Run the script: `python tools/sync_domains_suppliers_vendors.py`
4. Commit the new directories

To remove a domain:
1. Remove from both `CANONICAL_DOMAINS` lists
2. Manually delete the domain directories (script won't remove)
3. Update any documentation referencing the domain

## Related Documentation

- `Supplier/README.md` — Top-level Supplier documentation
- `Supplier/Services/README.md` — Services domain structure
- `Vendors/README.md` — Top-level Vendors documentation
- `Vendors/Components/README.md` — Components domain structure
- Each domain's `README.md` — Domain-specific documentation

---

**Last updated:** 2025-10-05  
**Version:** 1.0  
**Canonical domains:** 15
