---
name: project-scaffold-init
description: Stamp a new project's Codex/OpenAI agent scaffold from the canonical template layer (agentic-coding/project-rules-skills/templates/for-new-projects-deploy/) into a new hub folder, symlink it into the repo, then VERIFY completeness on disk — mission block non-empty, every path cited in COUNCIL.md/documentation-rules.md exists, AGENTS.md is canonical, no leaked project-specific literals (session handles, hardware strings, prior project names), full docs/documentation scaffold with .gitkeeps, all symlinks resolve. Invoke when onboarding a new project ("scaffold the new project", "set up the project rules/config", "init the project from templates").
---

# Skill: project-scaffold-init

## When to use
- Ali starts a new project and its Codex/OpenAI agent configuration must be created from the templates.
- An existing project's scaffold is suspected incomplete — run the verification pass alone (steps 4–5).
- NOT for editing the templates themselves (template repairs are their own task; templates are read-only sources here).

Why this exists: slm-thought-tracing shipped with an empty mission block, three 404 directory references, and an inherited foreign session handle — manual copying has no completeness check. The verification pass below (which absorbs the one-off "template-placeholder-lint" idea as step 5) is the deliverable.

## Ground rules (global rules cited by name — not re-typed here)
- **Estate Architecture rule:** scaffold lives in `agentic-coding/project-rules-skills/<project>/` and is SYMLINKED into the repo — never local copies, never shadowed hub files.
- **Standing Canvases rule:** COUNCIL.md is created only on Ali's explicit instruction — a scaffold run Ali requested covers stamping it from the template; never create it unbidden outside that grant.
- **Naming:** new projects use the underscore spellings (`AGENT_CHANGES.md`, `FUNCTION_MAP.md`, `agent_roles.md`); the hyphen grace exists only for legacy projects.

## Template layer (the stamp source — read-only)
`agentic-coding/project-rules-skills/templates/for-new-projects-deploy/` — current canvases (AGENT_CHANGES, COUNCIL, DYNAMIC_LEDGER, FUNCTION_MAP, IMPLEMENTATION_PLAN, agent_roles, documentation-rules, SCHEMATIC-PALETTE-RULES), the unavailable-by-default `external-agent-availability.md` manifest template, `.agents/ignore/.ignore`, `docs/documentation/templates/run-completion-entry-template.md`, and `docs/primitives/` (research projects only). Retired provider surfaces are quarantined and are not stamp inputs. Template health: the template-layer repairs (D1–D13) completed 2026-07-09 (source of record: `system-level/documentation/completed-template-layer-execution-brief.md` + the system-level AGENT_CHANGES entry 2026-07-09 21:15:53 PKT); if template health is in doubt, run `agentic-coding/scripts/estate_health_check.py` before stamping.

## Workflow
1. **Stamp:** copy the template set into `project-rules-skills/<project>/` (research projects include `docs/primitives/`; ops projects skip it). Copy, never move — templates stay intact.
2. **Fill:** Mission/Deliverable/North-Star block (draft from the project's blueprint if Ali hasn't written one — mark the draft `<!-- drafted by <agent> <date> — Ali may refine -->`); roster in `agent_roles.md` with per-project role references derived from the current seats (`lead`, `architecture-reviewer`, `assurance-reviewer`, or `<external-review-role>`) — never a session handle inherited from another project; replace the `REPLACE_WITH_*` values in `external-agent-availability.md` only after a fresh status observation, leaving every unverified seat unavailable; `.agents/ignore/.ignore` with env exclusions ACTIVE (uncommented).
3. **Symlink the current Codex/OpenAI scaffold into the repo root:** `AGENTS.md`, `.agents/`, `agent_roles.md`, and canvases per the Estate Architecture rule; do not add retired provider surfaces.
4. **Scaffold the docs tree:** `docs/documentation/{agent-changes,councils,detailed-explanations,implementation-plans,playbooks}/{markdown,html}` each with a `.gitkeep` (adjust the set to what documentation-rules.md for this project actually names — the tree must match the doc, or the doc must be edited to match the tree).
5. **Verify (definition of done — every box asserted against disk, not memory):**
   - [ ] Mission/Deliverable/North-Star non-empty and placeholder-free.
   - [ ] Every path cited in COUNCIL.md and documentation-rules.md resolves on disk (exists-check per cited path).
   - [ ] AGENTS.md is the sole canonical project rule source (verify its symlink resolves into the hub).
   - [ ] `external-agent-availability.md` is the one canonical project-root manifest (or an explicitly authorized nested rules-bundle root), parses as one strict JSON block, matches that root, uses the shared status/reason-code correlations, has an explicit expiry, and contains no session handle material.
   - [ ] Placeholder lint: no leaked project-specific literals — grep the stamped set for foreign session handles (`<current-seat>-<other-project>`), hardware strings, prior project names, and template placeholder tokens (`<project>`, `TBD`, `example`).
   - [ ] Full docs/documentation tree with .gitkeeps present.
   - [ ] Every symlink in the repo resolves into the hub (`os.path.realpath` under the hub, target exists).
   - [ ] `agentic-coding/scripts/estate_health_check.py` run — the new project introduces zero new findings.
6. **Log:** entry in the new project's AGENT_CHANGES.md (fresh tool-acquired PKT timestamp) + a [PENDING] DYNAMIC_LEDGER row for anything Ali still owes (mission refinement, roster confirmation, COUNCIL header).
7. **Seed the memory:** apply the memory-porting boundary in `codex-research-lifecycle`: enumerate applicable indexes, classify portable versus non-portable material, copy only adapted portable doctrine into the new project's memory directory, record exclusions, and build the index. No separate memory-seeding skill is required or assumed; research projects later author their statistics protocol via `codex-seed-statistics-protocol` when the first sweep approaches.

## Hard rules
1. Templates are read-only sources — a scaffold run never edits `templates/`.
2. Hub-first, symlink-in — a file created directly in the repo that should live in the hub is a defect, not a shortcut.
3. The verification pass (step 5) is not optional and not sampled — every box, every run; report per-gap honestly.
4. Only Ali commits; the scaffold run ends with the checklist verdict + [PENDING] rows, not a git push.
