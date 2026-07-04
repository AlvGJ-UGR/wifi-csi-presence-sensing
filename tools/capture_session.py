#!/usr/bin/env python3
"""
capture_session.py — Host-side capture helper for raw CSI acquisition sessions.

This script does NOT process or analyse CSI. It only:
  1. Opens a serial connection to the ESP32 that is streaming CSI frames
     (per firmware/README.md).
  2. Tags each incoming line with a host-side reception timestamp.
  3. Writes the raw lines, untouched, to csi_raw.csv inside a correctly
     named session folder under data/raw/, per docs/acquisition_protocol.md.
  4. Writes metadata.json with the session parameters you provide on the
     command line.

It does not parse, filter, decode, or interpret the CSI payload itself —
that exact format depends on the esp-csi build/example used, which is not
yet finalised (see the "Known open question" note in firmware/README.md).
Treat the host_recv_time_us column as a diagnostic cross-check (packet
rate, gaps), not as a substitute for whatever timestamp the firmware
itself emits inside the line.

Usage example:

    python tools/capture_session.py \\
        --mode modoB \\
        --label presente_estatico \\
        --distance 2.0 \\
        --port /dev/ttyUSB0 \\
        --channel 6 \\
        --environment "salon, sin obstaculos" \\
        --wall-type none \\
        --num-people 1 \\
        --participant-consent \\
        --participant-id P01

Sessions with --num-people > 0 REQUIRE --participant-consent (per ADR-010
in .ai/DECISIONS.md) — the script refuses to run otherwise. Only pass this
flag once informed consent has actually been obtained from every
participant for this specific session, not preemptively.

Press Ctrl+C to stop the capture. The script then finalises metadata.json
with the actual start/end timestamps and line count.

Requires: pyserial (`pip install pyserial`)
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import serial
except ImportError:
    print("ERROR: pyserial is not installed. Run: pip install pyserial", file=sys.stderr)
    sys.exit(1)

VALID_MODES = {"modoA", "modoB"}
VALID_LABELS = {"ausente", "presente_estatico", "presente_movimiento"}
VALID_WALL_TYPES = {"none", "tabique", "carga", "unknown"}

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"


def parse_args():
    p = argparse.ArgumentParser(
        description="Capture a raw CSI session to data/raw/, per docs/acquisition_protocol.md."
    )
    p.add_argument("--port", required=True, help="Serial port of the CSI-receiving ESP32, e.g. /dev/ttyUSB0 or COM5")
    p.add_argument("--baud", type=int, default=115200, help="Serial baud rate (default: 115200)")
    p.add_argument("--mode", required=True, choices=sorted(VALID_MODES))
    p.add_argument("--label", required=True, choices=sorted(VALID_LABELS))
    p.add_argument("--distance", required=True, type=float, help="Distance in metres between the two ESP32s (or ESP32 and router)")
    p.add_argument("--channel", type=int, default=None, help="WiFi channel in use (unknown if omitted)")
    p.add_argument("--environment", default=None, help="Free-text room/obstacle description")
    p.add_argument("--wall-type", choices=sorted(VALID_WALL_TYPES), default="unknown")
    p.add_argument("--ap-placement", default=None, help="Free-text AP placement (height, orientation)")
    p.add_argument("--sta-placement", default=None, help="Free-text STA placement (height, orientation)")
    p.add_argument("--num-people", type=int, default=None)
    p.add_argument(
        "--participant-consent",
        action="store_true",
        help="Confirms informed consent was obtained from every participant for THIS session (required if --num-people > 0). See ADR-010.",
    )
    p.add_argument(
        "--participant-id",
        action="append",
        default=None,
        help="Anonymised participant code, e.g. P01. Repeat the flag for multiple participants. Never pass a real name.",
    )
    p.add_argument("--notes", default=None, help="Short free-text note, also written to notes.md")
    return p.parse_args()


def build_session_id(now, mode, label, distance):
    ts = now.strftime("%Y%m%d_%H%M%S")
    distance_str = f"{distance:g}".replace(".", "_")
    return f"{ts}_{mode}_{label}_{distance_str}m"


def main():
    args = parse_args()

    now = datetime.now(timezone.utc)
    session_id = build_session_id(now, args.mode, args.label, args.distance)
    session_dir = RAW_DIR / session_id

    if args.num_people and args.num_people > 0 and not args.participant_consent:
        print(
            "ERROR: --num-people > 0 but --participant-consent was not passed.\n"
            "Per ADR-010, no session involving people may be captured without an\n"
            "explicit, per-session confirmation that informed consent was obtained.\n"
            "Re-run with --participant-consent once consent has actually been obtained\n"
            "(don't pass this flag preemptively before asking).",
            file=sys.stderr,
        )
        sys.exit(1)

    if session_dir.exists():
        print(f"ERROR: session directory already exists: {session_dir}", file=sys.stderr)
        sys.exit(1)

    session_dir.mkdir(parents=True)
    csv_path = session_dir / "csi_raw.csv"
    meta_path = session_dir / "metadata.json"
    notes_path = session_dir / "notes.md"

    print(f"Session: {session_id}")
    print(f"Writing raw frames to: {csv_path}")
    print(f"Opening {args.port} @ {args.baud} baud...")

    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
    except serial.SerialException as e:
        print(f"ERROR: could not open serial port: {e}", file=sys.stderr)
        session_dir.rmdir()
        sys.exit(1)

    frame_count = 0
    start_time = datetime.now(timezone.utc)

    print("Capturing... press Ctrl+C to stop.")

    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            f.write("# host_recv_time_us,raw_serial_line\n")
            f.write("# raw_serial_line is written EXACTLY as emitted by the firmware -- not parsed.\n")
            f.write("# See docs/acquisition_protocol.md for the intended csi_raw.csv schema and\n")
            f.write("# firmware/README.md 'Known open question' for the current format caveat.\n")
            while True:
                line = ser.readline()
                if not line:
                    continue
                host_recv_time_us = int(time.time() * 1_000_000)
                try:
                    decoded = line.decode("utf-8", errors="replace").rstrip("\r\n")
                except Exception:
                    decoded = repr(line)
                f.write(f"{host_recv_time_us},{decoded}\n")
                f.flush()
                frame_count += 1
                if frame_count % 100 == 0:
                    print(f"  {frame_count} lines captured...")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        ser.close()

    end_time = datetime.now(timezone.utc)

    metadata = {
        "session_id": session_id,
        "mode": args.mode,
        "label": args.label,
        "distance_m": args.distance,
        "start_time_utc": start_time.isoformat(),
        "end_time_utc": end_time.isoformat(),
        "environment": args.environment or "unknown",
        "wall_type": args.wall_type,
        "esp32_ap_placement": args.ap_placement or "unknown",
        "esp32_sta_placement": args.sta_placement or "unknown",
        "wifi_channel": args.channel if args.channel is not None else "unknown",
        "num_people": args.num_people if args.num_people is not None else "unknown",
        "participant_consent_obtained": (
            "n/a" if not args.num_people else bool(args.participant_consent)
        ),
        "participant_ids": args.participant_id or [],
        "notes_ref": "notes.md",
        "line_count": frame_count,
        "capture_tool": "tools/capture_session.py",
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(f"# Notes -- {session_id}\n\n")
        if args.notes:
            f.write(args.notes + "\n")
        else:
            f.write("(no notes provided at capture time -- edit this file manually if needed)\n")

    duration_s = (end_time - start_time).total_seconds()
    print(f"\nDone. {frame_count} lines captured over {duration_s:.1f}s.")
    print(f"Session stored at: {session_dir}")
    print("Remember to manually inspect csi_raw.csv for obvious corruption before trusting this session.")


if __name__ == "__main__":
    main()
