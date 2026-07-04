# Firmware — CSI Acquisition (Phase 1)

## Status

No custom firmware exists yet. This directory currently holds only setup
instructions. Per ADR-001 (`.ai/DECISIONS.md`), the project uses Espressif's
official `esp-csi` framework as the acquisition layer rather than a
from-scratch implementation.

## Objective of this phase

Get raw CSI out of the ESP32 and onto disk, in both candidate configurations
(Modo A — existing router, Modo B — two dedicated ESP32s), with zero signal
processing. Phase 1 is acquisition-only (see ADR-002, ADR-003).

## Prerequisites

- ESP-IDF installed (v5.x recommended — check compatibility against the
  `esp-csi` repo's README at the time of cloning, since CSI struct fields
  have changed across IDF versions historically).
- 2× ESP32-WROOM connected via USB.
- `idf.py` on PATH, or use the ESP-IDF VS Code extension.

## Steps

1. **Clone the reference framework** (kept out of this repo — used only as a
   reference / starting point, not vendored):
   ```bash
   git clone https://github.com/espressif/esp-csi.git
   ```
2. **Identify the right example.** Inside `esp-csi/examples/`, the relevant
   starting points are the active CSI examples (one device pings, the other
   sniffs). Read their `README.md` before touching config — CSI capture
   requires specific `sdkconfig` options (promiscuous mode, CSI enabled in
   `esp_wifi_set_csi_config`).
3. **Modo B first (two dedicated ESP32s)** — per ADR-002 this is the primary
   experimental platform:
   - Flash one ESP32 as a dedicated soft-AP.
   - Flash the second as a station that connects to it and either pings it
     or simply receives beacon/data frames, with CSI capture enabled on the
     receiving side.
   - Confirm CSI structs are being printed over serial (`idf.py monitor`).
4. **Modo A (existing router)** — optional secondary path, documented after
   Modo B is validated:
   - Flash a single ESP32 in station mode, associated to the real household
     router.
   - Generate periodic traffic (ICMP ping to the router, or a lightweight
     UDP echo) so CSI is refreshed at a known rate.
5. **Capture to raw sessions.** Do not process anything at this stage.
   Use `tools/capture_session.py` (see `tools/README.md`) to stream the
   serial CSI output straight into a correctly named session folder under
   `data/raw/`, with `metadata.json` generated automatically from the
   flags you pass in. This replaces manually redirecting `idf.py monitor`
   output and hand-writing metadata — same result, less room for a
   mislabelled or malformed session. Run `tools/validate_session.py` on
   each resulting folder immediately afterwards to catch structural
   problems (missing consent field, empty CSV, malformed JSON) before
   moving to the next capture.

## What "done" looks like for Phase 1

- At least one raw capture session per mode (A and B), each a few minutes
  long, with no visible packet corruption in the serial log.
- Packet rate is roughly consistent across a session (no long silent gaps).
- Files exist under `data/raw/` following the session naming convention.
- Hardware configuration used (board revision, antenna placement, distance,
  channel) is written down in the session metadata — without this, nothing
  downstream (Phase 2 characterisation) can be trusted.

## Explicitly out of scope for this directory right now

- Any signal processing (belongs in `analysis/`).
- Any detection logic.
- Any custom modification of `esp-csi` beyond what's needed to get clean
  serial output — don't optimise prematurely.

## Known open question

Whether Modo A (existing router) is even viable depends on the router's
firmware/driver exposing enough beacon/data frame regularity for stable CSI
timing. This has not been tested yet — treat any assumption about it as
unverified until Modo A capture actually happens.
