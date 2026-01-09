#!/usr/bin/env python3
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[1]

# Canonical domain codes (fixed list)
CANONICAL_DOMAINS = [
    "AAA", "AAP", "CCC", "CQH", "DDD", "EDI", "EEE", "EER",
    "IIF", "IIS", "LCC", "LIB", "MEC", "OOO", "PPP"
]

# Targets to scaffold
TARGETS = [
    REPO / "Supplier" / "Services" / "domains",
    REPO / "Vendors" / "Components" / "domains",
]

# Standard subtrees
PLM_SUB = ["CAO", "CAD", "CAE", "CAM", "CAV", "CAI", "CAS", "CAP", "CMP"]
QOA_SUB = ["QOX", "MILP", "LP", "QP", "QUBO", "QAOA", "SA", "GA"]
TOPS = ["DELs", "PAx", "PLM", "QUANTUM_OA", "policy", "tests"]

README_STUB = """# {code} — Domain

This directory mirrors the **{code}** domain for {scope} alignment.

- **Source of truth (product roots):** see `PRODUCTS/**/domains/{code}/`
- **Structure here:** DELs, PAx, PLM, QUANTUM_OA, policy, tests
- **IEF/UTCS:** evidence lives with artifacts; link SBOMs from `sbom/` when packaging
"""

def discover_domain_codes():
    """Return the canonical domain codes."""
    return sorted(CANONICAL_DOMAINS)

def ensure_dir(d: Path):
    d.mkdir(parents=True, exist_ok=True)
    (d / ".gitkeep").write_text("", encoding="utf-8")

def scaffold_for_code(root: Path, code: str, scope_label: str):
    base = root / code
    # top-level bins
    for t in TOPS:
        ensure_dir(base / t)
    # PLM detail
    for s in PLM_SUB:
        ensure_dir(base / "PLM" / s)
    # QUANTUM_OA detail
    for s in QOA_SUB:
        ensure_dir(base / "QUANTUM_OA" / s)
    # README stub once
    readme = base / "README.md"
    if not readme.exists():
        readme.write_text(README_STUB.format(code=code, scope=scope_label), encoding="utf-8")

def main():
    codes = discover_domain_codes()
    
    for tgt in TARGETS:
        tgt.mkdir(parents=True, exist_ok=True)
        scope_label = "Supplier/Services" if "Supplier" in tgt.parts else "Vendors/Components"
        for code in codes:
            scaffold_for_code(tgt, code, scope_label)
    print(f"✓ Scaffolded {len(codes)} canonical domains into Supplier/Services and Vendors/Components.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
