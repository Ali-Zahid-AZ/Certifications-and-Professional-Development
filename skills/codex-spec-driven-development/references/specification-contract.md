# Specification Contract

Use this reference for a persistent specification or a material requirement
delta. The specification describes WHAT and WHY, constraints, and acceptance;
the technical plan describes HOW. A technology belongs in the specification
only when it is itself a hard constraint.

## Required abstraction boundary

The specification must define externally meaningful behavior and the reasons
for it without prematurely forcing an implementation. It may state platform,
runtime, deployment, protocol, or interface choices when they are approved
constraints. Implementation sequence, file-level mechanics, and concrete code
edits belong in the approved plan and tasks.

## Persistent specification fields

Use only applicable sections; do not create filler.

1. **Metadata:** title, `SPEC-ID`, `CAPABILITY-ID` when applicable, status
   (`draft`, `under-review`, `approved`, or `superseded`), revision, accountable
   human, approval date, and supersession links.
2. **Objective and rationale:** what is being built, why it exists, the problem
   or opportunity, and the measurable outcome it supports.
3. **Users and consumers:** human users, internal services, external systems,
   and operational/support consumers.
4. **Current state/problem:** current behavior or limitation, supporting
   evidence, and why the current state is insufficient.
5. **Scope:** in scope, out of scope, deferred items, and non-goals.
6. **Functional requirements:** stable identifiers such as `REQ-001`; each
   requirement should be externally meaningful and testable.
7. **Non-functional requirements:** applicable latency, throughput,
   availability, durability, scalability, resource, recovery, maintainability,
   portability, observability, and determinism/reproducibility requirements,
   with identifiers such as `NFR-001`.
8. **Security and governance:** identity, authorization, privileged actions,
   secret handling, sensitivity, privacy, auditability, human approvals, and
   actions the system must never perform autonomously, using `SEC-###` where
   useful.
9. **Data and state semantics:** authoritative sources, ownership, schemas and
   invariants, state transitions, persistence, idempotency, replay/recovery,
   retention/deletion, and null/unknown/error semantics.
10. **Interfaces and integrations:** inputs, outputs, invariants, compatibility,
    error semantics, authentication, versioning, and upstream/downstream
    ownership.
11. **Failure and degraded mode:** dependency loss, incomplete or stale data,
    invalid requests, timeouts, resource limits, partial completion, duplicate
    effects, retries, and inability to establish confidence or safety.
12. **Constraints:** required platform/runtime, prohibited services, hardware
    envelope, regulatory or compatibility limits, deployment environment, and
    other approved hard constraints.
13. **Assumptions:** material but unproven assumptions, marked as blocking,
    risk-bearing, or scheduled for validation.
14. **Dependencies:** dependency, owner, required state/output, timing, and
    failure consequence.
15. **Success metrics:** project/business outcomes, engineering acceptance, and
    operational health metrics kept distinct.
16. **Acceptance criteria:** stable IDs such as `AC-001`; each criterion must
    support a meaningful `PASS`, `FAIL`, or `NOT VERIFIED` verdict.
17. **Capability boundaries:** capability-specific `Always`, `Ask first`, and
    `Never` behavior. These may tighten, never relax, project rules.
18. **Open questions:** unresolved material questions remain visible; blocking
    questions prevent approval unless the project’s named human authority
    explicitly accepts the recorded risk.
19. **Traceability:** parent capability, architecture decisions, plan/tasks, and
    verification evidence.

## Identity vocabulary

Use stable identifiers only where they improve traceability:

| Identifier | Meaning |
|---|---|
| `CAP-###` | Capability-map entry |
| `REQ-###` | Functional requirement |
| `NFR-###` | Non-functional requirement |
| `SEC-###` | Security/governance requirement |
| `AC-###` | Acceptance criterion |
| `TASK-###` | Executable implementation task |
| `ADR-###` | Architecture decision when the project uses ADRs |

## Specification review readiness

Before the project marks a specification approved, verify that:

- scope and exclusions are explicit;
- material assumptions and dependencies are visible;
- blocking ambiguities are resolved or explicitly accepted;
- requirements are internally consistent and measurable where applicable;
- acceptance criteria are testable;
- security, authorization, data/state, and degraded-mode behavior are defined
  where material;
- multi-capability work traces to an approved capability map; and
- the specification does not silently embed unjustified implementation choices.

The project’s named human authority performs any approval reserved to that
authority. This checklist does not approve the specification.
