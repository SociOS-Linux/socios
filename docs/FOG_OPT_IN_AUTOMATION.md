# Fog Opt-In Automation Role in socios

This document captures the intended **opt-in automation and catalog role** of `socios` for the Fog layer.

The Fog layer must function without `socios`.

`SociOS-Linux/socios` is the **optional commons / automation plane** that can distribute, validate, catalog, and update fog-related artifacts once a node is explicitly enrolled.

## Non-negotiable posture

- no SourceOS device is enrolled by default
- no fog node requires `socios` to boot or function locally
- any mutation requires explicit, user-signed intent
- community artifacts must be digest-pinned and verifiable

## What belongs here for the Fog layer

### 1. Signed catalogs

This repo is the right place to carry or publish signed catalogs for:
- approved fog agent images
- local storage / CSI chart pins
- ignition profile references
- installer profile references
- conformance policy packs

### 2. Opt-in update automation

Once a node is enrolled, this repo may drive:
- update proposals
- validation runs
- policy checks
- signed rollout receipts

### 3. Training / testing workflow automation

Where fog agents or compute workers need optional community automation for:
- training pipelines
- test lanes
- benchmark runs
- artifact publication

That orchestration belongs here only after explicit enrollment.

## What does not belong here

This repo should not become a hidden dependency for:
- substrate boot correctness
- first-boot disk and mount realization
- local container runtime viability
- the canonical contract layer

Those remain upstream in SourceOS, sourceos-spec, and the related runtime/conformance repos.

## Expected follow-up

Future PRs here should add:
1. fog-related signed catalog structures
2. policy packs controlling admissible fog updates
3. rollout receipts / evidence patterns for fog artifacts
4. explicit opt-in enrollment docs for fog nodes
