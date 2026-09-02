---
name: getting-acquainted-with-project
description: Initializes project context by strictly loading core architectural documents (all five standing canvases) and respecting defined context boundaries via the native Read/Grep tools and CodeGraph. Invoke AUTOMATICALLY when joining a new session on a project, or when explicitly asked to "get acquainted with the project".
---

# Note

- **Explore Agent Definition:** An "Explore Agent" is NOT a separate subagent. It is the main session performing batch file reading using the native Read and Grep tools. The term refers to the exploration pattern (batch-read → synthesize → return), not a spawned process. Do NOT use sub-agent, multi-agent, or browser-agent tools for filesystem exploration.

# Skill: getting-acquainted-with-project

# Tool Constraints (Strict — Do Not Deviate)

1. Native file tools are the read path during this workflow:
   - `Read`,
   - `Grep`,
   - `Glob`,
   - raw `bash` with `cat`/`grep`/`find`/`ls` is also permitted.
2. All file content operations MUST use:
   - `Read`,
   - `Grep`,
   - `Glob`.
3. Prefer CodeGraph MCP tools for structural operations:
   - `codegraph_codegraph_files`,
   - `codegraph_codegraph_status`,
   - `codegraph_codegraph_search`,
   - `codegraph_codegraph_node`,
   - any other `codegraph_codegraph_` commands (that are not prohibited).
4. **Note**: MCP runtime prefixes tool names with the server name, so the registered names are double-prefixed (e.g., `codegraph_codegraph_files`, not `codegraph_files`).
5. `codegraph_codegraph_context` and `codegraph_codegraph_explore` are not used for file-content reading in the main session. The Explore Agent term in this skill means the main session's bounded batch-read pattern, not a spawned sub-agent.

---

# Execution Protocol

## Project memory namespace preflight

Before onboarding reads or writes any project memory, apply
`codex-project-memory-protocol`: resolve the current project's documented
namespace alias or exact repository-root basename, check
`/home/az/.codex/memories/<namespace>/`, and if it is absent create only that
namespace plus a `MEMORY.md` index using the canonical format of existing
project indexes. Project-specific memory is written directly in that
namespace; `/home/az/.codex/memories/extensions/ad_hoc/notes/` is reserved for
genuinely global or cross-project policy. This preflight does not authorize
reading unrelated namespaces or treating memory as authority. If the root,
alias, namespace, or index cannot be resolved and checked, stop onboarding's
memory work and report `BLOCKED`; do not use `ad_hoc` as a fallback. A hook is
only defense-in-depth.

## Phase 1: Structural Topology (CodeGraph MCP)

1. Call `codegraph_codegraph_files` with `format="tree"` to retrieve the full project file tree.
   - **Purpose:** This gives you the directory layout and identifies key source directories.
2. Call `codegraph_codegraph_status` to verify the index is healthy and note file/symbol counts.
   - **Fallback:** If the index is unavailable, empty, or errored, record the limitation and continue with native `find`, `Read`, `Grep`, and `Glob`; do not invent structural results or halt solely because CodeGraph is unavailable.

## Phase 2: Core Document Loading (native Read)

3. Load `agent_roles.md` from the project root — the SINGLE SOURCE OF TRUTH for agent roles:
   - `Read <project-root>/agent_roles.md`
   - Adopt your assigned role for this session. If the file is absent, note it and ask Ali to create one from `project-rules-skills/templates/for-new-projects-deploy/agent_roles.md` (never invent roles).
4. Load `AGENT_CHANGES.md` for change history:
   - `Read <project-root>/AGENT_CHANGES.md`
5. Load `FUNCTION_MAP.md` (or `FUNCTION-MAP.md` in legacy projects — read whichever exists) into working memory:
- `Read <project-root>/FUNCTION_MAP.md` (or `FUNCTION-MAP.md` in legacy projects)
6. Load `IMPLEMENTATION_PLAN.md` (or `IMPLEMENTATION-PLAN.md` in legacy projects — read whichever exists) into working memory:
- `Read <project-root>/IMPLEMENTATION_PLAN.md` (or `IMPLEMENTATION-PLAN.md` in legacy projects)
7. Load `COUNCIL.md` (the cross-agent dialectic canvas) — read its header protocol, then the newest entries first:
   - `Read <project-root>/COUNCIL.md`
8. Load `DYNAMIC_LEDGER.md` (the canonical task/status ledger — open [PENDING]/[IN_PROGRESS] items are session context):
   - `Read <project-root>/DYNAMIC_LEDGER.md`

**Missing-File Grace (Phase 2 only):** If any of the above files (steps 4-8) does NOT exist at the path, do NOT halt. Record the filename in a "Missing Files" list, continue to the next step, and report ALL missing files in Phase 5. This is by design — some projects (research projects, Obsidian vaults) may not have IMPLEMENTATION_PLAN.md, FUNCTION_MAP.md, or AGENT_CHANGES.md.

## Phase 3: Ignore File & Guardrails

9. Read the project's current agent ignore file in the project root — Codex/OpenAI projects use `.agents/ignore/.ignore`.
10. Do NOT read the `.gitignore`.
11. Note all blocked patterns (especially CSV, parquet, .env, binary assets) and strictly respect them for the entire session.

## Phase 4: Key Source Code Scan (If Needed)

12. If the project has >3 key source files to examine, enter bounded batch-read mode in the main session. Use CodeGraph metadata when available and native `Read`/`Grep` for content:
    - "Use CodeGraph structural tools when indexed."
    - "Use the native Read and Grep tools to read file contents and search strings."
    - "Do not re-read files that have already been returned."
    - "Synthesize the logic and return only your analysis to the main session."
13. If ≤3 files, read them directly from the main session:
    - For structural audits (signatures/structure): use CodeGraph, or `Read <file>`.
    - For implementation review: `Read <file>`

## Phase 5: Confirmation

14. After all phases complete, explicitly report to the user:
    - List of **rule file paths** loaded (absolute paths).
    - **Missing Files Report:** If any files from steps 4-8 were not found, list them with their attempted paths. Example: *"The following expected files do not exist in this project: FUNCTION_MAP.md, IMPLEMENTATION_PLAN.md. This is normal for research/documentation projects."*
    - Name of the ignore file respected (example: `.ignore` at `<path>`).
    - CodeGraph index stats (files, symbols, edges).
    - Any files not loaded because they were out of scope, inaccessible, or because a bounded-read/tool limitation prevented loading them.
    - Do NOT re-read or re-attempt missing files — the report is sufficient.

---

# When to Use Me

Use this skill automatically:
1. when joining a new session or,
2. when explicitly asked to "get acquainted with the project."
