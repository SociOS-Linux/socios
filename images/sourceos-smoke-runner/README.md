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
- `image-policy.yaml` records digest, SBOM, scan, provenance, evidence-bundle, and signing expectations without inventing an unverified digest
- `promotion-policy.yaml` records manual release-candidate promotion expectations and required evidence
- the Tekton image pipeline now builds the image, emits an SBOM, runs a scanner task, emits a provenance receipt, bundles image evidence, can optionally run attestation tasks, and can optionally promote the image
- attestation and promotion remain disabled by default until cross-stack signing and release authority are finalized

## Follow-on

The next tranche should add:
- verified base image digest replacement in `image-policy.yaml`
- signed SBOM / provenance bundle publication policy
- promotion into the SourceOS/SociOS registry catalog
