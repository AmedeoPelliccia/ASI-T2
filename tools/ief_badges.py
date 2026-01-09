#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IEF · HUELLΔ badge generator (no external deps)

Examples:
  # Genera badges para todos los assets vistos en verify-results
  python tools/ief_badges.py \
      --verify verification/verify-results.json \
      --root . \
      --out badges/

  # Solo para un asset concreto (UID)
  python tools/ief_badges.py \
      --verify verification/verify-results.json \
      --asset "urn:ideale:component:AAA:BWQ1:FWD-SPAR:SN-000123" \
      --root . --out badges/
"""
import argparse
import json
import sys
from pathlib import Path

# Cobertura objetivo por ciclo de vida (ajusta si quieres)
TARGET_STAGES = {"assemble", "service", "transport", "handoff"}


def load_verify(path: Path) -> list:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("results", [])


def safe_load_event(root: Path, path: str):
    try:
        fp = (root / path).resolve()
        return json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return None


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def badge_json(label, message, color):
    return {
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color
    }


def color_for_trace(covered: int, total: int):
    ratio = covered / max(1, total)
    if ratio >= 1.0:
        return "brightgreen"
    if ratio >= 0.75:
        return "green"
    if ratio >= 0.5:
        return "yellow"
    return "orange"


def color_for_risk(r):
    if r is None:
        return "lightgrey"
    if r <= 0.20:
        return "success"
    if r <= 0.50:
        return "yellow"
    if r <= 0.80:
        return "orange"
    return "red"


def color_for_quality(q):
    if q is None:
        return "lightgrey"
    if q >= 0.98:
        return "brightgreen"
    if q >= 0.95:
        return "green"
    if q >= 0.90:
        return "yellow"
    return "orange"


def color_for_energy(kwh):
    if kwh is None:
        return "lightgrey"
    if kwh <= 1.0:
        return "brightgreen"
    if kwh <= 10.0:
        return "green"
    if kwh <= 50.0:
        return "yellow"
    return "orange"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", required=True, help="verification/verify-results.json")
    ap.add_argument("--root", default=".", help="Repo root para resolver rutas")
    ap.add_argument("--out", required=True, help="Directorio raíz para badges/")
    ap.add_argument("--asset", help="UID de activo (opcional; si falta, procesa todos)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out_root = Path(args.out).resolve()
    results = load_verify(Path(args.verify))

    # Agrupa por asset_uid con sus event file paths
    by_asset = {}
    for r in results:
        asset = r.get("asset_uid")
        if not asset:
            continue
        by_asset.setdefault(asset, []).append(r)

    if args.asset:
        by_asset = {args.asset: by_asset.get(args.asset, [])}

    generated = 0
    for asset_uid, items in by_asset.items():
        # Descubre un path estable para el asset: intenta inferir dominio/serie de ruta
        # Buscamos el primer evento que exista físicamente para derivar carpeta
        event_paths = []
        for r in items:
            p = r.get("path")
            if not p:
                continue
            # Adivina ubicación de carpeta de badges desde event path
            event_paths.append(p)

        # Métricas agregadas
        stages = set()
        max_risk = None
        min_quality = None
        sum_energy = 0.0
        sum_co2 = 0.0
        have_energy = False
        have_co2 = False

        # Itera eventos reales y lee "calc" si existe
        for r in items:
            p = r.get("path")
            evt = safe_load_event(root, p) if p else None
            if not evt:
                continue
            et = evt.get("event_type")
            if et:
                # normaliza a minúsculas
                stages.add(et.lower())
            calc = evt.get("calc", {})
            if isinstance(calc, dict):
                # risk
                rv = calc.get("risk_score")
                if isinstance(rv, (int, float)):
                    max_risk = rv if (max_risk is None or rv > max_risk) else max_risk
                # quality
                qv = calc.get("quality_score")
                if isinstance(qv, (int, float)):
                    min_quality = qv if (min_quality is None or qv < min_quality) else min_quality
                # energy
                ev = calc.get("energy_kwh_est")
                if isinstance(ev, (int, float)):
                    sum_energy += float(ev)
                    have_energy = True
                # co2
                cv = calc.get("co2e_kg_est")
                if isinstance(cv, (int, float)):
                    sum_co2 += float(cv)
                    have_co2 = True

        # Determina carpeta de salida: badges/<DOMAIN>/<SERIAL|ASSET_ID>/
        # Intento: si algún event path contiene "AAA/<MIC>/<SERIAL>", reutilízalo:
        # p.ej: events/AAA/BWQ1/SN-000123/evt-045.json  -> badges/AAA/SN-000123/
        out_dir = None
        for p in event_paths:
            parts = Path(p).parts
            if len(parts) >= 4 and parts[0] == "events":
                domain = parts[1]
                # Try to extract serial from the path
                # If parts[3] looks like a file (has extension), use parts[2] as serial
                # Otherwise, use parts[3] as serial
                if len(parts) >= 5:
                    # events/DOMAIN/MIC/SERIAL/file.json
                    serial = parts[3]
                elif len(parts) == 4 and not parts[3].endswith('.json'):
                    # events/DOMAIN/MIC/SERIAL (folder, no file yet)
                    serial = parts[3]
                else:
                    # events/DOMAIN/SERIAL/file.json or events/DOMAIN/MIC
                    serial = parts[2] if len(parts) >= 3 else "ASSET"
                out_dir = out_root / domain / serial
                break
        if out_dir is None:
            # fallback genérico: badges/GEN/<hash-short>
            out_dir = out_root / "GEN" / (asset_uid[-12:].replace(":", "_"))
        ensure_dir(out_dir)

        # 1) TRACE
        covered = len(TARGET_STAGES.intersection({s.lower() for s in stages}))
        total = len(TARGET_STAGES)
        trace_msg = "complete v1.0" if covered == total else f"partial {covered}/{total}"
        trace = badge_json("Traceability", trace_msg, color_for_trace(covered, total))
        (out_dir / "trace.json").write_text(json.dumps(trace, indent=2), encoding="utf-8")

        # 2) RISK
        risk_msg = "unknown" if max_risk is None else f"{'low' if max_risk<=0.2 else 'mid' if max_risk<=0.5 else 'high' if max_risk<=0.8 else 'blocked'} · {max_risk:.2f}"
        risk = badge_json("Risk", risk_msg, color_for_risk(max_risk))
        (out_dir / "risk.json").write_text(json.dumps(risk, indent=2), encoding="utf-8")

        # 3) QUALITY
        qual_msg = "unknown" if min_quality is None else f"{min_quality:.3f}"
        qual = badge_json("Quality(min)", qual_msg, color_for_quality(min_quality))
        (out_dir / "quality.json").write_text(json.dumps(qual, indent=2), encoding="utf-8")

        # 4) IMPACT (energía/CO₂)
        if have_energy:
            imp = badge_json("Energy Σ", f"{sum_energy:.3f} kWh", color_for_energy(sum_energy))
            (out_dir / "impact_energy.json").write_text(json.dumps(imp, indent=2), encoding="utf-8")
        if have_co2:
            co2 = badge_json("CO₂e Σ", f"{sum_co2:.3f} kg", color_for_energy(sum_energy if have_energy else 0.0))
            (out_dir / "impact_co2.json").write_text(json.dumps(co2, indent=2), encoding="utf-8")

        generated += 1
        print(f"✓ badges → {out_dir}  [{asset_uid}]")

    if generated == 0:
        print("Nada que generar (¿UID no encontrado o verify-results vacío?)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
