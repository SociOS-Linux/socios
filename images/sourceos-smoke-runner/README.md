# SourceOS smoke runner image

This directory defines the first container image scaffold for the SourceOS live ISO smoke runner.

## Purpose

The image provides a minimal runtime for `tools/sourceos-smoke-runner`:
- Python 3
- QEMU x86 system binary
- basic core utilities

## Current posture

- base image is configurable through `BASE_IMAGE`
- intended default base is Fedora minimal
- image is not yet digest-pinned
- image build/sign/publish policy is intentionally outside this scaffold

## Follow-on

The next tranche should add:
- pinned base image digest
- SBOM generation
- image signing
- vulnerability scan policy
- promotion into the SourceOS/SociOS registry catalog
