---
name: codex-work-parallelization-luna-sub-agents
description: "Enforce a three-worker Luna Max parallelization gate for material work when three independent tracks are available."
---

# Codex Work Parallelization Luna Sub Agents

Use this skill when an Ali-armed Luna parent is planning material implementation,
diagnostic, research, verification, or bounded documentation work and the work
may be split into independent tracks. It makes the three-worker parallelization
assessment explicit and operational. It does not create authority, a roster, a
model assignment, or an exception to the active `AGENTS.md`, project rules,
`agent_roles.md`, Ali's instruction, or platform limits.

## Hard gate

Before sizeable solo work, the parent Luna MUST perform and record a
parallelization assessment in the current task list. Identify the candidate
tracks, their dependencies, owner, model/reasoning/transport, write scope,
report destination, acceptance evidence, and recovery path.

When three useful, genuinely independent tracks can be formed and the active
role file permits Luna workers, the parent MUST dispatch exactly three
concurrent Luna Max workers. “Up to three” is not sufficient in this case.
Do not fill a seat with duplicate or artificial work. The only valid reasons to
use fewer than three are a recorded concrete dependency, safety constraint,
role/concurrency cap, or live availability failure that makes three useful
tracks impossible. Convenience, impatience, quota optimism, or a preference for
solo work is not an exception.

The parent Luna is not counted as one of the three workers. Read the live
`agent_roles.md` immediately before dispatch and use its assigned model,
reasoning effort, transport, depth, concurrency ceiling, and write permission.
Use Max reasoning only when the dispatch surface exposes and verifies the
role-file-required Max setting; otherwise record the limitation and do not
claim a compliant Max wave. This skill never authorizes inventing a model,
seat, session handle, transport, or depth argument.

## Worker contract

Each of the three worker prompts must be self-contained and contain all of the
following:

- one genuinely disjoint bounded scope and one concrete deliverable;
- the upstream callers, downstream consumers, and acceptance checks to inspect;
- the exact permitted write, or an explicit read-only/report-only permission;
- one report destination and the required evidence format; and
- the operational depth-1 boundary:

  > Do not call any `multi_agent_v1__*` tool and do not spawn, delegate to, or
  > ask another sub-agent to perform any work.

Workers may share read scope, but they must not edit one another's files or
shared integration points. The parent owns shared integration, candidate
assembly, `agent_roles.md`, `DYNAMIC_LEDGER.md`, council closure, and any
Ali-only action. A worker report is evidence, not truth; the parent verifies
its claims against current disk, diffs, tests, logs, measurements, and
artifacts.

## Required Luna supervisor sequence

Apply this order whenever the hard gate fires:

1. **Fan out:** dispatch exactly three independent Luna Max workers in
   parallel, at the verified role-file settings and operational depth 1.
2. **Collect and release:** collect each report as soon as its bounded work is
   complete. Verify the report, diff, candidate bytes, tests, and artifacts.
   Close ordinary seats marked disposable after their reports are verified.
   Keep a role-declared retained/reusable fallback seat alive; it is not one of
   the three ordinary worker seats.
3. **Parent synthesis:** integrate only evidence that passes the parent checks,
   record the candidate and unresolved findings, and re-read mutable state
   before any next action. A parent does not self-certify independent quality
   or convergence.
4. **Independent review:** only after parent verification and synthesis,
   dispatch the role-assigned Terra, Sol, and exactly one permitted adversarial
   external-advisor-or-fallback seat, plus a disposable Luna Max council-chair
   reviewer when the active role and concurrency ceiling require/permit it.
   The chair is feedback, not a vote or a replacement for a required seat. A
   project-specific role exception, such as a route with no council chair,
   remains authoritative.
5. **Gate honestly:** missing, stale, unavailable, timed-out,
   candidate-mismatched, or fallback review is incomplete evidence, not
   agreement. Record the actual responder identity and never present a
   fallback as the requested external advisor.

Do not begin the review wave while the worker wave remains open if doing so
would exceed the active Luna ceiling. Do not create a new user-facing Codex
thread for these workers; use the native multi-agent tools inside the current
parent task/thread. Every worker or reviewer must make the one report write
required by the active project protocol.

## Timing and recovery

The 30-minute (`1,800,000 ms`) observation boundary is a maximum, not a
required wait. Completed workers and reviewers return immediately; they must
not sleep, idle, or hold a report to consume the window. Follow the active
role file for disposable-seat closure and retained-seat recovery. If a worker
or required reviewer is unavailable, do not silently reduce the wave or treat
silence as agreement: apply the configured fallback once, or record the gate
as incomplete.

## Canonical flow

```text
Ali arms Luna-led scope
        │
        ▼
Parent Luna
        │
        ├── Parallelization assessment
        ├── Luna Max Worker 1 ── independent track
        ├── Luna Max Worker 2 ── independent track
        └── Luna Max Worker 3 ── independent track
                    │
                    ▼
          Parent verifies + synthesizes
                    │
                    ▼
       Terra · adversarial seat · Sol ·
       disposable Luna Max council chair
                    │
                    ▼
                 Ali gate
```

## Source basis and precedence

This contract consolidates the live wording found in the estate sources:

| Source | Reusable wording or rule |
|---|---|
| `global/AGENTS.md`, `global/CLAUDE.md`, `global/GEMINI.md`, and the system-level `AGENTS.md` | Parent Luna assesses parallelism, dispatches exactly three Luna Max workers at operational `max_depth 1` when three independent tracks exist, verifies/synthesizes, then routes independent review. |
| 13 current Luna-enabled `project-rules-skills/*/agent_roles.md` files and the new-project template | Three-track assessment is mandatory; exactly three workers are mandatory when useful; the role file sets the up-to-three ceiling, disjoint scopes, parent integration, and disposable-seat lifecycle. |
| `project-rules-skills/oh-jira-tickets-agent/agent_roles.md` | This project currently has no Luna seat; its conditional future Luna rule does not override its current single-seat boundary. |
| `codex-second-in-command` and `codex-subagent-orchestration` | Fewer than three requires a concrete dependency, safety, role-cap, or availability reason; no duplicate filler work; workers do not nest; reports are verified; 30 minutes is a maximum observation boundary. |
| `codex-focus-task-list` | Parallel tracks must be genuinely disjoint, named with owners and evidence, and completed only after live acceptance checks. |

When wording conflicts, use this precedence: Ali's current instruction and
platform/developer safety, applicable global rules, the active project's rules,
the live `agent_roles.md`, then this skill. Project-specific exceptions remain
valid; this skill centralizes the common gate and cannot broaden them.
