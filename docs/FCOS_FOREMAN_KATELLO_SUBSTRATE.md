# FCOS + Foreman/Katello substrate (v0 scaffold)

This document records the intended substrate split for the SourceOS build and release lane.

## Boundaries

### `SourceOS`
Owns the substrate artifact truth only:
- flavors
- coreos-assembler config
- Butane / Ignition source material
- installer surfaces
- release channels and manifests

### `socios`
Owns the opt-in automation around that truth:
- Foreman / Katello management hosts
- Smart Proxies
- Tekton pipelines for build/customize/sign/publish/promote
- Argo CD deployment of K8s-native automation services
- enrollment, rollout, and promotion automation

### Foreman / Katello
Own the provisioning/content/lifecycle control plane.
They are not the image composer.

### FCOS toolchain
- `coreos-assembler` = thick derivative build lane
- `coreos-installer` = live ISO / PXE customization and install lane

## Initial implementation slice in this repo

This scaffold adds:
- Ansible bootstrap for Foreman/Katello on EL9
- Tekton pipeline skeletons for customized FCOS live ISO and Katello publish
- Argo CD landing note for cluster-native automation services

## Explicit non-goals in this scaffold

This scaffold does not yet provide:
- fully pinned images and package sources
- Smart Proxy rollout automation
- production Vault/Tang/object-store wiring
- release-signing implementation
- smoke tests against a real Foreman/Katello host

Those belong in the next tranche.
