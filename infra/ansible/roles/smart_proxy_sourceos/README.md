# smart_proxy_sourceos role

This role scaffolds SourceOS Smart Proxy / site-edge provisioning and content distribution.

## Scope in this scaffold

The role models:
- a dedicated EL9 x86_64-class Smart Proxy host
- certificate tarball preflight for `foreman-proxy-certs-generate` output
- registration back to the parent Foreman/Katello management host
- registration verification using `hammer proxy list`
- automatic registered proxy ID discovery from Hammer CSV output
- TFTP / HTTP boot / template / content feature posture
- optional DHCP and DNS posture
- domain creation/checks using Hammer CLI
- subnet creation/checks using Hammer CLI
- subnet bindings for domain, organization, location, and optional DHCP/DNS/TFTP proxy IDs
- fallback subnet proxy binding using the discovered Smart Proxy ID when explicit IDs are omitted
- a SmartProxyReceipt artifact for auditability

## Current posture

- dry-run by default
- previews the intended `foreman-installer --scenario foreman-proxy-content` command
- requires a cert tarball before non-dry-run installation
- verifies Smart Proxy registration after non-dry-run installation when enabled
- derives `socios_smart_proxy_discovered_proxy_id` from `hammer proxy list` when `socios_smart_proxy_auto_discover_proxy_ids=true`
- uses the discovered proxy ID as fallback for DHCP/DNS/TFTP subnet bindings when enabled and explicit IDs are not supplied
- can create missing domains and subnets when `socios_smart_proxy_network_bindings_enabled=true`
- emits a local unsigned `SmartProxyReceipt` scaffold with cert, registration, discovered proxy ID, domain, and subnet state
- does not yet generate or retrieve the cert tarball automatically
- does not yet verify Smart Proxy feature capabilities with `hammer proxy info`
- does not yet sync selected lifecycle content to the proxy

## Follow-on

The next tranche should add:
- certificate tarball generation / retrieval flow from the parent Foreman/Katello host
- proxy feature verification using `hammer proxy info`
- lifecycle-content sync policies
- UEFI HTTP Boot artifact publication/verification
- signed SmartProxyReceipt emission
