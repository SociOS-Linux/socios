# SourceOS Upload Lifecycle Link v0

Status: Draft v0
Scope: linking Katello upload receipts to lifecycle publication/promote receipts

## Purpose

This document defines the seam between SourceOS artifact upload evidence and Katello lifecycle evidence.

The goal is to make downstream catalog/evidence lanes able to reason over both:

- artifact upload receipts
- upload verification receipts
- lifecycle/content-view publish/promote receipts

without merging artifact truth, lifecycle truth, and catalog truth into one repo.

## v0 flow

```text
SourceOS artifact upload lane
  -> SourceOSKatelloHammerUploadReceipt
  -> SourceOSKatelloUploadedArtifactVerificationReceipt
  -> link-sourceos-upload-lifecycle-receipts
  -> SourceOSLifecycleLinkValidationReceipt
  -> SourceOSUploadLifecycleLinkReceipt
```

## Receipt behavior

The link task requires:

- upload receipt
- upload verification receipt

The lifecycle receipt path is checked and recorded as either:

- `present`
- `missing`

The task also invokes `tools/validate-sourceos-lifecycle-link` to validate lifecycle/content-view evidence.

## Channel gates

Lifecycle receipt behavior is channel-aware:

- `dev`: lifecycle receipt may be missing; validator emits warning status
- `qa`: lifecycle receipt is required
- `prod`: lifecycle receipt is required

When a lifecycle receipt is present, it must include non-empty `latestContentViewVersions`. Each content-view version entry must include:

- `id`
- `version`

## Output receipts

Link receipt:

```text
.workstation/reports/sourceos/upload-lifecycle-link-receipt.json
```

kind:

```text
SourceOSUploadLifecycleLinkReceipt
```

Validation receipt:

```text
.workstation/reports/sourceos/lifecycle-link-validation-receipt.json
```

kind:

```text
SourceOSLifecycleLinkValidationReceipt
```

## Non-goals

- does not publish/promote content views
- does not mutate SourceOS release manifests
- does not publish to catalog
- does not claim lifecycle correctness beyond receipt validation

## Follow-on work

- validate expected content-view names against BuildRequest / ContentSpec metadata
- connect link receipt to catalog publication request generation
- add agentplane validation/run/replay refs for upload lifecycle linkage
