---
id: ATA-22-AUTO-FLIGHT-ROOT
project: PRODUCTS/AMPEL360/BWB-Q100
artifact: PRODUCTS/AMPEL360/AMPEL360_AIR_TRANSPORT/BWB-Q100/domains/IIS/ata/ATA-22-auto-flight/README.md
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

# ATA-22 Auto Flight — Directory Structure

This directory contains the complete **ATA 22 Auto Flight** system breakdown for the **BWB-Q100** hydrogen-hybrid aircraft, following the **ATA iSpec 2200 / ATA Standard Numbering System**.

## Overview

**ATA 22 = Auto Flight** is scoped to **flight guidance/automatic flight functions**:
- Autopilot
- Auto-throttle
- Monitoring
- Load alleviation

**NOT included in ATA 22:**
- Primary flight controls (→ ATA 27)
- Communications (→ ATA 23)
- Power generation (→ ATA 24)
- Navigation sensors (→ ATA 34)
- Cockpit displays (→ ATA 31)
- IMA computing platform (→ ATA 42)

## Directory Structure

```
ATA-22-auto-flight/
├── 00_INDEX.md                                    # Quick navigation index
├── README.md                                      # This file
│
├── 22-00-auto-flight-general/
│  ├── 22-00-00-auto-flight-general/
│  │  ├── SSOT/                                   # Single Source of Truth (lifecycle)
│  │  │  ├── LC01_Requirements/
│  │  │  ├── LC02_System_Requirements/
│  │  │  ├── LC03_Design/
│  │  │  ├── LC04_Analysis/
│  │  │  ├── LC05_VnV/
│  │  │  ├── LC06_Quality/
│  │  │  ├── LC07_Safety/
│  │  │  └── LC08_Certification/
│  │  └── PUB/                                    # Publications (S1000D)
│  │     ├── AMM/                                 # Aircraft Maintenance Manual
│  │     │  ├── CSDB/
│  │     │  │  ├── DM/                           # Data Modules
│  │     │  │  ├── PM/                           # Publication Modules
│  │     │  │  ├── DML/                          # Data Module List
│  │     │  │  ├── ICN/                          # Illustrations
│  │     │  │  ├── BREX/                         # Business Rules Exchange
│  │     │  │  ├── COMMON/                       # Common Information Repositories
│  │     │  │  └── APPLICABILITY/                # Applicability
│  │     │  ├── EXPORT/
│  │     │  ├── bindings.csv
│  │     │  └── csdb.profile.yaml
│  │     └── IPC/                                 # Illustrated Parts Catalog
│  │        ├── CSDB/
│  │        │  ├── DM/
│  │        │  ├── PM/
│  │        │  ├── DML/
│  │        │  ├── ICN/
│  │        │  ├── BREX/
│  │        │  ├── COMMON/
│  │        │  └── APPLICABILITY/
│  │        ├── EXPORT/
│  │        ├── bindings.csv
│  │        └── csdb.profile.yaml
│  └── 22-00-YY-<subject-name>/                   # Add as needed
│
├── 22-10-autopilot/
│  ├── 22-10-00-autopilot-general/
│  │  ├── SSOT/ (LC01..LC08 as above)
│  │  └── PUB/ (AMM + IPC as above)
│  └── 22-10-YY-<subject-name>/
│
├── 22-20-speed-attitude-correction/
│  ├── 22-20-00-speed-attitude-correction-general/
│  │  ├── SSOT/ (LC01..LC08)
│  │  └── PUB/ (AMM + IPC)
│  └── 22-20-YY-<subject-name>/
│
├── 22-30-auto-throttle/
│  ├── 22-30-00-auto-throttle-general/
│  │  ├── SSOT/ (LC01..LC08)
│  │  └── PUB/ (AMM + IPC)
│  └── 22-30-YY-<subject-name>/
│
├── 22-40-system-monitor/
│  ├── 22-40-00-system-monitor-general/
│  │  ├── SSOT/ (LC01..LC08)
│  │  └── PUB/ (AMM + IPC)
│  └── 22-40-YY-<subject-name>/
│
└── 22-50-aerodynamic-load-alleviating/
   ├── 22-50-00-load-alleviation-general/
   │  ├── SSOT/ (LC01..LC08)
   │  └── PUB/ (AMM + IPC)
   └── 22-50-YY-<subject-name>/
```

## Section Breakdown

### 22-00 Auto Flight, General

**Scope:** Architecture, modes philosophy, redundancy concept, integration boundaries, dispatch criteria, maintenance overview.

**BWB deltas:** Mode logic and limitations tied to BWB envelope (pitch-moment management, trim strategy, high-lift interactions), electrical power quality assumptions (ride-through, brownout behavior), DAL allocation rationale for AF functions.

### 22-10 Autopilot

**Scope:** Automatic control laws (AP), engagement/disengagement logic, fail-operational/fail-passive behavior, servo/command outputs **to the Flight Control System** (but **not** the flight controls themselves).

**BWB deltas:** Distributed control effectors (elevons/spoilers/drag devices) coordination and reconfiguration handling; integration with FBW laws and gust response.

### 22-20 Speed–Attitude Correction

**Scope:** Speed/attitude capture and correction functions that sit "between" guidance and control (depending on OEM, this may include speed stability augmentation behaviors).

**BWB deltas:** Tighter coupling to energy state management (electric propulsion responsiveness, thrust limits, fuel cell transient constraints) and to load alleviation constraints.

### 22-30 Auto Throttle

**Scope:** Autothrottle/autothrust computation and mode logic; commands **to propulsion control**.

**BWB H₂-electric deltas:** Thrust command shaping to respect **fuel cell dynamics**, battery buffering strategy, inverter limits, thermal derates, and any distributed propulsion allocation logic (if propulsors are multiple).

### 22-40 System Monitor

**Scope:** Monitoring, built-in tests, fault detection/isolation, mode inhibition, annunciations specific to Auto Flight.

**BWB deltas:** Expanded monitoring of cross-domain dependencies (power availability, network health, flight control reconfiguration state), and robust "graceful degradation" mode tables.

### 22-50 Aerodynamic Load Alleviating

**Scope:** Gust/load alleviation functions (structural load reduction via control law scheduling).

**BWB deltas:** Typically more prominent due to large lifting surfaces and structural bending sensitivities; close integration with FBW and structural monitoring; explicit constraints to avoid adverse aeroelastic excitation.

## SSOT Lifecycle Phases

Each section contains a **SSOT/** directory with lifecycle phases:

- **LC01_Requirements** — Stakeholder requirements, operational concepts
- **LC02_System_Requirements** — Derived technical requirements
- **LC03_Design** — Architecture, interfaces, algorithms
- **LC04_Analysis** — Performance, safety, trade studies
- **LC05_VnV** — Verification & Validation plans and results
- **LC06_Quality** — Reviews, audits, metrics
- **LC07_Safety** — Safety analysis, hazard logs, FMEA
- **LC08_Certification** — Compliance documentation, certification artifacts

## Publications (S1000D)

Each section contains a **PUB/** directory with:

- **AMM (Aircraft Maintenance Manual)** — Maintenance procedures, fault isolation
- **IPC (Illustrated Parts Catalog)** — Parts identification, illustrated breakdowns

Both follow **S1000D** standards with CSDB (Common Source Database) structure.

## References

- **ATA iSpec 2200** — [Airlines for America (A4A)](https://publications.airlines.org/products/ispec-2200-extract-ata-standard-numbering-system-revision-2024-1)
- **ATA Chapters** — [itlims-zsis.meil.pw.edu.pl](https://itlims-zsis.meil.pw.edu.pl/pomoce/ESL/2016/ATA_Chapters.pdf)
- **ATA 100** — [Wikipedia](https://en.wikipedia.org/wiki/ATA_100)

## Version History

- **v1.0.0 (2026-01-08)** — Initial structure with all six ATA 22 sections
