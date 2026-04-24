# smart_proxy_sourceos role

This role scaffolds SourceOS Smart Proxy / site-edge provisioning and content distribution.

## Scope in this scaffold

The role models:
- a dedicated EL9 x86_64-class Smart Proxy host
- certificate tarball preflight for `foreman-proxy-certs-generate` output
- registration back to the parent Foreman/Katello management host
- registration verification using `hammer proxy list`
- TFTP / HTTP boot / template / content feature posture
- optional DHCP and DNS posture
- a SmartProxyReceipt artifact for auditability

## Current posture

- dry-run by default
- previews the intended `foreman-installer --scenario foreman-proxy-content` command
- requires a cert tarball before non-dry-run installation
- verifies Smart Proxy registration after non-dry-run installation when enabled
- emits a local unsigned `SmartProxyReceipt` scaffold with cert and registration state
- does not yet generate or retrieve the cert tarball automatically
- does not yet configure DHCP/DNS/subnets
- does not yet sync selected lifecycle content to the proxy

## Follow-on

The next tranche should add:
- certificate tarball generation / retrieval flow from the parent Foreman/Katello host
- subnet and domain binding
- lifecycle-content sync policies
- UEFI HTTP Boot artifact publication/verification
- signed SmartProxyReceipt emission
