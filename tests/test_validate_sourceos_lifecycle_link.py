#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "validate-sourceos-lifecycle-link"

spec = importlib.util.spec_from_file_location("validate_sourceos_lifecycle_link", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

VALID_LIFECYCLE = {
    "latestContentViewVersions": {
        "sourceos-workstation": {"id": "42", "version": "3.0"}
    }
}


class ValidateSourceOSLifecycleLinkTests(unittest.TestCase):
    def test_dev_warns_when_lifecycle_missing(self) -> None:
        result = module.validate("dev", None)
        self.assertEqual(result["status"], "warn")
        self.assertFalse(result["requiresLifecycle"])

    def test_qa_fails_when_lifecycle_missing(self) -> None:
        result = module.validate("qa", None)
        self.assertEqual(result["status"], "fail")
        self.assertTrue(result["requiresLifecycle"])

    def test_prod_fails_when_lifecycle_missing(self) -> None:
        result = module.validate("prod", None)
        self.assertEqual(result["status"], "fail")
        self.assertTrue(result["requiresLifecycle"])

    def test_valid_lifecycle_receipt_passes(self) -> None:
        result = module.validate("prod", VALID_LIFECYCLE)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["missingVersionEntries"], [])

    def test_lifecycle_without_versions_fails(self) -> None:
        result = module.validate("dev", {"latestContentViewVersions": {}})
        self.assertEqual(result["status"], "fail")
        self.assertIn("latestContentViewVersions", result["missingVersionEntries"])

    def test_lifecycle_entry_missing_id_or_version_fails(self) -> None:
        result = module.validate("qa", {"latestContentViewVersions": {"sourceos-workstation": {"id": "42"}}})
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["missingVersionEntries"], ["sourceos-workstation"])


if __name__ == "__main__":
    unittest.main()
