# SourceOS Build Request Orchestration v0

Status: Draft v0
Scope: SourceOS build request intake in `SociOS-Linux/socios`

## Purpose

This document defines the first automation boundary for turning a typed SourceOS build request into a `socios` automation receipt.

The goal is to connect `sourceos-spec` build/release concepts to Tekton automation without making `socios` the artifact truth authority.

## Authority boundary

- `SourceOS` owns artifact truth, flavor definitions, release manifests, and durable artifact references.
- `sourceos-spec` owns the typed object vocabulary for `ContentSpec`, `BuildRequest`, `ReleaseManifest`, `EvidenceBundle`, and `CatalogEntry`.
- `agentplane` owns execution evidence surfaces when agents validate/run/replay build workflows.
- `socios` owns automation scaffolds, receipts, and policy checks.

## v0 intake flow

```text
BuildRequest-style params
  -> materialize-sourceos-build-request task
  -> SourceOSBuildRequestMaterializationReceipt
  -> downstream build / Katello / Smart Proxy / smoke / catalog lanes
```

## Required fields

The v0 materialization task requires:

- `contentSpecRef`
- `buildRequestRef`
- `channel`
- `architecture`
- `requestedBy`

The task currently accepts `channel` values:

- `dev`
- `qa`
- `prod`

The task currently accepts `architecture` values:

- `x86_64`
- `aarch64`

## Optional refs

The materialization receipt may carry:

- `overlayRefs`
- `enrollmentProfileRef`
- `agentplaneBundleRef`
- `localExecutionProtocolRef`
- `remoteExecutionProtocolRef`
- `katelloProduct`
- `katelloRepository`

## Agentplane integration

`agentplaneBundleRef` is intentionally carried as metadata. The materialization task does not validate or execute agentplane bundles.

A later execution lane should project this ref into agentplane validation/run/replay artifacts.

## Local and remote protocols

The task defaults:

- local execution protocol: `urn:srcos:contract:workstation-contracts:m2-ipc:v1.0`
- remote execution protocol: `urn:srcos:protocol:tritrpc:v1`

This preserves the local M2 IPC / remote TriTRPC split established in the upstream specs.

## Output receipt

The task emits:

```text
.workstation/reports/sourceos/build-request-materialization.json
```

with kind:

```text
SourceOSBuildRequestMaterializationReceipt
```

## Non-goals

- no artifact build yet
- no release manifest mutation
- no catalog mutation
- no automatic agentplane execution
- no registry or credential handling

## Follow-on work

- add a downstream image-build task that consumes the materialization receipt
- add a Katello upload/publish task that consumes the materialization receipt
- add agentplane validation/run/replay projection for build-request execution
- add catalog publication request generation after build evidence exists
