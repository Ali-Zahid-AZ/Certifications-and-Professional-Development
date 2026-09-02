---
name: audit-agents-changes-log
description: Per-version forensic audit of AGENT_CHANGES.md — structural integrity, code cross-referencing, FUNCTION-MAP/IMPLEMENTATION-PLAN sync, change-group verdicts, and omission detection. Invoke when Ali explicitly requests an audit of the change log ("audit AGENT_CHANGES", "audit the changes log").
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# What I Do

I execute a deterministic, phased audit of the project's `AGENT_CHANGES.md` — the canonical change log. I do not audit source code quality. I audit whether the change log is truthful, complete, consistent with the codebase, and synchronized with `FUNCTION_MAP.md` (or `FUNCTION-MAP.md` in legacy projects — read whichever exists) and `IMPLEMENTATION_PLAN.md` (or `IMPLEMENTATION-PLAN.md` in legacy projects — read whichever exists). Every change group receives a verdict, every entry is cross-referenced against static code, and every undocumented gap is flagged as a finding.

# When To Use Me

Use this when the user explicitly requests an audit of `AGENT_CHANGES.md`. I produce a standalone audit report as a timestamped markdown artifact in `audits/agent-changes-md-audits/markdown`.

---

# Phase 1 — Scope & Discovery

Before analyzing a single entry, load the full context boundary.

> **Sync note:** this skill shares its severity ladder, output conventions, and agent-name rules with `audit-codebase` — when revising either skill, revise both.

1. **Read `AGENT_CHANGES.md`** (project root; a few legacy projects still use the hyphen name `AGENT-CHANGES.md` — read whichever exists) — load the complete change history into working memory. Note the timestamp range (oldest to newest) and total entry count.
2. **Read `FUNCTION_MAP.md`** — load the declared function registry. This is the ground truth for function existence.
3. **Read `IMPLEMENTATION_PLAN.md`** — load the version/sprint boundary map. This defines what each version was supposed to deliver.
4. **Read `AGENTS.md`** from `.agents/rules/` — absorb project-level rules about change-log format (timestamp requirements, PKT enforcement, entry structure).
5. **Map the file tree** — use `codegraph_codegraph_files` to get the full project structure. This is the ground truth for file existence.
6. **Identify change groups** — parse `AGENT_CHANGES.md` into logical groups. Groups are determined by sprint/version boundaries (e.g., `## V6 Bayesian Analysis`, `### Sprint 1 — Experiments 1, 4, 7`). If no explicit sprint headings exist, group by continuous date ranges that share a common feature or version tag.
7. **Load key source files** — for each referenced source file in the change log, read only its signature map (via CodeGraph — `codegraph_codegraph_node`). Do not read full bodies unless a specific finding requires deep verification.

---

# Phase 2 — Systematic Analysis (10 Audit Domains)

Execute these domains **in order**. Do not skip any domain. For each, use the appropriate tools (CodeGraph for structure, native Read/Grep for content) and document every finding.

## Domain 1: Structural Integrity

Verify the file itself is well-formed and follows project conventions.

- Are entries in **reverse chronological order** (newest first)?
- Are all timestamps in **PKT** timezone as required?
- Are timestamps monotonically decreasing? Flag any out-of-order entries.
- Are version/sprint headings consistent and properly nested?
- Are there any duplicate timestamps or overlapping date ranges?
- Is the file encoding UTF-8? Are there any corrupt characters or broken markdown?
- Are there any entries that lack a timestamp entirely?

## Domain 2: Entry Completeness

Every change entry must contain certain fields. Audit each entry against this checklist:

- **Timestamp** present and in `YYYY-MM-DD HH:MM:SS PKT` format?
- **Action/Brief** — one-line description of what was done?
- **Files Modified** — absolute or relative paths to changed files?
- **Root Cause / Rationale** — WHY the change was made?
- **Verification / Outcome** — how was the change verified?
- **Cross-references** — does it reference related issues, PRs, or prior entries?

Flag any entry missing 2+ of these as a **P3** finding. Flag any entry missing 4+ as **P2**.

## Domain 3: Code Cross-Reference

Every referenced file path and function name must actually exist in the codebase.

- For every file path mentioned in an entry: does the file exist on disk (using Glob or CodeGraph)?
- For every function/method mentioned: does the symbol exist in the current codebase (using `codegraph_codegraph_search`)?
- For every line number mentioned: does that line exist in the referenced file?
- For every symbol that was "added" or "created": does it exist on disk now?
- For every symbol that was "removed" or "deleted": is it actually gone from the codebase?

Flag any mismatch as a **P1** finding (the entry claims a change that doesn't match reality).

## Domain 4: FUNCTION_MAP.md Sync Status

Cross-reference every function-level change against `FUNCTION_MAP.md`.

- For every function "added" or "created" in a change entry: is it documented in `FUNCTION_MAP.md`?
- For every function "removed" or "deprecated": is it removed from `FUNCTION_MAP.md`?
- For every function signature change: is `FUNCTION_MAP.md` updated to reflect the new signature?
- Are there functions in `FUNCTION_MAP.md` that have no corresponding change entry in `AGENT_CHANGES.md`?

Flag any drift as follows:
- Missing new function documentation: **P2**
- Stale function entry (function deleted but still in FUNCTION-MAP): **P2**
- Entire function map out of sync by 5+ entries: **P1**

## Domain 5: IMPLEMENTATION_PLAN.md Sync Status

Cross-reference every version/sprint change against `IMPLEMENTATION_PLAN.md`.

- Does every version/sprint mentioned in the change log appear in the implementation plan?
- Does every delivered feature in the implementation plan have a corresponding change entry?
- For entries marked as "bug fix": does the implementation plan document the bug?
- Are there version headings in `IMPLEMENTATION_PLAN.md` marked as "complete" that have no corresponding entries in the change log?

Flag any drift:
- Missing version in implementation plan: **P2**
- Implementation plan claims delivery but no change log entry exists: **P1**
- Bug fix with no corresponding issue in implementation plan: **P3**

## Domain 6: Change Group Quality

For each change group (sprint/version), produce a structured assessment:

1. **Group identification** — version number, date range, number of entries.
2. **Verdict** — exactly one of: `✅ Right changes` (correct, complete, well-documented), `⚠️ Mostly right` (minor issues or omissions), `❌ Wrong changes` (incorrect approach, regressions introduced).
3. **Entry-by-entry assessment** — for each entry in the group:
   - **Claim:** What the entry says was done.
   - **Verification:** Does the codebase confirm this claim?
   - **Assessment:** 1-3 sentence first-principles analysis of whether the change was the correct approach.
   - **Issues:** Any problems found (missing detail, incorrect claim, cross-ref failure).
4. **Group-level summary** — aggregate assessment of the group's quality.

Every entry in every group must receive an Assessment. No skips.

## Domain 7: Cross-Version Regression Detection

Identify changes in later versions that may have broken invariants established by earlier versions.

- Did a later version delete or rename a function that an earlier version depends on?
- Did a later version change an API contract (signature, return type) that an earlier version's callers expect?
- Did a later version remove configuration, environment variables, or infrastructure that an earlier version requires?
- Are there two entries that claim to fix the same bug (suggesting incomplete fix)?

Flag any regression as **P1**. Flag any recurring bug pattern (same issue fixed 3+ times) as **P0**. **Disambiguation (score a cluster ONCE, under whichever fits):** *same issue* = the identical defect at the same locus (same root cause, same function/file) re-fixed 3+ times — the fix is not sticking → **P0**; *same category* = 3+ DISTINCT bugs sharing a defect class (e.g. import errors) at different loci → **P1** (systemic weakness).

## Domain 8: Bug Fix Pattern Analysis

Analyze the nature and recurrence of bug fixes.

- Categorize each bug fix: integration bug, logic error, regression, documentation gap, performance issue.
- Are there recurring bug categories? (e.g., 5 import errors suggests a systemic import architecture problem.)
- Are bug fixes accompanied by root cause analysis, or just surface patches?
- For each bug fix: was the fix verified (test added, manual check documented, or unverified)?
- Are there bugs that were introduced by a change and then fixed in a follow-up entry? These are normal, but the gap between introduction and fix matters.

Flag systemic patterns:
- 3+ bugs in the same category: **P1** (systemic weakness)
- Bug fix with no verification: **P3**
- Bug introduced and fixed within 1 hour: informational
- Bug introduced and fixed after 7+ days: **P2** (delayed response)

## Domain 9: Gap & Omission Detection

Identify changes that happened but were not logged, or logs that reference non-existent changes.

- Read `FUNCTION_MAP.md` and `IMPLEMENTATION_PLAN.md` — identify anything that exists in these files but has no corresponding entry in `AGENT_CHANGES.md`.
- Use `codegraph_codegraph_status` and `codegraph_codegraph_files` to identify recent files (by modification time) that have no corresponding change log entry.
- Are there large time gaps (>48 hours) in the change log during active development periods? If so, is there a plausible explanation (documented elsewhere, user explicitly asked to skip logging)?
- Are there entries that say "See previous entry" or "Same as above" without repeating critical detail?

Flag each omission:
- Function exists in code + FUNCTION-MAP but no change entry: **P2**
- File modified on disk but no change entry in 7+ days: **P2**
- Unexplained time gap >48 hours during active sprint: **P3**

## Domain 10: Observability & Traceability

Assess whether each change can be traced back to its origin.

- Does the entry include a rationale that explains WHY the change was needed?
- Can the rationale be cross-referenced against a requirement, bug report, user request, or audit finding?
- Are security-related changes explicitly labeled as security fixes?
- Are there entries that describe WHAT was done but not WHY? (e.g., "Refactored X" without explaining the motivation.)
- Are change impacts scoped? (e.g., "This affects Y module only" or "This changes behavior for all Z.")

Flag traceability failures:
- Entry with no rationale: **P2**
- Security change not labeled as security: **P3**
- Entry with vague scope ("various fixes", "multiple changes"): **P3**

---

# Phase 3 — Severity Classification

Every finding MUST be classified into exactly one of these tiers:

| Tier | Label | Definition | Action Required |
|------|-------|-----------|-----------------|
| **P0** | **CRITICAL** | Recurring bug pattern (3+ fixes for same issue), active regression that breaks production, or completely fabricated change entry. | Immediate remediation before any other work. |
| **P1** | **HIGH** | Change log claims that contradict codebase reality, missing version entries, systemic weakness identified. | Remediate within the current sprint/cycle. |
| **P2** | **MEDIUM** | Missing function map sync, incomplete entries, untraceable changes, gap >7 days. | Schedule for near-term remediation. |
| **P3** | **LOW** | Missing rationale, vague scope, formatting inconsistencies, minor omissions. | Address opportunistically. |
| **P4** | **INFORMATIONAL** | Observation, positive pattern recognition, suggestion for future consideration. | No action required; logged for awareness. |

---

# Phase 4 — Report Generation

## Output File Convention

The audit report MUST be saved as a markdown file in the `audits/agent-changes-md-audits/markdown` directory within the project directory, with the following naming convention: `audit_agent-changes_<YYYY-MM-DD_HHmm>_<agent-name>.md`.

**Examples:**
- `audit_agent-changes_2026-08-04_1430_<lead-role-handle>.md`
- `audit_agent-changes_2026-08-04_1500_<architecture-review-role-handle>.md`
- `audit_agent-changes_2026-08-04_1530_<assurance-role-handle>.md`
- `audit_agent-changes_2026-08-04_1600_<external-review-role-handle>.md`

**Agent Name Rules:**
- Use the short, lowercase role handle declared by the current project `agent_roles.md`; do not invent or copy a handle from another project.
- If the agent cannot determine its own model name, use `unknown-agent`.

## Report Structure

The audit markdown file MUST follow this exact structure:

```markdown
# AGENT_CHANGES.md Audit Report
| Field | Value |
|-------|-------|
| **Project** | <project name from AGENTS.md> |
| **Date** | <YYYY-MM-DD HH:mm TZ> |
| **Agent** | <full model identifier> |
| **Scope** | <total entries audited> entries across <N> change groups |
| **Time Span** | <oldest entry date> to <newest entry date> |
| **Duration** | <approximate time taken> |

## Executive Summary
<2-4 paragraph high-level summary. Overall verdict on the change log health.
State the number of change groups, how many passed/failed, and the top 1-2
critical findings.>

## Detailed Analysis by Change Group

### <Group N>: <Group Title>
**Verdict:** <✅ Right changes / ⚠️ Mostly right / ❌ Wrong changes>
**Date Range:** <start> to <end>
**Entries:** <count>

#### <Entry Timestamp> — <Entry Brief>
- **Claim:** <What the entry says was done.>
- **Verification:** <Does the codebase confirm this claim? Quote evidence.>
- **Assessment:** <First-principles analysis — was this the correct approach?>
- **Issues:** <Any problems found, or "None.">

(Repeat per entry in the group)

**Group Summary:** <Aggregate assessment of all entries in this group.>

---

(Repeat per change group)

## Summary Table
| # | Change Group | Verdict | Entries | Key Issues |
|---|-------------|---------|---------|------------|
| 1 | <Group>     | ✅/⚠️/❌ | <N>     | <brief>    |

**Total: <X>/<Y> groups passed, <Z> groups with issues**

## Findings by Severity

### P0 — Critical
<findings, or "No critical findings." if none>

### P1 — High
<findings>

### P2 — Medium
<findings>

### P3 — Low
<findings>

### P4 — Informational
<findings>

## Cross-Reference Integrity

### FUNCTION_MAP.md Sync Status
<table of discrepancies, or "Fully synchronized." if clean>

### IMPLEMENTATION_PLAN.md Sync Status
<table of discrepancies, or "Fully synchronized." if clean>

## Remaining Issues
<Items flagged during audit that the original agent did not address.
Organized by severity.>

## Documentation Quality
<Overall assessment of AGENT_CHANGES.md quality — formatting, thoroughness,
consistency, and adherence to project rules.>
```

## Per-Entry Assessment Format

Every individual entry in every change group MUST include these four sections:

```markdown
#### <Timestamp> — <Brief>
- **Claim:** <What the entry says>
- **Verification:** <Codebase evidence>
- **Assessment:** <First-principles analysis>
- **Issues:** <Problems or "None.">
```

Informational findings (P4) may use an abbreviated format without the full Assessment.

---

## Execution Guardrails

1. **Tool Protocol:** Obey all tool-routing rules from the user's global rules. Use CodeGraph for structure, native Read/Grep for content.
2. **No Auto-Fix:** The audit NEVER modifies project code, config, or docs. Its ONLY writes are its own deliverables: the audit report file, the `AGENT_CHANGES.md` summary entry, and (for P0/P1 findings) their `[PENDING]` rows in `DYNAMIC_LEDGER.md`. Everything else is strictly read-only. Sync note: shared with `audit-codebase` — revising either revises both.
3. **Deterministic Ordering:** Execute all 10 domains in the numbered order. Do not reorder or parallelize domains.
4. **Evidence-Based:** Every finding must cite the exact file, line range, or entry timestamp. No vague references like "multiple entries."
5. **First Principles:** Every finding at P0-P2 must explain the failure mechanism from first principles, not just state that something "looks wrong."
6. **Static Only:** All cross-referencing is static. Do NOT run tests, execute scripts, or invoke any command that modifies state.
7. **AGENT_CHANGES.md:** After generating the audit report, append a summary entry to `AGENT_CHANGES.md` logging that an audit was performed, by which agent, and the file name of the report.
