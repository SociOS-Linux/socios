#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


class SourceOSKatelloPublicationShapeTests(unittest.TestCase):
    def assertContainsAll(self, text: str, needles: list[str]) -> None:  # noqa: N802
        missing = [needle for needle in needles if needle not in text]
        self.assertEqual(missing, [], f"missing expected snippets: {missing}")

    def test_katello_publication_task_emits_receipt(self) -> None:
        text = read("pipelines/tekton/task-publish-sourceos-artifacts-to-katello.yaml")
        self.assertContainsAll(
            text,
            [
                "SourceOSKatelloArtifactPublicationReceipt",
                "artifactBuildReceiptPath",
                "katelloServerUrl",
                "organization",
                "product",
                "repository",
                "enabled",
            ],
        )

    def test_katello_publication_pipeline_chains_receipts(self) -> None:
        text = read("pipelines/tekton/pipeline-sourceos-artifact-katello-publication.yaml")
        self.assertContainsAll(
            text,
            [
                "sourceos-artifact-katello-publication",
                "materialize-sourceos-build-request",
                "record-sourceos-artifact-build",
                "publish-sourceos-artifacts-to-katello",
                "runAfter: [record-sourceos-artifact-build]",
            ],
        )

    def test_katello_publication_doc_preserves_non_goals(self) -> None:
        text = read("docs/sourceos/katello-artifact-publication-v0.md")
        self.assertContainsAll(
            text,
            [
                "SourceOS remains artifact truth",
                "upload execution is disabled by default",
                "does not mutate SourceOS release manifests",
                "does not publish to catalog",
                "does not store credentials or secrets",
            ],
        )


if __name__ == "__main__":
    unittest.main()
