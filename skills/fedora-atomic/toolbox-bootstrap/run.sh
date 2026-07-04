#!/usr/bin/env bash
set -euo pipefail

# toolbox-bootstrap
# NOTE: execution should be gated by signed intent in higher layers.

container_name="dev"

toolbox create --container "${container_name}" || true
# Entering a toolbox is interactive; we provide a non-interactive install path below.

# Install baseline packages inside toolbox via `toolbox run` to avoid interactive shell.
toolbox run --container "${container_name}" sudo dnf install -y git make gcc gcc-c++ python3 python3-pip ripgrep fd-find

toolbox list
