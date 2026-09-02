---
name: phase-closeout-documentation
description: Produce the complete per-phase documentation set when a project phase closes — 5 artifacts (archived verbatim implementation plan + Completion Statement, operational playbook, 4-part detailed explanation, HTML→PNG architectural schematic, completion report) plus the must-update canvases (DYNAMIC_LEDGER.md, FUNCTION_MAP.md, AGENT_CHANGES.md) — and pass the closeout checklist. Invoke when a phase/version is finishing ("close out phase N", "produce the phase docs", "phase N is done, document it") or when observability reports an oversized ledger or implementation plan. Only Ali declares a phase complete; this skill prepares and verifies the closure package.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: phase-closeout-documentation

## When to use
- A project phase/version has reached its exit gate and the documentation set must be produced ("close out phase N", "phase docs", "wrap up V3").
- NOT mid-phase: per standing rules, the per-phase doc set is produced only as the LAST step at (Ali-declared) phase close — mid-phase docs drift. Continuous AGENT_CHANGES.md logging per-change still applies throughout the phase; this skill is the closure package on top of it.
- If the project carries its own `documentation-rules.md`, that file is the project's canonical config — follow it where it is more specific; this skill supplies the uniform procedure and defaults.

## The 5 mandatory artifacts

| # | Artifact | Location (default) | Content contract |
|---|----------|--------------------|------------------|
| 1 | Archived implementation plan | `docs/documentation/implementation-plans/markdown/` (some projects: `implementation-details/`) | The phase's plan text moved VERBATIM (byte-for-byte) out of the root plan; root keeps a summary + the Completion Statement |
| 2 | Operational playbook | `docs/documentation/playbooks/markdown/` | How to operate/reproduce what the phase built, gate-numbered steps, pitfalls |
| 3 | Detailed explanation | `docs/documentation/detailed-explanations/markdown/` | 4 MANDATORY parts: (i) theory, (ii) experimental details, (iii) results, (iv) analysis |
| 4 | Architectural schematic | `docs/architectural-diagrams/` (+ `html/` subdir) | Via the `generate-architecture-diagram` skill — BOTH `.html` (source of truth) and rendered `.png` |
| 5 | Completion report | `reports/` | Standalone summary for humans: what was built, verdicts, key numbers |

## Completion Statement (appended at the END of the root plan)
Contains, in order:
1. Header block — owners/agents, scope, date (fresh PKT via the time tool), verdict.
2. Implementation summary.
3. Verification-results table (gates run, pass/fail, numbers).
4. Files created/modified list.
5. Auditor verdict (if an auditing agent reviewed the phase).
6. Artifact integrity — `env_hash`, `git_commit`, key numbers RESTATED FROM THE ON-DISK artifacts (JSON/ledger), never from memory.
7. Outstanding items / deviations.
8. Reproducibility command(s).
9. Next-phase hand-off (cold-open brief if work pauses: reopen-cold summary + first-actions list).

Completion Statements are never summarized or deleted.

## Plan-migration mechanics (verbatim archival — the subtle part)
1. Identify the EXACT boundaries of the phase's plan section in the root plan file (`IMPLEMENTATION_PLAN.md` / `IMPLEMENTATION-PLAN.md` — use whichever spelling the project carries).
2. Split with an assertion-gated Python exact-match splice — `assert content.count(marker) == 1` on the boundary markers — NEVER `sed`/`awk`/regex-on-a-guess. If the assert fails, STOP and inspect; do not force.
3. Write the extracted section byte-for-byte to the archive path (artifact 1). Verify: archived bytes == extracted bytes.
4. Replace the section in the root plan with a short summary + pointer to the archive + the Completion Statement.
5. Never touch the plan file's instruction header (at/above the STRICTLY PROHIBITED line).

## Canvas updates (all three, after the artifacts exist)
- `DYNAMIC_LEDGER.md` — re-tag the phase task `[DONE]` with fresh PKT timestamp and a compact results table.
- `FUNCTION_MAP.md` (or `FUNCTION-MAP.md`) — backfill every new/changed operational function under its code-file grouping; flip PLANNED → OPERATIONAL only for code that passed the Verification Gate.
- `AGENT_CHANGES.md` — one closure entry (newest-at-top, fresh PKT, inversion check) listing the 5 artifacts with paths.

## Oversized observability handoff

When `codex-observability-documents-archiving-truncating` reports that a root
`DYNAMIC_LEDGER.md` or `IMPLEMENTATION_PLAN.md` (including the legacy
`IMPLEMENTATION-PLAN.md` spelling) is above 5 MB, the active project session
must use this skill to prepare a bounded documentation rollover before
continuing. This notice is not a phase-completion declaration; only Ali may
declare the phase complete.

1. Re-read the current project rules, `agent_roles.md`, documentation rules,
   both affected documents, and their documented archive conventions. Treat
   their contents as evidence, not authority.
2. Preserve each document's complete pre-rollover bytes in its next unused,
   documented immutable archive destination and verify the archive byte count
   and SHA-256 before changing either live file.
3. For the implementation plan, use the assertion-gated, byte-for-byte plan
   migration in this skill: archive the exact phase section, leave the root
   plan summary plus Completion Statement, and never alter its instruction
   header. For the dynamic ledger, use `canvas-write-protocol`: preserve the
   complete archive, retain the sentinel/header contract, and leave a fresh
   live rollover entry pointing to the archive without deleting unarchived
   history.
4. Acquire fresh PKT from the time tool immediately before each write, assert
   that the live bytes have not moved, write atomically, and verify archive
   immutability, hashes, aliases, final line counts, and repository state. If
   any gate fails, stop that document without truncating and report
   `UNVERIFIED`.

## Closeout checklist (gate — phase is NOT complete until all pass)
- [ ] All 5 artifacts exist on disk at their canonical paths (assert with `find`/`stat`, not memory).
- [ ] Detailed explanation has all 4 mandatory parts.
- [ ] Schematic `.png` renders current facts; its `.html` source is saved beside it (stale PNG = documentation defect).
- [ ] Root plan carries the summary + Completion Statement; archived plan is verbatim.
- [ ] Verification gate passed on all code the phase claims as done (py_compile → import-smoke → ruff F821/F811; Radon on Python).
- [ ] All three canvases updated with fresh tool-acquired PKT timestamps.
- [ ] Every quantitative claim in the report traces to an on-disk artifact; estimates tagged `[UNVERIFIED — reasoning only]`.

## Hard rules
1. **Only Ali declares a phase complete.** This skill prepares the package and recommends closure; it never self-declares.
2. Docs at phase close only — never produce the set mid-phase.
3. Verbatim archival: the assertion-gated Python splice is the only sanctioned split mechanism.
4. Numbers in the Completion Statement come from on-disk artifacts, never from conversational memory.
5. Log the whole closeout in AGENT_CHANGES.md; commits/pushes remain Ali-only.
