# SourceOS Katello Hammer Upload v0

Status: Draft v0
Scope: Gated Hammer CLI upload lane for SourceOS artifacts

## Purpose

This document defines the first executable upload seam for SourceOS artifacts into Katello-backed repositories.

The lane consumes a `SourceOSArtifactBuildReceipt`, uses the SourceOS Hammer runner image, and emits upload plus verification receipts.

## v0 flow

```text
BuildRequest-style params
  -> materialize-sourceos-build-request
  -> record-sourceos-artifact-build
  -> publish-sourceos-artifacts-to-katello
  -> upload-sourceos-artifacts-with-hammer
  -> SourceOSKatelloHammerUploadReceipt
  -> SourceOSKatelloHammerUploadVerificationReceipt
```

## Safety posture

- upload execution is disabled by default
- the task requires an existing artifact-build receipt
- the task requires explicit artifact paths
- the task uses a dedicated Hammer runner image
- no credentials or secrets are stored in repo
- SourceOS remains artifact truth
- catalog publication remains separate

## Execution gate

Actual upload is controlled by:

```text
uploadEnabled=true
```

If upload is disabled, the task still validates local artifact paths and emits skipped receipts.

## Verification posture

The v0 verification step records repository info after upload when enabled.

It does not yet assert that every uploaded artifact appears in repository content listings. That should be added once stable Hammer output for file content listing is validated.

## Non-goals

- no SourceOS release manifest mutation
- no catalog publication
- no credential handling
- no release promotion

## Follow-on work

- add Hammer-capable runner image digest/SBOM/scan policy hardening
- verify uploaded artifact names/checksums against Katello repository content listings
- connect upload receipt to content-view publish/promote receipts
- connect upload receipt to catalog publication request generation
