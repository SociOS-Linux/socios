# Argo CD placement for the SourceOS build substrate

Argo CD is used here for the Kubernetes-native parts of the automation stack:
- Tekton controllers and tasks/pipelines
- object storage / registry / signing helpers
- observability components
- optional policy or secret-management sidecars

## Explicit boundary

Foreman/Katello management hosts are **not** treated as in-cluster app payloads in this scaffold.
They remain dedicated EL9 management hosts and are provisioned/bootstraped via infrastructure + Ansible.

## Desired posture

- Argo CD reconciles the K8s-native automation substrate
- Tekton executes build/customize/sign/publish pipelines
- Foreman/Katello manages content lifecycle and provisioning
- Smart Proxies serve site-local provisioning/content traffic

## Follow-on

A later tranche should add concrete `Application` or `ApplicationSet` manifests for:
- Tekton
- build-worker namespace resources
- artifact/object store
- signing/verification helpers
- observability stack
