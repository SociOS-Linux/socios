#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


class SourceOSUploadLifecycleLinkShapeTests(unittest.TestCase):
    def assertContainsAll(self, text: str, needles: list[str]) -> None:  # noqa: N802
        missing = [needle for needle in needles if needle not in text]
        self.assertEqual(missing, [], f"missing expected snippets: {missing}")

    def test_upload_lifecycle_link_task_emits_receipts_and_validation(self) -> None:
        text = read("pipelines/tekton/task-link-sourceos-upload-lifecycle-receipts.yaml")
        self.assertContainsAll(
            text,
            [
                "SourceOSUploadLifecycleLinkReceipt",
                "SourceOSLifecycleLinkValidationReceipt",
                "uploadReceiptPath",
                "uploadVerificationReceiptPath",
                "lifecycleReceiptPath",
                "lifecycleReceiptStatus",
                "validationReceiptPath",
                "validate-sourceos-lifecycle-link",
                "channel",
            ],
        )

    def test_upload_lifecycle_pipeline_chains_upload_to_link(self) -> None:
        text = read("pipelines/tekton/pipeline-sourceos-upload-lifecycle-link.yaml")
        self.assertContainsAll(
            text,
            [
                "sourceos-upload-lifecycle-link",
                "upload-sourceos-artifacts-with-hammer",
                "link-sourceos-upload-lifecycle-receipts",
                "runAfter: [upload-sourceos-artifacts-with-hammer]",
                "verifyChecksums",
                "channel",
            ],
        )

    def test_upload_lifecycle_doc_preserves_boundaries_and_channel_gates(self) -> None:
        text = read("docs/sourceos/upload-lifecycle-link-v0.md")
        self.assertContainsAll(
            text,
            [
                "does not publish/promote content views",
                "does not mutate SourceOS release manifests",
                "does not publish to catalog",
                "SourceOSUploadLifecycleLinkReceipt",
                "SourceOSLifecycleLinkValidationReceipt",
                "qa",
                "prod",
                "latestContentViewVersions",
            ],
        )


if __name__ == "__main__":
    unittest.main()
