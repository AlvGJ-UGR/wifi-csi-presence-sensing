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
  "participant_consent_obtained": "true | false | n/a (n/a only valid when num_people is 0)",
  "participant_ids": ["P01"],
  "notes_ref": "notes.md"
}
```

Every field is mandatory except `notes_ref`. If a field is genuinely
unknown, write `"unknown"` explicitly — do not omit the key. Silent omission
is what makes datasets impossible to audit later.

### Consent fields (ADR-010)

- `participant_consent_obtained` is mandatory whenever `num_people > 0`. A
  session with people and no recorded consent is not a valid session — do
  not backfill this field after the fact from memory; obtain and record
  consent before capturing.
- `participant_ids` holds anonymised codes only (e.g. `P01`, `P02`) — never
  real names. Keep the mapping from code to real identity, if you need one
  at all, outside this repository entirely (e.g. a private, access-controlled
  note), never in `data/`.
- These fields exist to make the ethical scope in `README.md` → "Ética y
  consentimiento" operationally enforced, not just stated.

## Tooling

`tools/capture_session.py` automates producing a session folder in this
exact format directly from a live serial capture — see `tools/README.md`
for usage and an important caveat about the raw CSV schema below (the
column layout depends on the exact firmware build in use, which is not
yet finalised).

`tools/validate_session.py` checks a captured session folder against this
schema and the ADR-010 consent requirements. Run it right after each
capture, before trusting the session — see `tools/README.md`.

## Raw CSV format (`csi_raw.csv`)

Each captured line, as written by `tools/capture_session.py`, is:

```
host_recv_time_us,raw_serial_line
```

`raw_serial_line` is the firmware's own output verbatim (not parsed at
capture time, per ADR-005). Confirmed against real capture (2026-07,
`csi_recv_router` example, ESP-IDF v5.2), the firmware's own line format
is the standard `esp-csi` CSV, 25 comma-separated fields followed by a
quoted JSON-style array:

```
type,seq,mac,rssi,rate,sig_mode,mcs,bandwidth,smoothing,not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,ampdu_cnt,channel,secondary_channel,local_timestamp,ant,sig_len,rx_state,len,first_word,data
```

Example (real capture, trimmed for length):

```
1784806142593379,CSI_DATA,507430,84:aa:9c:26:48:57,-60,11,1,7,0,1,1,0,1,0,0,-95,08,0,100,1,128,1,"[100,-64,5,0,...]"
```

So a full row is `host_recv_time_us,` followed by these 25 fields (24
scalar header fields + the trailing `data` array).

### Known issue: occasional line corruption at 921600 baud

Real captures at 921600 baud (the console baud rate the `csi_recv_router`
example actually uses — confirmed by reading `idf.py monitor`'s own
startup line, do not assume 115200) show occasional corrupted lines:
missing commas producing concatenated numbers (e.g. `-7-8` instead of two
separate values), missing values producing empty fields (double commas),
and occasional wildly out-of-range spikes (e.g. `146` or `-123` where
neighbouring values are within ±30). This is consistent with UART buffer
pressure at a high CSI packet rate (~130-160 pkt/s observed) without
hardware flow control, not a parsing artefact on the host side.

Do not silently "fix" these lines by guessing the intended value. Treat
any line that doesn't match the expected field count/array shape as
corrupted and exclude it from analysis, counted and reported (see
`tools/validate_session.py`), not repaired.

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
