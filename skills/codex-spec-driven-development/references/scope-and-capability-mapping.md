# Scope and Capability Mapping

Use this reference to choose the lightest workflow that still makes the
decision boundary and completion evidence explicit. Project-local rules may
require a stricter path.

## Scope classes

| Class | Use when | Minimum durable result |
|---|---|---|
| A — trivial/mechanical | Typo, formatting, comment, rename with no behavior or contract change | Normal project change record; no new capability specification unless local rules require one |
| B — bounded change | One bounded behavior or component changes, with clear scope and observable acceptance | Lightweight specification or requirement delta, explicit exclusions, acceptance criteria, and a plan when implementation is non-trivial |
| C — architectural/new capability | New behavior, subsystem, interface, state lifecycle, security boundary, or materially changed architecture | Persistent specification, approval evidence, technical plan, traceable tasks, and conformance evidence |
| D — feasibility spike/investigation | The purpose is to answer a bounded feasibility question rather than deliver production behavior | Hypothesis, method, resource/ safety envelope, stop or success condition, evidence destination, and explicit non-production boundary |
| E — multi-capability modifier | The request contains two or more independently testable capabilities | An approved capability map first, then one scoped specification per capability unless the project explicitly approves another structure |

When uncertain between classes, classify upward until the risk is resolved. Do
not use a “small fix” label to hide a change to interfaces, data/state
semantics, security, architecture, or external behavior.

## Capability map gate

For multi-capability work, create a map before capability-level specifications.
Each entry should identify:

| Field | Required meaning |
|---|---|
| Capability ID | Stable identifier, for example `CAP-001` |
| Name and objective | The independently testable outcome |
| Owner/consumer | Accountable human and affected users or systems |
| Scope | In-scope behavior, explicit non-goals, and deferred work |
| Dependencies | Required upstream state, outputs, timing, or ownership |
| Interfaces/state | Shared contracts, persistence, and lifecycle boundaries |
| Acceptance | Observable completion conditions and evidence destination |
| Risks/open questions | Blocking assumptions and unresolved material questions |
| Sequence | Required ordering or justified parallelism |

The map must make dependencies and shared integration points visible. A
capability may not be treated as independently complete when its acceptance
depends on an unapproved sibling capability or an unresolved shared contract.

## Assumptions and clarification

Before approval, surface assumptions that materially affect scope, security,
data meaning, architecture, schedule, cost, resource envelope, or acceptance.
For each assumption, record:

- the assumption and its source;
- whether it is blocking, risk-bearing, or scheduled for validation;
- the evidence that would confirm or falsify it; and
- the owner and timing when those are material.

Do not silently choose product behavior, security behavior, data ownership,
failure semantics, or an implementation constraint merely because it seems
obvious. Ask or record an explicit project decision. Unresolved blocking
questions keep the specification in `HOLD` or `under-review` status.

## Default artifact layout

Unless the project declares a different convention, a multi-capability effort
may use:

```text
specs/
├── CAPABILITY_MAP.md
├── <capability-id>/
│   ├── SPEC.md
│   ├── PLAN.md
│   └── TASKS.md
└── <another-capability-id>/
    └── ...
```

Do not create a capability map for genuinely single-capability work. Project
path conventions override this default. Do not overwrite an active plan with a
phase-close archive; active planning artifacts and immutable completion records
serve different purposes.
