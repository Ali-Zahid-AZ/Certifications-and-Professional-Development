---
name: log-run-completion
description: Log a COMPLETED run/experiment to AGENT_CHANGES.md in the canonical tables-first format — one-line COMPLETE header with verdict + key numbers, per-probe sections (tables first, numbered analysis second), pipeline-integrity gate tables, and the four mandatory closers (Verification gate · Telemetry · Output path · Pending). Invoke when a compute run, experiment, ingestion, or long script finishes and its outcome must be recorded ("log the run", "record the results in AGENT_CHANGES"). Portable copy of the run-completion entry template — works even in projects that never deployed the doc templates.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: log-run-completion

## When to use
- A run/experiment/script has FINISHED (success, marginal, or failure) and its outcome goes into `AGENT_CHANGES.md` (or the project's hyphen-spelled `AGENT-CHANGES.md` — whichever exists).
- Composes with the observation-protocol skill: observation-protocol watches the run; this skill is its step-5 logging format in full detail.
- If the project ships its own `docs/documentation/templates/run-completion-entry-template.md`, that copy governs; this skill is the portable fallback and must stay consistent with it.

## Entry skeleton (copy, then fill)
```markdown
# [<YYYY-MM-DD HH:MM:SS PKT>] — <RUN NAME> COMPLETE — <one-line verdict + key numbers>

---

## <Probe/Stage 1 name>
| <metric> | <config/strategy> | <value> | <gate/threshold> | <verdict> |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

1. <Numbered first-principles analysis point — interprets the table, does not re-list it.>
2. ...

## <Probe/Stage 2 name>
(same shape — tables first, numbered analysis second)

## Pipeline-integrity gates
| Gate | Assertion (read-only) | Expected | Observed | Pass/Fail |
|---|---|---|---|---|

## Closers (all four, always)
- **Verification gate:** the **codex-engineering-standards** skill (canonical ruff invocation is `uv run ruff check --select F821,F811 <files>` from the project root, plus Radon) — result.
- **Telemetry:** peak VRAM · peak RAM · peak disk · wall-clock · seed(s).
- **Output path:** <exact artifact path(s) on disk>.
- **Pending:** <what awaits Ali / council / next phase — or "none">.
```

## Fill rules
1. **Timestamp** from the time MCP tool (Asia/Karachi), acquired immediately before the append; newest-at-top below the STRICTLY PROHIBITED line; concurrent-write inversion check.
2. **Header verdict is honest**: FAILED and MARGINAL gates are reported with their numbers, never smoothed over. A crashed run gets a COMPLETE-entry too (verdict: FAILED, traceback + log path).
3. **Tables first** — every result presented as a table before any prose; analysis is numbered and interprets, never re-lists.
4. **Every number traces to the on-disk artifact** (parse the JSON/ledger, don't trust stdout or memory); tag any estimate `[UNVERIFIED — reasoning only]`.
5. **Fill only applicable rows — never pad.** Omit sections that genuinely don't apply rather than inventing content.
6. **Config tagging:** every number is tagged with the configuration/strategy that produced it (quant level, residency, seed).

## Hard rules
1. The four closers are mandatory on every entry — an entry without Verification/Telemetry/Output/Pending is incomplete.
2. Append via the sanctioned write path — the **assertion-gated Python splice** (read the file → `assert text.count(anchor) == 1` → replace → verify the new head landed) — where native edits are guarded; `sed -i` forbidden.
3. Update DYNAMIC_LEDGER.md's task tag in the same pass ([IN_PROGRESS] → [DONE]/[BLOCKED]).
4. Restate a one-line result in chat after logging (Ali reads prose; the classifier reads message text).
