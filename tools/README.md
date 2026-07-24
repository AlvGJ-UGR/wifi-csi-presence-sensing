# tools/

Host-side scripts that support acquisition. Nothing here does signal
processing or analysis — that boundary is intentional (see ADR-003:
signal understanding before ML, and the standing project rule that
`analysis/` does not start until raw data exists).

## `capture_session.py`

Automates the mechanical part of recording a raw session so it always
matches the format defined in `docs/acquisition_protocol.md`:

- creates the correctly named folder under `data/raw/`
- streams serial output from the CSI-receiving ESP32 straight to
  `csi_raw.csv`, tagging each line with a host-side reception timestamp
  (`host_recv_time_us`) without touching the payload itself
- writes `metadata.json` from the command-line arguments you pass in
  (anything not provided is recorded as `"unknown"` explicitly, never
  silently omitted — see the honesty rule in `docs/acquisition_protocol.md`)
- writes a stub `notes.md`

### Install

```bash
pip install pyserial
```

### Run

```bash
python tools/capture_session.py \
    --mode modoB \
    --label presente_estatico \
    --distance 2.0 \
    --port /dev/ttyUSB0 \
    --channel 6 \
    --environment "salon, sin obstaculos" \
    --wall-type none \
    --num-people 1 \
    --participant-consent \
    --participant-id P01
```

Stop with `Ctrl+C`. The script finalises `metadata.json` with real
start/end timestamps and the total line count on exit.

### Consent enforcement (ADR-010)

Any session with `--num-people` greater than 0 requires `--participant-consent`,
or the script exits with an error and no session is created. This is a
deliberate hard stop, not a formality — see `.ai/DECISIONS.md` ADR-010 and
`README.md` → "Ética y consentimiento". Use `--participant-id` (repeatable)
to record anonymised participant codes (e.g. `P01`); never pass real names.
Only pass `--participant-consent` once consent has actually been obtained
for that specific session — not preemptively "just in case."

### Other optional flags

Not shown in the example above, but available:

- `--baud` — serial baud rate (default `115200`)
- `--ap-placement` / `--sta-placement` — free-text placement notes for each
  board (height, orientation), stored in `metadata.json`
- `--notes` — a short free-text note, written into the session's `notes.md`

Run `python tools/capture_session.py --help` for the authoritative, current
list — this README is kept in sync manually and could lag behind the
script if a flag is added without updating both.

### Important caveat — raw format is provisional

`docs/acquisition_protocol.md` specifies the intended `csi_raw.csv` schema
as `timestamp_us,rssi,channel,csi_data`, coming directly from the firmware.
Until the exact `esp-csi` example/build in use is confirmed (see
`firmware/README.md`, "Known open question"), this script does not assume
that schema — it writes whatever the firmware prints on each line,
unmodified, prefixed only with `host_recv_time_us`. If the firmware's own
line already follows `timestamp_us,rssi,channel,csi_data`, the resulting
file effectively becomes `host_recv_time_us,timestamp_us,rssi,channel,csi_data`,
which satisfies the protocol. Confirm this once real firmware output is
available, and update `docs/acquisition_protocol.md` if it needs
adjusting — don't silently assume it matches.

### Why not parse/validate the CSI payload here?

Because that would be a (very small) form of processing, and the project
principle (ADR-005, immutable raw data) is that nothing between the
firmware and `data/raw/` interprets the signal. Validation and
visualisation belong in `analysis/`, once it exists.

## `validate_session.py`

Structural validator: checks a `data/raw/<session_id>/` folder against the
schema in `docs/acquisition_protocol.md` and the ADR-010 consent
requirements — file presence, `metadata.json` field validity,
consent-field consistency, and (since 2026-07, confirmed against real
capture) per-line shape of `csi_raw.csv`'s `CSI_DATA` rows: field count
and a syntactically clean trailing array. It does **not** interpret the
CSI signal *values* themselves (amplitude/phase content) — only whether
each line has the shape a real `CSI_DATA` line should have. A session with
more than 15% shape-corrupted lines fails; below that it's a warning (real
captures at 921600 baud have shown occasional corruption from UART
overrun — see `docs/acquisition_protocol.md`, "Known issue"). Corrupted
lines are reported and should be dropped by the analysis loader, never
guessed at or repaired.

### Run against a real session

```bash
python tools/validate_session.py data/raw/20260702_183000_modoB_ausente_2m/
```

Or validate every session at once:

```bash
python tools/validate_session.py data/raw/*/
```

Exits `0` if every session passes, `1` if any fails. Recommended as a
matter of course right after each capture — catching a malformed
`metadata.json` immediately is much cheaper than discovering it during
Phase 2 characterisation.

### Tests

`tools/tests/` contains synthetic fixtures (clearly marked as such, not
real captures) and a unit test suite that runs the validator against them
to confirm both the pass and fail paths work:

```bash
python -m unittest tools.tests.test_validate_session -v
```

Run this after modifying `validate_session.py`, before trusting it against
real data.
