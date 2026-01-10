#!/usr/bin/env python3
"""
Test suite for KNU Distribution System

Tests the distribution formula, weight calculation, spillover mechanics,
eligibility validation, and integration with tek_tokens.py
"""

import json
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))

from knu_distribution import (
    KNUDistributor,
    KNUEntry,
    KNOTPool,
    Distribution,
    ValidationError,
    ConfigError
)

REPO_ROOT = Path(__file__).parent.parent


class TestKNUDistribution:
    """Test suite for KNU distribution system."""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_dir = None
    
    def setup(self):
        """Setup test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="knu_test_")
        print(f"Test directory: {self.test_dir}")
    
    def teardown(self):
        """Cleanup test environment."""
        if self.test_dir and Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
        
        print(f"\n{'='*60}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_failed}")
        print(f"{'='*60}")
    
    def assert_true(self, condition, message):
        """Assert that condition is True."""
        if condition:
            print(f"  ✓ {message}")
            self.tests_passed += 1
        else:
            print(f"  ✗ {message}")
            self.tests_failed += 1
    
    def assert_approx(self, a, b, tolerance, message):
        """Assert that a and b are approximately equal."""
        if abs(a - b) < tolerance:
            print(f"  ✓ {message}")
            self.tests_passed += 1
        else:
            print(f"  ✗ {message} (got {a}, expected {b})")
            self.tests_failed += 1
    
    def test_load_configs(self):
        """Test loading pool and adjacency configurations."""
        print("\nTest 1: Load Configurations")
        
        try:
            distributor = KNUDistributor()
            
            self.assert_true(
                distributor.pools_data is not None,
                "Pools config loaded"
            )
            self.assert_true(
                distributor.adjacency_data is not None,
                "Adjacency config loaded"
            )
            self.assert_true(
                distributor.alpha == 0.30,
                "Alpha parameter is 0.30"
            )
            self.assert_true(
                distributor.lambda_spillover == 0.50,
                "Lambda spillover is 0.50"
            )
            
            # Test loading specific pool
            pool = distributor.load_pool_config("K06")
            self.assert_true(
                pool.pool_tt == 150,
                "K06 pool is 150 TT"
            )
            self.assert_true(
                "Data governance" in pool.description,
                "K06 description correct"
            )
            
        except Exception as e:
            print(f"  ✗ Config loading failed: {e}")
            self.tests_failed += 1
    
    def test_weight_calculation_equal_effort_impact(self):
        """Test weight calculation with equal effort and impact."""
        print("\nTest 2: Weight Calculation - Equal Effort and Impact")
        
        knus = [
            KNUEntry(
                knu_id="KNU-K06-00-001",
                knot_id="K06",
                owner="alice",
                E_pred=5.0,
                dR_primary=30.0,
                dR_adj_sum=10.0,
                status="merged",
                artifacts=["evidence/001.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            ),
            KNUEntry(
                knu_id="KNU-K06-00-002",
                knot_id="K06",
                owner="bob",
                E_pred=3.0,
                dR_primary=15.0,
                dR_adj_sum=5.0,
                status="merged",
                artifacts=["evidence/002.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            ),
            KNUEntry(
                knu_id="KNU-K06-00-003",
                knot_id="K06",
                owner="charlie",
                E_pred=2.0,
                dR_primary=5.0,
                dR_adj_sum=0.0,
                status="merged",
                artifacts=["evidence/003.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            )
        ]
        
        distributor = KNUDistributor()
        weighted = distributor.calculate_weights(knus)
        
        # Check weights sum to 1.0
        total_weight = sum(w for _, w in weighted)
        self.assert_approx(
            total_weight, 1.0, 1e-6,
            "Total weight sums to 1.0"
        )
        
        # Alice should have highest weight (highest effort and impact)
        alice_weight = next(w for knu, w in weighted if knu.owner == "alice")
        bob_weight = next(w for knu, w in weighted if knu.owner == "bob")
        charlie_weight = next(w for knu, w in weighted if knu.owner == "charlie")
        
        self.assert_true(
            alice_weight > bob_weight > charlie_weight,
            "Weights ordered: alice > bob > charlie"
        )
        
        print(f"    alice:   {alice_weight:.4f}")
        print(f"    bob:     {bob_weight:.4f}")
        print(f"    charlie: {charlie_weight:.4f}")
    
    def test_weight_calculation_no_effort(self):
        """Test weight calculation when all effort is zero (impact only)."""
        print("\nTest 3: Weight Calculation - Zero Effort (Impact Only)")
        
        knus = [
            KNUEntry(
                knu_id="KNU-K06-00-001",
                knot_id="K06",
                owner="alice",
                E_pred=0.0,  # No effort recorded
                dR_primary=50.0,
                dR_adj_sum=0.0,
                status="merged",
                artifacts=["evidence/001.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            ),
            KNUEntry(
                knu_id="KNU-K06-00-002",
                knot_id="K06",
                owner="bob",
                E_pred=0.0,
                dR_primary=30.0,
                dR_adj_sum=0.0,
                status="merged",
                artifacts=["evidence/002.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            )
        ]
        
        distributor = KNUDistributor()
        weighted = distributor.calculate_weights(knus)
        
        total_weight = sum(w for _, w in weighted)
        self.assert_approx(
            total_weight, 1.0, 1e-6,
            "Total weight sums to 1.0 (impact only)"
        )
        
        # With zero effort, distribution is based purely on impact
        alice_weight = next(w for knu, w in weighted if knu.owner == "alice")
        bob_weight = next(w for knu, w in weighted if knu.owner == "bob")
        
        # alice has 50/(50+30) = 0.625 impact
        expected_alice = 50.0 / (50.0 + 30.0)
        self.assert_approx(
            alice_weight, expected_alice, 0.01,
            f"Alice weight ~{expected_alice:.2f} (impact-based)"
        )
        
        print(f"    alice: {alice_weight:.4f}")
        print(f"    bob:   {bob_weight:.4f}")
    
    def test_weight_calculation_no_impact(self):
        """Test weight calculation when all impact is zero (effort only)."""
        print("\nTest 4: Weight Calculation - Zero Impact (Effort Only)")
        
        knus = [
            KNUEntry(
                knu_id="KNU-K06-00-001",
                knot_id="K06",
                owner="alice",
                E_pred=8.0,
                dR_primary=0.0,  # No impact
                dR_adj_sum=0.0,
                status="merged",
                artifacts=["evidence/001.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            ),
            KNUEntry(
                knu_id="KNU-K06-00-002",
                knot_id="K06",
                owner="bob",
                E_pred=2.0,
                dR_primary=0.0,
                dR_adj_sum=0.0,
                status="merged",
                artifacts=["evidence/002.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            )
        ]
        
        distributor = KNUDistributor()
        weighted = distributor.calculate_weights(knus)
        
        total_weight = sum(w for _, w in weighted)
        self.assert_approx(
            total_weight, 1.0, 1e-6,
            "Total weight sums to 1.0 (effort only)"
        )
        
        # With zero impact, distribution is based purely on effort
        alice_weight = next(w for knu, w in weighted if knu.owner == "alice")
        expected_alice = 8.0 / (8.0 + 2.0)
        
        self.assert_approx(
            alice_weight, expected_alice, 0.01,
            f"Alice weight ~{expected_alice:.2f} (effort-based)"
        )
    
    def test_weight_calculation_different_alpha(self):
        """Test weight calculation with different alpha values."""
        print("\nTest 5: Weight Calculation - Different Alpha Values")
        
        knus = [
            KNUEntry(
                knu_id="KNU-K06-00-001",
                knot_id="K06",
                owner="alice",
                E_pred=10.0,  # High effort
                dR_primary=10.0,  # Low impact
                dR_adj_sum=0.0,
                status="merged",
                artifacts=["evidence/001.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            ),
            KNUEntry(
                knu_id="KNU-K06-00-002",
                knot_id="K06",
                owner="bob",
                E_pred=5.0,  # Lower effort
                dR_primary=40.0,  # High impact
                dR_adj_sum=0.0,
                status="merged",
                artifacts=["evidence/002.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            )
        ]
        
        distributor = KNUDistributor()
        
        # Test with alpha=0.30 (default - 30% effort, 70% impact)
        weighted_30 = distributor.calculate_weights(knus, alpha=0.30)
        alice_w30 = next(w for knu, w in weighted_30 if knu.owner == "alice")
        bob_w30 = next(w for knu, w in weighted_30 if knu.owner == "bob")
        
        # With 30% effort weight, bob (high impact) should get more
        self.assert_true(
            bob_w30 > alice_w30,
            "With α=0.30, bob (high impact) > alice (high effort)"
        )
        
        # Test with alpha=0.80 (80% effort, 20% impact)
        weighted_80 = distributor.calculate_weights(knus, alpha=0.80)
        alice_w80 = next(w for knu, w in weighted_80 if knu.owner == "alice")
        bob_w80 = next(w for knu, w in weighted_80 if knu.owner == "bob")
        
        # With 80% effort weight, alice (high effort) should get more
        self.assert_true(
            alice_w80 > bob_w80,
            "With α=0.80, alice (high effort) > bob (high impact)"
        )
        
        print(f"    α=0.30: alice={alice_w30:.4f}, bob={bob_w30:.4f}")
        print(f"    α=0.80: alice={alice_w80:.4f}, bob={bob_w80:.4f}")
    
    def test_spillover_calculation(self):
        """Test spillover impact calculation with lambda factor."""
        print("\nTest 6: Spillover Impact Calculation")
        
        knus = [
            KNUEntry(
                knu_id="KNU-K06-00-001",
                knot_id="K06",
                owner="alice",
                E_pred=5.0,
                dR_primary=30.0,
                dR_adj_sum=20.0,  # Significant spillover
                status="merged",
                artifacts=["evidence/001.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            ),
            KNUEntry(
                knu_id="KNU-K06-00-002",
                knot_id="K06",
                owner="bob",
                E_pred=5.0,  # Same effort
                dR_primary=30.0,  # Same primary impact
                dR_adj_sum=0.0,  # No spillover
                status="merged",
                artifacts=["evidence/002.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            )
        ]
        
        distributor = KNUDistributor()
        
        # Test with lambda=0.50 (default)
        weighted_50 = distributor.calculate_weights(knus, lambda_spill=0.50)
        alice_w50 = next(w for knu, w in weighted_50 if knu.owner == "alice")
        bob_w50 = next(w for knu, w in weighted_50 if knu.owner == "bob")
        
        # Alice should get more due to spillover (worth 50% of direct)
        self.assert_true(
            alice_w50 > bob_w50,
            "With λ=0.50, alice (with spillover) > bob (no spillover)"
        )
        
        # Test with lambda=0.0 (no spillover value)
        weighted_0 = distributor.calculate_weights(knus, lambda_spill=0.0)
        alice_w0 = next(w for knu, w in weighted_0 if knu.owner == "alice")
        bob_w0 = next(w for knu, w in weighted_0 if knu.owner == "bob")
        
        # With no spillover value, should be equal (same effort and primary impact)
        self.assert_approx(
            alice_w0, bob_w0, 0.01,
            "With λ=0.0, alice ≈ bob (spillover ignored)"
        )
        
        print(f"    λ=0.50: alice={alice_w50:.4f}, bob={bob_w50:.4f}")
        print(f"    λ=0.00: alice={alice_w0:.4f}, bob={bob_w0:.4f}")
    
    def test_eligibility_validation(self):
        """Test KNU eligibility validation."""
        print("\nTest 7: Eligibility Validation")
        
        distributor = KNUDistributor()
        
        # Valid KNU
        valid_knu = KNUEntry(
            knu_id="KNU-K06-00-001",
            knot_id="K06",
            owner="alice",
            E_pred=5.0,
            dR_primary=30.0,
            dR_adj_sum=10.0,
            status="merged",
            artifacts=["evidence/001.md"],
            validated_by="knot_owner",
            validated_at="2026-01-10T00:00:00Z"
        )
        
        is_valid, error = distributor.validate_eligibility(valid_knu)
        self.assert_true(is_valid, "Valid KNU passes validation")
        
        # Invalid status
        invalid_status = KNUEntry(
            knu_id="KNU-K06-00-002",
            knot_id="K06",
            owner="bob",
            E_pred=5.0,
            dR_primary=30.0,
            dR_adj_sum=10.0,
            status="pending",  # Not accepted/merged
            artifacts=["evidence/002.md"],
            validated_by="knot_owner",
            validated_at="2026-01-10T00:00:00Z"
        )
        
        is_valid, error = distributor.validate_eligibility(invalid_status)
        self.assert_true(not is_valid, "Pending status rejected")
        self.assert_true("Status" in error, "Error mentions status")
        
        # Missing artifacts
        no_artifacts = KNUEntry(
            knu_id="KNU-K06-00-003",
            knot_id="K06",
            owner="charlie",
            E_pred=5.0,
            dR_primary=30.0,
            dR_adj_sum=10.0,
            status="merged",
            artifacts=[],  # No artifacts
            validated_by="knot_owner",
            validated_at="2026-01-10T00:00:00Z"
        )
        
        is_valid, error = distributor.validate_eligibility(no_artifacts)
        self.assert_true(not is_valid, "Missing artifacts rejected")
        self.assert_true("artifacts" in error.lower(), "Error mentions artifacts")
        
        # Missing validation
        no_validation = KNUEntry(
            knu_id="KNU-K06-00-004",
            knot_id="K06",
            owner="dave",
            E_pred=5.0,
            dR_primary=30.0,
            dR_adj_sum=10.0,
            status="merged",
            artifacts=["evidence/004.md"],
            validated_by="",  # No validator
            validated_at=""
        )
        
        is_valid, error = distributor.validate_eligibility(no_validation)
        self.assert_true(not is_valid, "Missing validation rejected")
        self.assert_true("validat" in error.lower(), "Error mentions validation")
    
    def test_distribution_totals(self):
        """Test that distribution totals sum to pool amount."""
        print("\nTest 8: Distribution Totals")
        
        knus = [
            KNUEntry(
                knu_id="KNU-K06-00-001",
                knot_id="K06",
                owner="alice",
                E_pred=5.0,
                dR_primary=30.0,
                dR_adj_sum=10.0,
                status="merged",
                artifacts=["evidence/001.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            ),
            KNUEntry(
                knu_id="KNU-K06-00-002",
                knot_id="K06",
                owner="bob",
                E_pred=3.0,
                dR_primary=15.0,
                dR_adj_sum=5.0,
                status="merged",
                artifacts=["evidence/002.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            ),
            KNUEntry(
                knu_id="KNU-K06-00-003",
                knot_id="K06",
                owner="charlie",
                E_pred=2.0,
                dR_primary=5.0,
                dR_adj_sum=0.0,
                status="merged",
                artifacts=["evidence/003.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            )
        ]
        
        distributor = KNUDistributor()
        
        # Mock execute_reward to avoid actual token operations
        with patch.object(distributor, 'execute_reward', return_value='TX-000001'):
            distributions = distributor.distribute("K06", knus, dry_run=True)
        
        # Check total
        pool = distributor.load_pool_config("K06")
        total_deg = sum(d.tokens_deg for d in distributions)
        expected_deg = int(pool.pool_tt * 360)
        
        self.assert_true(
            total_deg == expected_deg,
            f"Total distributed ({total_deg} deg) equals pool ({expected_deg} deg)"
        )
        
        print(f"    Pool: {pool.pool_tt} TT ({expected_deg} deg)")
        print(f"    Distributed: {total_deg} deg")
        for d in distributions:
            print(f"      {d.owner}: {d.tokens_tt:.2f} TT ({d.tokens_deg} deg)")
    
    def test_single_knu_distribution(self):
        """Test distribution with a single KNU (edge case)."""
        print("\nTest 9: Single KNU Distribution")
        
        knus = [
            KNUEntry(
                knu_id="KNU-K06-00-001",
                knot_id="K06",
                owner="alice",
                E_pred=5.0,
                dR_primary=30.0,
                dR_adj_sum=10.0,
                status="merged",
                artifacts=["evidence/001.md"],
                validated_by="knot_owner",
                validated_at="2026-01-10T00:00:00Z"
            )
        ]
        
        distributor = KNUDistributor()
        weighted = distributor.calculate_weights(knus)
        
        # Single KNU should get weight = 1.0
        alice_weight = weighted[0][1]
        self.assert_approx(
            alice_weight, 1.0, 1e-6,
            "Single KNU gets weight 1.0"
        )
        
        # Distribution should give entire pool
        with patch.object(distributor, 'execute_reward', return_value='TX-000001'):
            distributions = distributor.distribute("K06", knus, dry_run=True)
        
        pool = distributor.load_pool_config("K06")
        expected_deg = int(pool.pool_tt * 360)
        
        self.assert_true(
            distributions[0].tokens_deg == expected_deg,
            f"Single KNU gets entire pool ({expected_deg} deg)"
        )
    
    def test_adjacency_graph_loading(self):
        """Test loading adjacency graph."""
        print("\nTest 10: Adjacency Graph Loading")
        
        distributor = KNUDistributor()
        adjacency = distributor.load_adjacency_graph()
        
        self.assert_true(
            "K06" in adjacency,
            "K06 exists in adjacency graph"
        )
        
        # Check K06 connections
        k06_adj = adjacency.get("K06", {})
        self.assert_true(
            "K01" in k06_adj,
            "K06 connects to K01"
        )
        self.assert_true(
            k06_adj.get("K01") == 0.4,
            "K06→K01 weight is 0.4"
        )
        
        print(f"    K06 connections: {list(k06_adj.keys())}")
        print(f"    K06→K01: {k06_adj.get('K01', 0)}")
    
    def run_all_tests(self):
        """Run all tests."""
        print("="*60)
        print("KNU Distribution Test Suite")
        print("="*60)
        
        try:
            self.setup()
            
            self.test_load_configs()
            self.test_weight_calculation_equal_effort_impact()
            self.test_weight_calculation_no_effort()
            self.test_weight_calculation_no_impact()
            self.test_weight_calculation_different_alpha()
            self.test_spillover_calculation()
            self.test_eligibility_validation()
            self.test_distribution_totals()
            self.test_single_knu_distribution()
            self.test_adjacency_graph_loading()
            
        finally:
            self.teardown()
        
        return self.tests_failed == 0


def main():
    """Run test suite."""
    test_suite = TestKNUDistribution()
    success = test_suite.run_all_tests()
    
    if success:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {test_suite.tests_failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
