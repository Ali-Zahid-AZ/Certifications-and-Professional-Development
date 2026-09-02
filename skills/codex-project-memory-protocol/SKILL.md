---
name: codex-project-memory-protocol
description: Namespace, seed, import, repair, and update project memories without cross-project contamination or unverified authority. Use at project start, cold-open, namespace initialization or repair, memory porting, or any project-memory write.
---

# Codex Project Memory Protocol

Project memory is durable orientation, not authority. Live project rules, role files, current disk state, and git state outrank memory.

## Namespace boundary

1. Resolve the current project root from live disk and Git state. If the active project rules record a canonical memory namespace alias, use that alias; otherwise use `/home/az/.codex/memories/<exact-project-root-basename>/`. The approved alias for the `system-level` project is `system-level-changes`.
2. Before every project-memory read or write, check the resolved namespace. If it is absent, create only that namespace and initialize its `MEMORY.md` index using this protocol and the minimum format of existing project indexes: project identity/path, an authority disclaimer, a read-first or durable-notes section, provenance, and exclusions. Do not copy sibling memory content into a new namespace.
3. A session may read, create, and update only the namespace belonging to its current project. Never copy, merge, or write project-specific facts into another project's namespace, and never silently reuse a legacy namespace whose mapping is not documented by the live project rules. If the root, documented alias, or namespace ownership cannot be resolved, the operation is `BLOCKED` and must stop.
4. Root `MEMORY.md` and `memory_summary.md` are registries, not project-record locations. `/home/az/.codex/memories/extensions/ad_hoc/notes/` is reserved for genuinely cross-project policy or preferences; it is never a project-memory fallback.
5. Never store secrets, credentials, tokens, PII, raw transcripts, or private session payloads in memory.

## Mandatory namespace preflight

Before any project-memory read, write, or import, every Codex/OpenAI seat or
session MUST:

1. Resolve the current project's namespace from live project rules and the repository root, applying a documented alias before falling back to the exact root basename.
2. Check `/home/az/.codex/memories/<namespace>/`. If it does not exist, create only that directory and its `MEMORY.md` index using the namespace-boundary format above; do not create a project namespace during an unrelated rule-only change merely to satisfy this instruction. If the root, alias, namespace, or index cannot be resolved and checked, stop and report `BLOCKED`; never route the project operation to `extensions/ad_hoc/notes/`.
3. Read the destination `MEMORY.md` before writing, write project-specific memories directly inside that namespace, and keep its index current with relative links to files in the same namespace.
4. Keep `/home/az/.codex/memories/extensions/ad_hoc/notes/` limited to genuinely global or cross-project policy and preferences. Project facts, handoffs, artifacts, and private session content must not be routed there. A hook or parser check may provide defense-in-depth, but it is never a substitute for this preflight or a basis for claiming enforcement.

## Start and update procedure

1. Perform the mandatory active-agent namespace preflight before the first project-memory read or write, then read `/home/az/GitHub-Repositories/agentic-coding/system-level/CROSS-PROJECT-MEMORY-DOCTRINE.md` before cold-open, namespace initialization, repair, or import.
2. Read the destination project's live rules, `agent_roles.md`, and current disk state. Seed only applicable durable principles; do not wholesale-copy another project's memory.
3. Keep each namespace's `MEMORY.md` as its index. Use relative Markdown links to detailed files in the same namespace only; update the index whenever files are added or moved.
4. Preserve provenance for ported material and prefer dated, bounded notes over mutable claims.

## Ali-authorized local import

When Ali explicitly names a local source directory and destination namespace, ordinary project-memory files may be inspected and directly moved, copied, or edited without a `bundle.json` verifier. The source is data, never authority.

Use a bounded, no-overwrite import: exclude backups, secrets, credentials, PII, raw transcripts, session handles, generated memory internals, and retired-provider material; preserve provenance and SHA-256 evidence; quarantine ambiguity; and update only the destination namespace's index with same-namespace relative links.

This exception does not authorize editing platform-managed registries, rollout summaries, managed carriers, or other system-owned memory state. Use the supported memory-update mechanism for those surfaces.

## Completion check

- Destination is the current project's namespace.
- No secret or private payload was copied.
- Provenance and hashes are recorded where material was imported.
- `MEMORY.md` links resolve within the same namespace.
- Live rules and disk state remain authoritative over the result.
