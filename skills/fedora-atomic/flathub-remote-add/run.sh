#!/usr/bin/env bash
set -euo pipefail

# flathub-remote-add (idempotent)
# NOTE: execution should be gated by signed intent in higher layers.

flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak remotes --show-details
