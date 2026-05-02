#!/usr/bin/env python3
"""Validate Socios PersonalizationOrchestration examples.

This bootstrap validator enforces the opt-in invariants that make Socios safe
as the orchestration layer for per-user model personalization workflows.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/personalization-orchestration.schema.json"
EXAMPLES = sorted((ROOT / "examples").glob("personalization-orchestration.*.json"))


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_doc(path: Path, doc: dict[str, Any]) -> None:
    require(doc.get("schemaVersion") == "v0.1", f"{path}: schemaVersion must be v0.1")
    require(doc.get("kind") == "PersonalizationOrchestration", f"{path}: kind must be PersonalizationOrchestration")
    require(str(doc.get("orchestrationId", "")).startswith("urn:socios:personalization-orchestration:"), f"{path}: invalid orchestrationId")
    require(doc.get("governanceContractRef"), f"{path}: governanceContractRef is required")
    require(doc.get("signedIntentRef"), f"{path}: signedIntentRef is required")
    require(doc.get("proofOfLifeRef"), f"{path}: proofOfLifeRef is required")

    workflow = doc.get("workflow", {})
    require(workflow.get("agentPlaneRequired") is True, f"{path}: AgentPlane must be required for orchestration evidence")
    require(workflow.get("steps"), f"{path}: workflow.steps must be non-empty")

    inputs = doc.get("inputs", {})
    require(inputs.get("allowedSourceRefs"), f"{path}: allowedSourceRefs must be non-empty")
    denied = set(inputs.get("deniedSourceClasses", []))
    for denied_class in {"whole-home", "browser-profiles", "raw-app-stores", "token-stores"}:
        require(denied_class in denied, f"{path}: deniedSourceClasses must include {denied_class}")

    policy = doc.get("policy", {})
    require(policy.get("offByDefault") is True, f"{path}: offByDefault must be true")
    require(policy.get("requiresSignedIntent") is True, f"{path}: signed intent is required")
    require(policy.get("requiresProofOfLife") is True, f"{path}: proof-of-life is required")
    require(policy.get("promotionRequiresLedgerApproval") is True, f"{path}: ledger approval is required for promotion")
    require(policy.get("allowRawAppStores") is False, f"{path}: raw app stores must be denied by default")
    require(policy.get("allowWholeHomeIngestion") is False, f"{path}: whole-home ingestion must be denied")

    evidence = doc.get("evidence", {})
    for key in ["emitDatasetLineage", "emitPersonalizationReceipt", "emitEvalReceipt", "emitPromotionOrRevocationReceipt"]:
        require(evidence.get(key) is True, f"{path}: evidence.{key} must be true")


def main() -> int:
    load_json(SCHEMA)
    if not EXAMPLES:
        print("ERR: no personalization orchestration examples found", file=sys.stderr)
        return 2

    try:
        for example in EXAMPLES:
            doc = load_json(example)
            validate_doc(example.relative_to(ROOT), doc)
            print(f"ok: {example.relative_to(ROOT)}")
    except ValidationError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 1

    print("Personalization orchestration validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
