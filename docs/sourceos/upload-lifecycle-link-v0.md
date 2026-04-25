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
  -> SourceOSUploadLifecycleLinkReceipt
```

## Receipt behavior

The link task requires:

- upload receipt
- upload verification receipt

The lifecycle receipt path is checked and recorded as either:

- `present`
- `missing`

This keeps the task useful across local/dev runs where lifecycle publication may happen separately.

## Output receipt

```text
.workstation/reports/sourceos/upload-lifecycle-link-receipt.json
```

kind:

```text
SourceOSUploadLifecycleLinkReceipt
```

## Non-goals

- does not publish/promote content views
- does not mutate SourceOS release manifests
- does not publish to catalog
- does not claim lifecycle correctness by itself

## Follow-on work

- require lifecycle receipt for qa/prod channels
- validate content-view version ids from lifecycle receipt
- connect link receipt to catalog publication request generation
- add agentplane validation/run/replay refs for upload lifecycle linkage
