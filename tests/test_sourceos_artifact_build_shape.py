#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


class SourceOSArtifactBuildShapeTests(unittest.TestCase):
    def assertContainsAll(self, text: str, needles: list[str]) -> None:  # noqa: N802
        missing = [needle for needle in needles if needle not in text]
        self.assertEqual(missing, [], f"missing expected snippets: {missing}")

    def test_artifact_receipt_task_records_hashes_and_sizes(self) -> None:
        text = read("pipelines/tekton/task-record-sourceos-artifact-build.yaml")
        self.assertContainsAll(
            text,
            [
                "SourceOSArtifactBuildReceipt",
                "materializationReceiptPath",
                "artifactPaths",
                "sha256sum",
                "sizeBytes",
                "buildSystemRef",
            ],
        )

    def test_artifact_receipt_pipeline_chains_intake_to_recording(self) -> None:
        text = read("pipelines/tekton/pipeline-sourceos-build-artifact-receipt.yaml")
        self.assertContainsAll(
            text,
            [
                "sourceos-build-artifact-receipt",
                "materialize-sourceos-build-request",
                "record-sourceos-artifact-build",
                "runAfter: [materialize-sourceos-build-request]",
                "artifactPaths",
            ],
        )

    def test_artifact_receipt_doc_preserves_authority_boundary(self) -> None:
        text = read("docs/sourceos/artifact-build-receipt-v0.md")
        self.assertContainsAll(
            text,
            [
                "SourceOS remains artifact truth",
                "SourceOSArtifactBuildReceipt",
                "does not mutate SourceOS release manifests",
                "does not upload to Katello",
                "does not publish to catalog",
            ],
        )


if __name__ == "__main__":
    unittest.main()
