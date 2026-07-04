# toolbox-bootstrap

Creates a toolbox container profile and installs baseline tooling inside it.

## Why

On Fedora Atomic, CLI/dev tooling belongs in Toolbox, not on the host.
This preserves rollback semantics and keeps the host OS immutable.

## Execute

Create + enter:

```bash
toolbox create --container dev || true
toolbox enter --container dev
```

Install baseline tools (inside the toolbox):

```bash
sudo dnf install -y git make gcc gcc-c++ python3 python3-pip ripgrep fd-find
```

## Verify

```bash
toolbox list
```

## Notes

- For per-project isolation, prefer venv/conda/pixi inside the toolbox.
- Keep toolbox images small and role-specific (dev vs ops vs forensic).
