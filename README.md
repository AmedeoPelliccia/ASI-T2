---
id: ASIT2-README.md
project: ASI-T2
artifact: Repository Master README
llc: GENESIS
classification: INTERNAL–EVIDENCE-REQUIRED
version: 1.0.6
release_date: "2025-10-01"
maintainer: "ASI-T Architecture Team"
bridge: "CB→QB→UE→FE→FWD→QS"
ethics_guard: MAL-EEM
utcs_mi: v5.0
framework: IDEALE.eu
ideale_pillars:
  - Intelligence
  - Defense
  - Energy
  - Aerospace
  - Logistics
  - ESG
  - Europe
canonical_hash: pending
---

# IDEALE.eu — Intelligence • Defense • Energy • Aerospace • Logistics • ESG

[**IDEALE.eu**](https://ideale.eu) is a federated **brand & standards** program for **verifiable critical systems**. We prioritize **evidence over assertions** and publish portable formats and vendor‑neutral CI hooks.

> **Principle:** If it didn’t run in **CI**, it doesn’t count as **evidence**.

- **Public framework:** [**IDEALE Evidence Framework (IEF)**](#ideale-evidence-framework-ief)  
- **Primary sector profile:** [**TFA · Aerospace**](#tfa-aerospace-domain-profile)  
- **Reference implementation:** [**ASI‑T2**](#asit2-reference-implementation)

---

## 📚 Quick Nav

- [What is IDEALE?](#what-is-ideale)
- [Naming Canon](#naming-canon)
- [IDEALE Evidence Framework (IEF)](#ideale-evidence-framework-ief)
- [Visual Overview](#visual-overview)
- [Sector Profiles](#sector-profiles)
- [ASI‑T2 · Reference Implementation](#asit2-reference-implementation)
- [Programs by Pillar · IDEALE](#programs-by-pillar-ideale)
- [Evidence Objects](#evidence-objects)
- [Conformance Ladder](#conformance-ladder)
- [Roadmap Phases](#roadmap-phases)
- [Contact & Pilots](#contact-pilots)
- [Link Map](#link-map-for-clustered-keywords)

---

## What is IDEALE?

**IDEALE.eu** is an open **brand + standards** initiative that enables **verifiability** across Europe’s strategic sectors (Intelligence, Defense, Energy, Aerospace, Logistics, ESG). The specifications let teams produce **verifiable artifacts** that travel between tools and organizations without vendor lock‑in.

> **Bridge flow · TFA canon:** **QS→FWD→UE→FE→CB→QB**.

---

## Naming Canon

**Entity types**

- **Family** — related products sharing a common baseline (**AMPEL360**, **GAIA**). Families are organized into **Manned Vehicles**, **Unmanned Vehicles**, and **Infrastructure Systems** (**INFRANET**).

- **Model** — the product baseline within a family (e.g., **BWB** under AMPEL360: Blended‑Wing‑Body, hydrogen‑hybrid baseline).

- **Variant** — a **configured model** of a given model for a specific mission or capacity (e.g., **Q100** under BWB for ~100 passengers, quantum‑enhanced).

- **Program** — a sustained line of work or capability stream (e.g., **LH2_CORRIDOR**, **GAIA‑AIR DRONES**, **GAIA‑SEA HYDROBOTS**, **GAIA‑SPACE IDENTITY**).

**Canonical invariants**

- **AMPEL360** is a **family**.  
- **BWB** is the **model** under AMPEL360 Air Transport.  
- **Q100** is the **variant** (configured model) of BWB.

---

## IDEALE Evidence Framework (IEF)

A reusable **evidence & verification layer** adoptable in stages.

- **Manifests:** **UTCS** / **CXP**  
- **SBOM:** **SPDX 2.3 JSON**  
- **Verify & Replay:** policy‑pinned verification, hash‑chained logs, reproducibility  
- **Badges:** human‑readable status + machine endpoints for procurement/regulatory portals

**Open evidence flow · UTCS → SPDX → Verify → Badge**

1) **UTCS/CXP** anchor who/what/where/when/why.  
2) **SPDX SBOM** records components & licenses.  
3) **Verify (CI)** enforces policy and emits a replayable log.  
4) **Badge** publishes status and links to evidence blobs.

---

## Visual Overview

```mermaid
graph TD
  IDEALE[IDEALE.eu Brand and Standards]

  subgraph Pillars
    I[ASI-T2 Intelligence]
    D[GAIA Defense]
    ENE[Propulsion-and-Grids Energy]
    A[AMPEL360 Aerospace]
    L[INFRANET Logistics]
    ESG[Commitment ESG]
  end

  IDEALE --> I
  IDEALE --> D
  IDEALE --> ENE
  IDEALE --> A
  IDEALE --> L
  IDEALE --> ESG

  %% Aerospace canon
  A --> AT[AMPEL360 Air Transport]
  AT --> BWB[BWB Model]
  BWB --> Q100[Q100 Variant]

  %% GAIA fan-out
  D --> GAIR[GAIA-AIR]
  D --> GSEA[GAIA-SEA]
  D --> GSPACE[GAIA-SPACE]
  GAIR --> HYD[HYDROBOTS Program]

  %% Logistics programs
  L --> AQUA[AQUA_OS_AIRCRAFT]
  L --> LH2[LH2_CORRIDOR]

  %% Intelligence bridge
  I --> QAIM[QAIM-2 Bridge]
````

---

## Sector Profiles

Profiles specialize IEF per regulatory domain. First up:

### TFA — Aerospace Domain Profile

* Aligns **UTCS** fields to aviation semantics (ATA, safety, maintainability)
* Adds aerospace‑specific **policy pins** and **conformance gates**
* Ships **reference badges** and **regulatory report layouts**

---

## ASI‑T2 · Reference Implementation

**ASI‑T2** is the **reference repository** showing how to wire IEF in a real organization (templates, workflows, examples).

* **Bundle:** `UTCS_BUNDLE/` (manifests, attestations)
* **Docs:** `WHITEPAPERS/` (architecture & interfaces)
* **Profiles:** TFA (aerospace)
* **Evidence:** `sbom/`, `badges/`, `.github/workflows/` (**Verify**)

> Treat it as a **living reference**: copy what you need; keep your own governance.

---

## Programs by Pillar · IDEALE

* **I · ASI‑T2 — Intelligence**
  Reference implementation, QAIM‑2 hybrid bridge, UTCS/CXP/QS rails.

* **D · GAIA — Defense**
  Family of multi‑domain robotic systems — **GAIA‑AIR**, **GAIA‑SEA**, **GAIA‑SPACE**. Programs include **HYDROBOTS**.

* **E · Propulsion‑and‑Grids — Energy**
  Propulsion systems and energy networks. Aligns to domains **PPP**, **EEE**, **EER**.

* **A · AMPEL360 — Aerospace**
  **Family** → **Model** **BWB** → **Variant** **Q100** (configured model for ~100 pax).
  Evidence wiring: **UTCS → SPDX → Verify → Badge** aligned to **ATA**.

* **L · INFRANET — Logistics**
  Supply, maintenance, delivery chains and runtime packaging. Includes **AQUA_OS_AIRCRAFT**, **LH2_CORRIDOR**.

* **E · Commitment — ESG**
  Ethics, sustainability and trust‑mark. **MAL‑EEM**, data classification, privacy, export control.

---

## Evidence Objects

* **UTCS / CXP** — machine‑readable context (e.g., `UTCS/context.manifest.json`)
* **SPDX SBOM** — generated on build/release (`sbom/`)
* **Verify (CI)** — policy‑pinned workflows under `.github/workflows/`
* **Badge + Replay** — status + links to replayable logs (`badges/`)

<details>
  <summary><strong>UTCS manifest skeleton YAML</strong></summary>

```yaml
id: UTCS-MI:v5.0:<PRODUCT_FAMILY>:<PROCESS>:<MODEL>:<VARIANT>:<ATA>:<artifact-id>
framework: IDEALE.eu
bridge: QS→FWD→UE→FE→CB→QB
source:
  repo_path: <relative/path/to/artifact>
  commit: <git-sha>
  created_at: <iso8601>
context:
  who:
    org: <org-name>
    team: <team-name>
    owner: <contact@domain>
  what:
    product_family: <AMPEL360|GAIA|INFRANET>
    product_model: <e.g., BWB>
    variant: <e.g., Q100|PLUS|NULL>
  where:
    env: <OB|OFF|SIM|LAB|FLIGHT>
    region: <EU|US|...>
  when:
    ts_build: <iso8601>
    ts_verify: <iso8601>
  why:
    objective: <design|safety|compliance|maintenance|...>
    ticket_ref: <issue-id or URL>
inputs:
  - path: <path/to/input>
    digest: <sha256>
outputs:
  - type: <mesh|report|package|run|sbom>
    path: <path/to/output>
    digest: <sha256>
evidence:
  ata_dm_refs:
    - <DMC-...-EN-US>
  sbom:
    format: SPDX-2.3
    path: sbom/AMPEL360/BWB/Q100/OB/2025-10-01/AMPEL360-BWB-Q100-OB-rc1.spdx.json
  verify_log: .evidence/logs/<run-id>.jsonl
provenance:
  signatures:
    qs_anchor: <sha256>
    sigstore_bundle: <path/to/intoto.jsonl>
ethics_guard: MAL-EEM
classification: INTERNAL–EVIDENCE-REQUIRED
```

</details>

---

## Conformance Ladder

| Level | Name           | Requirements (summary)                                                    |
| ----: | -------------- | ------------------------------------------------------------------------- |
|     1 | **Baseline**   | Valid **UTCS** + one **SPDX** per release + visible **Badge**             |
|     2 | **Replayable** | Policy‑pinned **Verify** + hash‑chained logs + retention policy           |
|     3 | **Assured**    | Third‑party attestation + sector **profile** (e.g., **TFA**) + revocation |
|     4 | **Certified**  | **IDEALE Trust Mark** aligned to EU frameworks                            |

> Progress is **evidence‑driven**; each level adds traceability without lock‑in.

---

## Roadmap Phases

1. **Standards** — freeze **MVS v0.1** (UTCS/CXP schema, SPDX baseline, Verify action, Badge endpoint)
2. **Services** — Verification‑as‑a‑Service (SaaS), data residency, signed attestations
3. **Trust Mark** — Levels, controls, assessor marketplace, revocation
4. **Policy Alignment** — Map primitives to EU requirements; public‑sector pilots

---

## Contact & Pilots

Interested in a 2‑week pilot (Aerospace · Energy · Defense · Logistics)?

* Email: **[pilots@ideale.eu](mailto:pilots@ideale.eu)**
* Issues: **[Open a Pilot request](https://github.com/Robbbo-T/IDEALE-IEF/issues/new?title=Pilot%3A%20Org)**

---

## Link Map (for clustered keywords)

* **IDEALE.eu** → [https://ideale.eu](https://ideale.eu)
* **What is IDEALE?** → #what-is-ideale
* **Naming Canon** → #naming-canon
* **IEF · IDEALE Evidence Framework** → #ideale-evidence-framework-ief
* **Visual Overview** → #visual-overview
* **Sector Profiles** → #sector-profiles
* **TFA · Aerospace Domain Profile** → #tfa-aerospace-domain-profile
* **ASI‑T2 · Reference Implementation** → #asit2-reference-implementation
* **Programs by Pillar** → #programs-by-pillar-ideale

  * **AMPEL360** → #programs-by-pillar-ideale
  * **GAIA** → #programs-by-pillar-ideale
  * **QAIM‑2** → #programs-by-pillar-ideale
  * **HYDROBOTS** → #programs-by-pillar-ideale
* **Evidence Objects** → #evidence-objects

  * **UTCS · manifest skeleton** → #utcs-manifest-skeleton-yaml
  * **CXP** → #evidence-objects
  * **SBOM** → #evidence-objects
  * **Verify · Badge** → #evidence-objects
* **Conformance Ladder** → #conformance-ladder
* **Roadmap** → #roadmap-phases
* **Contact & Pilots** → #contact-pilots
* **SPDX** → [https://spdx.dev](https://spdx.dev)

```
```







