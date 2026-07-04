# SourceOS Artifact Build Receipt v0

Status: Draft v0
Scope: SourceOS artifact-build receipt capture in `SociOS-Linux/socios`

## Purpose

This document defines the first downstream build-recording lane after SourceOS build request intake.

The goal is to let `socios` record evidence about produced build artifacts without claiming ownership of SourceOS artifact truth.

## Authority boundary

- `SourceOS` remains artifact truth.
- `sourceos-spec` remains schema truth for release/evidence/catalog object vocabulary.
- `agentplane` remains execution evidence truth when builds are agent-executed.
- `socios` records automation receipts and hashes.

## v0 flow

```text
SourceOS build request params
  -> materialize-sourceos-build-request
  -> SourceOSBuildRequestMaterializationReceipt
  -> record-sourceos-artifact-build
  -> SourceOSArtifactBuildReceipt
```

## Artifact recording semantics

The v0 task accepts an explicit space-separated list of artifact paths.

For each artifact, it records:

- path
- SHA-256 hash
- byte size

The task fails if:

- materialization receipt is missing
- any expected artifact path is missing
- hash calculation fails

## Output receipt

The task emits:

```text
.workstation/reports/sourceos/artifact-build-receipt.json
```

with kind:

```text
SourceOSArtifactBuildReceipt
```

## Non-goals

- does not build the artifact itself
- does not mutate SourceOS release manifests
- does not upload to Katello
- does not publish to catalog
- does not claim release promotion

## Follow-on work

- add a real image-build task for selected SourceOS build systems
- add Katello upload/publish task consuming this receipt
- add smoke-runner integration consuming this receipt
- map this receipt into `sourceos-spec` `EvidenceBundle`
- project agentplane validation/run/replay refs when applicable
