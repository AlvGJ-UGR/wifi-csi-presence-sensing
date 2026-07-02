# PROJECT_STATE.md

# WiFi CSI Presence Sensing
## Current Project State

---

Last Updated

2026-07-02

---

# Current Phase

Phase 1 — CSI Acquisition

Status:

🟡 In progress — infrastructure and documentation ready, hardware capture not yet performed.

Next Phase:

Phase 2 — Signal Characterisation (blocked until raw sessions exist).

---

# Current Objective

Validate reliable CSI acquisition using Espressif's official esp-csi firmware on ESP32 hardware.

The objective of the next work session is NOT to process the data.

Only to demonstrate stable acquisition and create the first reproducible raw dataset.

---

# Current Status

Repository structure completed.

README completed — merge conflicts from prior branches resolved (README.md and LICENSE had unresolved Git conflict markers; both now clean).

Project architecture defined.

Research methodology defined.

Hardware available.

Firmware flashing guide written (`firmware/README.md`) — describes cloning `esp-csi`, the Modo A / Modo B setup steps, and Phase 1 exit criteria. No custom firmware code exists yet; none is expected until `esp-csi` proves insufficient.

Raw session format and acquisition protocol formally defined (`docs/acquisition_protocol.md`) — session naming convention, required `metadata.json` fields, raw CSV format, labelling discipline, immutability rule.

No firmware modifications have been made yet.

No datasets have been collected yet — this requires physical hardware in hand, which is outside what an AI session can perform. The documentation is now ready for that session.

No Python analysis scripts exist yet — intentionally deferred (see ADR-003, ADR-005; nothing to analyse before raw data exists).

No experiments have been executed.

---

# Next Task

Physical, hands-on task (requires the user at the bench with the ESP32 boards):

1. Clone `espressif/esp-csi`, flash Modo B (two dedicated ESP32s: AP + STA/sniffer) following `firmware/README.md`.
2. Confirm CSI frames appear over serial with `idf.py monitor`, no corruption, roughly stable packet rate.
3. Capture at least one raw session per label class (`ausente`, `presente_estatico`, `presente_movimiento`) at Modo B, following the format in `docs/acquisition_protocol.md`.
4. Store the resulting files under `data/raw/<session_id>/` (csi_raw.csv + metadata.json).
5. Optionally repeat for Modo A (existing router) once Modo B is confirmed stable.

---

# Immediate Priorities

Priority 1

Reliable CSI acquisition (hardware-dependent, next physical session).

Priority 2

Raw dataset generation.

Priority 3

Initial signal visualisation (first `analysis/` script — just load + plot, no detection logic yet).

Nothing else should be implemented before these tasks are complete.

---

# Known Decisions

Current architecture uses:

• Espressif esp-csi as acquisition framework.

• Two ESP32 devices (Modo B) as the primary experimental configuration; Modo A (existing router) as secondary/optional.

• Python for all offline signal processing.

Refer to DECISIONS.md before modifying any architectural choice.

---

# Known Risks

Possible router incompatibilities (Modo A specifically — untested, flagged as an open question in `firmware/README.md`).

ESP32 firmware limitations.

Packet loss.

Unstable packet timing.

Dataset quality depends heavily on experimental methodology.

These risks should be evaluated experimentally, not assumed.

---

# Available Hardware

2 × ESP32-WROOM

1 × WiFi Router (2.4 GHz)

USB cables

Development PC

No additional hardware required.

---

# Pending Deliverables

☑ Firmware flashing guide (documentation only — code pending physical session)

☑ Raw dataset format specification

□ Raw CSI acquisition (actual capture — requires hardware session)

□ Initial signal plots

---

# Blockers

Raw CSI acquisition itself requires physical access to the ESP32 hardware and cannot be completed in a documentation-only session. Everything needed to perform that session (guide + format spec) is now in place.

---

# Session Resume

When continuing work:

1. Complete the current phase before starting the next.

2. Do not begin feature extraction until raw acquisition is fully validated.

3. Do not implement Machine Learning before a classical baseline exists.

4. Update PROJECT_STATE.md after every completed work session.

5. Record important architectural decisions in DECISIONS.md.

6. Record completed work in CHANGELOG.md.
