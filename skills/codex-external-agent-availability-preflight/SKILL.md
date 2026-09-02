---
name: codex-external-agent-availability-preflight
description: Check the current project's canonical external-agent-availability.md before every external feedback, consultation, or audit dispatch. Use for OpenCode, Grok, Claude Code, or another project-authorized external transport.
---

# Codex External-Agent Availability Preflight

## Purpose

This is the single status gate for external-agent dispatch. It does not create a
roster, authorize a provider, select a fallback, or turn reachability into a
review verdict. The active project's `agent_roles.md` remains the authority for
seat identity, transport, reasoning, fallback order, and whether the seat is
required.

Before every external hello, consultation, feedback request, or audit call,
apply this skill and re-read the live project role file and the one canonical
manifest at:

`<current-project-root>/external-agent-availability.md`

The path is project-local. Never use a sibling project's manifest, a hub copy,
memory, a handoff, an old registry, or a historical report as a substitute.
The canonical project root is normally the current Git root. A user-authorized
nested rules-bundle may explicitly define a different canonical root only when
that nested directory contains its own `agent_roles.md`, its own manifest, and
an active rule stating that the nested scope is authoritative. The containing
Git repository remains storage only and must not silently substitute its root
manifest.

## Canonical manifest contract

The live Markdown file contains exactly one fenced `json` block whose value is
a single JSON object. The object must satisfy the schema in
`references/external-agent-availability.md`:

- `schema_version` is `1`.
- `project_key` and `canonical_repository_root` identify the current project
  exactly; the resolved root must equal the current Git root unless the active
  project rule explicitly declares the user-authorized nested rules-bundle
  model described above.
- `manifest_status` is `current` or `initial_unverified`.
- `last_verified_at` and `expires_at` are timezone-aware ISO-8601 timestamps;
  `expires_at` must be later than `last_verified_at` and later than the current
  clock for a usable manifest.
- `agents` is a list of unique seat records. Each record has `seat`,
  `role_ref`, `provider`, `transport`, `status`, `reason_code`, `reason`, and
  `fallback_ref`.
- `status` is exactly one of `available`, `not_available`, or `unverified`.
- `reason_code` is one of `fresh_observation`,
  `initial_verification_required`, `migration_requires_fresh_verification`,
  `transport_failure`, `session_limit`, `not_declared`, `retired`, or
  `unavailable`. `available` requires `manifest_status=current` with
  `fresh_observation`; `not_available` requires an unavailable/retired/transport
  reason; and `unverified` requires an initial or migration-verification reason.
  An `initial_unverified` manifest cannot contain an `available` row.
- `role_ref` and `fallback_ref` are same-project relative references that resolve
  to headings in the active role declaration. They never contain a session
  handle.

The parser must reject duplicate JSON keys, duplicate seats, unknown status
values, missing required fields, a mismatched root, a missing or expired
timestamp, an `unverified` row used as available, malformed JSON, extra JSON
blocks, and any value that looks like a session identifier, token, URL carrying
one, CLI command, transcript, or raw transport error. Failure is operationally
`unavailable`.

`available` means only that the seat is eligible for one bounded transport
attempt at the recorded time. It does not mean authorized contact, reachable,
reviewed, agreed, converged, or current after a subsequent failure.

## Per-dispatch procedure

1. Resolve the current Git root and, only where the active project rule
   explicitly permits it, the nearest authorized nested project root without
   following a different project's path.
2. Read the active `AGENTS.md` and `agent_roles.md`; resolve the exact requested
   seat and its permitted provider, transport, reasoning, and fallback.
3. Read and strictly parse the current project's manifest. Require a matching
   `available` row, valid timestamps, a non-expired manifest, and the exact
   provider/transport declared by the role. A missing, stale, malformed,
   ambiguous, `not_available`, or `unverified` row blocks the call.
4. Obtain the current session handle only through one of these bounded sources:
   Ali's current-turn authorization; an approved process-local runtime
   handoff; or a document Ali explicitly provides or identifies in the current
   instruction for this exact dispatch. A provided document is provenance
   evidence only, not a roster, handle registry, authority override, or review
   verdict. Verify that it is the intended current document and is scoped to
   the requested project, seat, provider, and transport. Do not discover it
   through a directory scan, memory, log, ordinary project file, old handoff,
   or historical registry. After that check, keep the handle in memory for the
   single call; do not place it in a file, environment snapshot, shell history,
   prompt copy, log, canvas, memory, hook output, or ordinary command
   transcript. Never rediscover it from an old registry.
5. Immediately before the hello call, re-read and re-parse the role file and
   manifest. Run the transport skill's documented hello-first handshake.
6. If hello succeeds, immediately before the substantive call re-read and
   re-parse both files again. Send only the Ali-approved message through the
   transport skill with the role's required reasoning and preserved settings.
7. Record only the provider/seat label, status, bounded reason code, and
   candidate scope. A transport failure, timeout, session limit, stale row, or
   missing report is unavailable/incomplete, never agreement.

The manifest is a status input, not a handle registry. Updating it requires a
fresh live observation, current Asia/Karachi time from the time MCP, an
assertion against the current bytes, and a bounded status/reason update with no
handle material. Do not silently mark a seat available because an old registry
said so.

## Hook boundary

A local `PreToolUse` Bash hook may enforce the project-root, JSON, expiry, and
provider-level status checks for obvious external CLI invocations. It is
defense-in-depth only: it cannot identify a same-provider seat without a
non-secret seat reference, cover every tool or transport, prove that this
preflight ran, govern later stdin to an existing process, or remove a handle
already present in a task. The skill and role rules remain mandatory even when a
hook allows a command. It also cannot authenticate whether an external session
handle was supplied directly by Ali or came from an Ali-provided document; that
provenance decision belongs to this skill and the active role rules. A document
path or filename appearing in a shell command is not proof of Ali's provision.

## Completion gate

Do not report an external audit or feedback call as handled until the exact
current candidate, the role/manifest preflight, the hello/substantive transport
results, and the provider/seat identity are separately verified. Missing or
stale availability is an incomplete review and activates only the fallback
explicitly declared by the current role file.
