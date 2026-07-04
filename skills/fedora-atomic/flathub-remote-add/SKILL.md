# flathub-remote-add

Adds Flathub as a Flatpak remote.

## Preconditions

- Running on Fedora Atomic (Silverblue/Kinoite/Sway Atomic) or Fedora Workstation.
- `flatpak` is installed (it is by default on Atomic desktops).
- Enrollment: this operation should only be executed when the user has explicitly opted in and signed intent.

## Execute (idempotent)

```bash
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak remotes --show-details
```

## Verify

- Confirm the `flathub` remote exists.
- Confirm the URL points to `dl.flathub.org`.

## Notes

This skill does not install any applications; it only adds the remote.
