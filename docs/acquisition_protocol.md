# Acquisition Protocol — Raw CSI Sessions

This document defines the concrete, reproducible format for every raw
capture session stored under `data/raw/`. It exists so that Phase 2
(signal characterisation) and Phase 3 (dataset generation) can trust what's
in `data/raw/` without guessing.

## Session naming convention

```
data/raw/<YYYYMMDD>_<HHMMSS>_<mode>_<label>_<distance_m>m/
```

- `mode` — `modoA` (existing router) or `modoB` (two dedicated ESP32s).
- `label` — one of `ausente`, `presente_estatico`, `presente_movimiento`
  (extend only if a genuinely new class is introduced — keep it consistent
  with the classes defined in the README methodology section).
- `distance_m` — straight-line distance between the two ESP32s (or ESP32 and
  router), in metres, rounded to the nearest 0.5 m.

Example: `data/raw/20260702_183000_modoB_presente_estatico_2m/`

## Required contents of each session folder

```
<session_dir>/
├── csi_raw.csv          raw CSI records, one per line, serial capture
├── metadata.json         structured session metadata (see below)
└── notes.md              free-text observations (optional but encouraged)
```

## `metadata.json` required fields

```json
{
  "session_id": "20260702_183000_modoB_presente_estatico_2m",
  "mode": "modoB",
  "label": "presente_estatico",
  "distance_m": 2.0,
  "start_time_utc": "2026-07-02T18:30:00Z",
  "end_time_utc": "2026-07-02T18:35:00Z",
  "environment": "free-text description (room, obstacles, wall type)",
  "wall_type": "none | tabique | carga",
  "esp32_ap_placement": "free-text (height, orientation)",
  "esp32_sta_placement": "free-text (height, orientation)",
  "wifi_channel": 6,
  "num_people": 0,
  "notes_ref": "notes.md"
}
```

Every field is mandatory except `notes_ref`. If a field is genuinely
unknown, write `"unknown"` explicitly — do not omit the key. Silent omission
is what makes datasets impossible to audit later.

## Raw CSV format (`csi_raw.csv`)

One row per received CSI frame, in the order the firmware emits it. Exact
column set depends on the `esp-csi` struct fields available at flash time,
but at minimum:

```
timestamp_us,rssi,channel,csi_data
```

Where `csi_data` is the raw amplitude/phase array as emitted by the
firmware (do not pre-process, round, or filter — this file is immutable
once written, per ADR-005).

## Labelling discipline

- Start/stop the capture script only after the room is already in the
  target state (e.g. don't start "ausente" capture while someone is still
  walking out).
- Log start/end timestamps from the capture machine's clock, not estimated
  after the fact.
- One label per session. Do not mix states within a single raw file — if
  the state changes mid-capture, split it into two sessions.

## Immutability

Per ADR-005, files under `data/raw/` are never edited or overwritten after
capture. Any correction (e.g. a mislabelled session) is handled by adding a
`corrected_metadata.json` alongside the original, never by rewriting
`metadata.json` in place.
