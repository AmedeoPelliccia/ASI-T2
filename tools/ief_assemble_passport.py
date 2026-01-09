#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IEF · HUELLΔ passport assembler

Example:
  python tools/ief_assemble_passport.py \
      --verify verification/verify-results.json \
      --asset "urn:ideale:component:AAA:BWQ1:FWD-SPAR:SN-000123" \
      --family AMPEL360 --model BWB --variant Q100 \
      --domain AAA --ata ATA-57 \
      --sbom sbom/AMPEL360-BWQ1.spdx.json \
      --policy-sha sha256:...pinned... \
      --root . --out-root evidence/passports --badges-root badges
"""
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone


def load_verify(path: Path) -> list:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("results", [])


def load_event(root: Path, path: str):
    fp = (root / path).resolve()
    return json.loads(fp.read_text(encoding="utf-8"))


def first_existing(root: Path, candidates):
    for p in candidates:
        fp = (root / p).resolve()
        if fp.exists():
            return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", required=True)
    ap.add_argument("--asset", required=True, help="UID del activo")
    ap.add_argument("--family", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--domain", required=True)
    ap.add_argument("--ata", required=True)
    ap.add_argument("--sbom", required=True)
    ap.add_argument("--policy-sha", required=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--out-root", default="evidence/passports")
    ap.add_argument("--badges-root", default="badges")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    results = load_verify(Path(args.verify))

    evrecs = [r for r in results if r.get("asset_uid") == args.asset and r.get("status") == "pass"]
    if not evrecs:
        raise SystemExit(f"No hay eventos verificados para {args.asset}")

    # inferir dominio/serie desde el primer evento
    first_path = evrecs[0]["path"]
    parts = Path(first_path).parts
    serial = "ASSET"
    domain = args.domain
    if len(parts) >= 4 and parts[0] == "events":
        domain = parts[1]
        serial = parts[3] if parts[2] else serial

    # agrega métricas
    stages, sum_energy, sum_co2 = set(), 0.0, 0.0
    max_risk, min_quality = None, None
    events_out = []
    have_energy, have_co2 = False, False

    for r in evrecs:
        p = r["path"]
        evt = load_event(root, p)
        calc = evt.get("calc", {})
        # métricas
        rv = calc.get("risk_score")
        if isinstance(rv, (int, float)):
            max_risk = rv if (max_risk is None or rv > max_risk) else max_risk
        qv = calc.get("quality_score")
        if isinstance(qv, (int, float)):
            min_quality = qv if (min_quality is None or qv < min_quality) else min_quality
        ev = calc.get("energy_kwh_est")
        if isinstance(ev, (int, float)):
            sum_energy += float(ev)
            have_energy = True
        cv = calc.get("co2e_kg_est")
        if isinstance(cv, (int, float)):
            sum_co2 += float(cv)
            have_co2 = True
        et = evt.get("event_type")
        if et:
            stages.add(et.lower())
        # huella del propio evento
        events_out.append({
            "path": p,
            "sha256": r.get("hash") or "",  # si en el futuro añades hash de evento aquí
            "ts": evt.get("ts")
        })

    coverage = {k: (k in stages) for k in ["assemble", "service", "transport", "handoff"]}

    # endpoints de badges esperados
    badge_dir = Path(args.badges_root) / domain / serial
    trace_ep = str(badge_dir / "trace.json").replace("\\", "/")
    risk_ep = str(badge_dir / "risk.json").replace("\\", "/")

    # construye pasaporte
    passport = {
        "passport_version": "0.1",
        "ief_version": "0.1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "asset": {
            "uid": args.asset,
            "family": args.family,
            "model": args.model,
            "variant": args.variant,
            "domain": domain,
            "ata": args.ata
        },
        "lifecycle": {
            "design_ref": None,
            "manufacture_ref": None,
            "service_state": "unknown"
        },
        "events": events_out,
        "calculations": {
            "energy_kwh_total_est": sum_energy if have_energy else None,
            "co2e_kg_total_est": sum_co2 if have_co2 else None,
            "quality_min": min_quality,
            "risk_max": max_risk,
            "coverage": coverage
        },
        "badges": [
            {"name": "Traceability", "endpoint": trace_ep},
            {"name": "Risk", "endpoint": risk_ep}
        ],
        "evidence": {
            "sbom": args.sbom,
            "verify_log": args.verify,
            "signatures": [],  # opcional: agrega bundles si quieres
            "policy_hash": args.policy_sha
        },
        "privacy": {
            "geohash_precision": 5,
            "pii": "none"
        }
    }

    out_dir = (Path(args.out_root) / domain).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    outp = out_dir / f"{serial}.json"
    outp.write_text(json.dumps(passport, indent=2), encoding="utf-8")
    print(f"✓ passport → {outp}")


if __name__ == "__main__":
    main()
