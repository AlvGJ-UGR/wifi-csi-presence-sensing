#!/usr/bin/env python3
"""
validate_session.py -- Structural validator for raw CSI session folders.

Checks a session directory under data/raw/ against the schema defined in
docs/acquisition_protocol.md and the consent requirements from ADR-010
(.ai/DECISIONS.md).

This is a FORMAT/STRUCTURE check only -- it does not read, interpret, or
validate the CSI signal content itself. That belongs to analysis/, which
does not exist yet (see ADR-003, ADR-005: no signal processing before raw
acquisition is validated and understood).

Usage:
    python tools/validate_session.py data/raw/<session_id>/
    python tools/validate_session.py data/raw/*/          # validate all sessions

Exit code is 0 if every given session passes, 1 if any fails.
"""

import argparse
import json
import sys
from pathlib import Path

REQUIRED_METADATA_KEYS = {
    "session_id", "mode", "label", "distance_m", "start_time_utc",
    "end_time_utc", "environment", "wall_type", "esp32_ap_placement",
    "esp32_sta_placement", "wifi_channel", "num_people",
    "participant_consent_obtained", "participant_ids", "notes_ref",
}
VALID_MODES = {"modoA", "modoB"}
VALID_LABELS = {"ausente", "presente_estatico", "presente_movimiento"}
VALID_WALL_TYPES = {"none", "tabique", "carga", "unknown"}


class ValidationResult:
    def __init__(self, session_dir):
        self.session_dir = session_dir
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    @property
    def ok(self):
        return not self.errors


def validate_files_present(session_dir, result):
    for fname in ("csi_raw.csv", "metadata.json"):
        if not (session_dir / fname).exists():
            result.error(f"missing required file: {fname}")
    if not (session_dir / "notes.md").exists():
        result.warn("notes.md missing (optional, but recommended)")


def validate_metadata(session_dir, result):
    meta_path = session_dir / "metadata.json"
    if not meta_path.exists():
        return None
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except json.JSONDecodeError as e:
        result.error(f"metadata.json is not valid JSON: {e}")
        return None

    missing = REQUIRED_METADATA_KEYS - set(meta.keys())
    if missing:
        result.error(f"metadata.json missing required keys: {sorted(missing)}")

    mode = meta.get("mode")
    if mode is not None and mode not in VALID_MODES:
        result.error(f"invalid mode: {mode!r} (expected one of {sorted(VALID_MODES)})")

    label = meta.get("label")
    if label is not None and label not in VALID_LABELS:
        result.error(f"invalid label: {label!r} (expected one of {sorted(VALID_LABELS)})")

    wall_type = meta.get("wall_type")
    if wall_type is not None and wall_type not in VALID_WALL_TYPES:
        result.error(f"invalid wall_type: {wall_type!r} (expected one of {sorted(VALID_WALL_TYPES)})")

    distance_m = meta.get("distance_m")
    if distance_m is not None and not isinstance(distance_m, (int, float)):
        result.error(f"distance_m must be numeric, got {type(distance_m).__name__}")

    # ADR-010 consent enforcement
    num_people = meta.get("num_people")
    consent = meta.get("participant_consent_obtained")
    participant_ids = meta.get("participant_ids")

    if isinstance(num_people, int) and num_people > 0:
        if consent is not True:
            result.error(
                f"num_people={num_people} but participant_consent_obtained is "
                f"{consent!r}, expected true (ADR-010: no session with participants "
                f"may be trusted without recorded consent)"
            )
        if not participant_ids:
            result.error(
                f"num_people={num_people} but participant_ids is empty -- "
                f"expected anonymised codes (e.g. ['P01'])"
            )
        else:
            for pid in participant_ids:
                if not isinstance(pid, str) or len(pid) > 10:
                    result.warn(
                        f"participant id {pid!r} looks unusual for an anonymised "
                        f"code -- double-check it isn't a real name"
                    )
    elif num_people == 0:
        if consent not in ("n/a", None):
            result.warn(
                f"num_people=0 but participant_consent_obtained={consent!r} "
                f"(expected 'n/a')"
            )

    return meta


def validate_csv(session_dir, result):
    csv_path = session_dir / "csi_raw.csv"
    if not csv_path.exists():
        return
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    data_lines = [l for l in lines if l.strip() and not l.lstrip().startswith("#")]
    if not data_lines:
        result.error("csi_raw.csv contains no data lines (only comments/empty, or file is empty)")
    elif len(data_lines) < 10:
        result.warn(f"csi_raw.csv has only {len(data_lines)} data line(s) -- session may be too short to be useful")


def validate_session(session_dir):
    result = ValidationResult(session_dir)
    if not session_dir.is_dir():
        result.error("not a directory")
        return result
    validate_files_present(session_dir, result)
    validate_metadata(session_dir, result)
    validate_csv(session_dir, result)
    return result


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("session_dirs", nargs="+", type=Path, help="One or more session directories to validate")
    args = p.parse_args()

    all_ok = True
    for session_dir in args.session_dirs:
        result = validate_session(session_dir)
        status = "PASS" if result.ok else "FAIL"
        print(f"[{status}] {session_dir}")
        for w in result.warnings:
            print(f"  WARN: {w}")
        for e in result.errors:
            print(f"  ERROR: {e}")
        if not result.ok:
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
