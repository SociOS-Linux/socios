package fog

# Hardened admissibility rules for fog artifact rollout.
# Placeholder or malformed digests must fail by default.

default allow = false

valid_sha256(d) {
  regex.match("^sha256:[0-9a-f]{64}$", d)
}

not_placeholder(v) {
  not contains(lower(v), "replace_me")
  not contains(lower(v), "placeholder")
}

allow if {
  input.kind == "FogCatalogEntry"
  valid_sha256(input.spec.digest)
  not_placeholder(input.spec.version)
}
