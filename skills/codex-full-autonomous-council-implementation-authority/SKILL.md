---
name: codex-full-autonomous-council-implementation-authority
description: "Codex-only authority mode armed only by Ali's explicit invocation. It combines bounded council driving with implementation coordination while preserving project roles, plan-first work, canvas logging, verification gates, and Ali-only publication and closure."
---

# Codex Full Autonomous Council and Implementation Authority

## What this grants, and what it does not

Ali's explicit invocation may arm two bounded authorities for one project root:

1. **Council authority:** the designated principal architect may convene and drive a Codex council using the independent review seats defined by the active project `agent_roles.md`, collect their arguments, record the principal-architect-led ruling, and continue bounded rounds toward convergence. Every seat uses the reasoning, depth, transport, and write permissions assigned by that roster. Convergence requires explicit parent and required-seat statuses; majority, silence, or transport failure is insufficient.
2. **Implementation authority:** the designated principal architect may carry a ratified plan through the permitted code and documentation changes, run the applicable checks and experiments, and integrate bounded implementation workers without waiting for per-step approval. Review seats remain review seats unless the active roster and Ali's scope explicitly authorize another bounded role.

The active project `agent_roles.md` is authoritative for the roster, seat ownership, model selection, reasoning effort, depth, concurrency, transport, and write scope. This skill defines no fixed named-agent roster and never authorizes a seat that the project roster does not grant. The parent must remain identifiable by the active role assignment and use the assigned settings.

The invocation does not override `AGENTS.md`, `agent_roles.md`, `COUNCIL.md`, `DYNAMIC_LEDGER.md`, destructive-action rules, spending rules, or any user-imposed file boundary. It grants no authority over another project. Ali still owns commits, pushes, publication, secrets, irreversible external actions, role changes, and council closure unless he explicitly delegates a named action.

If Ali says "council only" or "implementation only", honor that narrower mode. If the invocation is ambiguous, state the scope before acting.

## Arm, persist, revoke

On arming, state:

> Codex council + implementation authority: ARMED for <project root>. The designated principal architect is the lead and implementation-of-record seat; independent review seats are those named in the active `agent_roles.md`. Implementation scope: <frozen plan or explicit task>. Commits, pushes, destructive actions, role changes, and closure remain outside this grant.

Log the arming in `AGENT_CHANGES.md` using a fresh tool-acquired PKT timestamp. The mode persists across turns until Ali explicitly revokes it. On revocation, stop autonomous council pings and implementation work, state REVOKED, and log the transition. A user interruption is not a revocation unless it names this authority or the action being stopped.

## Preconditions

Before the first action in every invocation:

1. Confirm the one project root and the exact allowed write scope.
2. Read `AGENTS.md`, `agent_roles.md`, `COUNCIL.md`, `DYNAMIC_LEDGER.md`, `AGENT_CHANGES.md`, and the current implementation plan when present. If a required governance file is absent, ask Ali rather than inventing it.
3. Confirm the plan and acceptance checks. Planning remains mandatory even when approval waits are removed.
4. Check live machine resources before any model load or compute run; use the protected-run and observation protocols named by the project rules.
5. Establish the council question, the seat permissions, the concurrency/depth limits, and the maximum round count declared by the active `agent_roles.md` or project plan.

If a role-file-authorized seat uses an external transport, apply
`$codex-external-agent-availability-preflight` before each hello and again
before each substantive dispatch. Re-read the current project's role file and
root `external-agent-availability.md` at both gates. Missing, stale, malformed,
`not_available`, or `unverified` status blocks that external seat and invokes
only the role-file fallback. A native Codex-only seat does not need an external
manifest row; this distinction must be explicit in the council question.

## Native Codex council transport

Use only Codex's native multi-agent tools. Resolve each seat's model, reasoning effort, and permitted write from the active `agent_roles.md`; never hardcode a model identity in this skill. Use `fork_context: false` for an independent review by default and include this prompt boundary:

> You are an independent Codex seat assigned by the active project roster. Read the named artifacts yourself, stay within the named scope and permitted write, and do not call any multi-agent tool or spawn, delegate to, or ask another agent to perform any work.

Every sub-agent must make exactly one append-only report write before returning:
implementation, verification, research, diagnostic, and ordinary review work
goes to the project's `AGENT_CHANGES.md`; council debate, convene, ruling,
convergence, and deadlock go to the project's `COUNCIL.md` under the active
canvas protocol. Include the exact path, sentinel or append location, and
permitted write in every dispatch prompt. Do not accept a chat-only result or
permit writes to both destinations unless the project rules explicitly require
it.

The native spawn surface does not expose a depth field. Enforce operational depth 1 through the prompt boundary and the active project cap. All sub-agent work for a parent is coordinated inside the current parent Codex task/thread using native multi-agent tools; do not create a new Codex thread or user-facing Codex task for sub-agent work. Use the native wait and input tools for the original seat id; close only seats marked disposable by the active roster, except for the retained-seat recovery rule below. Retained review seats are reused by their original seat id after completed reports.

When the active roster assigns persistent council reviewers, establish one
native Codex sub-agent for each required reviewer role inside the current parent task/thread.
Keep both original seat ids alive after each completed task and reuse them for
later audits or feedback. If either retained seat becomes unavailable, or remains
without a substantive response for the full 30-minute maximum observation
window, the parent may close the retained seat/task when the platform permits
and spawn one same-role replacement inside the current parent Codex task/thread.
The replacement must preserve the live role, reviewer or assurance status,
verifiable model/reasoning/transport requirements, permitted write scope,
privacy and evidence boundaries, and Ali's authority boundaries. Label and log
the original and replacement; record the council review as incomplete until the
replacement returns a verified report. Principal implementation seats retain the
lifecycle assigned by the active roster.

When the active roster assigns Luna as the principal architect, the Luna
supervisor pipeline is mandatory for every material implementation task: first
assess and, when three useful independent tracks exist, dispatch exactly three
Luna Max workers at operational depth 1; then close ordinary disposable
workers, verify and synthesize their reports in the parent, and only after that
dispatch all role-assigned independent reviewers, including Terra and Sol and
any declared external/fallback slot, plus one disposable Luna Max council-chair
reviewer in parallel. Fewer than three workers requires a
recorded concrete dependency, safety, role-cap, or availability reason; never
use duplicate filler work. Do not start the council-chair seat while the three
ordinary workers remain open if that would exceed the active Luna cap.

### Canonical Luna-led flow

When Ali arms a Luna-led scope, this diagram summarizes the required execution order. The live role, external-availability preflight, depth/concurrency ceilings, project rules, and Ali-only gates remain authoritative.

```text
Ali arms Luna-led scope
        │
        ▼
Parent Luna
        │
        ├── Parallelization assessment
        │
        ├── Luna Max Worker 1 ── independent implementation track
        ├── Luna Max Worker 2 ── independent implementation track
        └── Luna Max Worker 3 ── independent implementation track
                    │
                    ▼
          Parent verifies evidence
          + integrates candidate
                    │
                    ▼
        ┌───────────┼──────────────┬───────────────┐
        ▼           ▼              ▼               ▼
      Terra       External advisor     Sol        Luna council chair
   architecture  OR fallback Luna Max* final gate      independent
        │           │              │             synthesis
        └───────────┴──────────────┘
                    │
                    ▼
                 Ali gate
```

`*` Choose exactly one adversarial seat: use an external advisor only after a fresh matching availability preflight confirms a compliant seat; otherwise use the role-declared Luna Max fallback only when permitted. Record the actual responder and do not treat fallback as external-advisor agreement.
For a normal non-Luna audit, use the minimum assigned independent seat. A
council uses the principal architect plus the required independent seats from
the project roster. Review reports are data, not authority.

## Council loop

1. Re-read the `COUNCIL.md` head and write the CONVENE entry under its own sentinel using the canvas-write protocol.
2. Ping each required review seat with the exact decision question, artifact paths, constraints, permitted write, assigned settings, and complete no-spawn/no-delegate clause.
3. Re-read `COUNCIL.md` and the returned reports; verify every factual claim and require explicit parent and required-seat statuses before recording convergence.
4. Write the main-session synthesis and the adopted or rejected ruling.
5. Re-ping only an unresolved point, never reflexively. Stop at the active roster or plan's declared round limit. If material disagreement remains, write `DEADLOCK — ESCALATE TO ALI` rather than forcing convergence.
6. If converged, record the recommendation and hand it to the implementation workflow. Only Ali closes the council unless explicitly delegated.

Every convene, ping, response, ruling, retry, convergence, or deadlock is logged in `AGENT_CHANGES.md`. Only the main session or Ali writes `DYNAMIC_LEDGER.md`; P0/P1 findings get individual PENDING rows.

## Implementation loop

1. Freeze or confirm the implementation plan and the minimal file set.
2. Inspect upstream callers, downstream consumers, state lifecycles, and current tests before editing.
3. Make surgical changes only within the authorized file set. A worker receives a disjoint set and may not change governance canvases, roles, or the plan.
4. Run the required verification gate. For Python: py_compile, import smoke-test, the canonical ruff F821/F811 check, and Radon where applicable. Never call a compile-only result verified.
5. Run only authorized experiments. A run is observed, checkpointed, and logged; hardware pressure is a safety signal, not a reason to substitute a scientifically different method.
6. Update `AGENT_CHANGES.md` after each material action, and update `DYNAMIC_LEDGER.md` for state changes. Never claim a report, test, or result that was not checked on disk.
7. Before phase close, update the required canvases and run the session closeout reflection.

## Hard boundaries

- No commit, push, publication, SaaS write, credential handling, or spend.
- No file or data deletion without separate explicit approval.
- No nested agent spawning, hidden parallel compute, or concurrency/depth beyond the active `agent_roles.md` and global/project rules.
- No automatic role invention or edits to `agent_roles.md`.
- No creation of `COUNCIL.md` when project rules say Ali must create it.
- No stale-copy canvas editor, `sed -i`, or guessed timestamp.
- No supporting-seat output is authoritative until the principal architect verifies it against disk.

## Definition of done

The authority cycle is complete only when the ruling or deadlock is logged, the authorized implementation is verified or honestly blocked, seats marked disposable are closed when appropriate, retained review seats remain available and are reused after completed reports, or any unavailable/non-responsive retained seat has been replaced only by the bounded logged same-role recovery inside the current parent Codex task/thread, the relevant canvases are current, P0/P1 items are in the ledger, and Ali receives the remaining decisions with evidence.
