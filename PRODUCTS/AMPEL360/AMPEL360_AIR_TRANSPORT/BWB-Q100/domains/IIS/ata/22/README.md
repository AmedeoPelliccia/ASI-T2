---
id: ATA-22-OV-0001
project: PRODUCTS/AMPEL360/AMPEL360_AIR_TRANSPORT
artifact: /home/runner/work/ASI-T2/ASI-T2/PRODUCTS/AMPEL360/AMPEL360_AIR_TRANSPORT/BWB-Q100/domains/IIS/ata/22/README.md
llc: SYSTEMS
classification: INTERNAL–EVIDENCE-REQUIRED
version: 0.2.0
release_date: 2026-01-08
maintainer: "ASI-T Architecture Team"
bridge: "CB→QB→UE→FE→FWD→QS"
ethics_guard: MAL-EEM
utcs_mi: v5.0
canonical_hash: "TBD"
---

# ATA 22 — Auto Flight (BWB-Q100)

**ES:** Publicaciones y evidencia para **ATA-22 (Auto Flight)**.  
**EN:** Publications and evidence for **ATA 22 Auto Flight** system.

> **Scope:** Flight guidance, automatic flight functions (autopilot, auto-throttle, monitoring, load alleviation). This chapter covers the Auto Flight system **but NOT** primary flight controls (ATA 27), communications (ATA 23), or power generation (ATA 24).

---

## ATA iSpec 2200 / ATA Standard Numbering System

The **ATA Standard Numbering System** is published as an **extract of ATA iSpec 2200** by Airlines for America (A4A). ([A4A Publications](https://publications.airlines.org/products/ispec-2200-extract-ata-standard-numbering-system-revision-2024-1))

**ATA 22 = Auto Flight** is scoped to **flight guidance/automatic flight functions** (autopilot/auto-throttle/monitoring/load alleviation), **not** primary flight controls, comms, or power generation.

---

## ATA 22 Auto Flight (SNS breakdown)

The commonly used SNS section breakdown for **ATA 22** is: ([itlims-zsis.meil.pw.edu.pl](https://itlims-zsis.meil.pw.edu.pl/pomoce/ESL/2016/ATA_Chapters.pdf))

* **22-00 — Auto Flight, General**
* **22-10 — Autopilot**
* **22-20 — Speed–Attitude Correction**
* **22-30 — Auto Throttle**
* **22-40 — System Monitor**
* **22-50 — Aerodynamic Load Alleviating**

---

## What belongs in each ATA 22 section (BWB + H₂ fuel cell / electric context)

### 22-00 Auto Flight, General

**Scope:** architecture, modes philosophy, redundancy concept, integration boundaries, dispatch criteria, maintenance overview.

**BWB deltas:** mode logic and limitations tied to BWB envelope (e.g., pitch-moment management, trim strategy, high-lift interactions), electrical power quality assumptions (ride-through, brownout behavior), DAL allocation rationale for AF functions.

### 22-10 Autopilot

**Scope:** automatic control laws (AP), engagement/disengagement logic, fail-operational/fail-passive behavior, servo/command outputs **to the Flight Control System** (but **not** the flight controls themselves).

**BWB deltas:** distributed control effectors (elevons/spoilers/drag devices) coordination and reconfiguration handling; integration with FBW laws and gust response.

### 22-20 Speed–Attitude Correction

**Scope:** speed/attitude capture and correction functions that sit "between" guidance and control (depending on OEM, this may include speed stability augmentation behaviors).

**BWB deltas:** tighter coupling to energy state management (electric propulsion responsiveness, thrust limits, fuel cell transient constraints) and to load alleviation constraints.

### 22-30 Auto Throttle

**Scope:** autothrottle/autothrust computation and mode logic; commands **to propulsion control**.

**BWB H₂-electric deltas:** thrust command shaping to respect **fuel cell dynamics**, battery buffering strategy, inverter limits, thermal derates, and any distributed propulsion allocation logic (if propulsors are multiple).

### 22-40 System Monitor

**Scope:** monitoring, built-in tests, fault detection/isolation, mode inhibition, annunciations specific to Auto Flight.

**BWB deltas:** expanded monitoring of cross-domain dependencies (power availability, network health, flight control reconfiguration state), and robust "graceful degradation" mode tables.

### 22-50 Aerodynamic Load Alleviating

**Scope:** gust/load alleviation functions (structural load reduction via control law scheduling).

**BWB deltas:** typically more prominent due to large lifting surfaces and structural bending sensitivities; close integration with FBW and structural monitoring; explicit constraints to avoid adverse aeroelastic excitation.

---

## Boundary map (what is *not* ATA 22)

Other systems live in different ATA chapters: ([Wikipedia ATA 100](https://en.wikipedia.org/wiki/ATA_100))

* **Flight controls / actuators / FCC for surfaces:** **ATA 27** (Flight Controls)
* **Navigation sensors / GNSS / INS / RNAV:** **ATA 34** (Navigation)
* **Comms (VHF/HF/SATCOM):** **ATA 23** (Communications)
* **Electrical generation/distribution:** **ATA 24** (Electrical Power)
* **Displays / indicating / warnings:** largely **ATA 31** (Indicating/Recording)
* **Fire detection/suppression:** **ATA 26** (Fire Protection)
* **IMA / avionics computing platform:** often **ATA 42** (Integrated Modular Avionics) in many schemes

**Important note (OEM variance):** some manufacturers place **FMS** content under **ATA 34-60 (Flight Management Computing)** rather than ATA 22; treat FMS as a cross-reference, and decide one home chapter in your SSOT to avoid duplication.

---

## Directory Structure

See `/PRODUCTS/AMPEL360/AMPEL360_AIR_TRANSPORT/BWB-Q100/domains/IIS/ata/ATA-22-auto-flight/` for the complete breakdown with SSOT (lifecycle phases) and PUB (AMM/IPC) structures for each section.
