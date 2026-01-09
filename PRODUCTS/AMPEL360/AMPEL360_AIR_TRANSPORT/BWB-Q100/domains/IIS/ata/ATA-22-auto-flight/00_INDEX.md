---
id: ATA-22-INDEX
project: PRODUCTS/AMPEL360/BWB-Q100
artifact: PRODUCTS/AMPEL360/AMPEL360_AIR_TRANSPORT/BWB-Q100/domains/IIS/ata/ATA-22-auto-flight/00_INDEX.md
llc: SYSTEMS
classification: INTERNAL–EVIDENCE-REQUIRED
version: 1.0.0
release_date: 2026-01-08
maintainer: "ASI-T Architecture Team"
bridge: "CB→QB→UE→FE→FWD→QS"
ethics_guard: MAL-EEM
utcs_mi: v5.0
canonical_hash: "TBD"
---

# ATA-22 Auto Flight — Quick Navigation Index

## 📑 Main Documentation

- [README.md](./README.md) — Complete system overview and structure
- [ATA 22 Overview](../22/README.md) — Original ATA 22 reference

## 🔧 ATA 22 Sections

### 22-00 Auto Flight, General
**Path:** `22-00-auto-flight-general/22-00-00-auto-flight-general/`

Architecture, modes philosophy, redundancy concept, integration boundaries.

- [SSOT](./22-00-auto-flight-general/22-00-00-auto-flight-general/SSOT/)
- [Publications (AMM)](./22-00-auto-flight-general/22-00-00-auto-flight-general/PUB/AMM/)
- [Publications (IPC)](./22-00-auto-flight-general/22-00-00-auto-flight-general/PUB/IPC/)

---

### 22-10 Autopilot
**Path:** `22-10-autopilot/22-10-00-autopilot-general/`

Automatic control laws, engagement/disengagement logic, fail-operational behavior.

- [SSOT](./22-10-autopilot/22-10-00-autopilot-general/SSOT/)
- [Publications (AMM)](./22-10-autopilot/22-10-00-autopilot-general/PUB/AMM/)
- [Publications (IPC)](./22-10-autopilot/22-10-00-autopilot-general/PUB/IPC/)

---

### 22-20 Speed–Attitude Correction
**Path:** `22-20-speed-attitude-correction/22-20-00-speed-attitude-correction-general/`

Speed/attitude capture and correction functions.

- [SSOT](./22-20-speed-attitude-correction/22-20-00-speed-attitude-correction-general/SSOT/)
- [Publications (AMM)](./22-20-speed-attitude-correction/22-20-00-speed-attitude-correction-general/PUB/AMM/)
- [Publications (IPC)](./22-20-speed-attitude-correction/22-20-00-speed-attitude-correction-general/PUB/IPC/)

---

### 22-30 Auto Throttle
**Path:** `22-30-auto-throttle/22-30-00-auto-throttle-general/`

Autothrottle/autothrust computation and mode logic for H₂-electric propulsion.

- [SSOT](./22-30-auto-throttle/22-30-00-auto-throttle-general/SSOT/)
- [Publications (AMM)](./22-30-auto-throttle/22-30-00-auto-throttle-general/PUB/AMM/)
- [Publications (IPC)](./22-30-auto-throttle/22-30-00-auto-throttle-general/PUB/IPC/)

---

### 22-40 System Monitor
**Path:** `22-40-system-monitor/22-40-00-system-monitor-general/`

Monitoring, built-in tests, fault detection/isolation, mode inhibition.

- [SSOT](./22-40-system-monitor/22-40-00-system-monitor-general/SSOT/)
- [Publications (AMM)](./22-40-system-monitor/22-40-00-system-monitor-general/PUB/AMM/)
- [Publications (IPC)](./22-40-system-monitor/22-40-00-system-monitor-general/PUB/IPC/)

---

### 22-50 Aerodynamic Load Alleviating
**Path:** `22-50-aerodynamic-load-alleviating/22-50-00-load-alleviation-general/`

Gust/load alleviation functions for structural load reduction.

- [SSOT](./22-50-aerodynamic-load-alleviating/22-50-00-load-alleviation-general/SSOT/)
- [Publications (AMM)](./22-50-aerodynamic-load-alleviating/22-50-00-load-alleviation-general/PUB/AMM/)
- [Publications (IPC)](./22-50-aerodynamic-load-alleviating/22-50-00-load-alleviation-general/PUB/IPC/)

---

## 📚 Lifecycle Phases (SSOT)

Each section includes these lifecycle directories:

| Phase | Directory | Purpose |
|-------|-----------|---------|
| LC01 | Requirements | Stakeholder requirements, operational concepts |
| LC02 | System_Requirements | Derived technical requirements |
| LC03 | Design | Architecture, interfaces, algorithms |
| LC04 | Analysis | Performance, safety, trade studies |
| LC05 | VnV | Verification & Validation plans and results |
| LC06 | Quality | Reviews, audits, metrics |
| LC07 | Safety | Safety analysis, hazard logs, FMEA |
| LC08 | Certification | Compliance documentation, certification artifacts |

## 📖 Publication Structure (PUB)

Each section includes S1000D-compliant publications:

### AMM (Aircraft Maintenance Manual)
- **DM** — Data Modules
- **PM** — Publication Modules
- **DML** — Data Module List
- **ICN** — Illustrations
- **BREX** — Business Rules Exchange
- **COMMON** — Common Information Repositories
- **APPLICABILITY** — Applicability cross-reference

### IPC (Illustrated Parts Catalog)
- Same structure as AMM

## 🔗 Cross-References

### Related ATA Chapters (NOT in ATA 22)
- **ATA 23** — Communications
- **ATA 24** — Electrical Power
- **ATA 26** — Fire Protection
- **ATA 27** — Flight Controls
- **ATA 31** — Indicating/Recording
- **ATA 34** — Navigation
- **ATA 42** — Integrated Modular Avionics

## 🌐 External References

- [ATA iSpec 2200 (A4A)](https://publications.airlines.org/products/ispec-2200-extract-ata-standard-numbering-system-revision-2024-1)
- [ATA Chapters Reference](https://itlims-zsis.meil.pw.edu.pl/pomoce/ESL/2016/ATA_Chapters.pdf)
- [ATA 100 (Wikipedia)](https://en.wikipedia.org/wiki/ATA_100)

---

**Last Updated:** 2026-01-08  
**Maintainer:** ASI-T Architecture Team
