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
- `image-policy.yaml` records digest, SBOM, scan, provenance, and signing expectations without inventing an unverified digest
- the Tekton image pipeline now builds the image, emits an SBOM, runs a scanner task, emits a provenance receipt, and can optionally run an attestation task
- attestation remains disabled by default until cross-stack signing authority is finalized

## Follow-on

The next tranche should add:
- verified base image digest replacement in `image-policy.yaml`
- signed SBOM / provenance bundle
- promotion into the SourceOS/SociOS registry catalog
