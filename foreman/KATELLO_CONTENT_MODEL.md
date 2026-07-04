# SourceOS content model in Foreman/Katello

This note maps the SourceOS release/build object family onto Foreman/Katello concepts.

## Mapping

### Product
A Product represents a major SourceOS family, for example:
- SourceOS Workstation
- SourceOS Recovery
- SourceOS Builder

### Repository
Repositories represent artifact surfaces or content types, for example:
- custom file repo for ISO and disk images
- custom file repo for config bundles or branding packs
- OSTree repo for tree content
- container repo for bootc/image-mode outputs

### Content View
A Content View freezes a coherent release snapshot for one family/channel pair.

### Lifecycle Environment
Lifecycle environments represent release rings such as:
- dev
- qa
- prod
- customer or site-specific rings

### Activation Key / Enrollment Profile
Activation keys should map to enrollment and post-install consumption profiles.

## Why this matters

The same flavor can produce many task/customer/site variants without becoming an unmanaged snowflake set:
- flavor remains stable
- overlays vary
- build requests compose them
- Katello versions and promotes the outputs

## Follow-on

The next tranche should make this mapping executable in automation by adding:
- post-install seeding for products/repositories/content views/lifecycle envs
- publish tasks that upload FCOS/SourceOS outputs into the correct repo class
- activation-key generation or binding from EnrollmentProfile inputs
