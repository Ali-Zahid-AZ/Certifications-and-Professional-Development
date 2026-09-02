---
name: audit-codebase
description: Conducts a deep architectural codebase audit, identifying state mutations, injection vectors, big-O bottlenecks, and structural debt across 14 audit domains. Invoke when Ali explicitly requests a codebase/project audit ("audit the codebase", "run a code audit").
---
## What I Do

I execute a deterministic, phased codebase audit that goes far beyond linting or stylistic critique. I examine structural integrity, security posture, operational resilience, and documentation fidelity. Every finding is classified by severity, explained from first principles, and accompanied by a concrete remediation with code.

## When To Use Me

Use this when the user explicitly requests an audit of the project. I produce a standalone audit report as a timestamped markdown artifact in `audits/code_audits/markdown`.

---

## Phase 1 — Scope & Discovery

Before analyzing a single line of code, establish the audit boundary.

> **Sync note:** this skill shares its severity ladder, output conventions, and agent-name rules with `audit-agents-changes-log` — when revising either skill, revise both.

1. **Read `AGENTS.md`** (project root) — absorb all project-level rules, constraints, and execution boundaries.
2. **Read `FUNCTION_MAP.md` (or `FUNCTION-MAP.md` in legacy projects — read whichever exists)** — load the declared function registry into working memory.
3. **Read `AGENT_CHANGES.md`** (project root; a few legacy projects still use the hyphen name `AGENT-CHANGES.md` — read whichever exists) — understand the recent change history and its trajectory.
4. **Read `IMPLEMENTATION_PLAN.md` (or `IMPLEMENTATION-PLAN.md` in legacy projects — read whichever exists)** — this is the master index of all version implementations. It defines what each version was supposed to deliver, the architectural decisions made, and the current status of each section. Use this as the version boundary map.
5. **Read version-specific implementation plans** from `docs/documentation/implementation-details/markdown` — read every `V*-DETAILED-IMPLEMENTATION.md` file in this directory. These contain the granular implementation specifications for each version: what was built, how it was built, and what constraints it operates under. This context is critical for detecting **cross-version regressions** — where a newer version's changes may have broken invariants or contracts established by an earlier version.
   - **Priority order:** Read the `*-DETAILED-IMPLEMENTATION.md` files first (these define the contracts). Optionally consult the `*-DETAILED-EXPLANATIONS.md` files if deeper theoretical context is needed for a specific finding.
   - **Do NOT read:** `*-COUNCIL.md` files (these are debate logs, not specifications) unless a specific finding requires tracing a design decision back to its origin.
6. **Map the file tree** — use `codegraph_codegraph_files` to get the full project structure.
7. **Identify audit scope:**
   - Include all application code, configuration files, and infrastructure scripts.
   - Include relevant application code, configuration files, and infrastructure scripts regardless of file size. Exclude `node_modules/`, `.venv/`, `__pycache__/`, `.git/`, vendored dependencies, and binary payloads when they are outside the audit scope; use focused ranges or streaming for very large files when practical.
   - If the project has > 50 source files, prioritize: entry points, core business logic, data pipelines, and security-sensitive modules first.

---

## Phase 2 — Systematic Analysis (14 Audit Domains)

Execute these domains **in order**. Do not skip any domain. For each, use the appropriate tools (CodeGraph for structure, native Read/Grep for content) and document every finding.

### Domain 1: Architectural Anti-Patterns

- Tight coupling between modules that should be independent.
- God classes/functions that violate single-responsibility.
- Circular dependencies or import cycles.
- Hardcoded values that should be configurable.

### Domain 2: State Mutation Safety

- Unhandled or unprotected state mutations (shared mutable state).
- Race conditions in concurrent or async code paths.
- Global state that is modified without synchronization.
- Memory leaks from unclosed resources (file handles, DB connections, sessions).

### Domain 3: Security & Injection Vectors

- Improper input sanitization (SQL injection, command injection, path traversal).
- Prompt injection vulnerabilities in LLM-facing code.
- Secrets, API keys, or credentials hardcoded or committed to version control.
- Missing authentication/authorization checks on exposed endpoints.

### Domain 4: Validation & Schema Enforcement

- Absence of strict Pydantic Version 2 enforcement where data contracts exist.
- Implicit type inference during data joins or transformations (must be explicit).
- Missing or incomplete input validation on function boundaries.
- Schema drift between declared models and actual data shapes.

### Domain 5: Algorithmic Efficiency (Big-O)

- Hidden O(n²) or worse loops, especially in data processing pipelines.
- Unbounded queries or full-table scans against databases or graph stores.
- Redundant computations that should be cached or memoized.
- Inefficient data structure choices (e.g., list where set/dict is appropriate).

### Domain 6: Error Handling & Failure Modes

- Silent exception swallowing (`except: pass`, bare `except`).
- Generic catch-all handlers that mask root causes.
- Missing retry/backoff logic on external service calls.
- Functions that return `None` on failure instead of raising.

### Domain 7: Concurrency & Async Safety

- Async functions that block the event loop with synchronous I/O.
- Missing `await` on coroutines.
- Thread-unsafe shared state access.
- Deadlock potential in lock acquisition ordering.

### Domain 8: Logging & Observability

- Critical code paths with no logging or telemetry.
- Sensitive data (PII, credentials) being logged.
- Inconsistent log levels (errors logged as info, etc.).
- Missing structured logging where it would aid debugging.

### Domain 9: Dependency Health

- Outdated dependencies with known CVEs.
- Unpinned or loosely pinned dependency versions.
- Unused dependencies still listed in `pyproject.toml` / `package.json`.
- Shadow dependencies (used but not declared).

### Domain 10: Configuration & Environment Safety

- Environment variables used without defaults or validation.
- Configuration files with production secrets or credentials.
- Missing `.env.example` or equivalent documentation.
- Inconsistent configuration loading across modules.

### Domain 11: Dead Code & Unreachable Paths

- Functions declared but never called (cross-reference with `FUNCTION_MAP.md`).
- Commented-out code blocks left in production files.
- Feature flags or conditional branches that are permanently inactive.
- Orphaned imports.

### Domain 12: Test Coverage & Quality

- Critical business logic paths with no test coverage.
- Tests that assert nothing meaningful (tautological tests).
- Missing edge-case and failure-path tests.
- Test files that import production code but don't execute assertions.

### Domain 13: Documentation-to-Code Drift

- Functions in code that are missing from `FUNCTION_MAP.md`.
- Functions in `FUNCTION_MAP.md` that no longer exist in code.
- `AGENT_CHANGES.md` entries that reference code states no longer accurate.
- README or AGENTS.md instructions that contradict current implementation.

### Domain 14: Infrastructure & DevOps Integrity

- Docker/compose configurations with security misconfigurations.
- Missing health checks on services.
- Boot/teardown scripts that don't handle partial failures gracefully.
- Hardcoded ports, hosts, or paths that should be environment-driven.

---

## Phase 3 — Severity Classification

Every finding MUST be classified into exactly one of these tiers:

| Tier | Label | Definition | Action Required |
|------|-------|-----------|-----------------|
| **P0** | **CRITICAL** | Active security vulnerability, data loss risk, or production-breaking defect. | Immediate remediation before any other work. |
| **P1** | **HIGH** | Architectural flaw that will cause escalating technical debt or intermittent failures. | Remediate within the current sprint/cycle. |
| **P2** | **MEDIUM** | Code quality issue that reduces maintainability or introduces latent risk. | Schedule for near-term remediation. |
| **P3** | **LOW** | Minor inefficiency, style inconsistency, or non-critical improvement opportunity. | Address opportunistically. |
| **P4** | **INFORMATIONAL** | Observation, positive pattern recognition, or suggestion for future consideration. | No action required; logged for awareness. |

---

## Phase 4 — Report Generation

### Output File Convention

The audit report MUST be saved as a markdown file in the `audits/code_audits/markdown` directory, with the following naming convention: `audit_<YYYY-MM-DD_HHmm>_<agent-name>.md`.

**Examples:**
- `audit_2026-08-04_1430_<lead-role-handle>.md`
- `audit_2026-08-04_1500_<architecture-review-role-handle>.md`
- `audit_2026-08-04_1530_<assurance-role-handle>.md`
- `audit_2026-08-04_1600_<external-review-role-handle>.md`

**Agent Name Rules:**
- Use the short, lowercase role handle declared by the current project `agent_roles.md`; do not invent or copy a handle from another project.
- If the agent cannot determine its own model name, use `unknown-agent`.

### Report Structure

The audit markdown file MUST follow this exact structure:

```markdown
# Codebase Audit Report
| Field | Value |
|-------|-------|
| **Project** | <project name from AGENTS.md> |
| **Date** | <YYYY-MM-DD HH:mm TZ> |
| **Agent** | <full identity assigned by the current project `agent_roles.md`> |
| **Scope** | <number of files audited> / <total files in project> |
| **Duration** | <approximate time taken> |
## Executive Summary
<2-4 paragraph high-level summary of the audit findings, overall health
assessment, and the most critical items requiring attention.>
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
### AGENT_CHANGES.md Consistency
<any drift noted, or "Consistent with current codebase." if clean>
## Remediation Roadmap
<Prioritized list of recommended actions, ordered P0 → P4.>
```

### Per-Finding Format

Every individual finding (P0 through P3) MUST include all four of these sections:

```markdown
#### [DOMAIN-NUMBER.FINDING-NUMBER] <Short Title>
**Severity:** P<N> — <LABEL>
**Location:** `<file path>` lines <start>-<end>
**Mechanism:** <First-principles explanation of WHY this is a problem.
What is the failure mode? What invariant is being violated?>
**Impact:** <What happens if this is not fixed? Quantify where possible.>
**Remediation:**
```python  (or appropriate language)
<exact refactored code>
```
```

P4 (Informational) findings may use an abbreviated format without the full Remediation code block.

---

## Execution Guardrails

1. **Tool Protocol:** Obey all tool-routing rules from the user's global rules. Use CodeGraph for structure, native Read/Grep for content.
2. **No Auto-Fix:** The audit NEVER modifies project code, config, or docs. Its ONLY writes are its own deliverables: the audit report file, the `AGENT_CHANGES.md` summary entry, and the guardrail-7 `DYNAMIC_LEDGER.md` rows. Everything else is strictly read-only.
3. **Deterministic Ordering:** Execute all 14 domains in the numbered order. Do not reorder or parallelize domains.
4. **Evidence-Based:** Every finding must cite the exact file and line range. No vague references like "several places in the codebase."
5. **First Principles:** Every finding at P0-P2 must explain the failure mechanism from first principles, not just state that something "looks wrong."
6. **AGENT_CHANGES.md:** After generating the audit report, append a summary entry to `AGENT_CHANGES.md` logging that an audit was performed, by which agent, and the file name of the report.
7. **Ledger coupling (audit-finding→ledger rule):** At audit close, EVERY P0 and P1 finding also lands as its own `[PENDING]` entry in `DYNAMIC_LEDGER.md` (fresh PKT time, canvas write protocol) — findings that live only in report prose fall off when a project goes dormant (proven: a P0 LLM-injection finding sat unremediated for a month). Sync note: this guardrail is shared with `audit-agents-changes-log` — revising either revises both.
