# SourceOS Katello Artifact Publication v0

Status: Draft v0
Scope: SourceOS artifact publication receipt flow for Katello-backed artifact repositories

## Purpose

This document defines the first publication seam between SourceOS artifact-build receipts and Katello file repositories.

The goal is to record a publication request/receipt without making publication automatic or moving SourceOS artifact truth into `socios`.

## v0 flow

```text
BuildRequest-style params
  -> materialize-sourceos-build-request
  -> record-sourceos-artifact-build
  -> publish-sourceos-artifacts-to-katello
  -> SourceOSKatelloArtifactPublicationReceipt
```

## Authority boundary

- `SourceOS` remains artifact truth.
- `socios` emits automation receipts and publication requests.
- Katello stores lifecycle-managed content after an explicit publication step.
- Catalog publication remains separate and governed by the catalog authority boundary.

## Current posture

- upload execution is disabled by default
- the task validates that the artifact-build receipt exists
- the task records target Katello server/product/repository metadata
- actual Hammer upload execution is deferred to a Hammer-capable runner image

## Output receipt

The task emits:

```text
.workstation/reports/sourceos/katello-artifact-publication.json
```

with kind:

```text
SourceOSKatelloArtifactPublicationReceipt
```

## Non-goals

- does not mutate SourceOS release manifests
- does not publish to catalog
- does not claim release promotion
- does not store credentials or secrets
- does not execute upload unless explicitly enabled

## Follow-on work

- add Hammer-capable runner image policy
- add actual `hammer repository upload-content` execution path
- verify uploaded artifact exists in target repository
- connect publication receipt to lifecycle content-view publish/promote receipts
- connect publication receipt to catalog publication request generation
