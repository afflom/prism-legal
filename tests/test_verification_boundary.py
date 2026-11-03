"""Missing tools must never be presented as a successful verification."""

import unittest
import json
from unittest.mock import patch

from tools.case import checks


class VerificationBoundary(unittest.TestCase):
    @patch.object(checks, "lexlean_bin", return_value="lexlean")
    def test_zero_exit_status_without_evidence_is_not_verification(self, _):
        for output in ("", "[]", "not json", json.dumps({"success": True})):
            with self.subTest(output=output), patch.object(checks, "_run", return_value=(0, output, "")):
                result = checks.verify()
                self.assertFalse(result["ok"])
                self.assertIsNone(result["attestation"])

    @patch.object(checks, "lexlean_bin", return_value="lexlean")
    def test_check_result_cannot_impersonate_kernel_verification(self, _):
        output = json.dumps({"spec": "lexlean/command-result/1", "command": "check", "exit_code": 0, "success": True})
        with patch.object(checks, "_run", return_value=(0, output, "")):
            self.assertTrue(checks.check()["ok"])
            self.assertFalse(checks.verify()["ok"])

    @patch.object(checks, "lexlean_bin", return_value=None)
    def test_missing_compiler_fails_both_checks_and_verification(self, _):
        for operation in (checks.check, checks.verify):
            with self.subTest(operation=operation.__name__):
                result = operation()
                self.assertFalse(result["ok"])
                self.assertIsNone(result["attestation"])
                self.assertIn("No compiler or kernel verification", result["diagnostics"][0])

    @patch.object(checks, "lexlean_bin", return_value=None)
    def test_existing_lock_does_not_stand_in_for_the_compiler(self, _):
        self.assertTrue((checks.ROOT / "lexlean.lock").is_file())
        self.assertFalse(checks.lock()["ok"])

    @patch.object(checks, "lock", side_effect=AssertionError("verification must not relock"))
    @patch.object(checks, "_lexlean", return_value={"ok": False, "diagnostics": ["stale lock"]})
    def test_verification_keeps_stale_locks_visible(self, compiler, _):
        self.assertFalse(checks.verify()["ok"])
        compiler.assert_called_once_with(["verify"], timeout=1800)


if __name__ == "__main__":
    unittest.main()
