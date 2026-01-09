#!/usr/bin/env python3
"""
Basic smoke tests for IEF HUELLΔ tools
"""
import json
import tempfile
import shutil
from pathlib import Path
import sys
import subprocess

def test_badge_generator():
    """Test badge generator with sample data"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        
        # Create sample verification results
        verify_dir = tmppath / "verification"
        verify_dir.mkdir()
        verify_file = verify_dir / "verify-results.json"
        verify_file.write_text(json.dumps({
            "version": "0.1",
            "generated_at": "2025-10-05T16:30:00Z",
            "results": [
                {
                    "asset_uid": "urn:ideale:test:asset:001",
                    "path": "events/TEST/SN-001/evt-001.json",
                    "status": "pass"
                }
            ]
        }))
        
        # Create sample event
        events_dir = tmppath / "events" / "TEST" / "SN-001"
        events_dir.mkdir(parents=True)
        event_file = events_dir / "evt-001.json"
        event_file.write_text(json.dumps({
            "ief_version": "0.1",
            "event_type": "assemble",
            "ts": "2025-10-05T15:30:00Z",
            "calc": {
                "energy_kwh_est": 0.010,
                "co2e_kg_est": 0.002,
                "quality_score": 0.97,
                "risk_score": 0.07
            }
        }))
        
        # Run badge generator
        badges_dir = tmppath / "badges"
        result = subprocess.run([
            sys.executable, "tools/ief_badges.py",
            "--verify", str(verify_file),
            "--root", str(tmppath),
            "--out", str(badges_dir)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Badge generator failed:\n{result.stderr}")
            return False
        
        # Check output
        expected_files = ["trace.json", "risk.json", "quality.json", "impact_energy.json", "impact_co2.json"]
        badge_asset_dir = badges_dir / "TEST" / "SN-001"
        
        for fname in expected_files:
            fpath = badge_asset_dir / fname
            if not fpath.exists():
                print(f"Missing badge file: {fname}")
                return False
            
            # Verify JSON is valid
            try:
                badge_data = json.loads(fpath.read_text())
                assert badge_data.get("schemaVersion") == 1
                assert "label" in badge_data
                assert "message" in badge_data
                assert "color" in badge_data
            except Exception as e:
                print(f"Invalid badge JSON in {fname}: {e}")
                return False
        
        print("✓ Badge generator test passed")
        return True


def test_passport_assembler():
    """Test passport assembler with sample data"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        
        # Create sample verification results
        verify_dir = tmppath / "verification"
        verify_dir.mkdir()
        verify_file = verify_dir / "verify-results.json"
        verify_file.write_text(json.dumps({
            "version": "0.1",
            "generated_at": "2025-10-05T16:30:00Z",
            "results": [
                {
                    "asset_uid": "urn:ideale:test:asset:001",
                    "path": "events/TEST/MIC/SN-001/evt-001.json",
                    "status": "pass",
                    "hash": "sha256:test123"
                }
            ]
        }))
        
        # Create sample event
        events_dir = tmppath / "events" / "TEST" / "MIC" / "SN-001"
        events_dir.mkdir(parents=True)
        event_file = events_dir / "evt-001.json"
        event_file.write_text(json.dumps({
            "ief_version": "0.1",
            "event_type": "service",
            "ts": "2025-10-05T15:30:00Z",
            "calc": {
                "energy_kwh_est": 0.010,
                "co2e_kg_est": 0.002,
                "quality_score": 0.97,
                "risk_score": 0.07
            }
        }))
        
        # Run passport assembler
        passport_dir = tmppath / "evidence" / "passports"
        result = subprocess.run([
            sys.executable, "tools/ief_assemble_passport.py",
            "--verify", str(verify_file),
            "--asset", "urn:ideale:test:asset:001",
            "--family", "TEST",
            "--model", "M1",
            "--variant", "V1",
            "--domain", "TEST",
            "--ata", "ATA-00",
            "--sbom", "sbom/test.spdx.json",
            "--policy-sha", "sha256:test",
            "--root", str(tmppath),
            "--out-root", str(passport_dir),
            "--badges-root", "badges"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Passport assembler failed:\n{result.stderr}")
            return False
        
        # Check output
        passport_file = passport_dir / "TEST" / "SN-001.json"
        if not passport_file.exists():
            print(f"Missing passport file: {passport_file}")
            return False
        
        # Verify passport structure
        try:
            passport = json.loads(passport_file.read_text())
            assert passport.get("passport_version") == "0.1"
            assert passport.get("ief_version") == "0.1"
            assert "asset" in passport
            assert "events" in passport
            assert "calculations" in passport
            assert "badges" in passport
            assert "evidence" in passport
            assert "privacy" in passport
        except Exception as e:
            print(f"Invalid passport JSON: {e}")
            return False
        
        print("✓ Passport assembler test passed")
        return True


def test_event_templates():
    """Test that event templates are valid JSON"""
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("Templates directory not found")
        return False
    
    templates = ["event-inspect.json", "event-transport.json", "event-assemble.json"]
    for template_name in templates:
        template_path = templates_dir / template_name
        if not template_path.exists():
            print(f"Missing template: {template_name}")
            return False
        
        try:
            template_data = json.loads(template_path.read_text())
            assert template_data.get("ief_version") == "0.1"
            assert "event_type" in template_data
            assert "ts" in template_data
            assert "actor" in template_data
            assert "asset" in template_data
            assert "context" in template_data
            assert "signatures" in template_data
            assert "calc" in template_data
        except Exception as e:
            print(f"Invalid template {template_name}: {e}")
            return False
    
    print("✓ Event templates test passed")
    return True


if __name__ == "__main__":
    print("Running IEF HUELLΔ smoke tests...")
    print()
    
    tests = [
        test_event_templates,
        test_badge_generator,
        test_passport_assembler
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print()
    print(f"Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
