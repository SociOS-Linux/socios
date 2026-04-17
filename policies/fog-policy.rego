package fog

# Placeholder admissibility rules for fog artifact rollout.
# This policy is intentionally conservative until the signed catalog and receipt
# flow is fully wired.

default allow = false

allow if {
  input.kind == "FogCatalogEntry"
  input.spec.digest != ""
  startswith(input.spec.digest, "sha256:")
}
