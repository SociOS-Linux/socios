#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


class RoleShapeTests(unittest.TestCase):
    def assertContainsAll(self, text: str, needles: list[str]) -> None:  # noqa: N802
        missing = [needle for needle in needles if needle not in text]
        self.assertEqual(missing, [], f"missing expected snippets: {missing}")

    def test_katello_lifecycle_role_projects_versions_receipts_and_attestation(self) -> None:
        text = read("infra/ansible/roles/katello_lifecycle_sourceos/tasks/main.yml")
        self.assertContainsAll(
            text,
            [
                "hammer",
                "content-view",
                "version",
                "latestContentViewVersions",
                "activationKeyProductContentVerifications",
                "KatelloLifecycleReceipt",
                "sign_lifecycle_receipt.yml",
            ],
        )

    def test_smart_proxy_role_has_cert_network_feature_and_attestation_surfaces(self) -> None:
        text = read("infra/ansible/roles/smart_proxy_sourceos/tasks/main.yml")
        self.assertContainsAll(
            text,
            [
                "foreman-proxy-certs-generate",
                "foreman-installer",
                "proxy",
                "info",
                "domain",
                "subnet",
                "SmartProxyReceipt",
                "attest_smart_proxy_receipt.yml",
            ],
        )

    def test_content_policy_role_has_lookup_receipt_and_attestation_surfaces(self) -> None:
        text = read("infra/ansible/roles/smart_proxy_content_sync_sourceos/tasks/main.yml")
        self.assertContainsAll(
            text,
            [
                "proxy",
                "lifecycle-environment",
                "content-view",
                "SmartProxyContentPolicyReceipt",
                "attest_content_policy_receipt.yml",
            ],
        )

    def test_live_iso_smoke_task_calls_repo_runner(self) -> None:
        text = read("pipelines/tekton/task-smoke-live-iso.yaml")
        self.assertContainsAll(
            text,
            [
                "tools/sourceos-smoke-runner",
                "isoPath",
                "outDir",
            ],
        )

    def test_smoke_runner_image_pipeline_has_build_sbom_attestation_stages(self) -> None:
        text = read("pipelines/tekton/pipeline-build-smoke-runner-image.yaml")
        self.assertContainsAll(
            text,
            [
                "build-smoke-runner-image",
                "sbom-smoke-runner-image",
                "sign-smoke-runner-image",
                "requirePinnedBase",
                "baseImage",
            ],
        )

    def test_smoke_runner_image_policy_records_digest_and_sbom_expectations(self) -> None:
        text = read("images/sourceos-smoke-runner/image-policy.yaml")
        self.assertContainsAll(
            text,
            [
                "requireDigest: true",
                "REPLACE_WITH_VERIFIED_DIGEST",
                "sbom:",
                "signing:",
            ],
        )


if __name__ == "__main__":
    unittest.main()
