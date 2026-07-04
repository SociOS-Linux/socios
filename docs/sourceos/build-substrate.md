# SourceOS build substrate

The canonical SourceOS build substrate lives in **[`SociOS-Linux/sourceos-build`](https://github.com/SociOS-Linux/sourceos-build)**.

`socios` is the opt-in automation/orchestration commons that **drives** that substrate: it
emits `BuildRequest` documents and consumes `BuildReceipt` documents. It does not host build
IaC or pipelines itself.

## Consumed schema paths

Build orchestration in `socios` conforms to these canonical schema paths in `sourceos-build`:

- `schemas/sourceos/build-request.v0.1.schema.json` — the `BuildRequest` contract socios emits.
- `schemas/sourceos/build-receipt.v0.1.schema.json` — the `BuildReceipt` contract socios consumes.

Example payloads: `examples/build-request.example.json`, `examples/build-receipt.example.json`.

## Boundary

`sourceos-build` ships IaC (Terraform/Ansible), CD/pipeline skeletons (Argo CD/Tekton),
schemas, and receipts only — no product/runtime code, no secrets, no model weights. See
`sourceos-build/docs/adr/ADR-0001-sourceos-build-substrate.md`.
