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

## Execution gates

Actual upload is controlled by:

```text
uploadEnabled=true
```

Optional checksum-level verification is controlled by:

```text
verifyChecksums=true
```

If upload is disabled, the task still validates local artifact paths and emits skipped receipts.

## Verification posture

When upload is enabled, the task captures `hammer file list` output for the target organization/product/repository and invokes `tools/verify-katello-uploaded-artifacts`.

The verifier always checks that every expected artifact basename appears in the captured listing output and emits:

```text
SourceOSKatelloUploadedArtifactVerificationReceipt
```

When `verifyChecksums=true`, the verifier additionally computes local SHA-256 hashes and requires those hash values to appear in the captured listing output.

This is intentionally gated because checksum field availability may vary by target Foreman/Katello version and file listing configuration.

## Non-goals

- no SourceOS release manifest mutation
- no catalog publication
- no credential handling
- no release promotion
- no automatic checksum verification unless explicitly enabled

## Follow-on work

- add Hammer-capable runner image digest/SBOM/scan policy hardening
- validate checksum output against the exact target Foreman/Katello version
- connect upload receipt to content-view publish/promote receipts
- connect upload receipt to catalog publication request generation
