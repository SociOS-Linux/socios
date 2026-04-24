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
- emits an unsigned `KatelloLifecycleReceipt` scaffold to `socios_katello_lifecycle_receipt_path`
- does not yet emit signed lifecycle promotion receipts

## Follow-on

The next tranche should add:
- signed lifecycle promotion receipts
- activation-key repository override verification
- smoke tests against an ephemeral Katello fixture or mocked command runner
