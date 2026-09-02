# Traceability, Drift, and Conformance

Use this reference when moving from an approved specification to a plan,
tasks, implementation evidence, review, or phase close.

## Traceability chain

```text
requirement
  -> architecture/design decision
  -> implementation task
  -> code/configuration/infrastructure
  -> verification evidence
  -> acceptance criterion
```

Plans and tasks should identify the exact approved `SPEC-ID`, revision,
`CAPABILITY-ID` when applicable, and the requirement/acceptance IDs they cover.
Verification evidence must identify the criterion it proves. Unmapped behavior
is a review signal: classify it as required infrastructure, accidental scope,
or an undocumented requirement.

## Plan handoff

Only after the project-required specification approval should the technical
plan be produced or frozen. Use `$author-implementation-plan` for the plan’s
own mechanics, and require the plan to retain this SDD bridge:

- approved specification identity and revision;
- covered requirements and acceptance criteria;
- architecture and component boundaries;
- affected code paths, interfaces, data/state lifecycle, dependencies, and
  security implications;
- implementation sequence and justified parallelism;
- risk, rollback/recovery, observability, and verification checkpoints; and
- expected files/modules and unresolved implementation questions.

Planning must not silently change requirements, scope, success criteria,
acceptance criteria, or security boundaries. If it exposes a specification
defect, stop, update the specification through the project’s approval path,
then revise the plan and tasks.

## Task decomposition

Each executable task should include:

- a stable `TASK-###` when useful;
- description and dependencies/prerequisites;
- expected files or modules;
- requirement and acceptance IDs satisfied;
- explicit acceptance condition and verification method; and
- risk/rollback notes when material.

Size tasks by coherent responsibility and dependency boundaries. Do not split a
cross-file atomic change arbitrarily, and do not hide an architectural change
inside a task labeled “small.”

## Material changes and living specifications

Treat a change as material when it alters externally observable behavior,
scope/non-goals, acceptance criteria, security or authorization, data ownership
or semantics, an interface relied on by another component, persistence/state
lifecycle, an operational requirement, architecture/deployment risk, resource
envelope, or a risk-bearing assumption. When uncertain, treat it as material.

If evidence reveals that approved behavior, assumptions, interfaces,
constraints, or acceptance criteria must change:

1. stop the affected implementation;
2. identify the evidence forcing the change;
3. update the specification first;
4. record the first-principles reason;
5. obtain the project-required approval of the specification delta;
6. update the plan and tasks if affected; and
7. repeat every affected gate before resuming.

Never edit the specification after the fact merely to legitimize already
implemented behavior.

## Drift check

Review both directions:

- **Specification to code:** every approved requirement for the phase has an
  implementation and evidence.
- **Code to specification:** every material behavior introduced by the change is
  justified by the approved specification or explicitly classified as required
  infrastructure.

Examples include an unimplemented requirement, an undocumented security rule,
tests asserting behavior outside the specification, an unplanned dependency,
or acceptance criteria that no longer match observed behavior. Material drift
means `HOLD` until reconciled through the project’s approval path.

## Conformance evidence

For every applicable acceptance criterion, record:

| Field | Required content |
|---|---|
| Criterion | Exact `AC-###` and approved specification revision |
| Implemented behavior/artifact | What was produced or changed |
| Evidence | Reproducible command, observation, artifact, or test result |
| Verdict | `PASS`, `FAIL`, or `NOT VERIFIED` |
| Deviation | Any difference from the approved specification |

Any criterion without evidence is `NOT VERIFIED`. A failed mandatory criterion
blocks completion unless the project’s named human authority explicitly accepts
the recorded risk. Technical tests do not replace conformance evidence.

Evidence should be reproducible, tied to the exact version/configuration when
material, deterministic where practical, specific to the criterion, and
preserved or referenced in the project’s required closeout artifacts.

## HOLD conditions

Stop and surface the issue when:

- implementation starts before material ambiguity or required approval is
  resolved;
- planning changes behavior without a specification delta;
- one specification hides independently testable capabilities;
- acceptance cannot produce meaningful evidence;
- implementation introduces undocumented business or security behavior;
- tests prove implementation detail but not the specified outcome;
- mandatory criteria remain `NOT VERIFIED`;
- an architecture decision has no traceable requirement or rationale;
- code is changed first and the specification is rewritten afterward;
- an installed workflow conflicts with project governance; or
- a reviewer recommendation is treated as authority without the required human
  decision.

## Completion handoff

A specified phase or task is not complete merely because code exists or tests
pass. The project must have applicable implementation, technical verification,
criterion-level conformance evidence, no unresolved material drift, required
operational evidence, required local canvas/documentation updates, and explicit
recording of unresolved risks or deviations. Any completion action reserved to
the project’s named human authority remains reserved.
