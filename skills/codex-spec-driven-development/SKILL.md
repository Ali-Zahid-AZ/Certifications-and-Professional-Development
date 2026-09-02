---
name: codex-spec-driven-development
description: Structure non-trivial work from intent through specification, traceable planning, implementation handoff, conformance, and drift checks while deferring to project governance and human authority.
---

# Codex Spec-Driven Development

Use this skill for non-trivial, ambiguous, architectural, multi-capability, or
feasibility work when the project uses a specification-driven lifecycle. It is
the single SDD entry point; its references are progressive-disclosure material,
not additional registered skills.

## Non-negotiable boundary

This skill is a workflow aid, not a source of authority. The active project's
rules, `AGENTS.md`, `agent_roles.md`, approved project documents, and the
current human instruction take precedence. This skill MUST NOT:

- approve a specification, plan, phase close, or council decision;
- authorize code edits, terminal state changes, commits, pushes, publication,
  spending, deletion, or external communication;
- assign seats, models, providers, transports, concurrency, or review roles;
- replace a missing or stale role file, availability manifest, project plan,
  ledger, canvas, or memory namespace; or
- weaken a project-specific restriction or turn a recommendation into policy.

If required governance is missing, stale, contradictory, or unavailable, stop
and report `HOLD` at the applicable boundary. If this skill is required by the
project but is not installed, report `HOLD`; do not silently substitute an
unregistered workflow.

## When to use it

Apply the lifecycle below after the project onboarding/preflight required by
the project rules. Do not force a heavyweight specification onto a genuinely
trivial mechanical change; classify that change and record the reason for the
lighter path when the project requires a durable record.

1. Resolve the project's authoritative rules, role source, current state
   carriers, and applicable local documentation protocol.
2. Classify the request using
   [scope and capability mapping](references/scope-and-capability-mapping.md).
3. For architectural, ambiguous, or multi-capability work, surface assumptions
   and open questions before treating the scope as settled.
4. Load the
   [specification contract](references/specification-contract.md) when a
   persistent specification, capability specification, or material requirement
   set is needed.
5. Obtain the project-defined specification approval before planning or
   execution. The skill records the required gate; it cannot satisfy the gate.
6. Hand approved specifications to the existing plan workflow, then decompose
   the approved plan into traceable tasks.
7. Use the
   [traceability, drift, and conformance](references/traceability-drift-and-conformance.md)
   reference at planning, review, verification, and closeout boundaries.
8. Stop on material drift, an unapproved requirement change, missing evidence,
   or an unresolved blocking question.

## SDD lifecycle

```text
intent
  -> scope classification
  -> capability map when multi-capability
  -> explicit assumptions and open questions
  -> approved specification
  -> approved technical plan
  -> traceable tasks
  -> separately authorized implementation
  -> requirement-linked verification evidence
  -> drift reconciliation and accepted project state
```

The lifecycle is conditional: a single-capability bounded change may use a
lightweight specification, while a feasibility spike has a narrow hypothesis,
exit condition, and explicit non-production boundary. Project-local rules may
require stricter artifacts.

## Existing workflow handoffs

These are companion routes, not a new authority hierarchy:

| Need | Route |
|---|---|
| Project onboarding and authoritative context | `$getting-acquainted-with-project` and the project rules |
| Frozen technical implementation plan | `$author-implementation-plan`, only after the required specification approval |
| Code quality and implementation verification | `$codex-engineering-standards` |
| Phase documentation and closeout | `$documentation-rules` and `$phase-closeout-documentation` |
| Append-only ledger, change, function, or council writes | `$canvas-write-protocol` |
| Delegated implementation or review | `$codex-subagent-orchestration`, only when the live role and current instruction authorize it |
| Project-memory operations | `$codex-project-memory-protocol` |
| Recording a genuinely converged council decision | `$record-council-convergence` |

Do not copy the detailed procedure from these routes into this skill. When a
handoff requires a compatibility field, use the exact approved specification
and capability identities rather than inventing a parallel vocabulary.

## Required final posture

Before calling specified work complete, identify each applicable acceptance
criterion, its implemented behavior or artifact, its concrete evidence, and a
verdict of `PASS`, `FAIL`, or `NOT VERIFIED`. Check both specification-to-code
and code-to-spec drift. A technical test passing is not, by itself, proof of
specification conformance.

Use the references only when their decision boundary applies:

- [scope-and-capability-mapping.md](references/scope-and-capability-mapping.md)
  for classification, capability decomposition, and assumptions;
- [specification-contract.md](references/specification-contract.md) for the
  persistent specification fields, requirement IDs, and review readiness; and
- [traceability-drift-and-conformance.md](references/traceability-drift-and-conformance.md)
  for plan/task links, material changes, drift, evidence, and completion.
