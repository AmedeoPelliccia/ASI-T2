#!/usr/bin/env python3
"""
KNU (Knowledge Unit) Token Distribution System

Integrates with Teknia Token (TT) v3.14 to distribute rewards based on
effort and impact metrics using the formula:

    w_i = α·Ê_i + (1-α)·Î_i
    T_i = P_k · w_i

Where:
- P_k = Prize pool in TT for the KNOT
- E_i = Predicted effort (normalized)
- Ê_i = Normalized effort: E_i / Σ E_i
- I_i = Effective impact: ΔR_k,i + λ·S_i
- Î_i = Normalized impact: I_i / Σ I_i
- S_i = Spillover impact from adjacent KNOTs: Σ(a_k→j · ΔR_j,i)
- ΔR_k,i = Direct residue reduction (uncertainty resolved)
- a_k→j = Adjacency weight between KNOTs (0-1)

Default Parameters:
- α = 0.30 (30% effort weight, 70% impact weight)
- λ = 0.50 (spillover worth 50% of direct impact)

Usage:
    python tools/knu_distribution.py distribute --knot K06 --input knus.json
    python tools/knu_distribution.py calculate --knot K06 --input knus.json
    python tools/knu_distribution.py validate --input knus.json
    python tools/knu_distribution.py report --knot K06 --output report.json
"""

import argparse
import json
import os
import sys
import csv
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone

# ---------- Paths ----------

REPO_ROOT = Path(__file__).resolve().parent.parent
POOLS_CONFIG = REPO_ROOT / "finance" / "knu_pools.json"
ADJACENCY_CONFIG = REPO_ROOT / "finance" / "knu_adjacency.json"
KNU_LEDGER = REPO_ROOT / "finance" / "knu_ledger.csv"
TEK_TOKENS_CLI = REPO_ROOT / "tools" / "tek_tokens.py"

# ---------- Exceptions ----------

class DistributionError(Exception):
    """Base exception for distribution errors."""
    pass

class ValidationError(DistributionError):
    """Validation failed for KNU eligibility."""
    pass

class ConfigError(DistributionError):
    """Configuration loading error."""
    pass

# ---------- Dataclasses ----------

@dataclass
class KNUEntry:
    """A single Knowledge Unit submission."""
    knu_id: str           # e.g., "KNU-K06-00-001"
    knot_id: str          # e.g., "K06"
    owner: str            # GitHub username or account
    E_pred: float         # Predicted effort (story points/hours)
    dR_primary: float     # Direct residue reduction (0-100)
    dR_adj_sum: float     # Pre-calculated spillover impact
    status: str           # "pending", "accepted", "merged", "rejected"
    artifacts: List[str]  # Links to evidence artifacts
    validated_by: str     # KNOT owner who validated
    validated_at: str     # ISO timestamp

@dataclass
class KNOTPool:
    """Prize pool configuration for a KNOT."""
    knot_id: str
    pool_tt: float        # Total TT to distribute
    description: str = ""

@dataclass
class Distribution:
    """Result of distributing tokens to a KNU owner."""
    knu_id: str
    owner: str
    weight: float         # Calculated weight w_i
    tokens_tt: float      # Tokens in TT
    tokens_deg: int       # Tokens in deg (integer)
    tx_id: str = ""       # Transaction ID from tek_tokens

# ---------- KNU Distributor ----------

class KNUDistributor:
    """Main distribution calculator and executor."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize distributor with optional custom config."""
        self.pools_config_path = config_path or POOLS_CONFIG
        self.adjacency_config_path = ADJACENCY_CONFIG
        self.pools_data = None
        self.adjacency_data = None
        self.alpha = 0.30
        self.lambda_spillover = 0.50
        self._load_configs()
    
    def _load_configs(self) -> None:
        """Load pool and adjacency configurations."""
        # Load pools
        if not self.pools_config_path.exists():
            raise ConfigError(f"Pools config not found: {self.pools_config_path}")
        
        with self.pools_config_path.open(encoding="utf-8") as f:
            self.pools_data = json.load(f)
        
        # Extract parameters
        params = self.pools_data.get("parameters", {})
        self.alpha = params.get("alpha", 0.30)
        self.lambda_spillover = params.get("lambda_spillover", 0.50)
        
        # Load adjacency
        if not self.adjacency_config_path.exists():
            raise ConfigError(f"Adjacency config not found: {self.adjacency_config_path}")
        
        with self.adjacency_config_path.open(encoding="utf-8") as f:
            self.adjacency_data = json.load(f)
    
    def load_pool_config(self, knot_id: str) -> KNOTPool:
        """Load pool configuration for a specific KNOT."""
        pools = self.pools_data.get("pools", {})
        if knot_id not in pools:
            raise ConfigError(f"KNOT {knot_id} not found in pools config")
        
        pool_data = pools[knot_id]
        return KNOTPool(
            knot_id=knot_id,
            pool_tt=float(pool_data["pool_tt"]),
            description=pool_data.get("description", "")
        )
    
    def load_adjacency_graph(self) -> Dict[str, Dict[str, float]]:
        """Load adjacency graph for spillover calculations."""
        return self.adjacency_data.get("adjacency", {})
    
    def calculate_spillover(self, knu: KNUEntry, adjacency: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate spillover impact S_i for a KNU.
        
        Formula: S_i = Σ(a_k→j · ΔR_j,i)
        
        Note: In this implementation, we use the pre-calculated dR_adj_sum
        from the KNU entry, which should already contain the weighted sum
        of spillover impacts from adjacent KNOTs.
        """
        # For now, we trust the pre-calculated value
        # In a full implementation, this could validate against actual adjacent KNU impacts
        return knu.dR_adj_sum
    
    def calculate_weights(
        self,
        knus: List[KNUEntry],
        alpha: Optional[float] = None,
        lambda_spill: Optional[float] = None
    ) -> List[Tuple[KNUEntry, float]]:
        """
        Calculate distribution weights for all KNUs.
        
        Returns list of (KNU, weight) tuples where weights sum to 1.0
        
        Formula:
            Ê_i = E_i / Σ E_i
            I_i = ΔR_k,i + λ·S_i
            Î_i = I_i / Σ I_i
            w_i = α·Ê_i + (1-α)·Î_i
        """
        if not knus:
            return []
        
        alpha = alpha if alpha is not None else self.alpha
        lambda_spill = lambda_spill if lambda_spill is not None else self.lambda_spillover
        
        # Calculate normalized efforts
        total_effort = sum(knu.E_pred for knu in knus)
        if total_effort == 0:
            # If no effort recorded, distribute equally based on impact only
            effort_norm = [0.0] * len(knus)
        else:
            effort_norm = [knu.E_pred / total_effort for knu in knus]
        
        # Calculate effective impacts
        impacts = [
            knu.dR_primary + lambda_spill * knu.dR_adj_sum
            for knu in knus
        ]
        
        total_impact = sum(impacts)
        if total_impact == 0:
            # If no impact, distribute based on effort only
            impact_norm = [0.0] * len(knus)
        else:
            impact_norm = [imp / total_impact for imp in impacts]
        
        # Calculate final weights
        weights = [
            alpha * effort_norm[i] + (1 - alpha) * impact_norm[i]
            for i in range(len(knus))
        ]
        
        # Normalize to ensure sum = 1.0 (handle floating point errors)
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        
        return list(zip(knus, weights))
    
    def validate_eligibility(self, knu: KNUEntry) -> Tuple[bool, str]:
        """
        Validate KNU eligibility for distribution.
        
        Returns (is_valid, error_message)
        """
        eligibility = self.pools_data.get("eligibility", {})
        required_status = eligibility.get("required_status", ["accepted", "merged"])
        require_artifacts = eligibility.get("require_artifacts", True)
        require_validation = eligibility.get("require_validation", True)
        
        # Check status
        if knu.status not in required_status:
            return False, f"Status '{knu.status}' not in required: {required_status}"
        
        # Check artifacts
        if require_artifacts and not knu.artifacts:
            return False, "No artifacts provided (required)"
        
        # Check validation
        if require_validation:
            if not knu.validated_by:
                return False, "No validator specified (required)"
            if not knu.validated_at:
                return False, "No validation timestamp (required)"
        
        return True, ""
    
    def execute_reward(
        self,
        owner: str,
        tt_amount: float,
        metadata: Dict
    ) -> str:
        """
        Execute TT reward via tek_tokens.py CLI.
        
        Returns transaction ID from the reward operation.
        """
        # Build command
        cmd = [
            sys.executable,
            str(TEK_TOKENS_CLI),
            "reward",
            "--to", owner,
            "--tt", str(tt_amount)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT),
                check=False
            )
            
            if result.returncode != 0:
                raise DistributionError(
                    f"TT reward failed for {owner}: {result.stderr}"
                )
            
            # Parse tx_id from output (look for TX-XXXXXX pattern)
            import re
            tx_match = re.search(r'(TX-\d{6})', result.stdout)
            if not tx_match:
                raise DistributionError(
                    f"Could not parse transaction ID from output: {result.stdout}"
                )
            
            tx_id = tx_match.group(1)
            
            # Log to KNU ledger
            self._log_to_csv(metadata, tx_id)
            
            return tx_id
            
        except subprocess.SubprocessError as e:
            raise DistributionError(f"Failed to execute reward: {e}") from e
    
    def _log_to_csv(self, metadata: Dict, tx_id: str) -> None:
        """Log distribution to KNU ledger CSV."""
        KNU_LEDGER.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists and has header
        file_exists = KNU_LEDGER.exists()
        
        with KNU_LEDGER.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Write header if new file
            if not file_exists or KNU_LEDGER.stat().st_size == 0:
                writer.writerow([
                    "timestamp", "knot_id", "knu_id", "owner",
                    "E_pred", "dR_primary", "dR_adj_sum", "weight",
                    "tokens_tt", "tokens_deg", "tx_id", "validated_by"
                ])
            
            # Write data row
            writer.writerow([
                metadata.get("timestamp", ""),
                metadata.get("knot_id", ""),
                metadata.get("knu_id", ""),
                metadata.get("owner", ""),
                metadata.get("E_pred", ""),
                metadata.get("dR_primary", ""),
                metadata.get("dR_adj_sum", ""),
                metadata.get("weight", ""),
                metadata.get("tokens_tt", ""),
                metadata.get("tokens_deg", ""),
                tx_id,
                metadata.get("validated_by", "")
            ])
    
    def distribute(
        self,
        knot_id: str,
        knus: List[KNUEntry],
        dry_run: bool = False
    ) -> List[Distribution]:
        """
        Main distribution function.
        
        Validates eligibility, calculates weights, and executes rewards.
        
        Args:
            knot_id: KNOT identifier (e.g., "K06")
            knus: List of KNU entries to distribute to
            dry_run: If True, calculate but don't execute rewards
        
        Returns:
            List of Distribution results
        """
        # Load pool config
        pool = self.load_pool_config(knot_id)
        
        # Validate all KNUs
        valid_knus = []
        for knu in knus:
            is_valid, error = self.validate_eligibility(knu)
            if not is_valid:
                print(f"⚠ Skipping {knu.knu_id}: {error}", file=sys.stderr)
                continue
            
            # Ensure KNU belongs to this KNOT
            if knu.knot_id != knot_id:
                print(
                    f"⚠ Skipping {knu.knu_id}: belongs to {knu.knot_id}, not {knot_id}",
                    file=sys.stderr
                )
                continue
            
            valid_knus.append(knu)
        
        if not valid_knus:
            raise ValidationError("No valid KNUs found for distribution")
        
        # Calculate weights
        weighted_knus = self.calculate_weights(valid_knus)
        
        # Convert to deg for integer arithmetic
        # Note: Following TT v3.14 conventions: 1 TT = 360 deg
        DEG_PER_TT = 360
        pool_deg = int(pool.pool_tt * DEG_PER_TT)
        
        # Distribute tokens
        distributions = []
        total_distributed_deg = 0
        
        for i, (knu, weight) in enumerate(weighted_knus):
            # Calculate token allocation
            allocated_deg = int(pool_deg * weight)
            allocated_tt = allocated_deg / DEG_PER_TT
            
            # For last KNU, adjust for any rounding remainder
            if i == len(weighted_knus) - 1:
                remainder = pool_deg - total_distributed_deg
                allocated_deg = remainder
                allocated_tt = allocated_deg / DEG_PER_TT
            
            total_distributed_deg += allocated_deg
            
            # Create distribution record
            dist = Distribution(
                knu_id=knu.knu_id,
                owner=knu.owner,
                weight=weight,
                tokens_tt=allocated_tt,
                tokens_deg=allocated_deg
            )
            
            # Execute reward if not dry run
            if not dry_run:
                metadata = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "knot_id": knot_id,
                    "knu_id": knu.knu_id,
                    "owner": knu.owner,
                    "E_pred": knu.E_pred,
                    "dR_primary": knu.dR_primary,
                    "dR_adj_sum": knu.dR_adj_sum,
                    "weight": weight,
                    "tokens_tt": allocated_tt,
                    "tokens_deg": allocated_deg,
                    "validated_by": knu.validated_by
                }
                
                try:
                    tx_id = self.execute_reward(knu.owner, allocated_tt, metadata)
                    dist.tx_id = tx_id
                    print(f"✓ {knu.knu_id} → {knu.owner}: {allocated_tt:.2f} TT ({allocated_deg:,} deg) [{tx_id}]")
                except DistributionError as e:
                    print(f"✗ Failed to reward {knu.knu_id}: {e}", file=sys.stderr)
                    continue
            else:
                print(f"[DRY-RUN] {knu.knu_id} → {knu.owner}: {allocated_tt:.2f} TT ({allocated_deg:,} deg)")
            
            distributions.append(dist)
        
        return distributions

# ---------- CLI Commands ----------

def load_knus_from_file(filepath: Path) -> List[KNUEntry]:
    """Load KNU entries from JSON file."""
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")
    
    with filepath.open(encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle both array and object with "knus" key
    knus_data = data if isinstance(data, list) else data.get("knus", [])
    
    return [KNUEntry(**knu) for knu in knus_data]

def cmd_distribute(args) -> int:
    """Execute full distribution with TT rewards."""
    try:
        distributor = KNUDistributor()
        knus = load_knus_from_file(Path(args.input))
        
        print(f"\n{'='*60}")
        print(f"KNU Distribution: {args.knot}")
        print(f"{'='*60}\n")
        
        distributions = distributor.distribute(
            args.knot,
            knus,
            dry_run=args.dry_run
        )
        
        # Summary
        total_tt = sum(d.tokens_tt for d in distributions)
        total_deg = sum(d.tokens_deg for d in distributions)
        
        print(f"\n{'='*60}")
        print(f"Distribution Complete")
        print(f"{'='*60}")
        print(f"KNOT: {args.knot}")
        print(f"KNUs distributed: {len(distributions)}")
        print(f"Total allocated: {total_tt:.2f} TT ({total_deg:,} deg)")
        print(f"{'='*60}\n")
        
        return 0
        
    except (DistributionError, ConfigError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def cmd_calculate(args) -> int:
    """Calculate weights without executing (dry-run)."""
    try:
        distributor = KNUDistributor()
        knus = load_knus_from_file(Path(args.input))
        
        # Filter to specified KNOT
        knot_knus = [k for k in knus if k.knot_id == args.knot]
        
        if not knot_knus:
            print(f"No KNUs found for KNOT {args.knot}", file=sys.stderr)
            return 1
        
        # Validate
        valid_knus = []
        for knu in knot_knus:
            is_valid, error = distributor.validate_eligibility(knu)
            if is_valid:
                valid_knus.append(knu)
            else:
                print(f"⚠ {knu.knu_id}: {error}")
        
        if not valid_knus:
            print("No valid KNUs for calculation", file=sys.stderr)
            return 1
        
        # Calculate weights
        weighted_knus = distributor.calculate_weights(valid_knus)
        pool = distributor.load_pool_config(args.knot)
        
        print(f"\n{'='*60}")
        print(f"Weight Calculation: {args.knot}")
        print(f"Pool: {pool.pool_tt} TT")
        print(f"α (effort weight): {distributor.alpha}")
        print(f"λ (spillover factor): {distributor.lambda_spillover}")
        print(f"{'='*60}\n")
        
        for knu, weight in weighted_knus:
            tokens_tt = pool.pool_tt * weight
            print(f"{knu.knu_id:20s} {knu.owner:15s} w={weight:.4f} → {tokens_tt:8.2f} TT")
        
        total_weight = sum(w for _, w in weighted_knus)
        print(f"\n{'='*60}")
        print(f"Total weight: {total_weight:.6f} (should be 1.0)")
        print(f"{'='*60}\n")
        
        return 0
        
    except (DistributionError, ConfigError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def cmd_validate(args) -> int:
    """Validate KNU eligibility."""
    try:
        distributor = KNUDistributor()
        knus = load_knus_from_file(Path(args.input))
        
        print(f"\n{'='*60}")
        print("KNU Eligibility Validation")
        print(f"{'='*60}\n")
        
        valid_count = 0
        invalid_count = 0
        
        for knu in knus:
            is_valid, error = distributor.validate_eligibility(knu)
            if is_valid:
                print(f"✓ {knu.knu_id:20s} {knu.owner:15s} VALID")
                valid_count += 1
            else:
                print(f"✗ {knu.knu_id:20s} {knu.owner:15s} INVALID: {error}")
                invalid_count += 1
        
        print(f"\n{'='*60}")
        print(f"Valid: {valid_count}, Invalid: {invalid_count}")
        print(f"{'='*60}\n")
        
        return 0 if invalid_count == 0 else 1
        
    except (DistributionError, ConfigError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def cmd_report(args) -> int:
    """Generate distribution report."""
    try:
        distributor = KNUDistributor()
        knus = load_knus_from_file(Path(args.input))
        
        # Filter and validate
        knot_knus = [k for k in knus if k.knot_id == args.knot]
        valid_knus = [
            k for k in knot_knus
            if distributor.validate_eligibility(k)[0]
        ]
        
        if not valid_knus:
            print(f"No valid KNUs for KNOT {args.knot}", file=sys.stderr)
            return 1
        
        # Calculate
        weighted_knus = distributor.calculate_weights(valid_knus)
        pool = distributor.load_pool_config(args.knot)
        
        # Build report
        report = {
            "knot_id": args.knot,
            "pool_tt": pool.pool_tt,
            "pool_description": pool.description,
            "parameters": {
                "alpha": distributor.alpha,
                "lambda_spillover": distributor.lambda_spillover
            },
            "distributions": [
                {
                    "knu_id": knu.knu_id,
                    "owner": knu.owner,
                    "effort": knu.E_pred,
                    "impact_primary": knu.dR_primary,
                    "impact_spillover": knu.dR_adj_sum,
                    "weight": weight,
                    "tokens_tt": pool.pool_tt * weight,
                    "tokens_deg": int(pool.pool_tt * weight * 360)
                }
                for knu, weight in weighted_knus
            ],
            "summary": {
                "total_knus": len(valid_knus),
                "total_weight": sum(w for _, w in weighted_knus),
                "total_tt": pool.pool_tt
            }
        }
        
        # Output
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            print(f"✓ Report saved to {output_path}")
        else:
            print(json.dumps(report, indent=2))
        
        return 0
        
    except (DistributionError, ConfigError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

# ---------- Main ----------

def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="KNU Distribution System - Reward distribution based on effort and impact",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # distribute command
    dist = subparsers.add_parser(
        "distribute",
        help="Distribute rewards for a KNOT"
    )
    dist.add_argument("--knot", required=True, help="KNOT ID (e.g., K06)")
    dist.add_argument("--input", required=True, help="Input JSON file with KNU entries")
    dist.add_argument("--dry-run", action="store_true", help="Calculate without executing rewards")
    
    # calculate command
    calc = subparsers.add_parser(
        "calculate",
        help="Calculate weights without executing (dry-run)"
    )
    calc.add_argument("--knot", required=True, help="KNOT ID (e.g., K06)")
    calc.add_argument("--input", required=True, help="Input JSON file with KNU entries")
    
    # validate command
    val = subparsers.add_parser(
        "validate",
        help="Validate KNU eligibility"
    )
    val.add_argument("--input", required=True, help="Input JSON file with KNU entries")
    
    # report command
    rep = subparsers.add_parser(
        "report",
        help="Generate distribution report"
    )
    rep.add_argument("--knot", required=True, help="KNOT ID (e.g., K06)")
    rep.add_argument("--input", required=True, help="Input JSON file with KNU entries")
    rep.add_argument("--output", help="Output JSON file (default: stdout)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == "distribute":
            return cmd_distribute(args)
        elif args.command == "calculate":
            return cmd_calculate(args)
        elif args.command == "validate":
            return cmd_validate(args)
        elif args.command == "report":
            return cmd_report(args)
        else:
            parser.print_help()
            return 0
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
