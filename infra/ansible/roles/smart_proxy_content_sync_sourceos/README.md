# smart_proxy_content_sync_sourceos role

This role scaffolds SourceOS site-edge content placement policy.

## Scope in this scaffold

The role models:
- site-edge proxy lookup by name
- lifecycle environment lookup
- content view lookup
- intended lifecycle/content-view placement policy
- a placement-policy receipt for auditability

## Current posture

- dry-run by default
- records intended lifecycle/content-view placement only
- resolves the proxy ID when available
- records lifecycle and content view lookup output
- emits a local unsigned receipt scaffold

## Follow-on

The next tranche should add:
- validated site-edge content placement execution
- placement verification
- UEFI HTTP Boot artifact publication and verification
- signed receipt emission
