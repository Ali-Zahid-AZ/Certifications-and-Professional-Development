---
name: codex-safe-system-change
description: Plan, back up, execute, and verify reversible system-level changes involving configuration, packages, services, hooks, permissions, cleanup, or startup behavior. Use before any potentially destructive or machine-wide change.
---

# Codex Safe System Change

Use this skill for system configuration, package installation or removal, services, hooks, permissions, startup tasks, caches, runtime paths, or any change whose failure could affect other projects or the machine.

## Before acting

1. State the target, intended effect, risk, and rollback path to Ali. Treat standing permission as authorization within its exact scope, not as a blanket repeal of safety boundaries.
2. Inspect the live target, owning process/package/service, symlinks, configuration references, and current state. Do not infer from stale memory or a command's name.
3. Plan the smallest change. Identify whether the action is reversible, whether it can overwrite data, and whether it touches production, external services, spending, credentials, or other projects.
4. For any existing file that will be overwritten, create a recoverable, timestamped backup first and verify its hash. Never overwrite an unexamined target.

## Destructive and external actions

- Do not run `rm -rf`, `rm -r`, `rm -d`, `rmdir`, truncating redirects, history rewrites, database wipes, cache clears, or broad cleanup unless Ali explicitly authorizes the exact target and action. Prefer a timestamped move to a backup location.
- If an action is destructive, irreversible, production-facing, spend-incurring, or outward-facing and authorization is unclear, stop and ask. If it is authorized, announce the exact action immediately before execution and preserve a rollback record.
- Commands that only Ali can safely execute, including destructive infrastructure commands and human-only SaaS-console actions, belong in the project's `DYNAMIC_LEDGER.md` as `[PENDING]` with the exact command and rationale; do not execute them.
- Never place secrets in repositories, logs, prompts, chat, or memory. Use the approved runtime secret mechanism and record only non-sensitive operational guidance.

## After acting

1. Verify the resulting file, configuration parse, service/package state, symlink target, and idempotence as applicable. Check actual behavior, not only exit code.
2. Recheck for unintended processes, listeners, changed paths, permissions, and unrelated work.
3. Record every system change in the current project's `AGENT_CHANGES.md` using `canvas-write-protocol`; include the exact commands, absolute files, backup path, verification, and outcome.
4. Report remaining uncertainty and the rollback command. Do not claim system-wide success from a local or cached check.
