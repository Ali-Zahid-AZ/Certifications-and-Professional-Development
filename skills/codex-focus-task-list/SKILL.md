---
name: codex-focus-task-list
description: Maintain an explicit, goal-aligned, evidence-backed task list for multi-step, ambiguous, interrupted, or explicitly requested Codex work so execution stays focused without expanding authority or scope.
---

# Codex Focus Task List

Use this skill when Ali explicitly asks for a task list, when a task has multiple meaningful steps or dependencies, or when interrupted/restarted work needs a reliable continuity carrier. The list is an execution-control aid: it keeps the current goal visible, exposes dependencies and gates, and makes the next action unambiguous.

This skill does not grant authority, change project scope, replace the implementation plan, replace a project ledger, or convert a suggestion into an instruction.

## Core rule

Before substantive work begins, create or refresh one task list for the current Codex task. Base it on:

1. the active thread goal, when one exists;
2. the most recent explicit Ali instruction;
3. applicable global and project rules, which constrain how the work may proceed;
4. the current project role file and required skills; and
5. live disk, Git, runtime, and artifact evidence.

A newer explicit Ali instruction supersedes stale work in the list. Do not resume a superseded item merely because it remains in an older plan or handoff.

Use the host's native task-plan facility when it exists. In Codex, maintain the current task plan rather than creating a new task-list file. Create a durable project artifact only when Ali or the project rules explicitly require one.

## What the list must contain

For every material task, include enough detail that another session can determine what is in scope, what remains, and what evidence is required.

| Field | Required content |
|---|---|
| **ID** | Stable short identifier such as FOCUS-01; do not reuse an ID for a different task. |
| **Task or deliverable** | One observable outcome, written as an action or result rather than a vague intention. |
| **Source** | GOAL, ALI, RULE, ROLE, DEPENDENCY, or VERIFICATION; link or name the source where useful. |
| **Scope** | Exact project, files, services, artifacts, or external surfaces affected. |
| **Dependencies** | Earlier task IDs, decisions, permissions, tools, or evidence required first. |
| **Acceptance evidence** | The concrete file, command result, test, hash, runtime observation, or user confirmation that will prove completion. |
| **Status** | PENDING, IN_PROGRESS, BLOCKED, UNVERIFIED, COMPLETED, SKIPPED, or SUPERSEDED. |
| **Next action / blocker** | The smallest authorized next step, or the exact reason work cannot advance. |

For multi-agent work, add the assigned role or seat, model/reasoning/transport from the live agent_roles.md, the disjoint write scope, the required report path, and the fallback or recovery condition. Do not record raw session handles in the task list.

## Build an extensive list without inventing work

“Extensive” means complete enough to cover the real lifecycle, not a list of every shell command. For a material change, consider separate rows for the following when they actually apply:

1. re-grounding and discovery;
2. objective, scope, and exclusions;
3. authority, role, availability, and precondition gates;
4. callers, consumers, affected state, and rollback path;
5. backup or preservation before an overwrite;
6. implementation or configuration change;
7. focused validation and meaningful behavior checks;
8. independent review or external consultation required by the project rules;
9. runtime deployment, reload, or symlink/parity verification;
10. documentation, memory, ledger, and change-log obligations;
11. unresolved decisions, user confirmations, and safe follow-up actions; and
12. final closeout, evidence summary, and restart/hand-off instructions.

Do not add rows merely because they are customary. If a row does not serve the current goal, omit it or mark it NOT APPLICABLE in the reasoning rather than expanding scope. Do not hide a required gate inside a broad “finish everything” row.

## Status and execution discipline

- Create the list before the first substantive mutation, external dispatch, compute run, or multi-file investigation.
- Keep at most one ordinary item IN_PROGRESS. Parallel items are allowed only when their scopes are genuinely disjoint and the project orchestration rules permit them; identify each parallel track and its owner.
- Move an item to COMPLETED only after its acceptance evidence is checked from the live source. A clean exit code, a sub-agent report, a reachable session, or a majority opinion is evidence to evaluate, not completion by itself.
- Use BLOCKED for a missing authority, unavailable required seat, failed safety gate, missing input, or external dependency. Record what can continue independently.
- Use UNVERIFIED when work may have happened but the required evidence is missing, stale, candidate-mismatched, or contradictory.
- Use SKIPPED only with a reason that preserves the goal and does not conceal an unresolved required gate.
- Use SUPERSEDED when a newer Ali instruction replaces the item; preserve the reason and do not silently delete it.
- Never turn a blocked or unverified item into COMPLETED to make the list look finished.

## Lifecycle

### 1. Open

State the objective in one sentence, identify the goal or explicit user instruction that supplies it, list hard constraints and exclusions, and name the first observable action.

Then decompose the objective into ordered task rows. Separate implementation, verification, documentation, review, and closeout rows when each has a distinct acceptance gate.

### 2. Execute

Before each material action, check that its task row is current, authorized, and not blocked. After each meaningful action:

- update the status;
- record the evidence path or result;
- add newly discovered dependencies or risks;
- identify the next task; and
- re-read mutable state before the next mutation.

If the action changes the candidate reviewed by another agent, mark the affected review gate stale and schedule the required re-review according to the live role rules.

### 3. Rebase

Reconcile the list whenever Ali sends a new instruction, a goal changes, a sub-agent reports, an external agent responds, a retry occurs, a blocker clears, a restart or compaction happens, or live repository/runtime evidence conflicts with the list.

For a restart or interrupted task, use codex-session-recovery: inspect the live plan, rules, role file, Git state, canvases, artifacts, and runtime state. Classify each row from evidence, identify the first objectively incomplete authorized row, and resume there. Do not rely on an old list, memory, or handoff alone.

### 4. Close

Before declaring the task complete:

- every required row is COMPLETED, or an explicit unresolved row is reported;
- every acceptance gate has live evidence;
- no required reviewer, permission, backup, test, deployment, or documentation gate is silently missing;
- the final scope still matches Ali's current instruction;
- project canvases and AGENT_CHANGES.md are updated when their rules require it; and
- the closeout reflection has considered confidence, blind spots, load-bearing assumptions, and the next verification.

If any required condition fails, report PARTIAL, BLOCKED, or UNVERIFIED and name the exact row rather than claiming completion.

## Delegation and external feedback

When a task list includes a sub-agent:

1. Read the current project agent_roles.md and apply codex-subagent-orchestration.
2. Record the bounded deliverable, role, reasoning, transport, disjoint write scope, report location, acceptance gate, and recovery condition.
3. Keep all Codex sub-agent work inside the current parent task/thread; do not create a new user-facing Codex thread for it.
4. Require the assigned report write before treating the review or implementation row as complete.
5. Treat unavailable, stale, timed-out, or candidate-mismatched reports as incomplete review.

Before any external feedback, consultation, or audit dispatch, apply codex-external-agent-availability-preflight and record only non-sensitive availability evidence. Do not invent a session handle or treat an old availability document as a live roster.

## Durable records and boundaries

The task list is not a replacement for:

- an implementation plan, which freezes design and build intent;
- DYNAMIC_LEDGER.md, which records project task/status state under its canvas protocol;
- AGENT_CHANGES.md, which records what was actually changed;
- project memory, which is orientation and must use the project namespace; or
- COUNCIL.md, which records architectural debate and rulings.

If one of those artifacts is required, add it as a task-list row with its own acceptance evidence and use the artifact's governing skill. Do not create a second copy of a project ledger or memory merely to hold the checklist.

## Compact task-list template

Use this shape in the native task-plan surface:

~~~text
Objective: <one sentence tied to the current goal or explicit Ali instruction>
Scope: <projects, files, systems, and exclusions>
Constraints: <authority, safety, review, privacy, and toolchain gates>

FOCUS-01 | Re-ground and inventory live state
  source: GOAL + RULE
  depends_on: none
  evidence: current rules, role file, plan/canvas heads, Git/runtime state
  status: IN_PROGRESS
  next: <one bounded action>

FOCUS-02 | <deliverable>
  source: ALI
  depends_on: FOCUS-01
  evidence: <specific artifact or verification>
  status: PENDING
  next: blocked until FOCUS-01 passes

FOCUS-03 | Verify and document
  source: VERIFICATION + RULE
  depends_on: FOCUS-02
  evidence: <tests, hashes, logs, review, and final state>
  status: PENDING
  next: <bounded verification>
~~~

Keep updates concise for the user: report the completed row and evidence, the current row, and the exact blocker or next decision. The underlying list may be extensive; the conversational status does not need to repeat every unchanged row.

## When not to use

Do not inflate a one-step factual answer, translation, trivial formatting request, or simple read-only lookup into an extensive execution plan unless Ali explicitly asks for the task list. Do not use this skill to authorize destructive actions, external communication, spending, commits, pushes, publication, new directories, or other scope expansion. Those actions still require their own explicit authority and applicable project gates.
