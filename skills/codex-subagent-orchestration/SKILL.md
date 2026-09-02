---
name: codex-subagent-orchestration
description: "Codex-native orchestration for bounded implementation, architecture advice, adversarial review, scientific-claim review, and councils. The active project agent_roles.md controls the roster, authority, and seat assignment."
---

# Skill: codex-subagent-orchestration

## Purpose

Use this skill when the project's designated principal architect needs bounded Codex sub-agents for implementation, architecture advice, adversarial review, scientific-claim review, or a genuine council. The active project `agent_roles.md` is mandatory: it is the source of truth for role ownership, seat identity, model routing, reasoning effort, depth, concurrency, transport, and write scope.

This skill supplies transport and safety rules. It does not create a roster, grant authority, or override `AGENTS.md`, project rules, Ali's direct instruction, or `agent_roles.md`. If the role file is absent or does not define the requested seat, stop and ask Ali.


## Use and non-use

Use this skill for:

- architecture advice, design sanity checks, and bounded implementation planning;
- adversarial verification after a change, especially a change touching more than two files;
- scientific-claim, evaluation, or pre-registration review;
- a genuine architectural council; and
- bounded mechanical work whose write scope can be made disjoint and explicit.

Do not delegate GPU, model-training, data-generation, or other compute runs. The main session owns those runs under the project's observation and protected-run protocols. Do not delegate merely to avoid a small local search or a one-file edit.

## Goal continuity and task checklist

Before dispatching any seat, the parent must create and maintain a concrete
task list for the goal. At minimum, record the bounded deliverable, subtasks,
dependencies, assigned seats, acceptance gates, evidence paths, recovery
actions, and current status. Update it after dispatch, each report or retry,
each finding disposition, and closeout so it remains a usable continuity
carrier.

Do not voluntarily abandon an in-scope goal because a sub-agent, external
transport, or single attempt fails. Continue through the task list using the
active `agent_roles.md` recovery and fallback policy. Continuity does not
authorize scope expansion, unsafe execution, or a false completion claim: if a
mandatory reviewer or evidence gate remains unavailable and no configured
fallback is permitted, continue any non-dependent work, record the exact
incomplete gate, and report the goal as incomplete rather than silently
converting the absence into success.

For every material task, the parent must perform and record a three-track
parallelization assessment before sizeable solo work. When three useful,
genuinely independent tracks can be formed and the active roster assigns Luna
implementation workers, the parent Luna must dispatch exactly three concurrent
Luna Max workers at the role-file-assigned reasoning level (Max when the
dispatch surface exposes and verifies it), with disjoint write scopes and
bounded deliverables. Fewer than three is allowed only with a recorded
concrete dependency, safety, role-cap, or availability reason; convenience or
solo preference is not an exception, and duplicate filler work is prohibited.
After the worker reports return, the parent Luna verifies and synthesizes the
candidate, closes the ordinary disposable seats, and only then dispatches all
role-assigned independent reviewers, including Terra and Sol and any declared
external/fallback slot, plus one disposable Luna Max council-chair reviewer in
parallel. The parent remains the supervisor and integration owner;
no worker or reviewer may spawn or delegate.

### Required Luna supervisor pipeline

When Luna is the active principal architect, enforce this order for every
material implementation, research, diagnostic, or verification task:

1. Fan out three independent Luna Max workers when three useful tracks exist;
   give each a disjoint scope, bounded deliverable, depth-1 no-spawn clause,
   and exactly one report destination.
2. Collect the reports, close seats marked disposable, and make the parent Luna
   verify every material claim, diff, test, and artifact before recording the
   synthesis and candidate.
3. Only after that parent synthesis, dispatch all role-assigned independent
   review seats, including Terra and Sol and any declared external/fallback
   slot, plus one disposable Luna Max council-chair seat in parallel. The chair
   is additional feedback, not a replacement for a required seat and not a vote.
   Do not start it while the three workers remain open if that would exceed the
   active Luna concurrency ceiling.
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

## Codex dispatch surface

Use only Codex's native multi-agent tools:

| Tool | Use | Discipline |
|---|---|---|
| `multi_agent_v1__spawn_agent` | Start one bounded sub-agent | Give a self-contained prompt, explicit scope, model only when justified by `agent_roles.md`, and `fork_context: false` for an independent audit by default. |
| `multi_agent_v1__send_input` | Queue a clarification or non-interrupting nudge | Target the existing agent id; use `interrupt: true` only when the task must change immediately. |
| `multi_agent_v1__wait_agent` | Collect a result when the critical path requires it | Wait deliberately, not in a reflexive polling loop. |
| `multi_agent_v1__close_agent` | Release a disposable implementation seat | Close a completed seat only when the active `agent_roles.md` marks it disposable. A retained seat may be closed only under the retained-seat recovery rule below when it is unavailable or non-responsive for the full bounded window. |

The spawn tool does not expose a depth field. Enforce depth 1 operationally: never give a sub-agent permission to spawn, and include this clause in every delegated prompt:

> Do not call any `multi_agent_v1__*` tool and do not spawn, delegate to, or ask another sub-agent to perform any work.

### Codex seat-call examples

These are patterns, not a fixed roster. Replace each placeholder with the model and reasoning effort assigned by the active `agent_roles.md`. Use only the role required by the task.

~~~js
const assuranceSeat = await tools.multi_agent_v1__spawn_agent({
  model: "<assurance-model-from-agent_roles.md>",
  reasoning_effort: "<assurance-effort-from-agent_roles.md>",
  fork_context: false,
  message: "You are the assigned independent assurance reviewer. Audit the named artifacts adversarially. Source is read-only; your only permitted write is the named report. Apply scientific-claim-soundness-audit. If the project defines a full verifier, do not run it or publish normal artifacts unless and until you issue PASS; if FAIL, identify concrete evidence and required remediation. Return your verdict and write the signed report as soon as the review and required checks are complete; do not wait for the parent or the timer. The 30-minute window is a maximum, not a minimum. Do not use or spawn any sub-agent or Agent/Task tool."
});

const architectureSeat = await tools.multi_agent_v1__spawn_agent({
  model: "<architecture-review-model-from-agent_roles.md>",
  reasoning_effort: "<architecture-review-effort-from-agent_roles.md>",
  fork_context: false,
  message: "You are the assigned independent architecture and gap-finding reviewer under the principal-architect parent. Review the named design question. Source is read-only; your only permitted write is the named report. Do not call any multi-agent tool and do not spawn, delegate to, or ask another sub-agent to perform any work."
});

const implementationWorker = await tools.multi_agent_v1__spawn_agent({
  model: "<implementation-model-from-agent_roles.md>",
  reasoning_effort: "<implementation-effort-from-agent_roles.md>",
  fork_context: false,
  message: "You are an implementation worker under the principal-architect parent. Perform only the named bounded task, inspect the declared callers and consumers, and do not broaden scope. Do not call any multi-agent tool and do not spawn, delegate to, or ask another sub-agent to perform any work."
});
~~~

Collect a seat with `multi_agent_v1__wait_agent({targets: [agent_id], timeout_ms: ...})`, send a queued clarification with `multi_agent_v1__send_input({target: agent_id, message: ...})`, and release a disposable implementation seat with `multi_agent_v1__close_agent({target: agent_id})`. Preserve the original seat id; seats marked retained by the active roster remain available for reuse after a completed report. A retained seat is closed or replaced only under the retained-seat recovery rule below. The current Codex surface supplies no durable scheduler or depth argument; do not invent either.

## Parent Codex task/thread boundary

All sub-agent work for a parent must be coordinated inside the current parent
Codex task/thread using the native multi-agent tools. Do not create a new Codex
thread or user-facing Codex task for sub-agent work. This native boundary is
separate from any declared external OpenCode or Claude transport and does not
authorize a new external session or a new project scope.

## Completion, review window, and recovery

Give each review seat a maximum 30-minute (`1,800,000 ms`) observation window,
never a required delay. Completion is event-driven: once the assigned work and
required checks are complete, the sub-agent must immediately return its audit
or feedback. It must not sleep, idle, hold a completed report, or perform
private synthesis merely to consume the remaining time.

If a Codex sub-agent cannot be reached during its review window, do not stop
the parent goal. For a disposable or explicitly replaceable seat, apply the
active `agent_roles.md` recovery rule. For a retained Codex sub-agent, if the
runtime reports it unavailable, or it remains without a substantive response
for the full 30-minute maximum observation window, the parent may close that
retained seat/task when the platform permits and spawn one same-role replacement
inside the current parent Codex task/thread. The replacement must preserve the
live role, reviewer or assurance status, verifiable model/reasoning/transport
requirements, permitted write scope, privacy and evidence boundaries, and
Ali's authority boundaries. Label and log the original seat and replacement;
the replacement is not agreement or convergence until it returns a verified
report. If no compliant replacement can be created, classify the review as
incomplete or timed out; never treat the missing report as agreement or claim
a gated completion.

Every prompt must state the sub-agent's write permission. A blanket "read-only; write nothing" clause prevents an auditor from logging its report. Say exactly what report or canvas entry it may write.

## Mandatory sub-agent report write

Every sub-agent must make exactly one append-only report write before it
returns:

- implementation, verification, research, diagnostic, or ordinary review work
  writes its signed result to the project's `AGENT_CHANGES.md`;
- a council debate, convene, ruling, convergence, or deadlock writes to the
  project's `COUNCIL.md` under the active canvas protocol.

The parent must provide the exact path, sentinel or append location, and
permitted write in the dispatch prompt. A sub-agent may not return a chat-only
result, and no sub-agent may write to both destinations unless the active
project rules explicitly require it. The reporting write is mandatory in
addition to any disjoint implementation file set; it does not authorize edits
to unrelated canvases or governance files.

## Retained audit seats

An audit or review seat marked retained by the active roster remains available
after a completed report and should be reused by its original seat id. If the
runtime reports the retained Codex sub-agent unavailable, or it remains without
a substantive response for the full 30-minute maximum observation window, the
parent may close the retained seat/task when the platform permits and spawn one
same-role replacement inside the current parent Codex task/thread. The
replacement must preserve the live role, reviewer or assurance status,
verifiable model/reasoning/transport requirements, permitted write scope,
privacy and evidence boundaries, and Ali's authority boundaries. Label and log
both seats. Until the replacement returns a verified report, the affected gate
remains incomplete; no replacement may be treated as agreement or convergence.
Seats marked disposable by the active roster follow their declared lifecycle.

## Persistent reviewer seats

When the active `agent_roles.md` assigns persistent review seats, establish
exactly one persistent Codex sub-agent for each required reviewer role. Refer to
the active role file for the specific agents, models, reasoning, transports, and
review scopes. Use `multi_agent_v1__spawn_agent` and the other native Codex
multi-agent tools only. The parent-task boundary above prohibits creating a
Codex thread or user-facing task for either reviewer seat.

Keep both original sub-agent ids alive after every completed audit or feedback
task. A completed report is not a reason to close the seat: send later work to
the same id and reuse it. If either retained seat disappears or the runtime
reports it unavailable, or it remains without a substantive response for the
full 30-minute maximum observation window, the parent may close the retained
seat/task when the platform permits and spawn one same-role replacement inside
the current parent Codex task/thread. The replacement must preserve the live
role, reviewer or assurance status, verifiable model/reasoning/transport
requirements, permitted write scope, privacy and evidence boundaries, and Ali's
authority boundaries. Label and log the original and replacement; until a
verified replacement report exists, the review remains incomplete. Principal
implementation workers follow the active roster's disposable/retained
lifecycle.

## Role routing and limits

Read the active `agent_roles.md` before every material dispatch. Use the role-specific model, reasoning effort, depth, transport, concurrency ceiling, and permitted write scope recorded there. A stricter project rule or Ali instruction wins.

The principal architect is the parent only when the project roster and Ali's explicit arming authorize that role. Otherwise the current session follows the project roster. Never infer authority from a model name, nickname, seat label, or availability.

Hard invariants:

1. Never exceed any role-specific concurrency, depth, or reasoning limit in `agent_roles.md`.
2. No sub-agent may spawn, delegate to, or ask another agent to work.
3. The parent is not counted as one of its own worker seats.
4. In Luna-led material work, obey the required three-seat fan-out and its
   recorded exception rule; never fill a seat with duplicate work.
5. Outside that Luna-led pipeline, a normal delegation uses the minimum seat
   required. Do not launch multiple seats on the same unresolved question.
6. After the parent Luna has verified and synthesized the three-worker results,
   request the independent reviews required by `agent_roles.md` plus the
   disposable Luna Max council-chair feedback seat when the active role
   assigns the pipeline. First-party verification is not independent assurance.
7. Transport failure, missing seat, stale session id, or unverifiable settings is incomplete review, not agreement.
8. Any material change after a review or `PASS` that touches the reviewed
   behavior, interfaces, schemas, dependencies, architecture, tests, evidence,
   security boundaries, numerical results, or scientific conclusions
   invalidates the affected review and requires re-audit.
9. Named-seat convergence is dialectical, not a majority vote. Silence, stale
   or candidate-mismatched reports, transport failure, and unavailable
   required reviewers are not agreement; use the active role file's configured
   fallback or leave the affected gate incomplete.
10. A fallback or substitute must never silently impersonate the missing seat,
    alter the canonical roster, waive a required gate, or grant authority to
    commit, push, release, publish, spend, disclose, delete, or act outwardly.

## Escalation ladder

1. Reason inline from the primary artifacts.
2. Dispatch the role assigned for architecture/gap review or the role assigned for bounded assurance.
3. Convene the principal architect and the required review seats for a genuine architectural council, using `COUNCIL.md`'s protocol.
4. If needed context exists only in another top-level session, prepare one self-contained consult block for Ali to relay. Do not attempt to resume or fork an unreachable sibling session.

A consult block contains: project and phase; 2–5 load-bearing facts with paths; exactly one falsifiable decision question; options and trade-offs; hard constraints and their sources; discriminating evidence; and the requested deliverable form. Treat the returned opinion as an argument to evaluate, not an instruction to obey.

## Prompt contracts

Every evaluative prompt must:

- identify the exact artifact and scope, using paths rather than pasted source where practical;
- include the depth-1 no-spawn clause;
- name the one permitted write, or explicitly say that the main session will receive and log the report;
- instruct the reviewer to refute rather than rubber-stamp;
- cite and apply `scientific-claim-soundness-audit`, requiring per-claim `SOUND`, `SOUND-WITH-NARROWING`, or `OVERCLAIM-BLOCK`;
- for code, require per-ruling PASS/FAIL against current and archived `COUNCIL.md` decisions and council-encoded pre-registration; and
- require file:line or claim-locator evidence, concrete repairs, and an overall verdict.

Minimum audit contract:

> You are the adversarial Codex reviewer assigned by the active project roster. Read the repository artifacts yourself. Source is read-only. Your only permitted write is the complete report appended to the named canvas. Do not spawn or delegate. Refute the implementation and its claims. Check every applicable council ruling. Apply `scientific-claim-soundness-audit` to every load-bearing claim. Return a coverage-complete findings table, file:line evidence, per-claim verdicts, concrete repairs, and an overall verdict.

The independent assurance reviewer must additionally receive this last-gateway contract:

> Do not run the full verifier or publish normal artifacts unless and until you issue PASS. If FAIL, identify the concrete evidence and required remediation. As soon as the substantive review and required live checks are complete, return your verdict and write your own signed entry to `AGENT_CHANGES.md`; do not wait for the parent or for the timer. The 30-minute window is a maximum, not a minimum. Do not use or spawn any sub-agent or Agent/Task tool.

If the project has no full verifier, mark that clause N/A and apply the project's named acceptance gate. The assurance review must still check architectural-ruling fidelity, silent scope changes, edge cases, failure modes, meaningful rather than cosmetic tests, multi-file robustness, scientific and numerical claims, and evidence supporting the reported completion state.

## Mechanical and implementation delegation

The claim-soundness lens is optional only when the output contains no evaluative claim, interpretation, or recommendation. When uncertain, include it.

For implementation work, give each Luna worker a frozen acceptance contract,
upstream callers and downstream consumers to inspect, a minimal disjoint file
set, and explicit checks. The worker may edit only that set. It must not decide
a scientific interpretation, modify `DYNAMIC_LEDGER.md`, change
`agent_roles.md`, close a council, or broaden scope. The parent reviews every
worker diff, runs the applicable verification gate, synthesizes the three
reports, and owns the final canvas record before the independent review stage.

## Council protocol

Use a council only for a real architectural crossroads. Before dispatch:

1. Confirm `COUNCIL.md` exists and read its header and live append anchor. If absent, follow the project rule to ask Ali to create it.
2. Read relevant current and archived rulings and define the one decision at issue.
3. Dispatch the seats assigned by `agent_roles.md` with their assigned reasoning effort, operational depth, claim-soundness lens, same decision question, and permitted write.
4. Let seats provide dialectic arguments, not a majority vote. The main session remains the technical decision owner; Ali closes or ratifies where governance requires it.
5. Re-ping only an unresolved point, never reflexively. Stop at the project-defined round limit. If material disagreement remains, write `DEADLOCK — ESCALATE TO ALI` rather than forcing convergence.

Every convene, response, ruling, retry, convergence, or deadlock is logged in `AGENT_CHANGES.md`. Only the main session or Ali writes `DYNAMIC_LEDGER.md`.

## Mandatory code-audit gate

Before trusting or running a code change touching more than two files:

1. Apply `codex-engineering-standards` and its Radon procedure first. For markdown, rule, or skill-only work, state that the Python gate is N/A.
2. Prompt the auditor to REFUTE the change and require APPROVE, APPROVE-WITH-NITS, or BLOCK with file:line evidence.
3. Require per-ruling PASS/FAIL checks against council decisions and pre-registered constraints.
4. Keep source read-only for the auditor. The auditor writes only its complete report; the parent implements fixes and re-gates.

## Research fan-out

For an open research question, assign independent directions rather than prescribing the answer. Watch for entropy collapse and re-seed with an orthogonal direction if needed. This does not relax the role limits, depth-1, no-compute-delegation, verification, council, or claim-soundness rules in `agent_roles.md`.

## Verbatim reports and evidence

Sub-agent output is evidence, not truth:

1. Require the auditor to append its full report verbatim to `AGENT_CHANGES.md` when the project protocol permits.
2. If the report returns unlogged, the parent transcribes it verbatim and says so; transcription is fallback.
3. Re-read the canvas head before every append and rebase if it moved.
4. Verify every file:line, number, and P0/P1 assertion against disk before relaying or acting on it.
5. The parent owns P0/P1 ledger entries, implementation decisions, role changes, and final adjudication.

## External-session preflight and memory import

Before any review using an external transport, apply
`$codex-external-agent-availability-preflight`. Re-read the current project
role file and its one root `external-agent-availability.md` immediately before
the hello and again before the substantive dispatch. Obtain the current
session handle through Ali's approved transient channel or through a document
Ali explicitly provides or identifies in the current instruction for the exact
dispatch. Verify that the document is current and scoped to the project, seat,
provider, and transport; it is provenance evidence only, never a roster or
authority override. Never discover the handle from an unprovided project file,
memory, log, prompt, old handoff, or historical registry. Honor the
handshake interval in the active `agent_roles.md` (including a two-minute wait
when that fallback policy specifies it). Verify that the session responds
without inspecting files or doing work. Start the maximum 30-minute review
window only after a substantive session is established. A blank clean return is
neither a substantive review nor a timeout. If the manifest or requested
external session cannot be opened or confirmed, classify it unavailable
promptly rather than waiting indefinitely. Record only the provider/seat label,
manifest status, transport result, and response status in the project log.

When an external seat is unavailable, apply the exact fallback in the active
`agent_roles.md`; do not invent a roster or substitute. Where that policy
authorizes a Codex fallback, use a separate configured fallback seat (or the
explicitly configured fallback model) for the missing bounded slot. If one fallback seat
covers multiple missing slots, require separately labelled analyses and
verdicts for each slot. Log every unavailable slot and substitution in
`AGENT_CHANGES.md`, including the candidate and scope, reason, substitute
model/seat, and resulting verdict. The fallback remains advisory evidence and
must never be represented as the original external reviewer.

For an Ali-authorized local memory import, use the bounded raw-Markdown path without blocking on `bundle.json`. Before importing, apply `codex-project-memory-protocol`: resolve the live current-project root, select its documented alias or exact root basename, prove that the destination namespace belongs to that project, check the namespace and its `MEMORY.md`, and initialize only that namespace plus the canonical index if absent. If any part of this preflight fails, classify the import `BLOCKED` and perform no memory operation; never use `extensions/ad_hoc/notes/` as a fallback. Then exclude backups, secrets, credentials, PII, raw transcripts, session handles, generated memory internals, and retired-provider material; preserve provenance and hashes; do not overwrite; and update only the destination namespace's `MEMORY.md` with relative same-namespace links. This exception does not authorize edits to platform-managed memory. Any hook is defense-in-depth, not a replacement for the protocol.

## Completion checklist

- [ ] The task was suitable for delegation and had a bounded, explicit output.
- [ ] A comprehensive task list recorded the deliverable, dependencies, seats,
      gates, evidence, recovery actions, and current status.
- [ ] The model and reasoning effort came from `agent_roles.md`; no extra seat was launched.
- [ ] Every prompt carried the depth-1 no-spawn clause and named the permitted write.
- [ ] Each review received the bounded 30-minute maximum window, and any
      unavailable or unreachable seat followed the role-file recovery policy.
- [ ] Source write scope was respected.
- [ ] The full report landed verbatim, or fallback transcription was labeled.
- [ ] Every fallback or replacement was explicitly labelled and logged with
      its missing slot, candidate/scope, reason, model/seat, and verdict.
- [ ] Load-bearing claims were verified against disk.
- [ ] Material post-review changes were re-audited, or the affected gate was
      explicitly left incomplete.
- [ ] Relevant Verification Gate, code audit, scientific-claim, citation, and canvas protocols were applied or marked N/A.
- [ ] P0/P1 findings were placed in `DYNAMIC_LEDGER.md` as required; completed seats marked disposable were closed when appropriate, and retained seats were preserved and reused unless the bounded unavailable/non-responsive recovery rule permitted a logged same-role replacement inside the current parent Codex task/thread.
