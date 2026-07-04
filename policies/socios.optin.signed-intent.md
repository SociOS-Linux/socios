# urn:srcos:policy:socios.optin.signed-intent

Intent: prevent silent mutation.

Rule:
- No automation runs by default.
- Any mutation must be preceded by local Proof-of-Life and a user-signed intent record.
- Artifacts consumed by automation must be digest-pinned and verifiable.

This is a placeholder policy note until the canonical `Policy` schema is wired to an evaluator.
