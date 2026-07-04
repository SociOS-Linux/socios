# SourceOS/SociOS Catalog Publication Authority v0

Status: Draft v0
Scope: SourceOS/SociOS build evidence publication boundary

## Purpose

This document defines where catalog publication authority lives for SourceOS/SociOS build evidence and how automation-generated evidence becomes catalog-visible without letting the automation repo become the artifact truth authority.

The design follows the merged OS build substrate work:

- Foreman/Katello lifecycle and Smart Proxy/site-edge scaffolds
- SourceOS live ISO smoke runner
- smoke-runner image build/SBOM/scan/provenance/evidence pipeline
- disabled-by-default image promotion and evidence publication receipts
- digest verification and digest-application workflow scaffolds

## Authority split

### SourceOS artifact truth

SourceOS artifact truth remains outside this automation role boundary.

The `SourceOS` artifact/flavor repository owns:

- OS flavor definitions
- release manifests
- install media references
- durable artifact references
- artifact checksums
- promotion state for SourceOS artifacts

`SociOS-Linux/socios` does not become the source of truth for artifacts. It produces automation, receipts, and publication requests.

### SourceOS schema truth

`sourceos-spec` owns the typed contract vocabulary, including:

- `ContentSpec`
- `OverlayBundle`
- `BuildRequest`
- `ReleaseManifest`
- `EnrollmentProfile`
- `EvidenceBundle`
- `CatalogEntry`
- `AccessProfile`

Catalog publication requests emitted by `socios` must map cleanly to these typed objects.

### Execution evidence truth

`agentplane` owns execution-plane evidence surfaces, including validation/run/replay artifacts.

Catalog records should reference agentplane evidence when the build or promotion was agent-executed, but should not duplicate agentplane internals.

### Automation truth

`SociOS-Linux/socios` owns:

- Foreman/Katello automation
- Smart Proxy/site-edge automation
- Tekton task/pipeline scaffolds
- smoke-runner execution receipts
- image build/SBOM/scan/provenance/evidence receipts
- publication request receipts

`SociOS-Linux/socios` may emit catalog publication requests, but the catalog authority must decide whether to accept them.

## Publication authority

For v0, catalog publication authority is modeled as a logical service boundary named:

```text
sourceos-catalog-authority
```

This authority may initially be implemented as:

1. a repository-backed review flow,
2. a local catalog updater,
3. a controlled service endpoint,
4. or an agentplane-mediated workflow.

The authority must enforce policy before catalog mutation.

## Publication request shape

A publication request should be emitted as JSON and may later be promoted into a `sourceos-spec` schema object.

Minimum shape:

```json
{
  "apiVersion": "socios.sourceos.ai/v0",
  "kind": "CatalogPublicationRequest",
  "subjectRef": "quay.io/socios/sourceos-smoke-runner:dev",
  "targetCatalogRef": "sourceos://catalog/images/sourceos-smoke-runner",
  "requesterRef": "socios://pipeline/sourceos-build-smoke-runner-image",
  "evidenceBundleRef": ".workstation/reports/evidence/sourceos-smoke-runner-evidence.json",
  "requiredEvidence": [
    ".workstation/reports/images/sourceos-smoke-runner-base-image.json",
    ".workstation/reports/images/sourceos-smoke-runner-task-image-digests.json",
    ".workstation/reports/images/sourceos-smoke-runner-build.json",
    ".workstation/reports/sbom/sourceos-smoke-runner.spdx.json",
    ".workstation/reports/scans/sourceos-smoke-runner-grype.json",
    ".workstation/reports/provenance/sourceos-smoke-runner-provenance.json"
  ],
  "sourceosSpecRefs": {
    "catalogEntryType": "CatalogEntry",
    "evidenceBundleType": "EvidenceBundle"
  },
  "agentplaneRefs": {
    "validationArtifactRef": null,
    "runArtifactRef": null,
    "replayArtifactRef": null
  },
  "policy": {
    "autoPublish": false,
    "requiresHumanReview": true,
    "requiresDigestPinnedInputs": true
  }
}
```

## Required evidence gates

The catalog authority must require, at minimum:

1. base image digest verification receipt
2. task image digest-resolution receipt
3. image build receipt
4. SBOM
5. scan report
6. provenance receipt
7. evidence bundle receipt
8. promotion receipt if the subject is a promoted release-candidate image
9. attestation receipts when release policy requires them

## Policy gates

A publication request must fail if:

- any required evidence file is missing
- base image digest is unresolved for release-grade publication
- task image digests are unresolved for release-grade publication
- vulnerability policy fails
- provenance receipt does not reference the expected image and base image
- evidence bundle does not include required evidence refs
- the publication target is not authorized for the requester
- the request attempts to mutate SourceOS artifact truth from the automation repo

## Relationship to sourceos-spec

Accepted publication requests should produce or update a `CatalogEntry` whose object reference points at the published subject.

The `CatalogEntry` should reference an `EvidenceBundle` rather than copy every evidence artifact inline.

The `EvidenceBundle` should carry stable references to:

- build receipt
- SBOM
- scan report
- provenance receipt
- smoke receipt, when relevant
- image evidence bundle
- publication receipt
- agentplane validation/run/replay artifacts, when relevant

## Relationship to agentplane

When agentplane executes or governs a build/publish workflow, catalog publication must carry references to:

- `ValidationArtifact`
- `RunArtifact`
- `ReplayArtifact`

These references are catalog metadata, not ownership transfer.

The execution plane remains the source of truth for the execution artifacts.

## v0 implementation posture

For v0:

- publication remains disabled by default
- publication receipts are emitted by `socios`
- catalog mutation is not automatic
- final catalog writes require explicit authority implementation
- registry credentials and secrets are not stored in repo

## Follow-on implementation options

### Option A: repository-backed catalog PR

The publication authority opens a PR against the catalog/artifact truth repo with:

- `CatalogEntry`
- `EvidenceBundle`
- publication receipt
- links to required evidence

This is safest for v0.

### Option B: local catalog updater

A local catalog service accepts publication requests and writes to a local-first catalog store.

This is appropriate for disconnected builds.

### Option C: agentplane-mediated publication

Agentplane validates the publication request and emits execution evidence before catalog mutation.

This is appropriate once agentplane publication workflows are hardened.

## Recommendation

Use Option A for v0:

```text
socios pipeline -> publication request -> catalog authority review -> catalog PR
```

This keeps artifact truth separate, gives us a review boundary, and avoids accidental publication from automation scaffolds.

## Open work

- define exact repository target for catalog PRs
- add `CatalogPublicationRequest` to `sourceos-spec` if it graduates beyond v0 scaffold
- add a publisher task that creates a catalog PR rather than mutating catalog state directly
- wire agentplane validation/run/replay references into publication request generation
- define release-channel policy for dev/qa/prod publication
