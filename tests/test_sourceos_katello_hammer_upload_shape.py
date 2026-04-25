#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


class SourceOSKatelloHammerUploadShapeTests(unittest.TestCase):
    def assertContainsAll(self, text: str, needles: list[str]) -> None:  # noqa: N802
        missing = [needle for needle in needles if needle not in text]
        self.assertEqual(missing, [], f"missing expected snippets: {missing}")

    def test_hammer_upload_task_is_gated_and_receipted(self) -> None:
        text = read("pipelines/tekton/task-upload-sourceos-artifacts-with-hammer.yaml")
        self.assertContainsAll(
            text,
            [
                "upload-sourceos-artifacts-with-hammer",
                "SourceOSKatelloHammerUploadReceipt",
                "SourceOSKatelloUploadedArtifactVerificationReceipt",
                "artifactBuildReceiptPath",
                "hammerRunnerImage",
                "repository upload-content",
                "file list",
                "repositoryListingPath",
                "verify-katello-uploaded-artifacts",
                "enabled",
            ],
        )

    def test_hammer_upload_pipeline_chains_publication_to_upload(self) -> None:
        text = read("pipelines/tekton/pipeline-sourceos-katello-hammer-upload.yaml")
        self.assertContainsAll(
            text,
            [
                "sourceos-katello-hammer-upload",
                "materialize-sourceos-build-request",
                "record-sourceos-artifact-build",
                "publish-sourceos-artifacts-to-katello",
                "upload-sourceos-artifacts-with-hammer",
                "runAfter: [publish-sourceos-artifacts-to-katello]",
            ],
        )

    def test_hammer_upload_doc_preserves_safety_posture_and_verification_scope(self) -> None:
        text = read("docs/sourceos/katello-hammer-upload-v0.md")
        self.assertContainsAll(
            text,
            [
                "upload execution is disabled by default",
                "no credentials or secrets are stored in repo",
                "SourceOS remains artifact truth",
                "catalog publication remains separate",
                "uploadEnabled=true",
                "SourceOSKatelloUploadedArtifactVerificationReceipt",
                "checksum-level Katello content verification",
            ],
        )


if __name__ == "__main__":
    unittest.main()
