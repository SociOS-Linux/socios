# katello_lifecycle_sourceos role

This role scaffolds SourceOS lifecycle management in Katello.

## Scope in this scaffold

The role models:
- lifecycle environments: dev → qa → prod
- SourceOS content views
- repository membership in content views
- content-view publication and promotion
- content-view version lookup after publish
- canonical latest content-view version extraction into `latestContentViewVersions`
- activation keys mapped to enrollment profiles / release rings
- activation-key content overrides for selected SourceOS repositories
- lifecycle receipt emission for publish/promote/activation-key override outputs

## Current posture

- dry-run by default
- uses real Hammer CLI command shapes
- uses guarded list/search checks before lifecycle/content-view/activation-key creates
- records content-view version lists after publish
- extracts latest content-view version id/version pairs from Hammer CSV output
- applies activation-key content overrides from role defaults
- emits a `KatelloLifecycleReceipt` scaffold to `socios_katello_lifecycle_receipt_path`
- cosign-signs the receipt when a signing identity is configured (else fail-closed unsigned)

## Lifecycle receipt signing (cosign)

When `socios_katello_lifecycle_receipt_signing_enabled: true`, the role runs
`tasks/sign_lifecycle_receipt.yml`, which `cosign sign-blob`s the emitted
`KatelloLifecycleReceipt` JSON and writes the detached `.sig` plus a
`KatelloLifecycleReceiptSignature` metadata document.

Signing identity is resolved in this order (shared SourceOS cosign posture):

1. **keyless OIDC** — when the identity mode is `keyless` and an OIDC token is
   present in the environment;
2. **configured key** — a cosign key path / `env://VAR` / KMS ref;
3. **fail-closed** — if neither is usable (or `cosign` is not installed), the
   receipt is explicitly marked `status: unsigned` and is **never** labelled
   signed.

### Identity configuration (env vars / role vars)

| Purpose | Role var | Env fallback |
| --- | --- | --- |
| Identity mode (`keyless` enables OIDC) | `socios_katello_lifecycle_receipt_signing_identity_mode` | `SOCIOS_KATELLO_COSIGN_IDENTITY` |
| Configured signing key (path / `env://` / KMS) | `socios_katello_lifecycle_receipt_signing_key` | `SOCIOS_KATELLO_COSIGN_KEY` |
| Keyless OIDC token (any one) | — | `SIGSTORE_ID_TOKEN`, `ACTIONS_ID_TOKEN_REQUEST_TOKEN`, or `SOCIOS_KATELLO_COSIGN_OIDC_TOKEN` |
| Keyless verify cert identity | `socios_katello_lifecycle_receipt_verify_certificate_identity` | — |
| Keyless verify OIDC issuer | `socios_katello_lifecycle_receipt_verify_oidc_issuer` | — |

`tasks/verify_lifecycle_receipt.yml` mirrors signing with `cosign verify-blob`
(key or `--certificate-identity`/`--certificate-oidc-issuer`), and treats a
missing cosign binary, missing signature, or unconfigured verify identity as
**not verified** (fail-closed).

## Follow-on

The next tranche should add:
- activation-key repository override verification
- smoke tests against an ephemeral Katello fixture or mocked command runner
