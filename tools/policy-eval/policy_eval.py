#!/usr/bin/env python3
"""Minimal reference evaluator for SourceOS `Policy` artifacts.

Scope:
- Loads a SkillManifest.
- Resolves its `policyBindings` URNs to `policies/<id>.json`.
- Evaluates a single `operation` + `purpose` against each Policy.

This is intentionally dependency-free and implements a small CEL subset
sufficient for our current policies:
  - boolean literals: true/false
  - variables: context.<key>
  - operators: ==, !=, &&, ||, !
  - parentheses

This is NOT a full CEL engine.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class EvalResult:
    policy_id: str
    applicable: bool
    effect: str  # permit|deny|implicit_deny|not_applicable
    matched_rule_index: Optional[int]
    matched_rule: Optional[Dict[str, Any]]
    obligations: List[Dict[str, Any]]


# ---------------------------
# CEL-lite expression parsing
# ---------------------------

Token = Tuple[str, Any]  # (kind, value)


def _tokenize(expr: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    n = len(expr)

    def peek(k: int = 0) -> str:
        j = i + k
        return expr[j] if 0 <= j < n else ""

    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue

        # Two-char operators
        two = ch + peek(1)
        if two in ("&&", "||", "==", "!="):
            tokens.append(("op", two))
            i += 2
            continue

        # Single-char operators / parens
        if ch in ("!", "(", ")"):
            kind = "paren" if ch in ("(", ")") else "op"
            tokens.append((kind, ch))
            i += 1
            continue

        # Identifiers / literals (context.foo, true, false)
        if ch.isalpha() or ch in ("_",):
            j = i
            while j < n and (expr[j].isalnum() or expr[j] in ("_", ".")):
                j += 1
            word = expr[i:j]
            lw = word.lower()
            if lw == "true":
                tokens.append(("bool", True))
            elif lw == "false":
                tokens.append(("bool", False))
            else:
                tokens.append(("ident", word))
            i = j
            continue

        raise ValueError(f"Unexpected character at {i}: {ch!r}")

    return tokens


_PRECEDENCE = {
    "!": 3,
    "==": 2,
    "!=": 2,
    "&&": 1,
    "||": 0,
}

_ASSOC = {
    "!": "right",
    "==": "left",
    "!=": "left",
    "&&": "left",
    "||": "left",
}


def _to_postfix(tokens: List[Token]) -> List[Token]:
    out: List[Token] = []
    ops: List[Token] = []

    for kind, val in tokens:
        if kind in ("bool", "ident"):
            out.append((kind, val))
            continue

        if kind == "op":
            op = val
            while ops:
                top_kind, top_val = ops[-1]
                if top_kind != "op":
                    break
                top_op = top_val
                if (
                    _PRECEDENCE.get(top_op, -1) > _PRECEDENCE.get(op, -1)
                    or (
                        _PRECEDENCE.get(top_op, -1) == _PRECEDENCE.get(op, -1)
                        and _ASSOC.get(op) == "left"
                    )
                ):
                    out.append(ops.pop())
                else:
                    break
            ops.append(("op", op))
            continue

        if kind == "paren" and val == "(":
            ops.append(("paren", "("))
            continue

        if kind == "paren" and val == ")":
            while ops and ops[-1] != ("paren", "("):
                out.append(ops.pop())
            if not ops:
                raise ValueError("Mismatched parentheses")
            ops.pop()  # pop '('
            continue

        raise ValueError(f"Unhandled token: {(kind, val)}")

    while ops:
        tok = ops.pop()
        if tok[0] == "paren":
            raise ValueError("Mismatched parentheses")
        out.append(tok)

    return out


def _eval_postfix(postfix: List[Token], context: Dict[str, Any]) -> bool:
    stack: List[Any] = []

    def resolve_ident(name: str) -> Any:
        if name.startswith("context."):
            key = name[len("context.") :]
            return context.get(key)
        # Unknown identifiers are treated as None
        return None

    for kind, val in postfix:
        if kind == "bool":
            stack.append(bool(val))
            continue
        if kind == "ident":
            stack.append(resolve_ident(val))
            continue
        if kind == "op":
            op = val
            if op == "!":
                if not stack:
                    raise ValueError("Missing operand for '!'")
                a = stack.pop()
                stack.append(not bool(a))
                continue

            if op in ("==", "!=", "&&", "||"):
                if len(stack) < 2:
                    raise ValueError(f"Missing operands for {op!r}")
                b = stack.pop()
                a = stack.pop()

                if op == "==":
                    stack.append(a == b)
                elif op == "!=":
                    stack.append(a != b)
                elif op == "&&":
                    stack.append(bool(a) and bool(b))
                elif op == "||":
                    stack.append(bool(a) or bool(b))
                continue

            raise ValueError(f"Unsupported operator: {op!r}")

        raise ValueError(f"Unhandled token kind: {kind!r}")

    if len(stack) != 1:
        raise ValueError("Expression did not reduce to a single value")

    return bool(stack[0])


def eval_cel_lite(expr: str, context: Dict[str, Any]) -> bool:
    tokens = _tokenize(expr)
    postfix = _to_postfix(tokens)
    return _eval_postfix(postfix, context)


# -----------------
# Policy evaluation
# -----------------


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _policy_path_from_urn(repo_root: Path, policy_urn: str) -> Path:
    prefix = "urn:srcos:policy:"
    if not policy_urn.startswith(prefix):
        raise ValueError(f"Not a policy URN: {policy_urn}")
    local_id = policy_urn[len(prefix) :]
    return repo_root / "policies" / f"{local_id}.json"


def _eval_condition(cond: Dict[str, Any], context: Dict[str, Any]) -> bool:
    lang = cond.get("language")
    expr = cond.get("expr")
    if lang == "cel":
        # Convention: { "cel": "context.foo == true" }
        if isinstance(expr, dict) and "cel" in expr and isinstance(expr["cel"], str):
            return eval_cel_lite(expr["cel"], context)
        raise ValueError("CEL condition requires expr.cel string")

    if lang == "jsonlogic":
        raise NotImplementedError("jsonlogic not implemented in this reference evaluator")
    if lang == "rego":
        raise NotImplementedError("rego not implemented in this reference evaluator")
    if lang == "cedar":
        raise NotImplementedError("cedar not implemented in this reference evaluator")

    raise ValueError(f"Unknown condition language: {lang!r}")


def evaluate_policy(
    policy: Dict[str, Any],
    operation: str,
    purpose: str,
    context: Dict[str, Any],
) -> EvalResult:
    policy_id = policy.get("id", "<missing-id>")

    purposes = (policy.get("scope", {}) or {}).get("purposes", [])
    if purpose not in purposes:
        return EvalResult(
            policy_id=policy_id,
            applicable=False,
            effect="not_applicable",
            matched_rule_index=None,
            matched_rule=None,
            obligations=[],
        )

    rules = policy.get("rules", []) or []
    for idx, rule in enumerate(rules):
        ops = rule.get("operations", []) or []
        if operation not in ops:
            continue
        cond = rule.get("condition")
        if cond is None:
            eff = rule.get("effect", "deny")
            return EvalResult(
                policy_id=policy_id,
                applicable=True,
                effect=eff,
                matched_rule_index=idx,
                matched_rule=rule,
                obligations=(policy.get("obligations", []) or []) if eff == "permit" else [],
            )
        if _eval_condition(cond, context):
            eff = rule.get("effect", "deny")
            return EvalResult(
                policy_id=policy_id,
                applicable=True,
                effect=eff,
                matched_rule_index=idx,
                matched_rule=rule,
                obligations=(policy.get("obligations", []) or []) if eff == "permit" else [],
            )

    # No matching rule => implicit deny
    return EvalResult(
        policy_id=policy_id,
        applicable=True,
        effect="implicit_deny",
        matched_rule_index=None,
        matched_rule=None,
        obligations=[],
    )


def evaluate_skill(
    repo_root: Path,
    skill_manifest_path: Path,
    operation: str,
    purpose: str,
    context: Dict[str, Any],
) -> Dict[str, Any]:
    skill = _load_json(skill_manifest_path)

    bindings = skill.get("policyBindings", []) or []
    if not isinstance(bindings, list):
        raise ValueError("SkillManifest.policyBindings must be an array")

    results: List[EvalResult] = []
    for urn in bindings:
        p = _policy_path_from_urn(repo_root, urn)
        if not p.exists():
            results.append(
                EvalResult(
                    policy_id=urn,
                    applicable=True,
                    effect="implicit_deny",
                    matched_rule_index=None,
                    matched_rule={"error": f"policy file not found: {p.as_posix()}"},
                    obligations=[],
                )
            )
            continue
        policy = _load_json(p)
        results.append(evaluate_policy(policy, operation=operation, purpose=purpose, context=context))

    # Deny precedence.
    denied = [r for r in results if r.effect in ("deny", "implicit_deny")]
    permitted = [r for r in results if r.effect == "permit"]

    overall = "deny"
    if denied:
        overall = "deny"
    elif permitted:
        overall = "permit"

    obligations: List[Dict[str, Any]] = []
    if overall == "permit":
        for r in permitted:
            obligations.extend(r.obligations)

    return {
        "skill": {
            "id": skill.get("id"),
            "name": skill.get("name"),
            "version": skill.get("version"),
            "entryDoc": skill.get("entryDoc"),
        },
        "decision": overall,
        "operation": operation,
        "purpose": purpose,
        "context": context,
        "policies": [
            {
                "policyId": r.policy_id,
                "applicable": r.applicable,
                "effect": r.effect,
                "matchedRuleIndex": r.matched_rule_index,
                "matchedRule": r.matched_rule,
                "obligations": r.obligations,
            }
            for r in results
        ],
        "obligations": obligations,
    }


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(prog="policy_eval")
    ap.add_argument("--repo-root", default=".", help="Path to repo root (default: .)")
    ap.add_argument("--skill", required=True, help="Path to SkillManifest.json")
    ap.add_argument("--operation", required=True, help="Operation to evaluate (read|write|export|transform|share)")
    ap.add_argument("--purpose", required=True, help="Purpose string to evaluate (e.g. os.bootstrap)")

    ctx = ap.add_mutually_exclusive_group(required=True)
    ctx.add_argument("--context-json", help="Inline JSON object for context")
    ctx.add_argument("--context-file", help="Path to JSON file for context")

    ap.add_argument("--pretty", action="store_true", help="Pretty-print output JSON")

    args = ap.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    skill_path = Path(args.skill).resolve()

    if args.context_json:
        context = json.loads(args.context_json)
    else:
        context = _load_json(Path(args.context_file).resolve())

    if not isinstance(context, dict):
        raise ValueError("Context must be a JSON object")

    out = evaluate_skill(
        repo_root=repo_root,
        skill_manifest_path=skill_path,
        operation=args.operation,
        purpose=args.purpose,
        context=context,
    )

    if args.pretty:
        print(json.dumps(out, indent=2, sort_keys=False))
    else:
        print(json.dumps(out))

    return 0 if out.get("decision") == "permit" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
