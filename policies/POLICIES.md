# Policies

This directory contains typed `Policy` artifacts aligned with the SourceOS/SociOS Typed Contracts (spec v2.x).

Policy objects are URN-addressed (`urn:srcos:policy:<id>`) and contain:
- `scope`: subject selectors, object selectors, and purpose strings
- `rules`: ordered permit/deny rules with optional typed conditions (CEL/Rego/Cedar/JSONLogic)
- `obligations`: required actions pre/post/runtime

Current policies:
- `urn:srcos:policy:socios.optin.signed-intent` — require signed intent for opt-in automation
- `urn:srcos:policy:host.mutation.requires.review` — require review + rollback plan for host mutations

Notes:
- Our policy evaluation engine is not wired here yet; these artifacts establish the canonical topology and identifiers.
