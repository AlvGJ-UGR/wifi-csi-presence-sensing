"""
test_validate_session.py -- smoke tests for tools/validate_session.py

Runs the validator as a subprocess against the synthetic fixtures in
tools/tests/fixtures/. These fixtures contain no real CSI data -- they
exist solely to exercise the validator's format/consent checks.

Run with:
    python -m unittest tools/tests/test_validate_session.py -v
or simply:
    python tools/tests/test_validate_session.py
"""

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VALIDATOR = REPO_ROOT / "tools" / "validate_session.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TestValidateSession(unittest.TestCase):
    def run_validator(self, session_dir):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(session_dir)],
            capture_output=True,
            text=True,
        )

    def test_valid_session_passes(self):
        proc = self.run_validator(FIXTURES / "valid_session")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("[PASS]", proc.stdout)

    def test_missing_consent_fails(self):
        proc = self.run_validator(FIXTURES / "invalid_session_missing_consent")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("[FAIL]", proc.stdout)
        self.assertIn("participant_consent_obtained", proc.stdout)
        self.assertIn("participant_ids is empty", proc.stdout)

    def test_nonexistent_directory_fails(self):
        proc = self.run_validator(FIXTURES / "does_not_exist")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("[FAIL]", proc.stdout)


if __name__ == "__main__":
    unittest.main()
