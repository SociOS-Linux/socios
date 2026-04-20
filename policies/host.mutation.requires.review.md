# urn:srcos:policy:host.mutation.requires.review

Intent: ensure host mutations (rpm-ostree layering, kernel-adjacent changes) are rare and reviewed.

Rule:
- Host mutations default to review-only.
- Require a recorded rationale and a rollback plan.
- Prefer Flatpak/Toolbox whenever feasible.
- If a package is layered, record the deployment change and verify rollback works.

This is a placeholder policy note until the canonical `Policy` schema is wired to an evaluator.
