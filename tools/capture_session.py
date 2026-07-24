#!/usr/bin/env python3
"""
capture_session.py — Host-side capture helper for raw CSI acquisition sessions.

This script does NOT process or analyse CSI. It only:
  1. Opens a serial connection to the ESP32 that is streaming CSI frames.
  2. Tags each incoming line with a host-side reception timestamp (microsecond precision).
  3. Writes the raw lines, untouched, to csi_raw.csv inside a correctly
     named session folder under data/raw/, per docs/acquisition_protocol.md.
  4. Writes metadata.json with the session parameters provided on the command line.

Press Ctrl+C or supply --duration N to stop the capture.
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
    p.add_argument("--baud", type=int, default=921600, help="Serial baud rate (default: 921600)")
    p.add_argument("--mode", required=True, choices=sorted(VALID_MODES))
    p.add_argument("--label", required=True, choices=sorted(VALID_LABELS))
    p.add_argument("--distance", required=True, type=float, help="Distance in metres between the two ESP32s")
    p.add_argument("--duration", type=float, default=None, help="Optional capture duration in seconds. Stops automatically when reached.")
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


def validate_ethics_and_args(args):
    """Verifica reglas de negocio y consentimiento (ADR-010) antes de tocar I/O."""
    if args.num_people and args.num_people > 0 and not args.participant_consent:
        print(
            "ERROR: --num-people > 0 but --participant-consent was not passed.\n"
            "Per ADR-010, no session involving people may be captured without an\n"
            "explicit, per-session confirmation that informed consent was obtained.",
            file=sys.stderr,
        )
        sys.exit(1)
    if args.duration is not None and args.duration <= 0:
        print("ERROR: --duration must be a positive number of seconds.", file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_args()
    validate_ethics_and_args(args)

    now = datetime.now(timezone.utc)
    session_id = build_session_id(now, args.mode, args.label, args.distance)
    session_dir = RAW_DIR / session_id

    if session_dir.exists():
        print(f"ERROR: session directory already exists: {session_dir}", file=sys.stderr)
        sys.exit(1)

    session_dir.mkdir(parents=True, exist_ok=False)
    csv_path = session_dir / "csi_raw.csv"
    meta_path = session_dir / "metadata.json"
    notes_path = session_dir / "notes.md"

    print(f"Session: {session_id}")
    print(f"Writing raw frames to: {csv_path}")
    print(f"Opening {args.port} @ {args.baud} baud...")

    try:
        ser = serial.Serial(args.port, args.baud, timeout=0.5)
        
        # Expandir buffer RX del driver del SO a 64 KB
        try:
            ser.set_buffer_size(rx_size=65536)
        except (AttributeError, serial.SerialException):
            pass

        ser.reset_input_buffer()

    except serial.SerialException as e:
        print(f"ERROR: could not open serial port: {e}", file=sys.stderr)
        session_dir.rmdir()
        sys.exit(1)

    frame_count = 0
    start_time = datetime.now(timezone.utc)
    start_monotonic = time.monotonic()

    if args.duration:
        print(f"Capturing for {args.duration} seconds (or press Ctrl+C to stop)...")
    else:
        print("Capturing... press Ctrl+C to stop.")

    try:
        with open(csv_path, "w", encoding="utf-8", newline="", buffering=65536) as f:
            f.write("# host_recv_time_us,raw_serial_line\n")
            f.write("# raw_serial_line is written EXACTLY as emitted by the firmware -- not parsed.\n")
            f.write("# See docs/acquisition_protocol.md for the intended csi_raw.csv schema.\n")
            
            while True:
                # Comprobar límite de duración si está configurado
                if args.duration and (time.monotonic() - start_monotonic) >= args.duration:
                    print(f"\nTarget duration of {args.duration}s reached.")
                    break

                try:
                    line = ser.readline()
                except serial.SerialException as e:
                    print(f"\nWARNING: Serial communication interrupted: {e}", file=sys.stderr)
                    break

                if not line:
                    continue

                host_recv_time_us = time.time_ns() // 1000
                decoded = line.decode("utf-8", errors="replace").rstrip("\r\n")
                f.write(f"{host_recv_time_us},{decoded}\n")
                
                frame_count += 1
                if frame_count % 100 == 0:
                    f.flush()
                    elapsed = time.monotonic() - start_monotonic
                    if args.duration:
                        print(f"  {frame_count} lines captured ({elapsed:.1f}s / {args.duration:g}s)...", end="\r", flush=True)
                    else:
                        print(f"  {frame_count} lines captured ({elapsed:.1f}s)...", end="\r", flush=True)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        ser.close()

    end_time = datetime.now(timezone.utc)

    # Generación de Metadatos
    metadata = {
        "session_id": session_id,
        "mode": args.mode,
        "label": args.label,
        "distance_m": args.distance,
        "target_duration_s": args.duration if args.duration is not None else "unlimited",
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


if __name__ == "__main__":
    main()
