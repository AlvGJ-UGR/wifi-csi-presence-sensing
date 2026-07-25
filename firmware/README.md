# Firmware — CSI Acquisition (Phase 1)

## Status

No custom firmware exists yet.

At this stage, the project uses **Espressif's official `esp-csi` framework** as the acquisition layer. The firmware is intentionally **not included** in this repository to avoid duplicating third-party code and to simplify future updates as the upstream project evolves.

The development of a custom firmware is planned for later stages, once the acquisition pipeline and signal characteristics have been fully validated.

---

## Objective

The goal of **Phase 1** is to establish a reliable and reproducible CSI acquisition pipeline.

The firmware is responsible only for:

- Configuring the ESP32 for CSI capture.
- Acquiring raw Channel State Information.
- Streaming CSI frames to the host computer over UART.

No signal processing or detection logic is performed at this stage.

---

## Experimental Configurations

Two acquisition modes are planned.

### Mode A — Existing WiFi Infrastructure

A single ESP32 connects to an existing WiFi access point and captures CSI from regular network traffic.

This configuration requires no dedicated infrastructure but may suffer from irregular packet timing depending on the behaviour of the router.

---

### Mode B — Dedicated ESP32 Pair (Primary Platform)

Two ESP32 boards form an isolated experimental network:

- ESP32 #1 operates as a dedicated SoftAP.
- ESP32 #2 connects as a Station and captures CSI.

This configuration provides full control over channel selection, packet generation and experimental conditions, making it the preferred platform for the remainder of the project.

---

## Prerequisites

Before starting, ensure the following components are available:

- ESP-IDF (v5.x recommended)
- Git
- Two ESP32-WROOM-32D development boards
- USB cables
- Python environment (used by the acquisition tools)

The ESP-IDF version should always be checked against the compatibility notes in the official `esp-csi` repository, since CSI-related APIs have changed across SDK versions.

---

## Setup

### 1. Clone Espressif's reference implementation

```bash
git clone https://github.com/espressif/esp-csi.git
```

The repository is used as the firmware base and is intentionally kept outside this project.

---

### 2. Configure the project

Open one of the CSI examples provided by Espressif.

Typical configuration includes:

- Enable CSI collection.
- Configure WiFi mode.
- Configure UART output.
- Build using ESP-IDF.

Refer to the example documentation for any version-specific configuration steps.

---

### 3. Flash the firmware

Compile and flash the selected example onto the ESP32.

Verify that the firmware boots correctly and begins outputting CSI frames through the serial interface.

---

### 4. Verify CSI acquisition

Use:

```bash
idf.py monitor
```

to confirm that CSI frames are continuously printed over UART without unexpected interruptions or formatting errors.

---

### 5. Capture a session

Once the firmware is operating correctly, record the serial output using the project's acquisition tools.

Example:

```bash
python tools/capture_session.py
```

Each capture should generate:

- Raw CSI data.
- Session metadata.
- Folder structure under `data/raw/`.

---

### 6. Validate the session

Immediately after acquisition, validate the captured data:

```bash
python tools/validate_session.py data/raw/<session_name>/
```

This ensures that corrupted or incomplete sessions are detected before they enter the analysis pipeline.

---

## Acquisition Workflow

```text
Install ESP-IDF
        │
        ▼
Clone esp-csi
        │
        ▼
Configure firmware
        │
        ▼
Flash ESP32
        │
        ▼
Verify UART output
        │
        ▼
Capture raw session
        │
        ▼
Validate session
        │
        ▼
Store under data/raw/
```

---

## Phase 1 Completion Criteria

Phase 1 is considered complete when all of the following conditions are satisfied:

- Raw CSI is successfully exported over UART.
- Stable acquisition has been demonstrated in Mode B.
- At least one complete capture session exists for each supported mode.
- Packet rate remains stable throughout the recording.
- Session folders follow the project's directory conventions.
- Experimental metadata is recorded for every session.
- Captured data successfully passes the validation tool.

---

## Out of Scope

The following tasks do **not** belong to this phase:

- Signal processing.
- Feature extraction.
- Human presence detection.
- Machine Learning.
- Performance optimisation.
- Firmware customisation beyond what is required for reliable acquisition.

These topics will be addressed in later phases of the project.

---

## Known Open Questions

Several aspects of the acquisition system remain under investigation:

- Is Mode A sufficiently stable for long-term experiments?
- What packet rate is required for reliable presence detection?
- How reproducible are captures across different environments?
- How does channel selection affect CSI stability?
- Which firmware modifications will provide the greatest benefit once custom development begins?

These questions will be answered experimentally as the project progresses.

---

## Future Work

Once the acquisition pipeline has been validated, the firmware will gradually evolve beyond the official `esp-csi` examples.

Planned improvements include:

- Custom UART packet formats.
- Improved timestamp handling.
- Additional metadata fields.
- Configurable acquisition parameters.
- Reduced serial bandwidth through binary encoding.
- Firmware tailored specifically to the requirements of this project.

At that stage, this directory will transition from setup documentation to hosting the project's own firmware implementation.

---
