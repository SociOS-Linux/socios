# katello_lifecycle_sourceos role

This role scaffolds SourceOS lifecycle management in Katello.

## Scope in this scaffold

The role models:
- lifecycle environments: dev → qa → prod
- SourceOS content views
- repository membership in content views
- content-view publication and promotion
- activation keys mapped to enrollment profiles / release rings

## Current posture

- dry-run by default
- uses real Hammer CLI command shapes
- does not yet perform idempotent existence checks
- does not yet inspect content-view version numbers after publication
- does not yet enable/disable repository overrides on activation keys

## Follow-on

The next tranche should add:
- idempotent checks with `hammer ... list --search`
- explicit content-view version resolution after publish
- activation-key content overrides
- lifecycle promotion receipts
- smoke tests against an ephemeral Katello fixture or mocked command runner
