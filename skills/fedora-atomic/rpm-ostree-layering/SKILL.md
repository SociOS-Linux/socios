# rpm-ostree-layering

Guardrails for host package layering on Fedora Atomic.

## Why

Layering modifies the host deployment. It is valid for kernel-adjacent or host service requirements, but it should be rare.

## Workflow (review first)

1) Confirm the package truly must be on the host (cannot be Flatpak/Toolbox).
2) Record intent: what package, why, rollback plan.
3) Layer package (creates new deployment):

```bash
rpm-ostree install <package>
rpm-ostree status
```

4) Reboot into new deployment:

```bash
systemctl reboot
```

## Rollback

If the new deployment is bad:

```bash
rpm-ostree rollback
systemctl reboot
```

## Notes

- This skill is **reviewMode=true** by default (no automatic mutation). A higher-layer policy must explicitly allow execution.
