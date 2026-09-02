---
name: ops-handoff-docs
description: Author the production/client handoff documentation set — the ops quartet (kill-switch-first runbook, gated go-live checklist, monitoring-and-SLOs, test strategy) plus the root compliance/PRIVACY/SECURITY trio, and the two external-audience formats (client-dev review guide, vendor/FDE brief). Invoke when a build approaches go-live or must be handed to client developers, reviewers, or a vendor ("write the runbook", "go-live checklist", "prepare the dev review guide", "brief the vendor").
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: ops-handoff-docs

## When to use
- A production/client automation is approaching go-live, or its operation must be handed to people who did not build it.
- A client's developers must review the build, or a vendor/FDE consult needs a scoped brief.
- Documents live in `docs/documentation/ops/` (quartet) and `docs/documentation/dev/` (review guides), markdown as source of record (`markdown/` + rendered `html/`/`pdf/` siblings for client delivery).

## The ops quartet (`docs/documentation/ops/`)

### 1. `runbook.md` — kill-switch-first
- Open with a **Golden rule** callout: safe-state control first — e.g. *"stop calling first, diagnose second"*. Whatever the system does to the outside world, the FIRST instruction is how to make it stop safely.
- **§0 Quick reference card** — table: *Need to… | Do this | Section*.
- **§1 System topology (what can break)** — table enumerating each component and its failure surface.
- **§2 The master kill-switch** (most important control) — what it is, exact effect, disable steps, re-enable conditions with a NAMED approver.
- **§3 Severity & response tiers** — what counts as SEV1/2/3, response path per tier.
- Then per-failure diagnosis/recovery sections.

### 2. `go-live-checklist.md` — gated
- **§0 Pre-flight gates (must ALL be green)** as checkboxes, each gate pointing at a NAMED artifact: validation report path, `compliance.md` legal sign-off, `PRIVACY.md` open items closed, `SECURITY.md` secrets plan, owner approval, change window.
- Promote-inventory table (exactly what flips from Draft/sandbox to live).
- Rollback path (how to get back, verified before go-live, not during the incident).

### 3. `monitoring-and-slos.md` — what is watched, thresholds, who is paged, dashboards/log locations. Where the project has a platform health protocol, author this via the `generate-platform-health-protocol` skill — it owns the monitoring/health-check doc pattern; this quartet entry is the ops-facing summary of it.
### 4. `test-strategy.md` — what is tested at which layer, what is deliberately NOT automated (per the Non-Destructive Testing Mandate), and how test artifacts are tagged/stored.

Root trio referenced by the quartet: `compliance.md`, `PRIVACY.md`, `SECURITY.md` (secrets are never in docs — "held securely, never shared in docs").

## External-audience formats (`docs/documentation/dev/`)

### Client-dev review guide
1. **§1 How to use this document** — prescribed reading order ("Read §3 first…").
2. **§2 The system in one paragraph** + the ~3 design rules that constrain every component.
3. **"What is triggering what"** table — exact API names + activation state (call out anything intentionally Draft/disabled).
4. Per-stage sections mirroring the build stages.
5. **Consolidated gotchas list** — as-built naming quirks and traps, each one a real trap actually hit.
6. The custom-code component(s) isolated in their own section for focused review.
7. **Flat API-name index** — labeled "single source of truth".
8. Reviewer checklist.

### Vendor/FDE brief
- Header: For / From / Re / Date / Scope.
- **TL;DR for the consult** blockquote.
- **What we already built** (pre-empts scope creep).
- The exact API contract in use.
- **Numbered asks** list.
- Explicit out-of-scope section; state that secrets are never in docs.

## Workflow
1. Establish audience + go-live date; pick which of the six docs are needed (not every project needs all).
2. Author from the running system, not from memory — verify every API name, toggle, and path on disk/in the org before writing it.
3. Every factual claim about external platforms cites its raw-read source URL (global claim-level citation rule).
4. Render html/pdf siblings for client-delivered docs; verify links/basenames match.
5. Log the doc set in AGENT_CHANGES.md; versioned-doc headers (version/created/updated/status/parent-plan) on every doc.

## Handoff checklist (disk-asserted definition of done)
Mirrors `phase-closeout-documentation`'s pattern — every box is asserted from disk (`find`/Read), never from memory:
- [ ] Every selected doc (of the six) exists at its canonical path (`docs/documentation/ops/…` / `docs/documentation/dev/…`); markdown source of record present, rendered siblings present where client-delivered.
- [ ] Every go-live gate in `go-live-checklist.md` points at a NAMED artifact that exists on disk / in the org — path checked, not assumed.
- [ ] The runbook opens with the kill-switch/safe-state section (section order verified from the file).
- [ ] No secrets/tokens/credentials in any handoff doc — grep the doc set for credential patterns before delivery.
- [ ] Versioned-doc headers (version/created/updated/status/parent-plan) present on every doc; the doc set is logged in AGENT_CHANGES.md.

## Hard rules
1. Kill-switch/safe-state section is ALWAYS first in a runbook — never bury it.
2. A go-live gate without a named artifact behind it is not a gate — fix or remove it.
3. No secrets, tokens, or credentials in any handoff doc, ever.
4. Gotchas must be real (observed), not speculative padding.
5. Commits/pushes and the go-live action itself remain Ali-only.
