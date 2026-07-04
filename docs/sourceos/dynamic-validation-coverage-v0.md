# Linux image dynamic-validation coverage (v0)

This maps the **13 Linux image validation categories** the corpus enumerates to
the dynamic-validation scenarios that exercise them, and flags what remains
**TODO** (declared but not yet covered by a scenario, or only partially covered).

- Scenario set: `tools/dynamic-validation/scenario-set.example.yaml`
- Runner / contract: `tools/dynamic-validation/run.py`, `scenario-set.schema.json`
- Wiring to the gate: `tools/dynamic-validation/WIRING.md`

Each scenario's `covers:` field lists the `LIV-NN` ids below, so coverage is
machine-checkable from the scenario set itself.

## The 13 categories → scenarios

| ID | Linux image validation category | Dynamic-validation category | Covering scenario(s) | Status |
|----|----------------------------------|------------------------------|----------------------|--------|
| LIV-01 | Boots on the target firmware (UEFI) to a usable state | boot-login-firstrun | `boot-to-desktop` | COVERED |
| LIV-02 | Reaches the login greeter / desktop session | boot-login-firstrun | `boot-to-desktop`, `first-run-account` | COVERED |
| LIV-03 | First-run / out-of-box account setup completes | boot-login-firstrun | `first-run-account` | COVERED |
| LIV-04 | Network brings up and DNS resolves | network-storage | `network-bring-up` | COVERED |
| LIV-05 | Storage mounts read-write and persists a write | network-storage | `storage-mount-write` | COVERED |
| LIV-06 | System reaches `running` with no failed units | service-activation | `core-services-active` | COVERED |
| LIV-07 | Core SourceOS services activate | service-activation | `core-services-active` | PARTIAL — generic `--failed` check; per-service asserts TODO |
| LIV-08 | rpm-ostree update stages a new deployment | rollback-update | `ostree-update-rollback` | PARTIAL — `upgrade --check` only (isolated guest has no upgrade source) |
| LIV-09 | Rollback to the prior deployment is clean | rollback-update | `ostree-update-rollback` | COVERED |
| LIV-10 | Privilege boundaries hold (no unintended escalation) | redteam-safe-probe | `redteam-priv-esc-probe` | COVERED |
| LIV-11 | Sensitive files are not world-readable | redteam-safe-probe | `redteam-priv-esc-probe` | COVERED |
| LIV-12 | Security events are detectable (audit / kernel log populated) | blueteam-detect-contain-forensics | `blueteam-detect-contain` | COVERED |
| LIV-13 | Incident can be contained + forensically captured | blueteam-detect-contain-forensics | `blueteam-detect-contain` | PARTIAL — snapshot capture (contain); offline forensic analysis TODO |

## Coverage by dynamic-validation category

| Dynamic-validation category | Categories touched | Scenarios |
|------------------------------|--------------------|-----------|
| boot-login-firstrun | LIV-01..03 | `boot-to-desktop`, `first-run-account` |
| network-storage | LIV-04, LIV-05 | `network-bring-up`, `storage-mount-write` |
| service-activation | LIV-06, LIV-07 | `core-services-active` |
| rollback-update | LIV-08, LIV-09 | `ostree-update-rollback` |
| redteam-safe-probe | LIV-10, LIV-11 | `redteam-priv-esc-probe` |
| blueteam-detect-contain-forensics | LIV-12, LIV-13 | `blueteam-detect-contain` |

## Remaining TODO

These are partial or environment-dependent; they need a capable host (Linux +
/dev/kvm + Agent-S) and, in some cases, additional scenario authoring:

- **LIV-07** — add explicit per-service `systemctl is-active <unit>` asserts for
  the named SourceOS units (currently only the aggregate `--failed` check).
- **LIV-08** — the real upgrade-staging path needs a guest with `networkProfile:
  nat` and a reachable rpm-ostree remote; the example uses `isolated` and
  `upgrade --check`. Author a NAT-gated variant for the full stage→deploy path.
- **LIV-13** — `snapshot-guest` provides containment + capture; a follow-on
  **offline forensic-analysis** scenario (mount the captured snapshot read-only
  from the controller, run a triage pass) is not yet authored.
- **Secure Boot / measured boot (firmware attestation)** — not in the 13 here;
  flagged as a candidate LIV-14 once the corpus is extended. Would slot under a
  new boot sub-scenario with TPM evidence in `expected.serialMatches` + a host
  `collect-serial` action.
- **Real execution loop** — every scenario above is exercised by the dry-run
  planner today; the Agent-S → guest action/record loop itself is the HOST-GATED
  extension point in `run.py`.
