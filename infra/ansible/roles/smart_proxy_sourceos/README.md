# smart_proxy_sourceos role

This role scaffolds SourceOS Smart Proxy / site-edge provisioning and content distribution.

## Scope in this scaffold

The role models:
- a dedicated EL9 x86_64-class Smart Proxy host
- registration back to the parent Foreman/Katello management host
- TFTP / HTTP boot / template / content feature posture
- optional DHCP and DNS posture
- a SmartProxyReceipt artifact for auditability

## Current posture

- dry-run by default
- previews the intended `foreman-installer --scenario foreman-proxy-content` command
- emits a local unsigned `SmartProxyReceipt` scaffold
- does not yet manage certificates or Smart Proxy registration tokens
- does not yet configure DHCP/DNS/subnets
- does not yet sync selected lifecycle content to the proxy

## Follow-on

The next tranche should add:
- certificate tarball generation / retrieval flow
- explicit Smart Proxy registration and verification
- subnet and domain binding
- lifecycle-content sync policies
- UEFI HTTP Boot artifact publication/verification
- signed SmartProxyReceipt emission
