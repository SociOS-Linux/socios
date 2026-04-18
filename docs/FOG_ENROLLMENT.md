# Fog enrollment in socios

This document clarifies how a fog-capable node may participate in the optional `socios` automation commons.

## Non-default posture

Enrollment is off by default.
A fog-capable SourceOS node must be able to boot, mount its fog substrate, run local workloads, and participate in topic replication without `socios`.

## What enrollment enables

Once a node is explicitly enrolled, `socios` may provide:
- signed artifact catalogs
- rollout and update automation
- policy-checked artifact admission
- optional benchmark / training / test workflows

## Minimum enrollment requirements

A future concrete enrollment flow should require at least:
- explicit user intent
- a local proof-of-life or equivalent signed confirmation
- review of the catalogs or update class being admitted
- the ability to opt out and return to local-only operation

## Fog-specific enrollment classes

Potential classes include:
- storage-only participant
- topic replication participant
- compute worker participant
- benchmark/test-only participant

These classes should be independently selectable rather than forced as one bundle.
