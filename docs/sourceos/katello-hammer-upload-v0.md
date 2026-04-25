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
  -> SourceOSKatelloUploadedArtifactVerificationReceipt
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

When upload is enabled, the task now captures `hammer file list` output for the target organization/product/repository and invokes `tools/verify-katello-uploaded-artifacts`.

The verifier checks that every expected artifact basename appears in the captured listing output and emits:

```text
SourceOSKatelloUploadedArtifactVerificationReceipt
```

This is still intentionally conservative. It verifies artifact-name visibility, not checksum parity inside Katello. Checksum-level verification should be added after stable Hammer file checksum output is validated in the target Foreman/Katello version.

## Non-goals

- no SourceOS release manifest mutation
- no catalog publication
- no credential handling
- no release promotion
- no checksum-level Katello content verification yet

## Follow-on work

- add Hammer-capable runner image digest/SBOM/scan policy hardening
- add checksum-level verification against Katello file listing/details when stable output is validated
- connect upload receipt to content-view publish/promote receipts
- connect upload receipt to catalog publication request generation
