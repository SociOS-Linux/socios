#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


class SourceOSBuildRequestShapeTests(unittest.TestCase):
    def assertContainsAll(self, text: str, needles: list[str]) -> None:  # noqa: N802
        missing = [needle for needle in needles if needle not in text]
        self.assertEqual(missing, [], f"missing expected snippets: {missing}")

    def test_build_request_policy_preserves_authority_split(self) -> None:
        text = read("policies/sourceos/build-request-policy.yaml")
        self.assertContainsAll(
            text,
            [
                "artifactTruthRepo: SourceOS-Linux/SourceOS",
                "schemaTruthRepo: SourceOS-Linux/sourceos-spec",
                "automationRepo: SociOS-Linux/socios",
                "executionEvidenceRepo: SocioProphet/agentplane",
                "contentSpecRef",
                "buildRequestRef",
            ],
        )

    def test_materialization_task_emits_receipt_and_protocol_refs(self) -> None:
        text = read("pipelines/tekton/task-materialize-sourceos-build-request.yaml")
        self.assertContainsAll(
            text,
            [
                "SourceOSBuildRequestMaterializationReceipt",
                "contentSpecRef",
                "buildRequestRef",
                "agentplaneBundleRef",
                "urn:srcos:contract:workstation-contracts:m2-ipc:v1.0",
                "urn:srcos:protocol:tritrpc:v1",
                "katelloProduct",
                "katelloRepository",
            ],
        )

    def test_intake_pipeline_calls_materialization_task(self) -> None:
        text = read("pipelines/tekton/pipeline-sourceos-build-request-intake.yaml")
        self.assertContainsAll(
            text,
            [
                "sourceos-build-request-intake",
                "materialize-sourceos-build-request",
                "agentplaneBundleRef",
                "localExecutionProtocolRef",
                "remoteExecutionProtocolRef",
            ],
        )


if __name__ == "__main__":
    unittest.main()
