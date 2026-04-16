# Skills (Capability Manifests)

This directory contains **SkillManifests** (typed capability descriptors) plus their entry docs and optional helper scripts.

These manifests are intended to align with the SourceOS/SociOS Typed Contracts `SkillManifest` schema (spec v2.x).

Operational posture:
- `socios` is opt-in automation. Nothing here should assume enrollment by default.
- Any mutation must be gated by user intent (Proof-of-Life + signed intent).

Start here:
- `skills/fedora-atomic/README.md`
