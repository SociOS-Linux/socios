#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "apply-smoke-runner-digests"

spec = importlib.util.spec_from_file_location("apply_smoke_runner_digests", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

VALID_A = "sha256:" + "a" * 64
VALID_B = "sha256:" + "b" * 64
VALID_C = "sha256:" + "c" * 64


class ApplySmokeRunnerDigestsTests(unittest.TestCase):
    def test_replace_yaml_scalar_after_key(self) -> None:
        text = "spec:\n  baseImage:\n    ref: example/base\n    digest: REPLACE_WITH_VERIFIED_DIGEST\n"
        out = module.replace_yaml_scalar_after_key(text, "baseImage", "digest", VALID_A)
        self.assertIn(f"digest: {VALID_A}", out)
        self.assertNotIn("REPLACE_WITH_VERIFIED_DIGEST", out)

    def test_replace_task_digest_only_target_item(self) -> None:
        text = """spec:
  taskImages:
    - name: builderImage
      digest: REPLACE_WITH_VERIFIED_DIGEST
    - name: sbomImage
      digest: REPLACE_WITH_VERIFIED_DIGEST
"""
        out = module.replace_task_digest(text, "builderImage", VALID_B)
        self.assertIn(f"digest: {VALID_B}", out)
        self.assertEqual(out.count("REPLACE_WITH_VERIFIED_DIGEST"), 1)

    def test_validate_digest_rejects_bad_values(self) -> None:
        with self.assertRaises(SystemExit):
            module.validate_digest("sha256:nothex", "bad")

    def test_load_json_rejects_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(SystemExit):
                module.load_json(Path(td) / "missing.json")

    def test_task_image_name_map_contains_expected_policy_keys(self) -> None:
        self.assertEqual(module.TASK_IMAGE_NAME_MAP["attestImage"], "signingImage")
        self.assertEqual(module.TASK_IMAGE_NAME_MAP["utilityImage"], "shellUtilityImage")


if __name__ == "__main__":
    unittest.main()
