# SourceOS smoke runner image

This directory defines the first container image scaffold for the SourceOS live ISO smoke runner.

## Purpose

The image provides a minimal runtime for `tools/sourceos-smoke-runner`:
- Python 3
- QEMU x86 system binary
- basic core utilities

## Current posture

- base image is configurable through `BASE_IMAGE`
- the Containerfile requires explicit `BASE_IMAGE` input
- the Tekton build task can enforce digest-pinned base images with `requirePinnedBase=true`
- the Tekton image pipeline verifies the base image digest before build and records a `SmokeRunnerBaseImageReceipt`
- `task-image-policy.yaml` records task-image digest requirements for release-grade pipelines
- the Tekton image pipeline records both a task-image reference-check receipt and a task-image digest-resolution receipt
- `image-policy.yaml` records digest, base-image verification, SBOM, scan, provenance, evidence-bundle, and signing expectations without inventing an unverified digest
- `evidence-publication-policy.yaml` records the required evidence set before catalog or registry publication
- `promotion-policy.yaml` records manual release-candidate promotion expectations and required evidence
- the Tekton image pipeline checks task-image refs, resolves task-image digests, verifies the base image, builds the image, emits an SBOM, runs a scanner task, emits a provenance receipt, bundles image evidence, optionally attests, optionally promotes, and optionally emits an evidence-publication receipt
- attestation, promotion, and publication remain disabled by default until cross-stack signing and release authority are finalized

## Follow-on

The next tranche should add:
- verified base image digest replacement in `image-policy.yaml`
- verified task image digest replacement in `task-image-policy.yaml`
- concrete SourceOS/SociOS registry catalog publication implementation
