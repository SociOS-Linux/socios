# Fog catalogs

This directory is the placeholder home for signed fog-related catalogs once a node is explicitly enrolled into `socios`.

## Intended catalog items

- local-storage / CSI chart pins
- fog agent image pins
- ignition profile references
- installer profile references
- conformance policy pack references

## Admission posture

Catalog entries in this directory are expected to be:
- explicitly enrolled / policy-allowed
- digest-pinned
- verifiable

Placeholder entries may exist for design review, but they must fail the admissibility policy until replaced with real pins.

## Boundary

These catalogs are **optional** and must never become a hidden dependency for local substrate correctness.
