# katello_seed_sourceos role

This role seeds the first SourceOS products and repositories into Katello.

## Scope in this scaffold

The role currently models two product families:
- file-backed SourceOS artifact repositories
- OSTree-backed SourceOS repositories

The file product is intended for artifacts such as:
- customized live ISOs
- disk images
- config bundles

The OSTree product is intended for OSTree-style publication where that lane is active.

## Current posture

- dry-run by default
- uses `hammer product create` and `hammer repository create`
- does not yet handle idempotent existence checks
- does not yet create content views, lifecycle environments, or activation keys
- does not yet upload content automatically

## Follow-on

The next tranche should add:
- product/repository existence checks
- file upload / sync flows
- content view publication
- lifecycle environment promotion
- activation-key and enrollment-profile bindings
