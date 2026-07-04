# Agent-S dynamic validation → Katello evidence gate wiring

This note shows how dynamic validation of a running SourceOS image flows from a
scenario set in this repo to an evidence-gated promotion decision. It extends
the deterministic boot-smoke check (`tools/sourceos-smoke-runner`, QEMU + serial
oracle) into the full dynamic-validation categories, driven by **Agent-S**
(simular-ai computer-use agent) against a **disposable guest VM**.

It mirrors the COSA build → gate wiring (`cosa/build.py` in
`SociOS-Linux/SourceOS`): a host-agnostic wrapper that validates a descriptor,
runs the real thing only on a capable host, and otherwise emits a fail-closed
dry-run stub for the same gate.

## Chain

```text
tools/dynamic-validation/scenario-set.yaml      (this repo — declares WHAT to exercise)
        │  python tools/dynamic-validation/run.py validate   ← runs anywhere / in CI
        ▼
Agent-S (controller container) drives a DISPOSABLE guest VM    ← HOST-GATED
   host actions policy-gated by policies/dynamic-validation-host-actions.yaml
        │  (Linux host with /dev/kvm + qemu + Agent-S/gui_agents)
        ▼
per-scenario evidence: screenshots + action trace + OCR/grounding + replay ref
        │
        ▼
DynamicValidationEvidenceBundle  (result / inputs_hash / blockers)
        │  wrapped into the ReleaseEvidenceBundle the gate consumes
        ▼
Katello evidence gate decides promotion (Library → dev → qa → prod)
    infra/ansible/roles/katello_lifecycle_sourceos/tasks/evidence_gate.yml
```

## Controller spec

- **Where Agent-S runs.** Agent-S runs in a **controller container** on the
  build host. It does *not* run inside the image under test. It drives the
  guest's GUI over the framebuffer (vision + grounding) and issues
  `guest_command` steps into the guest.
- **The guest is disposable.** Each scenario set runs against a fresh,
  throwaway guest VM (`spec.guest.disposable: true`, enforced). Red-team and
  rollback scenarios (`safetyClass: destructive`) require a base snapshot and an
  `isolated`/`offline` network; the runner refuses otherwise.
- **Host actions are policy-gated.** Most steps are GUI/guest actions. A few
  (`host_command`: snapshot / revert / destroy the guest, collect serial /
  screen) touch the host and are checked, fail-closed, against
  `policies/dynamic-validation-host-actions.yaml`. Anything not on the allow-list
  is rejected — in dry-run *and* real run, before any VM exists.
- **What is recorded.** Per scenario the controller records: screenshots
  (`none|final|per-step|on-failure`), the ordered Agent-S **action trace**
  (instruction → grounded coordinates → result), **OCR/grounding** metadata per
  GUI action, an optional **serial log**, and a **replay ref** (guest snapshot
  id + scenario hash) — mirroring the reasoning-evidence `ReplayPlan` shape so a
  run is re-derivable.

## Step detail

1. **Declare** — author a `DynamicValidationScenarioSet`
   (`scenario-set.example.yaml`). Each scenario carries `id`, `category`,
   `steps`, `expected` (pass/fail oracle), and `evidence_requirements` (what the
   bundle must carry to be allowed to mark PASS).

2. **Validate** — `python tools/dynamic-validation/run.py validate
   --scenarios <file>` checks the set against
   `scenario-set.schema.json` *and* the host-action policy. CI lint gate; no VM
   needed. Prefers `jsonschema` if installed, else a built-in structural check.

3. **Run (HOST-GATED)** — `python tools/dynamic-validation/run.py run
   --scenarios <file>`:
   - on a Linux host with `/dev/kvm`, `qemu`, and Agent-S (`gui_agents`)
     importable, it would run Agent-S against a disposable guest and record
     per-scenario evidence;
   - anywhere else it auto-falls back to **dry-run** and prints the exact
     Agent-S actions and policy-gated host/guest commands that *would* run.
     `--dry-run` forces this even on a capable host.
   - The real execution loop is intentionally left as the HOST-GATED extension
     point (it raises a clear "not implemented in this scaffold" error). The
     validate + dry-run paths are fully functional.

4. **Evidence** — in both modes the runner emits a
   `DynamicValidationEvidenceBundle` (`--emit-evidence`). It carries the three
   fields the gate reads:
   - `result` — `PASS` only when a real run executed every scenario and all
     passed; `DRY_RUN` on the no-runner path;
   - `inputs_hash` — sha256 over the whole bundle (non-empty by construction);
   - `blockers` — empty only on an all-pass real run; populated in dry-run
     (`runner-unavailable-or-dry-run: …`) and for any failed scenario.

5. **Gate** — the bundle is wrapped into the `ReleaseEvidenceBundle` the gate
   consumes. The gate
   (`infra/ansible/roles/katello_lifecycle_sourceos/tasks/evidence_gate.yml`) is
   **fail-closed**: it admits content-view promotion only when the bundle
   reports `result == PASS`, a non-empty `inputs_hash`, and zero `blockers`
   (plus optional trust-chain admission). A dry-run bundle
   (`result=DRY_RUN`, non-empty `blockers`) is therefore correctly **denied** —
   verified against the gate's exact admission predicate.

## Relationship to the boot-smoke runner

`tools/sourceos-smoke-runner` stays as-is: it is the first deterministic VM
handoff check (QEMU + serial-regex oracle, no GUI). This runner is **additive**
and complementary — it reuses the same serial-log oracle (`expected.serialMatches`)
for boot scenarios but adds GUI/OS automation via Agent-S for the categories the
serial log cannot cover (first-run wizard, desktop, network/storage, services,
rollback, red-/blue-team). Neither replaces the other.

## Boundaries

- This repo declares validation truth (scenarios + policy) and emits the
  evidence bundle. The capable build host (Linux + KVM), the Agent-S controller
  container, the disposable guest backend, and the real execution loop are the
  HOST-GATED extension point.
- Signing is deferred — `signing.signed: false`. TODO(cosign): a separate task
  wires real evidence-bundle signing.
- The Katello role and `evidence_gate.yml` are **referenced by path, not
  modified**.
