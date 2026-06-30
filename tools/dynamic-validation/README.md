# Agent-S dynamic-validation harness

Extends the deterministic boot-smoke check (`tools/sourceos-smoke-runner`) into
the full Linux-image dynamic-validation categories, driven by **Agent-S**
(simular-ai computer-use agent) against a **disposable guest VM**.

## Files

| File | Purpose |
|------|---------|
| `scenario-set.schema.json` | Contract for a `DynamicValidationScenarioSet` (scenarios: `id`, `category`, `steps`, `expected`, `evidence_requirements`). |
| `scenario-set.example.yaml` | Example set covering all six dynamic-validation categories. |
| `run.py` | Controller runner: validate / run / dry-run; emits the `DynamicValidationEvidenceBundle`. |
| `WIRING.md` | How the bundle feeds the `ReleaseEvidenceBundle` + Katello evidence gate. |
| `../../policies/dynamic-validation-host-actions.yaml` | Fail-closed policy gating `host_command` steps. |
| `../../docs/sourceos/dynamic-validation-coverage-v0.md` | The 13 Linux validation categories → scenarios → TODO. |
| `../../pipelines/tekton/task-dynamic-validate-live-iso.yaml` | Tekton task entry point. |

## Run it

```bash
# Lint (anywhere, incl. CI — prefers jsonschema, else a built-in check):
python tools/dynamic-validation/run.py validate \
  --scenarios tools/dynamic-validation/scenario-set.example.yaml

# Dry-run: print the Agent-S/host/guest actions that WOULD run + emit a DRY_RUN
# evidence stub the fail-closed gate correctly denies:
python tools/dynamic-validation/run.py run \
  --scenarios tools/dynamic-validation/scenario-set.example.yaml \
  --dry-run --emit-evidence .workstation/state/dynval/evidence-bundle.json
```

## HOST-GATED requirement (explicit)

A **real** run needs all of:

- a **Linux** host,
- **`/dev/kvm`** (hardware virtualization for the disposable guest VM),
- **`qemu-system-x86_64`** on PATH (guest backend),
- the **Agent-S** package (`gui_agents`) importable.

When any is missing the runner auto-falls back to dry-run. The real
controller→guest action/record loop is the documented extension point in
`run.py` (it raises a clear "not implemented in this scaffold" error rather than
pretending to run). The validate + dry-run paths run anywhere.
