# External-Agent Availability Manifest Contract

This file defines the status-only manifest consumed by
`codex-external-agent-availability-preflight`. It is a contract/reference, not
a live project registry. Each project owns exactly one live copy at its
canonical project root: `external-agent-availability.md`. The canonical root
is normally the Git root; a user-authorized nested rules-bundle root is valid
only when its own role/rule files explicitly declare that scope authoritative.

The live copy must contain one fenced `json` block and no second data block:

```json
{
  "schema_version": 1,
  "project_key": "REPLACE_WITH_PROJECT_ROOT_BASENAME",
  "canonical_repository_root": "/REPLACE_WITH_ABSOLUTE_REPOSITORY_ROOT",
  "manifest_status": "initial_unverified",
  "last_verified_at": "1970-01-01T00:00:00+00:00",
  "expires_at": "1970-01-02T00:00:00+00:00",
  "agents": [
    {
      "seat": "REPLACE_WITH_ROLE_SEAT",
      "role_ref": "agent_roles.md#REPLACE_WITH_ROLE_ANCHOR",
      "provider": "REPLACE_WITH_PROVIDER",
      "transport": "REPLACE_WITH_TRANSPORT",
      "status": "unverified",
      "reason_code": "initial_verification_required",
      "reason": "No current transport observation has been recorded.",
      "fallback_ref": "agent_roles.md#REPLACE_WITH_FALLBACK_ANCHOR"
    }
  ]
}
```

Allowed status values are `available`, `not_available`, and `unverified`.
Allowed reason codes are `fresh_observation`, `initial_verification_required`,
`migration_requires_fresh_verification`, `transport_failure`,
`session_limit`, `not_declared`, `retired`, and `unavailable`.
`available` requires `manifest_status=current` and `reason_code=fresh_observation`;
`not_available` requires a bounded unavailable/retired/transport reason; and
`unverified` requires an initial or migration-verification reason.
An `initial_unverified` manifest may not contain an `available` row.
`unverified` and an expired timestamp are operationally unavailable. The
manifest contains no session identifier, token, fingerprint, command, URL
carrying a handle, transcript, or raw transport error. `role_ref` and
`fallback_ref` must resolve to headings in the same project's active
`agent_roles.md`; the role file remains the sole authority for contact,
reasoning, and fallback decisions.
