package fog

# Hardened admissibility rules for fog artifact rollout.
# Placeholder or malformed digests must fail by default.

default allow = false

valid_sha256(d) if {
  regex.match("^sha256:[0-9a-f]{64}$", d)
}

not_placeholder(v) if {
  lv := lower(v)
  lv != "pending-pin"
  not contains(lv, "replace_me")
  not contains(lv, "placeholder")
}

allow if {
  input.kind == "FogCatalogEntry"
  valid_sha256(input.spec.digest)
  not_placeholder(input.spec.version)
  object.get(input.spec, "placeholder", false) == false
}
