# socios

Opt-in community automation commons for SourceOS: CI/CD, update automation, personalization workflows, catalogs, signatures.

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
  - model-governance authority
- **Semantic direction:** this repo should eventually publish an automation-focused repo descriptor that references the shared SourceOS/SociOS vocabulary from `SourceOS-Linux/sourceos-spec`.

## socios in the SourceOS ecosystem (opt-in)

**socios** is the *opt-in* community automated agentic build + commons layer for **SourceOS**:
- CI/CD automation for updates and releases
- policy-checked build pipelines
- catalogs/registries with digest pins and attestations
- optional AI automation for evaluation and personalization workflows

**SourceOS must operate without socios.** Enrollment is always explicit and gated (Proof-of-Life + signed intent).

See: `docs/OPT_IN.md`

## Personalization orchestration

Socios may orchestrate per-user model personalization only after the user has opted in and a governance contract exists in `SocioProphet/model-governance-ledger`.

Contracts and examples:

```text
schemas/personalization-orchestration.schema.json
examples/personalization-orchestration.local-llama32.json
tools/validate_personalization_orchestration.py
docs/PERSONALIZATION_ORCHESTRATION.md
```

Personalization orchestration is not generic training. It is user-scoped, consented, evidence-backed workflow coordination.

Required chain:

```text
signed user intent
  -> proof-of-life
  -> model-governance-ledger contract
  -> Socios personalization orchestration
  -> AgentPlane evidence
  -> ledger receipts
  -> model-router binding
```

Safety invariants:

- off by default;
- signed intent required;
- proof-of-life required;
- governance contract required;
- whole-home ingestion denied;
- raw app stores denied;
- browser profiles and token stores denied;
- promotion requires model-governance-ledger approval.
