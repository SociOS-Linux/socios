# smart_proxy_sourceos role

This role scaffolds SourceOS Smart Proxy / site-edge provisioning and content distribution.

## Scope in this scaffold

The role models:
- a dedicated EL9 x86_64-class Smart Proxy host
- certificate archive generation/retrieval scaffolding for parent Foreman output
- certificate archive preflight for non-dry-run installation
- registration back to the parent Foreman/Katello management host
- registration verification using `hammer proxy list`
- automatic registered proxy ID discovery from Hammer CSV output
- Smart Proxy feature verification using `hammer proxy info`
- TFTP / HTTP boot / template / content feature posture
- optional DHCP and DNS posture
- domain creation/checks using Hammer CLI
- subnet creation/checks using Hammer CLI
- subnet bindings for domain, organization, location, and optional DHCP/DNS/TFTP proxy IDs
- fallback subnet proxy binding using the discovered Smart Proxy ID when explicit IDs are omitted
- a SmartProxyReceipt artifact for auditability

## Current posture

- dry-run by default
- previews the intended parent-host certificate archive generation command when enabled
- can optionally generate the certificate archive on the parent Foreman host
- can optionally fetch the archive to the controller and copy it onto the Smart Proxy host
- previews the intended `foreman-installer --scenario foreman-proxy-content` command
- requires a certificate archive before non-dry-run installation
- verifies Smart Proxy registration after non-dry-run installation when enabled
- derives `socios_smart_proxy_discovered_proxy_id` from `hammer proxy list` when `socios_smart_proxy_auto_discover_proxy_ids=true`
- inspects Smart Proxy details with `hammer proxy info --id <discovered-id>` when `socios_smart_proxy_verify_features=true`
- asserts expected features from `socios_smart_proxy_expected_features` are present in proxy info output
- uses the discovered proxy ID as fallback for DHCP/DNS/TFTP subnet bindings when enabled and explicit IDs are not supplied
- can create missing domains and subnets when `socios_smart_proxy_network_bindings_enabled=true`
- emits a local unsigned `SmartProxyReceipt` scaffold with certificate archive, registration, discovered proxy ID, feature info, domain, and subnet state
- does not yet sync selected lifecycle content to the proxy

## Follow-on

The next tranche should add:
- lifecycle-content sync policies
- UEFI HTTP Boot artifact publication/verification
- signed SmartProxyReceipt emission
