---
name: codex-engineering-standards
description: "Apply the estate's engineering standard and mandatory Python verification gate: uv-only dependency discipline, explicit assumptions, simplicity, holistic and surgical changes, py_compile, import smoke-testing, Ruff F821/F811, Radon complexity review, failure triage, and falsifiable completion reporting. Use before implementing or declaring code changes verified, complete, or done, and when asked to check code quality, complexity, lint, or verification."
---

# Codex Engineering Standards

Apply this skill before implementing or declaring a code change complete. Read the active project's agent_roles.md before assigning authority or interpreting role-specific instructions. Ali remains the system owner and final authority; current project rules, live disk, git, runtime state, and artifacts outrank memory, handovers, and sub-agent reports.

## 1. Engineering standard

### Environment and packages

- Target environment: Ubuntu 24.04 (Noble).
- Use uv for Python environments and packages; never use native pip.
- Before adding a library, run uv pip show <lib> to avoid duplicate dependencies.
- Do not add a dependency silently. Inspect the declared toolchain and existing environment first.

### Think first

- State assumptions before acting.
- Surface multiple interpretations instead of choosing silently.
- Propose simpler approaches and push back when warranted.
- If the request or acceptance condition is unclear, stop, name the ambiguity, and ask Ali.

### Simplicity

- Write the minimum code that solves the request.
- Do not add speculative features, abstractions for single-use code, unrequested configurability, or error handling for impossible cases.
- If 200 lines could be 50, rewrite it. Ask whether a senior engineer would call the result overcomplicated.

### Surgical changes

- Touch only what the request requires; match existing style.
- Do not improve, refactor, reformat, or delete adjacent pre-existing code merely because it can be improved.
- Remove only orphans created by your change. Mention unrelated dead code instead of deleting it.
- Every changed line must trace to the request.

### Holistic validation

- Before changing code, audit upstream callers, downstream consumers, interfaces, and state lifecycles.
- Prove that the change preserves macro-architectural integrity, not only that the local edit works.
- Recheck mutable resources before compute or system changes.

## 2. Mandatory verification gate

Never write, say, or log “verified”, “handled”, “complete”, or “done” about a code change until the applicable gate has run and its result is reported honestly. The gate is a floor, not a test-suite replacement.

The canonical gate invocation remains inline in global and project rule files and in verify.sh files. Keep this exact prose form, including the <files> scope placeholder:

py_compile on modified files → import smoke-test (python -c "import <module>") → uv run ruff check --select F821,F811 <files> from the project root.

### Gate steps

Run from the project root, scoped to the files changed:

| Step | Check | Catches |
|---|---|---|
| 1 | py_compile on each modified Python file | Syntax errors |
| 2 | python -c "import <module>" | Import-time NameError, ImportError, side effects, and import-graph failures |
| 3 | uv run ruff check --select F821,F811 <files> | Undefined names and redefinitions, including names hidden inside function bodies |

Ruff is resolved from the project's virtual environment. Do not run the legacy ruff --select form; it errors on newer Ruff releases. Use uv run ruff check --select F821,F811 <files> from the project root.

Projects may provide scripts/verify.sh <file1> [<file2> …] with flushed markers for each verification stage. Prefer that project runner when available. A non-importable top-level module may be reported as an understood SKIP; a SKIP is not a PASS and must be named.

### Gate failure triage

- Step 1 failure: fix the syntax error before interpreting downstream results.
- Step 2 exception: fix import-time side effects, cycles, or module-scope name use; do not silence it with a catch-all.
- F821: fix the missing, misspelled, or conditionally unavailable name.
- F811: remove or deliberately resolve the shadowing redefinition.
- Missing or unexpected Ruff: return to the project root and run it through uv.

### Exemptions and limits

- Deprecated CLIs with an intentional sys.exit(0) are exempt from import smoke-testing; state the exemption.
- Markdown, documentation, rule, skill, canvas, JSON, YAML, TOML, shell-only, and notebook changes are not Python-gate changes. State N/A and apply the relevant parser or bash -n check; for rule or skill edits, run the estate health check when a gate string or doctrine claim moved.
- Do not add pytest or mypy to this fast gate. They require a live stack or produce excessive false positives; real tests and end-to-end checks remain separate obligations.
- Automated health checks must inspect existing artifacts deterministically and must not regenerate data, download weights, recompute caches, or allocate GPU memory merely to verify.

## 3. Radon complexity loop

After any Python change, run both metrics on every changed Python file:

| Command | Threshold | Required response |
|---|---|---|
| radon cc <file> -s | CC > 10 / grade B | Flag the function for refactor consideration |
| radon cc <file> -s | CC > 15 / grade C | Refactor into small single-responsibility helpers; this is mandatory |
| radon mi <file> | MI < 65 | Improve it, comparing with sibling files before judging the number alone |
| radon mi <file> | Target MI > 80 | Use as the quality target, not a license to strip useful comments |

Self-correction loop: identify the per-function finding, flatten nesting with guard clauses and early returns, deconstruct distinct responsibilities into helpers, then re-run radon cc -s --max C and radon mi <file> until the changed code is clean or the remaining limitation is explicitly reported. Refactor complexity created by your change; mention pre-existing complexity outside scope.

If Radon is absent, use the project's approved uv-based tool setup. Do not silently install packages or fall back to native pip.

## 4. Change workflow and reporting

1. Establish the request, assumptions, acceptance conditions, callers, consumers, state transitions, and minimal file set.
2. Inspect current disk, git, configuration, and runtime state. Do not treat a plan, memory, or sub-agent report as proof of current state.
3. Make the smallest coherent surgical change.
4. Run the applicable verification gate and Radon loop before claiming completion or logging a completed code change.
5. Report the exact files checked, all three gate outcomes (including any SKIP or N/A), Radon's worst CC grade and MI context, meaningful tests or health checks, and unresolved gaps.
6. Before moving a FUNCTION_MAP entry past the gate or writing a completion outcome to AGENT_CHANGES.md, ensure the result is falsifiable and artifact-backed. Passing this gate alone does not establish end-to-end operational status.

For markdown, rule, skill, or canvas-only work, report: “verification gate: N/A (non-Python change set)” and perform the format-specific checks. Never silently omit an inapplicable check and never call an intended-but-unrun check a pass.
