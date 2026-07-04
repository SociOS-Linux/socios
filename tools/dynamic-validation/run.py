#!/usr/bin/env python3
"""Agent-S dynamic-validation controller runner for SourceOS images.

This is the controller-side wrapper around an Agent-S (simular-ai computer-use
agent) run that drives a DISPOSABLE guest VM through a DynamicValidationScenarioSet.
It extends the boot-smoke check (tools/sourceos-smoke-runner, QEMU + serial
oracle) into the full dynamic-validation categories: boot/login/first-run,
network/storage, service activation, rollback/update, red-team safe probes, and
blue-team detect/contain/forensics smoke.

It:

1. validates a scenario set against tools/dynamic-validation/scenario-set.schema.json
   and checks host_command steps against policies/dynamic-validation-host-actions.yaml,
2. runs Agent-S against a disposable guest VM IF a usable runner is available
   (Linux + /dev/kvm + a guest backend + the gui-agents/Agent-S package),
   otherwise runs in --dry-run mode, printing the exact Agent-S actions and
   policy-gated host/guest commands that WOULD run,
3. records, per scenario, screenshots + the ordered Agent-S action trace +
   OCR/grounding metadata + a replay ref, and assembles them into an
   EvidenceBundle shaped to feed the ReleaseEvidenceBundle consumed by the
   Katello evidence gate.

The real Agent-S + guest-VM execution is HOST-GATED: Agent-S needs a Linux host
with hardware virtualization (/dev/kvm) to run a disposable guest, plus the
Agent-S package and a guest backend on PATH. It cannot run on macOS or in a
container without KVM. The validate + --dry-run paths run anywhere (and in CI),
so a scenario set can always be linted and a DRY_RUN evidence stub emitted even
without a runner.

Design notes (mirrors cosa/build.py and tools/sourceos-smoke-runner):
- local-first, stdlib-only for the dry-run/validate path (PyYAML only for .yaml),
- deterministic canonical JSON for hashing,
- fail-closed: a dry-run EvidenceBundle is intentionally incomplete
  (result=DRY_RUN, non-empty blockers) so the gate correctly DENIES promotion.

Usage:
  # Lint a scenario set (runs anywhere, including CI):
  python tools/dynamic-validation/run.py validate \
    --scenarios tools/dynamic-validation/scenario-set.example.yaml

  # Show what a run WOULD do + emit a DRY_RUN evidence stub (gate denies it):
  python tools/dynamic-validation/run.py run \
    --scenarios tools/dynamic-validation/scenario-set.example.yaml \
    --dry-run --emit-evidence .workstation/state/dynval/evidence-bundle.json

  # Real run (HOST-GATED: Linux + /dev/kvm + Agent-S + disposable guest):
  python tools/dynamic-validation/run.py run \
    --scenarios tools/dynamic-validation/scenario-set.example.yaml \
    --out-dir .workstation/state/dynval \
    --emit-evidence .workstation/state/dynval/evidence-bundle.json

Schema validation prefers the `jsonschema` package if installed; otherwise it
falls back to a built-in structural check covering the required fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
SCHEMA_PATH = HERE / "scenario-set.schema.json"
DEFAULT_POLICY_PATH = REPO_ROOT / "policies" / "dynamic-validation-host-actions.yaml"

# The six dynamic-validation categories the corpus defines.
_CATEGORIES = {
    "boot-login-firstrun",
    "network-storage",
    "service-activation",
    "rollback-update",
    "redteam-safe-probe",
    "blueteam-detect-contain-forensics",
}
_GUI_ACTIONS = {"gui_observe", "gui_click", "gui_type", "gui_key", "gui_wait_for", "gui_observe"}
_ALL_ACTIONS = _GUI_ACTIONS | {"guest_command", "host_command", "screenshot", "sleep"}


# --------------------------------------------------------------------------- #
# helpers (mirror the c14n/hash style in cosa/build.py)
# --------------------------------------------------------------------------- #
def _utc_now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _c14n_json(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _load_yaml_or_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise SystemExit(
                f"error: PyYAML required to read {path.name}; "
                "install pyyaml or provide a .json file"
            ) from exc
        return yaml.safe_load(text)
    return json.loads(text)


# --------------------------------------------------------------------------- #
# validation
# --------------------------------------------------------------------------- #
def _fallback_validate(doc: dict) -> list[str]:
    """Minimal structural check used when `jsonschema` is unavailable."""
    errs: list[str] = []
    if doc.get("apiVersion") != "socios.sourceos.ai/v0":
        errs.append("apiVersion must be 'socios.sourceos.ai/v0'")
    if doc.get("kind") != "DynamicValidationScenarioSet":
        errs.append("kind must be 'DynamicValidationScenarioSet'")
    meta = doc.get("metadata") or {}
    if not meta.get("name"):
        errs.append("metadata.name is required")
    spec = doc.get("spec") or {}
    if not (spec.get("targetImage") or {}).get("artifactRef"):
        errs.append("spec.targetImage.artifactRef is required")
    guest = spec.get("guest") or {}
    if guest.get("disposable") is not True:
        errs.append("spec.guest.disposable must be true (guest MUST be disposable)")
    scenarios = spec.get("scenarios") or []
    if not scenarios:
        errs.append("spec.scenarios must have at least one scenario")
    seen: set[str] = set()
    for i, sc in enumerate(scenarios):
        loc = f"spec.scenarios[{i}]"
        sid = sc.get("id")
        if not sid:
            errs.append(f"{loc}.id is required")
        elif sid in seen:
            errs.append(f"{loc}.id '{sid}' is duplicated")
        else:
            seen.add(sid)
        if sc.get("category") not in _CATEGORIES:
            errs.append(f"{loc}.category '{sc.get('category')}' not in {sorted(_CATEGORIES)}")
        for field in ("steps", "expected", "evidence_requirements"):
            if field not in sc:
                errs.append(f"{loc}.{field} is required")
        for j, step in enumerate(sc.get("steps") or []):
            if step.get("action") not in _ALL_ACTIONS:
                errs.append(f"{loc}.steps[{j}].action '{step.get('action')}' not in {sorted(_ALL_ACTIONS)}")
    return errs


def validate_doc(doc: dict) -> list[str]:
    """Return a list of validation errors ([] means valid)."""
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return _fallback_validate(doc)

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
        for e in sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    ]


# --------------------------------------------------------------------------- #
# host-action policy (the policy gate)
# --------------------------------------------------------------------------- #
def load_policy(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"error: host-action policy not found: {path}")
    return _load_yaml_or_json(path)


def policy_checks(doc: dict, policy: dict) -> list[str]:
    """Fail-closed checks of host_command steps + destructive-scenario safety."""
    errs: list[str] = []
    spec = policy.get("spec") or {}
    allow = set(spec.get("allow") or [])
    destructive_nets = set(spec.get("destructiveNetworkProfiles") or [])
    require_disposable = bool(spec.get("requireDisposableGuest", True))

    sset = doc.get("spec") or {}
    guest = sset.get("guest") or {}
    net = guest.get("networkProfile", "isolated")

    if require_disposable and guest.get("disposable") is not True:
        errs.append("policy: guest.disposable must be true (requireDisposableGuest)")

    for i, sc in enumerate(sset.get("scenarios") or []):
        loc = f"scenario[{sc.get('id', i)}]"
        is_destructive = sc.get("safetyClass") == "destructive"
        if is_destructive:
            if not guest.get("snapshotBeforeRun", True):
                errs.append(f"{loc}: destructive scenario requires guest.snapshotBeforeRun=true")
            if net not in destructive_nets:
                errs.append(
                    f"{loc}: destructive scenario requires networkProfile in "
                    f"{sorted(destructive_nets)} (have '{net}')"
                )
        for j, step in enumerate(sc.get("steps") or []):
            if step.get("action") != "host_command":
                continue
            target = (step.get("target") or "").strip()
            verb = target.split()[0] if target else ""
            if verb not in allow:
                errs.append(
                    f"{loc}.steps[{j}]: host_command verb '{verb}' is not policy-allowed "
                    f"(allow={sorted(allow)})"
                )
    return errs


# --------------------------------------------------------------------------- #
# runner detection (the host gate, mirrors cosa builder_available)
# --------------------------------------------------------------------------- #
def runner_available() -> tuple[bool, str]:
    """Detect whether a real Agent-S dynamic-validation run can happen here.

    A real run needs:
      - a Linux host,
      - /dev/kvm present (to run a disposable guest VM),
      - a guest backend on PATH (qemu-system-x86_64),
      - the Agent-S package importable (gui_agents).
    """
    if platform.system() != "Linux":
        return False, f"host is {platform.system()}, Agent-S guest-VM run requires Linux"
    if not Path("/dev/kvm").exists():
        return False, "/dev/kvm not present (a disposable guest VM requires hardware virtualization)"
    if shutil.which("qemu-system-x86_64") is None:
        return False, "qemu-system-x86_64 not found on PATH (no guest backend)"
    try:
        import importlib.util

        if importlib.util.find_spec("gui_agents") is None:
            return False, "Agent-S (gui_agents) package not importable"
    except Exception as exc:  # pragma: no cover - defensive
        return False, f"Agent-S import check failed: {exc}"
    return True, "linux host with /dev/kvm, qemu, and Agent-S available"


# --------------------------------------------------------------------------- #
# action / command planning
# --------------------------------------------------------------------------- #
def plan_scenario(sc: dict) -> list[dict]:
    """Lower a scenario's steps into the ordered plan the controller would run.

    gui_* steps become Agent-S computer-use instructions against the guest
    framebuffer; *_command steps become deterministic commands. This plan is
    what the dry-run prints and what the real path would execute.
    """
    plan: list[dict] = []
    for step in sc.get("steps") or []:
        action = step.get("action")
        entry: dict = {"action": action}
        if action in _GUI_ACTIONS:
            entry["agentS"] = {
                "instruction": _gui_instruction(step),
                "target": step.get("target"),
                "text": step.get("text"),
            }
        elif action in ("guest_command", "host_command"):
            entry["exec"] = {"where": "guest" if action == "guest_command" else "host",
                             "command": step.get("target")}
        elif action == "screenshot":
            entry["capture"] = "screenshot"
        elif action == "sleep":
            entry["sleepSeconds"] = step.get("timeoutSeconds", 1)
        entry["timeoutSeconds"] = step.get("timeoutSeconds", 60)
        if step.get("note"):
            entry["note"] = step["note"]
        plan.append(entry)
    return plan


def _gui_instruction(step: dict) -> str:
    action = step["action"]
    target = step.get("target", "")
    text = step.get("text", "")
    if action == "gui_observe":
        return "observe the screen and report visible UI"
    if action == "gui_click":
        return f"click {target}"
    if action == "gui_type":
        return f"type '{text}' into {target}"
    if action == "gui_key":
        return f"press the key chord '{text}'"
    if action == "gui_wait_for":
        return f"wait until: {target}"
    return action


# --------------------------------------------------------------------------- #
# evidence bundle (feeds a ReleaseEvidenceBundle)
# --------------------------------------------------------------------------- #
def build_evidence_bundle(doc: dict, scenarios_path: Path, plans: list[dict],
                          dry_run: bool, runner_reason: str, policy_path: Path) -> dict:
    """Assemble an EvidenceBundle shaped to seed a ReleaseEvidenceBundle.

    The Katello evidence gate
    (infra/ansible/roles/katello_lifecycle_sourceos/tasks/evidence_gate.yml)
    admits promotion only when the wrapping bundle reports result == PASS, a
    non-empty inputs_hash, and zero blockers. This bundle carries exactly those
    three fields plus, per scenario, the evidence the runner recorded
    (screenshots, action trace, OCR/grounding, replay ref).

    On dry-run, no guest exists, so every scenario is reported as not-executed
    and the bundle is intentionally incomplete (result=DRY_RUN, non-empty
    blockers) -- the fail-closed gate then correctly DENIES promotion.
    """
    spec = doc["spec"]
    set_digest = "sha256:" + _sha256_hex(_c14n_json(doc).encode("utf-8"))

    scenario_evidence: list[dict] = []
    for plan in plans:
        ev_req = plan["evidence_requirements"]
        if dry_run:
            recorded = {
                "screenshots": [],
                "actionTrace": [],   # would carry the executed Agent-S trace
                "ocrGrounding": [],
                "replayRef": None,
                "serialLog": None,
            }
            status = "not-executed"
        else:  # pragma: no cover - HOST-GATED real path
            recorded = plan.get("recorded", {})
            status = plan.get("status", "unknown")
        scenario_evidence.append({
            "id": plan["id"],
            "category": plan["category"],
            "covers": plan.get("covers", []),
            "safetyClass": plan.get("safetyClass", "safe"),
            "status": status,
            "plannedActions": plan["plan"],
            "evidenceRequirements": ev_req,
            "recorded": recorded,
        })

    n_total = len(scenario_evidence)
    n_pass = sum(1 for s in scenario_evidence if s["status"] == "pass")

    bundle = {
        "type": "DynamicValidationEvidenceBundle",
        "specVersion": "0.1.0",
        "createdAt": _utc_now_iso(),
        "scenarioSet": {
            "name": doc["metadata"]["name"],
            "ref": _rel_or_abs(scenarios_path),
            "digest": set_digest,
        },
        "targetImage": spec["targetImage"],
        "guest": spec["guest"],
        "hostActionPolicy": _rel_or_abs(policy_path),
        "runner": {
            "agent": "Agent-S (simular-ai gui_agents)",
            "available": not dry_run,
            "reason": runner_reason,
            "dryRun": dry_run,
        },
        "scenarios": scenario_evidence,
        "summary": {"total": n_total, "passed": n_pass, "failed": n_total - n_pass},
        # TODO(cosign): signing wired by a separate task.
        "signing": {"provider": "cosign", "signed": False},
        # --- fields the Katello evidence gate reads ---
        "inputs_hash": "",
        # result: PASS only when a real run executed every scenario and all passed.
        # Dry-run produces DRY_RUN so the fail-closed gate withholds promotion.
        "result": "DRY_RUN" if dry_run else ("PASS" if n_pass == n_total and n_total > 0 else "FAIL"),
        "blockers": (
            ["runner-unavailable-or-dry-run: " + runner_reason] if dry_run
            else [f"scenario-failed: {s['id']}" for s in scenario_evidence if s["status"] != "pass"]
        ),
    }
    hashable = dict(bundle)
    hashable["inputs_hash"] = ""
    bundle["inputs_hash"] = "sha256:" + _sha256_hex(_c14n_json(hashable).encode("utf-8"))
    return bundle


def _rel_or_abs(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


# --------------------------------------------------------------------------- #
# subcommands
# --------------------------------------------------------------------------- #
def _resolve(path_str: str) -> tuple[Path, dict]:
    p = Path(path_str).resolve()
    if not p.exists():
        raise SystemExit(f"error: scenario set not found: {p}")
    return p, _load_yaml_or_json(p)


def _all_errors(doc: dict, policy: dict) -> list[str]:
    return validate_doc(doc) + policy_checks(doc, policy)


def cmd_validate(args: argparse.Namespace) -> int:
    scen_path, doc = _resolve(args.scenarios)
    policy = load_policy(Path(args.policy))
    errs = _all_errors(doc, policy)
    if errs:
        print(f"INVALID: {scen_path}", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1
    n = len((doc.get("spec") or {}).get("scenarios") or [])
    print(f"OK: {scen_path} is a valid DynamicValidationScenarioSet ({n} scenarios)")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    scen_path, doc = _resolve(args.scenarios)
    policy_path = Path(args.policy)
    policy = load_policy(policy_path)

    errs = _all_errors(doc, policy)
    if errs:
        print(f"INVALID scenario set {scen_path}; refusing to run:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1

    ok, reason = runner_available()
    forced_dry = args.dry_run or not ok

    # Build a per-scenario plan once; it drives both the dry-run print and the
    # (HOST-GATED) real execution.
    plans: list[dict] = []
    for sc in doc["spec"]["scenarios"]:
        plans.append({
            "id": sc["id"],
            "category": sc["category"],
            "covers": sc.get("covers", []),
            "safetyClass": sc.get("safetyClass", "safe"),
            "evidence_requirements": sc["evidence_requirements"],
            "plan": plan_scenario(sc),
        })

    print(f"scenario set : {doc['metadata']['name']}")
    print(f"target image : {doc['spec']['targetImage']['artifactRef']} "
          f"({doc['spec']['targetImage']['format']})")
    print(f"runner       : {'available' if ok else 'UNAVAILABLE'} ({reason})")
    print(f"mode         : {'DRY-RUN' if forced_dry else 'REAL RUN'}")
    print(f"host policy  : {_rel_or_abs(policy_path)}")
    print(f"scenarios    : {len(plans)}")
    for p in plans:
        print(f"\n  [{p['category']}] {p['id']} (covers {','.join(p['covers']) or '-'}, {p['safetyClass']})")
        for step in p["plan"]:
            if "agentS" in step:
                print(f"    Agent-S> {step['agentS']['instruction']}")
            elif "exec" in step:
                print(f"    {step['exec']['where']}$ {step['exec']['command']}")
            elif step.get("capture"):
                print(f"    capture> {step['capture']}")
            elif "sleepSeconds" in step:
                print(f"    sleep {step['sleepSeconds']}s")

    rc = 0
    if forced_dry:
        if not ok and not args.dry_run:
            print(
                "\nNo usable runner on this host; ran in dry-run instead. The real "
                "Agent-S guest-VM run is HOST-GATED (Linux + /dev/kvm + qemu + Agent-S).",
                file=sys.stderr,
            )
    else:  # pragma: no cover - HOST-GATED real path
        raise SystemExit(
            "REAL RUN path is HOST-GATED and not implemented in this scaffold. "
            "Provision a Linux host with /dev/kvm + qemu + Agent-S and wire the "
            "controller execution loop here, then emit per-scenario `recorded` "
            "evidence. The validate + --dry-run paths are fully functional."
        )

    # Evidence is emitted in both modes; dry-run bundles are intentionally
    # incomplete (result=DRY_RUN, non-empty blockers) so the gate stays fail-closed.
    bundle = build_evidence_bundle(doc, scen_path, plans, forced_dry, reason, policy_path)
    if args.emit_evidence:
        out = Path(args.emit_evidence)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"\nevidence bundle -> {out}  (result={bundle['result']})")
    else:
        print(f"\nevidence bundle (stdout; pass --emit-evidence to write; result={bundle['result']}):")
        print(json.dumps(bundle, indent=2, sort_keys=True))

    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description="Agent-S dynamic-validation controller runner")
    sub = ap.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate", help="validate a scenario set + host-action policy")
    v.add_argument("--scenarios", required=True, help="path to scenario-set.yaml")
    v.add_argument("--policy", default=str(DEFAULT_POLICY_PATH), help="path to host-action policy")
    v.set_defaults(func=cmd_validate)

    r = sub.add_parser("run", help="run (or dry-run) a dynamic-validation scenario set")
    r.add_argument("--scenarios", required=True, help="path to scenario-set.yaml")
    r.add_argument("--policy", default=str(DEFAULT_POLICY_PATH), help="path to host-action policy")
    r.add_argument("--dry-run", action="store_true", help="force dry-run even if a runner is available")
    r.add_argument("--out-dir", default=None, help="directory for evidence artifacts (real run)")
    r.add_argument("--emit-evidence", default=None, help="write the EvidenceBundle to this path")
    r.set_defaults(func=cmd_run)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
