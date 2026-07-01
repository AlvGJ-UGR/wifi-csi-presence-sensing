# PROJECT_STATE.md

# WiFi CSI Presence Sensing
## Current Project State

---

Last Updated

YYYY-MM-DD

---

# Current Phase

Phase 0 — Repository Preparation

Status:

🟢 Completed

Next Phase:

Phase 1 — CSI Acquisition

---

# Current Objective

Validate reliable CSI acquisition using Espressif's official esp-csi firmware on ESP32 hardware.

The objective of the next work sessions is NOT to process the data.

Only to demonstrate stable acquisition and create the first reproducible raw dataset.

---

# Current Status

Repository structure completed.

README completed.

Project architecture defined.

Research methodology defined.

Hardware available.

No firmware modifications have been made yet.

No datasets have been collected.

No Python analysis scripts exist yet.

No experiments have been executed.

---

# Next Task

Flash Espressif's official esp-csi firmware.

Verify:

- Successful firmware flashing.
- Stable CSI packet acquisition.
- Continuous serial output.
- Packet integrity.
- Capture at least one raw recording session.

Store the resulting dataset under:

data/raw/

Document the hardware configuration used.

---

# Immediate Priorities

Priority 1

Reliable CSI acquisition.

Priority 2

Raw dataset generation.

Priority 3

Initial signal visualisation.

Nothing else should be implemented before these tasks are complete.

---

# Known Decisions

Current architecture uses:

• Espressif esp-csi as acquisition framework.

• Two ESP32 devices as the primary experimental configuration.

• Python for all offline signal processing.

Refer to DECISIONS.md before modifying any architectural choice.

---

# Known Risks

Possible router incompatibilities.

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

□ Raw CSI acquisition

□ Dataset format

□ Initial signal plots

□ Acquisition documentation

---

# Blockers

None.

---

# Session Resume

When continuing work:

1. Complete the current phase before starting the next.

2. Do not begin feature extraction until raw acquisition is fully validated.

3. Do not implement Machine Learning before a classical baseline exists.

4. Update PROJECT_STATE.md after every completed work session.

5. Record important architectural decisions in DECISIONS.md.

6. Record completed work in CHANGELOG.md.
