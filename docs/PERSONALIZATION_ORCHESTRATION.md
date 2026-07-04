# Personalization orchestration

Socios can orchestrate per-user model personalization only as an explicit opt-in workflow.

This does not make Socios mandatory for SourceOS. SourceOS must continue to operate without Socios.

## Required authority chain

```text
user-signed intent
  -> proof-of-life
  -> SocioProphet PersonalTuningContract
  -> Socios PersonalizationOrchestration
  -> AgentPlane evidence
  -> model-governance-ledger receipts
  -> model-router binding
```

No personalization job may run from a local profile alone.

## Contract files

```text
schemas/personalization-orchestration.schema.json
examples/personalization-orchestration.local-llama32.json
tools/validate_personalization_orchestration.py
```

## Safety invariants

- Socios remains off by default.
- A signed user intent is required.
- Proof-of-life is required.
- A governance contract from `SocioProphet/model-governance-ledger` is required.
- AgentPlane evidence is required.
- Dataset lineage is required.
- Personalization/evaluation receipts are required.
- Promotion or revocation receipts are required.
- Whole-home ingestion is denied.
- Raw app stores are denied by default.
- Browser profiles and token stores are denied by default.
- Promotion requires model-governance-ledger approval.

## Repository split

| Repo | Responsibility |
|---|---|
| `SourceOS-Linux/sourceos-model-carry` | Local model profiles and carry-layer service references. |
| `SocioProphet/model-governance-ledger` | Per-user consent, data boundary, evaluation, promotion, rollback, and revocation contracts. |
| `SociOS-Linux/socios` | Opt-in orchestration of approved personalization workflows. |
| `SocioProphet/model-router` | Runtime routing to base local model, personal adapter/model, or hosted fallback. |

## Validation

```bash
python3 tools/validate_personalization_orchestration.py
```
