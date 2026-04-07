# socios

Opt-in community automation commons for SourceOS: CI/CD, update automation, training workflows, catalogs, signatures.

**OFF by default.** Enrollment requires local Proof-of-Life + signed intent.

---

## Topology position

- **Role:** opt-in community automation commons for SourceOS.
- **Connects to:**
  - `SociOS-Linux/SourceOS` — immutable substrate that must remain able to operate without socios
  - `SociOS-Linux/agentos-spine` — Linux-side integration/workspace spine that can route or reference socios as an optional layer
  - `SourceOS-Linux/sourceos-spec` — canonical typed contracts, JSON-LD contexts, and shared vocabulary
  - `SociOS-Linux/workstation-contracts` — workstation/CI contract and conformance lane
  - `SocioProphet/sociosphere` — platform workspace controller that may coordinate broader multi-repo automation lanes
  - `SociOS-Linux/socioslinux-web` — public docs surface that explains the commons layer downstream
- **Not this repo:**
  - base OS substrate
  - mandatory dependency of SourceOS
  - public docs site
  - canonical typed-contract registry
- **Semantic direction:** this repo should eventually publish an automation-focused repo descriptor that references the shared SourceOS/SociOS vocabulary from `sourceos-spec`.

## socios in the SourceOS ecosystem (opt-in)

**socios** is the *opt-in* community automated agentic build + commons layer for **SourceOS**:
- CI/CD automation for updates and releases
- policy-checked build pipelines
- catalogs/registries with digest pins and attestations
- optional AI automation for training/testing workflows

**SourceOS must operate without socios.** Enrollment is always explicit and gated (Proof-of-Life + signed intent).

See: `docs/OPT_IN.md`
