---
name: "record-council-convergence"
description: Record a converged council decision in the project's canonical index and linked proposal while keeping the dated COUNCIL.md block as source of record. Use after a council converges.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: record-council-convergence

## When to use
- A council cycle has just converged ([CONVERGED — RECOMMEND CLOSE] written, or Ali has ruled) and the decision must be persisted beyond the council canvas.
- Also on re-tabulation passes: when the index has drifted from the council blocks and needs reconciling.
- NOT for un-converged debate — nothing is recorded until the block is converged/ruled.

## The two-place recording protocol
The dated council block (in `COUNCIL.md` or an archived `NN-COUNCIL.md`) is and remains the **source of record**. Derive exactly TWO artifacts from it:

1. **Index row** — append a status-tagged row to the project's canonical tabulated index (e.g. `research_directions.md`, a portfolio index, a decisions register):
   - Row carries: ID/name, one-line thesis, status tag, source-of-record pointer (council file + entry date), link to the proposal doc.
   - Rows are NEVER deleted — only re-tagged (e.g. ACTIVE → SHELF → RETIRED).
   - Summarize; do not duplicate the full prose into the index.
   - Bump the index's "Last tabulation: <PKT timestamp>" line (fresh time-tool acquisition).
   - On every tabulation pass, verify each source-of-record pointer resolves to a file on disk (plain exists-check); a pointer to a retired/renamed filename is drift — fix the pointer to the live archive path, never rename the archive to match it.
2. **Proposal/blueprint document** — a standalone detailed working document linked from the index row (see skeleton below). It expands the decision into an executable design; it is the working copy, not the record.

Then **log the tabulation pass** in the project's changes ledger (AGENT_CHANGES.md): which block was recorded, which row/tag, which proposal file.

If the council canvas being recorded is stamped `[CLOSED]` (or has grown past ~150KB), the same pass also proposes its rotation into the archive tree (`docs/documentation/.../NN-COUNCIL.md`) as a `[PENDING]` ledger row — per the global rotation rule, "may be archived" with no trigger means it never happens.

## Precedence chain (state it in every derived artifact)
> On any conflict, the dated council block wins; the index summarizes; the proposal is the expanded working blueprint.

Each proposal opens with a status banner declaring exactly this: status tag + source-of-record pointer + conflict precedence.

## Proposal/blueprint skeleton (the S1/S2-class format)
Treat this as a **contents checklist**, not a rigid ordering — practiced proposals vary structure without harm. Cover every item that applies; omit what genuinely doesn't (and say so).

1. **Status banner** — status tag, source of record, precedence clause.
2. **One-line thesis.**
3. **Origin & motivation** — Ali's seed question + axiom/portfolio hooks.
4. **Pre-registered hypotheses** — H1/H2/H0, per the global research-epistemics rule (name the prior, do not smuggle the conclusion; correlated nulls are one bet).
5. **Prior art & scoop position** — risk level (LOW/MED/HIGH) + an explicit CARVE table: what the nearest neighbour covers vs what THIS covers.
6. **Model/tool selection** — with a disqualification table against stated constraints.
7. **Instruments** — primary vs illustration-only.
8. **Experimental design.**
9. **Hardware feasibility** — against the machine envelope, with a ~30% safety buffer + effort estimate (estimates tagged `[UNVERIFIED — reasoning only]`).
10. **Deliverables.**
11. **Risks & mitigations table.**
12. **Portfolio relation & sequencing.**
13. **References** — split ✅ verified (raw-read) / unverified / to-verify-at-unfreeze; carry verification debt explicitly; keep hallucinated-citation flags inline ("⚠ hallucinated — do not cite"), never silently drop them.

If the decision is deferred behind a gate, the closing entry must include the cold-open execution brief (per the global rule): reopen-cold summary + ordered first-actions-on-unfreeze + entry/exit/kill criteria. The freeze checklist also includes a **sibling-corrections check**: sweep sibling projects sharing this domain for ratified corrections the converged decision supersedes, and re-point/annotate any live restatements rather than leaving stale guidance live elsewhere.

## Hard rules
1. The council block is immutable once converged — recording NEVER edits it.
2. Recording a decision does NOT lift any active freeze/stop-loss (global gate-governance rule).
3. Index rows are append/re-tag only; fresh tool-acquired PKT timestamps on every pass.
4. Two places, no more — do not scatter the decision into additional summaries that can drift.
5. Log every tabulation pass in AGENT_CHANGES.md; commits remain Ali-only.
6. If the target project is the Obsidian vault, `vault-safe-note-editing` also governs every write this skill makes (note budget, frontmatter merge keys, AI-MODIFIED comments).
