#!/usr/bin/env python3
"""
ASI-T2 Filename Policy Linter

Validates S1000D DM and CAx filenames (CAD/CAE/CAM/CAV/CMP) against
standardized patterns with ATA short-code 5710 (57-10).

Usage:
    python3 tools/lint_names.py [path...]
    python3 tools/lint_names.py .  # check all files in current directory

Exit codes:
    0 - All files compliant
    1 - Non-compliant files found
"""

import re
import sys
import json
import hashlib
import pathlib
from typing import List, Set

# S1000D DM filename pattern (Issue 5.0/6.0)
# DMC-<MIC>-<SDC>-<SC>-<SSC>-<SSSC>-<AC><DAC>-<IC><ICV>-<ILC>-<LANG>-<COUNTRY>.xml
DM = re.compile(
    r'^DMC-[A-Z0-9]{3,4}-[A-Z]-\d{2}-\d{2}-\d{2}-\d{2}[A-Z]-\d{3}[A-Z0-9]-[A-Z]-[A-Z]{2}-[A-Z]{2}\.xml$'
)

# CAx filename pattern (CAD/CAE/CAM/CAV/CMP)
# <DISC>-<MIC>-<DOMAIN><ATA>-<SCOPE>-<HAND?>-<EFFT?>-<LIFE?>-r<REV>.<EXT>
CAx = re.compile(
    r'^(ASSY|PRT|DRW|FEM|CFD|MBD|EMI|NC|APT|OPR|FIX|TOOL|SET|QIP|QIF|DMIS|MEAS|MSA|CERT|EPR|RECY|TREAT|DISP|MATREC)-'  # DISC
    r'([A-Z0-9]{3,4})-'                                                    # MIC
    r'(CAD|CAE|CAM|CAV|CMP)'                                               # DOMAIN
    r'(57\d{2})-'                                                          # ATA short (e.g., 5710)
    r'([A-Z0-9-]+)'                                                        # SCOPE (kebab)
    r'(?:-(LH|RH|CEN))?'                                                   # HAND?
    r'(?:-([A-Z0-9]{3,8}-[A-Z0-9-]+))?'                                    # EFFT? (APPL-... or E0001-...)
    r'(?:-(GA|STAT|UL|FAT|DTA|CERT|VNV|QC|EOL))?'                          # LIFE?
    r'-r(\d{3})'                                                           # REV
    r'\.(step|stp|sldprt|sldasm|ipt|iam|dwg|dxf|pdf|inp|cdb|cas|dat|fem|nas|apt|cl|cls|nc|eia|qif|dmis|csv|xml|json)$'  # EXT
)

# Domain to DISC mapping for validation
DOMAIN_DISC_MAP = {
    'CAD': {'ASSY', 'PRT', 'DRW', 'MBD'},
    'CAE': {'FEM', 'CFD', 'EMI'},
    'CAM': {'NC', 'APT', 'OPR', 'FIX', 'TOOL', 'SET'},
    'CAV': {'QIP', 'QIF', 'DMIS', 'MEAS', 'MSA', 'CERT'},
    'CMP': {'EPR', 'RECY', 'TREAT', 'DISP', 'MATREC', 'CERT'}
}

# Domain to extension mapping
DOMAIN_EXT_MAP = {
    'CAD': {'step', 'stp', 'sldprt', 'sldasm', 'ipt', 'iam', 'dwg', 'dxf', 'pdf'},
    'CAE': {'inp', 'cdb', 'cas', 'dat', 'fem', 'nas'},
    'CAM': {'nc', 'eia', 'apt', 'cl', 'cls', 'csv', 'pdf', 'step', 'stp'},
    'CAV': {'qif', 'dmis', 'csv', 'pdf', 'xml'},
    'CMP': {'pdf', 'csv', 'xml', 'json'}
}


def fail(name: str, msg: str) -> None:
    """Print GitHub Actions error annotation."""
    print(f"::error file={name}::{msg}")


def scope_checks(name: str, scope: str) -> bool:
    """Validate SCOPE field rules."""
    if scope.startswith('-') or scope.endswith('-'):
        fail(name, "SCOPE must not start/end with '-'")
        return False
    if '--' in scope:
        fail(name, "SCOPE must not contain consecutive '-'")
        return False
    if not re.fullmatch(r'[A-Z0-9-]+', scope):
        fail(name, "SCOPE must be A–Z/0–9/-, UPPERCASE kebab-case")
        return False
    return True


def check_utcs_sidecar(path: pathlib.Path) -> None:
    """Optional: verify UTCS anchor in JSON sidecar if present."""
    json_path = path.with_suffix(path.suffix + '.json')
    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding='utf-8'))
            anchor = data.get('utcsAnchor', '')
            if anchor.startswith('sha256:'):
                h = hashlib.sha256(path.read_bytes()).hexdigest()
                if anchor != f"sha256:{h}":
                    fail(str(json_path), "utcsAnchor mismatch (recompute sha256 of CAx file)")
        except Exception as e:
            fail(str(json_path), f"invalid JSON sidecar: {e}")


def check_domain_disc_consistency(name: str, domain: str, disc: str) -> bool:
    """Verify DISC is valid for the domain."""
    if domain in DOMAIN_DISC_MAP:
        if disc not in DOMAIN_DISC_MAP[domain]:
            fail(name, f"DISC '{disc}' is not valid for domain '{domain}'. Expected one of: {', '.join(sorted(DOMAIN_DISC_MAP[domain]))}")
            return False
    return True


def check_domain_ext_consistency(name: str, domain: str, ext: str) -> bool:
    """Verify extension is valid for the domain."""
    if domain in DOMAIN_EXT_MAP:
        if ext not in DOMAIN_EXT_MAP[domain]:
            fail(name, f"Extension '.{ext}' is not typical for domain '{domain}'. Expected one of: {', '.join(sorted(DOMAIN_EXT_MAP[domain]))}")
            # This is a warning, not a hard failure - return True
    return True


def lint_path(p: pathlib.Path) -> bool:
    """Validate a single file path."""
    name = p.name
    
    # Check if it's a DM file
    if DM.match(name):
        return True
    
    # Check if it's a CAx file
    m = CAx.match(name)
    if m:
        disc, mic, domain, ata, scope, hand, efft, life, rev, ext = m.groups()
        
        # Validate SCOPE
        ok = scope_checks(name, scope)
        
        # Optional: pin to 5710 only during rollout (uncomment to enforce)
        # if ata != '5710':
        #     fail(name, "ATA must be 5710 during rollout")
        #     ok = False
        
        # Validate domain/DISC consistency
        ok = check_domain_disc_consistency(name, domain, disc) and ok
        
        # Validate domain/extension consistency (warning only)
        check_domain_ext_consistency(name, domain, ext)
        
        # Check UTCS sidecar if present
        check_utcs_sidecar(p)
        
        return ok
    
    # Try to provide helpful error messages
    if '571010' in name:
        fail(name, "Use short ATA (5710), not long (571010)")
        return False
    if re.search(r'\b571\b', name):
        fail(name, "Use 4-digit ATA (57xx), not very short (571)")
        return False
    
    # Not a recognized pattern - might be a regular file
    # Only fail if it looks like it might be a CAx or DM file
    if any(ext in name for ext in ['.step', '.stp', '.sldprt', '.sldasm', '.ipt', '.iam', 
                                     '.dwg', '.dxf', '.inp', '.cdb', '.cas', '.dat', '.fem', 
                                     '.nas', '.nc', '.eia', '.apt', '.qif', '.dmis']):
        fail(name, "Filename not compliant with DM or CAx patterns")
        return False
    
    if name.startswith('DMC-') or name.startswith(('ASSY-', 'PRT-', 'DRW-', 'FEM-', 'CFD-', 
                                                     'MBD-', 'EMI-', 'NC-', 'APT-', 'OPR-', 
                                                     'FIX-', 'TOOL-', 'SET-', 'QIP-', 'QIF-', 
                                                     'DMIS-', 'MEAS-', 'MSA-', 'CERT-', 'EPR-', 
                                                     'RECY-', 'TREAT-', 'DISP-', 'MATREC-')):
        fail(name, "Filename not compliant with DM or CAx patterns")
        return False
    
    # Regular file - ignore
    return True


def should_check_file(p: pathlib.Path) -> bool:
    """Determine if a file should be checked."""
    # Skip hidden files and directories
    if p.name.startswith('.'):
        return False
    
    # Skip common non-CAx directories
    skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 
                 'build', 'dist', '.pytest_cache', '.mypy_cache'}
    if any(skip_dir in p.parts for skip_dir in skip_dirs):
        return False
    
    return True


def main(paths: List[str]) -> int:
    """Main entry point."""
    ok = True
    checked_count = 0
    
    for arg in paths:
        p = pathlib.Path(arg)
        if p.is_file():
            if should_check_file(p):
                ok &= lint_path(p)
                checked_count += 1
        elif p.is_dir():
            for f in p.rglob('*'):
                if f.is_file() and should_check_file(f):
                    result = lint_path(f)
                    ok &= result
                    checked_count += 1
    
    if checked_count > 0:
        print(f"Checked {checked_count} CAx/DM files")
    
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ['.']))
