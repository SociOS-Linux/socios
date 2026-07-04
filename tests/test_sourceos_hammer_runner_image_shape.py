#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


class SourceOSHammerRunnerImageShapeTests(unittest.TestCase):
    def assertContainsAll(self, text: str, needles: list[str]) -> None:  # noqa: N802
        missing = [needle for needle in needles if needle not in text]
        self.assertEqual(missing, [], f"missing expected snippets: {missing}")

    def test_containerfile_has_hammer_runtime_and_no_static_secret_material(self) -> None:
        text = read("images/sourceos-hammer-runner/Containerfile")
        self.assertContainsAll(
            text,
            [
                "ARG BASE_IMAGE",
                "hammer_cli",
                "hammer_cli_foreman",
                "hammer_cli_katello",
                "ENTRYPOINT [\"hammer\"]",
            ],
        )
        self.assertNotIn("password", text.lower())
        self.assertNotIn("token", text.lower())

    def test_image_policy_requires_digest_and_documents_no_credentials(self) -> None:
        text = read("images/sourceos-hammer-runner/image-policy.yaml")
        self.assertContainsAll(
            text,
            [
                "requireDigest: true",
                "REPLACE_WITH_VERIFIED_DIGEST",
                "hammer_cli_katello",
                "Do not bake credentials",
            ],
        )

    def test_build_task_records_hammer_runner_image_receipt(self) -> None:
        text = read("pipelines/tekton/task-build-hammer-runner-image.yaml")
        self.assertContainsAll(
            text,
            [
                "HammerRunnerImageBuildReceipt",
                "BASE_IMAGE=$(params.baseImage)",
                "requirePinnedBase",
                "buildah bud",
            ],
        )

    def test_build_pipeline_calls_hammer_runner_build_task(self) -> None:
        text = read("pipelines/tekton/pipeline-build-hammer-runner-image.yaml")
        self.assertContainsAll(
            text,
            [
                "sourceos-build-hammer-runner-image",
                "build-hammer-runner-image",
                "baseImage",
                "requirePinnedBase",
            ],
        )


if __name__ == "__main__":
    unittest.main()
