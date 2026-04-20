# foreman_katello_install role

This role is the first bootstrap scaffold for a dedicated EL9 Foreman/Katello management host.

## Scope

This role currently does three things:
- asserts the expected management-host substrate (EL9 x86_64-class host)
- verifies `foreman-installer` is present
- runs `foreman-installer --scenario katello` when `socios_foreman_dry_run=false`

## Current posture

The role is intentionally conservative:
- `socios_foreman_dry_run` defaults to `true`
- package/repository bootstrap is not yet encoded here
- Smart Proxy, lifecycle-environment seeding, activation keys, and content views are follow-on work

## Variables

See `defaults/main.yml`.

## Follow-on

The next tranche should add:
- package repository bootstrap for the management host
- Smart Proxy roles
- post-install seeding for organizations, locations, lifecycle environments, and content views
- explicit FCOS custom-file / OSTree / container repository wiring
