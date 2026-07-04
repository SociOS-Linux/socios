# Fedora Atomic skills

These skills codify the Fedora Atomic (Silverblue/Kinoite/Sway Atomic) software lanes:

1) Flatpak (GUI apps)
2) Toolbox (CLI/dev tools)
3) rpm-ostree layering (host mutations)

Current skills:
- `flathub-remote-add` — add Flathub remote (idempotent)
- `toolbox-bootstrap` — create a toolbox profile and install baseline CLI tools
- `rpm-ostree-layering` — host package layering guardrails + rollback workflow

Note: these are capability descriptors + runbooks. Actual execution should be gated by policy and signed intent.
