# SourceOS Hammer runner image

This directory defines a minimal Hammer CLI runner image for SourceOS/Foreman/Katello automation.

## Purpose

The image provides a controlled runtime for future tasks that need Hammer CLI access, including:

- Katello artifact uploads
- repository verification
- content-view operations
- activation/enrollment key inspection
- Smart Proxy / Capsule inspection

## Current posture

- base image is configurable through `BASE_IMAGE`
- the Containerfile requires explicit `BASE_IMAGE` input
- the image policy requires a verified base-image digest before release-grade use
- no credentials, tokens, activation keys, or server-specific configuration are baked into the image
- image signing remains optional until cross-stack signing authority is finalized

## Follow-on

The next tranche should add:

- build/SBOM/scan/provenance pipeline for this image
- digest-resolution workflow matching the smoke-runner image lane
- Hammer upload task that uses this image and consumes `SourceOSArtifactBuildReceipt`
