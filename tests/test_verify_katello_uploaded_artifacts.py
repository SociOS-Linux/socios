#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "verify-katello-uploaded-artifacts"

spec = importlib.util.spec_from_file_location("verify_katello_uploaded_artifacts", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VerifyKatelloUploadedArtifactsTests(unittest.TestCase):
    def test_verify_passes_when_basenames_are_present(self) -> None:
        listing = "sourceos-live.iso\nsourceos-config.tar\n"
        result = module.verify(listing, ["dist/sourceos-live.iso", "out/sourceos-config.tar"])
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["missing"], [])

    def test_verify_reports_missing_basename(self) -> None:
        listing = "sourceos-live.iso\n"
        result = module.verify(listing, ["dist/sourceos-live.iso", "out/sourceos-config.tar"])
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["missing"], ["sourceos-config.tar"])

    def test_verify_ignores_empty_artifact_paths(self) -> None:
        listing = "sourceos-live.iso\n"
        result = module.verify(listing, ["dist/sourceos-live.iso", ""])
        self.assertEqual(result["expected"], ["sourceos-live.iso"])
        self.assertEqual(result["status"], "pass")

    def test_verify_checksum_passes_when_digest_is_present(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            artifact = Path(td) / "sourceos-live.iso"
            artifact.write_text("sourceos test artifact", encoding="utf-8")
            digest = module.sha256_file(artifact)
            listing = f"Name,Checksum\nsourceos-live.iso,{digest}\n"
            result = module.verify(listing, [str(artifact)], verify_checksums=True)
            self.assertEqual(result["status"], "pass")
            self.assertEqual(result["missingChecksums"], [])
            self.assertTrue(result["artifacts"][0]["checksumPresent"])

    def test_verify_checksum_reports_missing_digest(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            artifact = Path(td) / "sourceos-live.iso"
            artifact.write_text("sourceos test artifact", encoding="utf-8")
            listing = "Name,Checksum\nsourceos-live.iso,sha256-not-the-local-file\n"
            result = module.verify(listing, [str(artifact)], verify_checksums=True)
            self.assertEqual(result["status"], "fail")
            self.assertEqual(len(result["missingChecksums"]), 1)
            self.assertFalse(result["artifacts"][0]["checksumPresent"])


if __name__ == "__main__":
    unittest.main()
