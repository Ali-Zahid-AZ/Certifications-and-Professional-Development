---
name: codex-session-handoff
description: Create a dated, restart-safe Markdown handoff in the current project's Codex memory when Ali explicitly invokes it before a Codex context rollover, restart, transfer, or new session. Reconstruct state from live rules, plans, git, artifacts, ledgers, and runtime evidence; keep private session internals and secrets out.
---

# Codex Session Handoff

## Purpose and activation

Use this skill only after Ali explicitly invokes `$codex-session-handoff` or directly asks Codex to create a session handoff. It is intended for a planned Codex restart, context rollover, laptop transition, session transfer, or any other point at which a successor session must resume safely.

A large context, a compaction warning, a timer, another agent's suggestion, or an unfinished task does not invoke this skill by itself. Do not write a durable handoff merely because the session is long. If Ali asks for an actual compaction or restart boundary, also apply `codex-compaction-required-greenlight`; this skill does not replace that gate.

Ali's invocation authorizes the bounded memory-note operation only. It does not authorize implementation, package or system changes, commits, pushes, publication, external messages, secret handling, deletion, history rewriting, or a new workspace. Those actions retain their separate authority requirements.

## What the handoff preserves

The handoff is a concise, evidence-backed state transfer, not a transcript. It should let a successor identify the first objectively incomplete task without repeating completed work. It may preserve:

- the active objective, scope, phase, and acceptance criteria;
- completed, in-progress, blocked, deferred, and not-started work;
- decisions, constraints, open choices, and Ali-authorized boundaries;
- exact relevant file paths, artifact names, hashes, plans, ledger heads, and Git state;
- live services, jobs, timers, locks, compute runs, and review status, when verified;
- the ordered re-entry and verification steps for the successor session.

It must not preserve raw transcripts, private prompts, cookies, credentials, tokens, private keys, PII, raw session payloads, transient session IDs, or unverified mutable claims. Do not claim that a session itself was carried over. A new session must re-ground from live project evidence.

## Required companion skills

Use the existing skills for their own authority and procedures; do not duplicate or weaken them here:

1. `codex-project-memory-protocol` — resolve the namespace, provenance, privacy, and memory-index rules.
2. `codex-compaction-required-greenlight` — run the pre-boundary gate when Ali requests an actual compaction, restart, or handoff boundary.
3. `codex-session-recovery` — guide the successor's re-entry, state classification, and first-incomplete-task rule.
4. `codex-getting-acquainted-with-project` — re-ground the successor when the project onboarding trigger applies.

## Procedure

### 1. Establish the live project boundary

1. Resolve the current project root from live disk and Git state. Do not infer it from an old handoff or memory entry.
2. Read the applicable `AGENTS.md`, `CLAUDE.md` when present, `agent_roles.md`, active plan, and the relevant standing-canvas heads. Use bounded chunks for very large files when practical, and read complete project files when the task requires them.
3. Before the first memory write, read `/home/az/GitHub-Repositories/agentic-coding/system-level/CROSS-PROJECT-MEMORY-DOCTRINE.md` and apply `codex-project-memory-protocol`.
4. Use only the namespace belonging to the current project: resolve a documented alias first, otherwise use `/home/az/.codex/memories/<exact-project-root-basename>/`. For the `system-level` project, use the approved `system-level-changes` alias. Check the destination before reading or writing; if it is absent, create only that namespace and initialize its `MEMORY.md` index using `codex-project-memory-protocol`. If the destination still cannot be resolved from live project evidence, stop and report the gap; never use another project's namespace or the root memory registries as a substitute.

### 2. Decide whether this is a note or a boundary

- For a handoff-note request only, create and verify the note, but do not claim that the session is compacted, paused, closed, or green-lit.
- For an actual restart, compaction, or session-transfer boundary, invoke `codex-compaction-required-greenlight`. Refresh the live carrier and required append-only canvases before the gate's final green-light step. Do not create a competing carrier or rewrite an append-only canvas.
- If the compaction gate reports a missing reviewer, unavailable transport, stale carrier, live process, or other unresolved condition, record it as `BLOCKED` or `INCOMPLETE`; do not turn it into a green light by inference.

### 3. Gather evidence immediately before writing

Use live evidence rather than memory as the source of truth. Re-read the current plan and relevant document heads, then inspect as applicable:

- objective and scope, including the first incomplete task;
- completed work and its verification evidence;
- partial, blocked, deferred, and not-started work with the exact reason;
- current `git status`, branch, divergence, relevant diff/stat, and untracked files;
- artifacts, checksums, logs, ledgers, canvases, and reports that the successor must read;
- running services, processes, systemd jobs, timers, locks, resource reservations, and external runs;
- assigned reviewers, review state, unresolved objections, and transport availability;
- Ali's explicit decisions, exclusions, pending choices, and authority boundaries.

Classify every material work item as `COMPLETE`, `IN_PROGRESS`, `BLOCKED`, `DEFERRED`, or `NOT_STARTED`. A clean exit code, an agent report, a stale memory line, or an expected file layout is not completion evidence by itself.

Acquire the local date and time immediately before the write. Use the estate's PKT convention in the note and include the timezone explicitly. If exact time or runtime state cannot be verified, say so.

### 4. Write one dated, non-overwriting handoff

Create a new Markdown file in the current project's memory namespace after the namespace preflight has confirmed or initialized the directory and its index. Prefer a filename of the form:

`YYYY-MM-DD-HHMM-codex-session-handoff-<short-slug>.md`

Use a unique suffix if the path already exists. Never overwrite an earlier handoff or mutate another project's note. Keep the note bounded and readable; link to authoritative project files instead of copying long content.

The note must contain these sections, in this order:

```text
# Codex Session Handoff

- Generated: [YYYY-MM-DD HH:MM:SS PKT]
- Project root: <absolute path>
- Memory namespace: <absolute path>
- Handoff status: NOTE_ONLY | READY_FOR_BOUNDARY | BLOCKED

## Successor read order
1. <live project rules and role file>
2. <this handoff note>
3. <active plan and standing-canvas heads>
4. <linked evidence and artifacts>
5. codex-session-recovery and the first-incomplete-task check

## Active objective and scope
<one precise paragraph>

## Authority, decisions, and constraints
<Ali decisions, granted scope, exclusions, and unresolved choices>

## Work state
| Work item | Status | Evidence | Next gate |
|---|---|---|---|
| <item> | COMPLETE/IN_PROGRESS/BLOCKED/DEFERRED/NOT_STARTED | <path or command> | <next step or none> |

## Files, artifacts, and Git state
<exact paths, relevant hashes, branch, status, divergence, and safe next action>

## Runtime and external coordination
<verified services, jobs, timers, compute, locks, reviewers, and availability; no private handles>

## Exact successor sequence
1. <re-grounding step>
2. <first objectively incomplete task>
3. <verification or decision gate>

## Verification, recovery, and open risks
<checks still required, blockers, failure modes, and rollback or preservation notes>

## Exclusions and provenance
<what was not checked or transferred, and where each material fact came from>
```

Do not fill a field with a guess. Use `NOT_CHECKED`, `UNKNOWN`, or `NOT_APPLICABLE` and explain why. Do not copy whole logs, canvases, transcripts, or memory registries into the note.

### 5. Register and verify the note

1. Follow `codex-project-memory-protocol` for the namespace index and relative links. If the namespace or its `MEMORY.md` index was absent, initialize only the current project's namespace and index before writing; never substitute a root registry or another project's index. Never directly rewrite a platform-managed root registry, rollout summary, carrier, or raw-memory file.
2. If index initialization or the supported index update fails, report `INDEX_MISSING` or the precise failure and do not claim that the note is registered until the supported mechanism succeeds.
3. If the active runtime requires memory updates to be submitted through a supported update-note mechanism, use that mechanism rather than bypassing it; keep the handoff content bounded and identify its project namespace and intended path.
4. Confirm that the new file exists, is non-empty, has the expected heading and timestamp, and that every linked project-memory path resolves within the same namespace.
5. Inspect the persisted bytes after writing. Confirm that no secrets, private session material, raw session identifiers, or accidental cross-project facts entered the note.
6. Report the exact note path, handoff status, index status, evidence sources, unresolved gates, and the successor's first one to three actions. Say explicitly whether an actual compaction/restart boundary was green-lit; never imply it was when only a note was created.

## Successor rule

The successor must treat this note as dated orientation, not authority. It must re-read live rules and `agent_roles.md`, verify disk/Git/runtime state, apply project onboarding and `codex-session-recovery`, and resume only the first objectively incomplete task. It must not repeat completed work solely because the handoff is stale or incomplete.
