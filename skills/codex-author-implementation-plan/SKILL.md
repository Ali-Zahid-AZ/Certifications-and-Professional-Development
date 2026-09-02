---
name: author-implementation-plan
description: Author a frozen, ratified, per-version implementation plan under the plan-first freeze contract. Use when drafting or freezing a build-phase implementation plan.
---

# Skill: author-implementation-plan

## When to use
- A new version/phase needs its build contract before implementation starts ("write the V<N> plan", "freeze the plan for stage 3").
- After a council convergence or an audit, when rulings/fixes must be folded into a fresh frozen plan.
- NOT for ad-hoc small tasks — those use the normal ToDo protocol.

## The freeze-then-implement contract
The plan is authored, audited, ratified, then FROZEN — implementation begins only against the frozen text. Post-freeze changes happen only via an explicitly logged amendment (never silent edits).

## Standard header block (top of the document)
```
> **Author:** <implementing agent> (role)
> **Architecture + Audit:** <auditing agent> (verdict, e.g. "CONDITIONAL APPROVE, 6 corrections")
> **Rulings:** Ali (D1–D<n> ratified at <HH:MM PKT>)
> **Status:** PLAN FROZEN — Awaiting Implementation
> **Depends On:** <V(N-1) completion + review / COUNCIL consensus window>
> **Parent plan:** <path to the canonical parent doc>
```
The `Depends On` line operationalizes the global Version Coupling rule: V(N+1) may not begin until V(N) outputs exist and are reviewed.

## §0 — Pre-Flight: Constraints & Non-Negotiables (always the first section)
A table `C1..Cn` with columns **Constraint | Source | Consequence**, prefaced by:
> *Every architectural decision below traces to one of these.*

Sources cite ruling/audit IDs + PKT timestamps (e.g. "D3 ratification (20:17 PKT)", "independent assurance audit B1 (20:54 PKT)").

## ID-ledger vocabulary (use throughout the project, not just the plan)
| Prefix | Meaning | Example |
|--------|---------|---------|
| `C#` | Constraint / non-negotiable | C1 batch-phasing |
| `D#` | Ali ruling (ratified, PKT-timestamped) | D1–D4 ratified at 20:17 PKT |
| `B#` | Auditor-found bug/fix | B4 mapper fix |
| `G#` | Verification gate | G8 = 138,642 rows |
| `WS#` | Workstream | WS3 first |

Every decision in any doc cites its ruling ID + PKT timestamp. This gives every line of the system traceable provenance to a ruling or audit finding.

## Body structure
1. **Delta vs previous version** — a table of what changes relative to V(N-1) (and why).
2. **Workstreams & build order** — WS1..WSn with an explicitly justified order ("Why WS3 first: ..."). Each workstream: scope, target artifacts split into *New Files (Create)* / *Source Data (Read-Only)* / *Existing Files (Not Modified — Referenced Only)*, verification gates (G#), owner.
3. **Verification & exit gates** — the G# battery that must pass before the version closes (read-only assertions per the Non-Destructive Testing Mandate).
4. **Time estimates** — per-workstream table (Task | What | Why | Est. time + total), `[UNVERIFIED — reasoning only]` where not measured.
5. **Risks & rollback.**

## Workflow
1. Gather inputs: council rulings (D#), audit findings (B#), constraints (C#), the previous version's outputs and review verdicts.
2. Draft the plan with the header, §0 constraints table, and body structure above.
3. Route for audit — typically the `audit-codebase` skill or the auditor seat assigned in `agent_roles.md`; fold corrections in as B#-cited updates.
4. Present decision questions to Ali in chat (plain prose, ~3-line gist + questions); on ratification, stamp the D# line with the exact PKT time from the time tool.
5. Set Status to PLAN FROZEN, log the freeze in AGENT_CHANGES.md, and re-tag the ledger task.

## Definition of done (disk-asserted)
- [ ] The plan file exists at its canonical path with the full header block (Author / Architecture+Audit / Rulings / Status / Depends On / Parent plan).
- [ ] §0 constraints table present; every C# row carries Source + Consequence.
- [ ] Every architectural decision in the body cites a C#/D#/B# ID — grep for un-cited decisions before freeze.
- [ ] Time-estimate table present; unmeasured estimates tagged `[UNVERIFIED — reasoning only]`.
- [ ] Freeze logged in AGENT_CHANGES.md (fresh PKT) and the ledger task re-tagged.

## Hard rules
1. No implementation before the freeze; no silent edits after it (amendments are logged, cited, and versioned — bump `Document version`).
2. Every architectural decision traces to a C#/D#/B# entry — untraceable decisions are flagged, not smuggled.
3. Header + `Parent plan:` pointer are mandatory (global versioned-doc header rule).
4. Fresh tool-acquired PKT timestamps on ratification/freeze lines; never guessed.
5. Only Ali ratifies (D#) and only Ali declares the version complete.
