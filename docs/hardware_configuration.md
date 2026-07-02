# Hardware Configuration — Phase 1 Acquisition

This document records the *specific* hardware configuration used for
acquisition, as required by MASTER_PLAN Phase 1 ("Document hardware
configuration"). It is separate from `firmware/README.md` (generic flashing
steps) and `docs/acquisition_protocol.md` (per-session metadata format).

Fields below are templates — fill them in during the physical session, do
not guess or pre-fill with assumed values. An unfilled `TBD` is honest;
a guessed number is not (per ADR-008, scientific honesty over positive
results).

## Boards

| Role | Board | Revision | MAC address | Antenna | Firmware version |
|---|---|---|---|---|---|
| AP (Modo B) | ESP32-WROOM | TBD | TBD | TBD (PCB / external) | TBD (esp-csi commit hash) |
| STA / sniffer (Modo B) | ESP32-WROOM | TBD | TBD | TBD | TBD |

## Router (Modo A, if/when used)

| Field | Value |
|---|---|
| Make/model | TBD |
| Firmware/driver | TBD |
| WiFi standard in use | TBD (802.11n / ac) |
| Channel width | TBD (20/40 MHz) |

## Fixed capture parameters

| Parameter | Value | Rationale |
|---|---|---|
| WiFi channel | TBD — pick one with least local interference, check with a WiFi scanner first | Avoid co-channel interference confounding CSI variance with real environmental interference |
| Packet/ping rate (Modo B) | TBD | Needs to be fast enough to resolve human movement (≥10 Hz recommended per literature reviewed in README) but not so fast it saturates serial output |
| CSI type captured | TBD (LLTF only vs LLTF+HT-LTF, depends on esp-csi config) | Document once decided — affects downstream feature dimensionality |

## Physical environment (fill in per room used, or link to session `metadata.json` if it varies per session)

- Room description:
- Typical furniture/clutter:
- Known WiFi interference sources nearby (other APs, microwave, Bluetooth devices):

---

# Pre-flight checklist (physical session)

Run through this before starting any labelled capture, to avoid discovering
a problem only after "presente_movimiento" data is already collected:

- [ ] ESP-IDF environment active (`. $HOME/esp/esp-idf/export.sh` or equivalent)
- [ ] Both boards flash without errors (`idf.py build flash`)
- [ ] `idf.py monitor` on both boards shows expected boot logs, no crash loop
- [ ] AP board confirmed broadcasting (visible in a WiFi scan)
- [ ] STA board confirmed associated to AP (Modo B) or to the router (Modo A)
- [ ] CSI frames visible on serial output of the receiving board, at a
      roughly stable rate — watch for 30s, note if the rate drifts or stalls
- [ ] Test capture (60s, empty room) saved and manually inspected for
      obvious corruption (garbled lines, wildly inconsistent frame count)
      before starting the real labelled sessions
- [ ] Fields above in this document filled in with the actual boards/channel
      used, not left as TBD
- [ ] `docs/acquisition_protocol.md` open for reference while naming session
      folders and filling `metadata.json`

## Known open question carried over from firmware/README.md

Whether Modo A (existing router) is viable at all is untested — the
pre-flight checklist above should be run for Modo A independently before
trusting any Modo A capture, since router-side beacon/frame regularity is
unverified.
