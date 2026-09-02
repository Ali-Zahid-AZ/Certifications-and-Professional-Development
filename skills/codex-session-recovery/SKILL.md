---
name: codex-session-recovery
description: Recover interrupted, compacted, restarted, or handed-off work from live plans, repository state, git evidence, ledgers, and runtime state. Use whenever conversation history is incomplete or conflicts with the project.
---

# Codex Session Recovery

When execution history is incomplete, compacted, interrupted, or inconsistent with repository state, do not infer progress from memory or conversation context. Repository, disk, git, and live runtime evidence win.

## Recovery sequence

1. Read the active implementation plan, phase-status document, and current project rules. If a referenced document is absent, record it as unavailable; do not invent it.
2. Inspect `git status`, `git diff`, recent commits, changed files, file timestamps, and relevant service/process/log state. Re-read current canvas heads rather than relying on an earlier snapshot.
3. Classify each task as completed, partially completed, blocked, or unstarted using direct evidence. Reconcile the Codex task list, `DYNAMIC_LEDGER.md`, `AGENT_CHANGES.md`, and persisted artifacts.
4. Identify the first objectively incomplete task and resume only there. Never repeat completed work merely because conversational context was lost.
5. Preserve unrelated changes and open decisions. Do not commit, push, close a phase, launch compute, or declare convergence while a required gate is unresolved.
6. Treat memory and handoff summaries as orientation only. Verify every mutable claim against live rules, disk, git, and runtime state before acting.

## Project-memory recovery gate

When recovery needs to read, import, repair, or write project memory, apply
`codex-project-memory-protocol` first. Resolve the live project root and its
documented namespace, check that namespace and its `MEMORY.md`, and stop with
`BLOCKED` if that preflight cannot be completed. Project facts must never be
written to `extensions/ad_hoc/notes/`; read that location only for a bounded,
Ali-authorized import of genuinely global or cross-project material. Hooks are
defense-in-depth and do not change this routing rule.

## Restart and compaction boundary

Before green-lighting compaction, restart, or handoff, use `compaction-required-greenlight` to refresh the current carrier and confirm durable canvas entries. After resuming, re-ground from the live rules, role file, plan, ledger, and carrier before any other state-changing action.

## Completion report

Report the evidence used, completed work, partial work, blockers, missing documents, and the exact next task. If evidence is insufficient, mark the state UNVERIFIED rather than guessing.
