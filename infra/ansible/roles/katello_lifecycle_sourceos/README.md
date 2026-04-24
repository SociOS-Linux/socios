# katello_lifecycle_sourceos role

This role scaffolds SourceOS lifecycle management in Katello.

## Scope in this scaffold

The role models:
- lifecycle environments: dev → qa → prod
- SourceOS content views
- repository membership in content views
- content-view publication and promotion
- content-view version lookup after publish
- activation keys mapped to enrollment profiles / release rings
- activation-key content overrides for selected SourceOS repositories

## Current posture

- dry-run by default
- uses real Hammer CLI command shapes
- uses guarded list/search checks before lifecycle/content-view/activation-key creates
- records content-view version lists after publish for later promotion receipts
- applies activation-key content overrides from role defaults
- does not yet resolve and persist a single canonical content-view version ID per publish
- does not yet emit signed lifecycle promotion receipts

## Follow-on

The next tranche should add:
- explicit extraction of latest content-view version IDs from `hammer content-view version list`
- persisted lifecycle promotion receipts
- activation-key repository override verification
- smoke tests against an ephemeral Katello fixture or mocked command runner
