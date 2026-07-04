#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "tools" / "dynamic-validation" / "run.py"
EXAMPLE = ROOT / "tools" / "dynamic-validation" / "scenario-set.example.yaml"
SCHEMA = ROOT / "tools" / "dynamic-validation" / "scenario-set.schema.json"
POLICY = ROOT / "policies" / "dynamic-validation-host-actions.yaml"
COVERAGE = ROOT / "docs" / "sourceos" / "dynamic-validation-coverage-v0.md"

# The six dynamic-validation categories the corpus defines.
CATEGORIES = {
    "boot-login-firstrun",
    "network-storage",
    "service-activation",
    "rollback-update",
    "redteam-safe-probe",
    "blueteam-detect-contain-forensics",
}


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUN), *args],
        capture_output=True, text=True, cwd=str(ROOT),
    )


class DynamicValidationShapeTests(unittest.TestCase):
    def test_files_exist(self) -> None:
        for p in (RUN, EXAMPLE, SCHEMA, POLICY, COVERAGE):
            self.assertTrue(p.exists(), f"missing {p}")

    def test_schema_declares_required_scenario_fields(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        sc = schema["$defs"]["scenario"]
        self.assertEqual(
            sc["required"],
            ["id", "category", "steps", "expected", "evidence_requirements"],
        )
        enum = set(schema["$defs"]["category"]["enum"])
        self.assertEqual(enum, CATEGORIES)

    def test_example_covers_all_six_categories(self) -> None:
        result = _run("validate", "--scenarios", str(EXAMPLE))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_dry_run_emits_gate_denied_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "bundle.json"
            result = _run(
                "run", "--scenarios", str(EXAMPLE),
                "--dry-run", "--emit-evidence", str(out),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            bundle = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(bundle["result"], "DRY_RUN")
            self.assertTrue(bundle["inputs_hash"].startswith("sha256:"))
            self.assertGreater(len(bundle["blockers"]), 0)
            # Mirror the gate's admission predicate (evidence_gate.yml):
            admitted = (
                bundle["result"] == "PASS"
                and len(bundle["inputs_hash"]) > 0
                and len(bundle["blockers"]) == 0
            )
            self.assertFalse(admitted, "dry-run bundle must NOT be gate-admitted")

    def test_policy_rejects_unlisted_host_command(self) -> None:
        bad = (
            "apiVersion: socios.sourceos.ai/v0\n"
            "kind: DynamicValidationScenarioSet\n"
            "metadata: {name: bad}\n"
            "spec:\n"
            "  targetImage: {artifactRef: x.iso, format: iso}\n"
            "  guest: {disposable: true}\n"
            "  scenarios:\n"
            "    - id: bad\n"
            "      category: blueteam-detect-contain-forensics\n"
            "      steps: [{action: host_command, target: 'rm -rf /'}]\n"
            "      expected: {}\n"
            "      evidence_requirements: {}\n"
        )
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.yaml"
            p.write_text(bad, encoding="utf-8")
            result = _run("validate", "--scenarios", str(p))
            self.assertEqual(result.returncode, 1)
            self.assertIn("not policy-allowed", result.stderr)

    def test_coverage_doc_maps_thirteen_categories(self) -> None:
        text = COVERAGE.read_text(encoding="utf-8")
        for n in range(1, 14):
            self.assertIn(f"LIV-{n:02d}", text, f"coverage doc missing LIV-{n:02d}")


if __name__ == "__main__":
    unittest.main()
