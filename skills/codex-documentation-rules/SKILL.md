---
name: documentation-rules
description: Apply a project's per-phase documentation protocol, including closeout artifacts, plan migration, append-only canvases, and the final verification gate. Use when opening or closing a phase, migrating a completed plan, or checking whether a phase is genuinely complete.
---

# Phase Documentation Rules

Use this skill with the project's own `documentation-rules.md`. Before acting, read the project root's `agent_roles.md`; it determines the active lead and review responsibilities. The project documentation file is authoritative for local variations.

## Authority and timing

- Treat documentation rules as a protocol, not a suggestion.
- Only the project owner may edit, unlock, close, purge, or declare completion of the protocol unless the project explicitly grants a narrower authority.
- Produce polished phase documentation at phase close. During an open phase, keep continuous evidence in the project canvases and working artifacts.
- Never write results into a polished deliverable while the inputs for that story are still changing.

## Phase-close package

At phase close, check the project protocol and produce every applicable artifact as one coherent package:

- archived implementation plan with its completion statement;
- phase playbook;
- detailed explanation covering theory, experimental details, results, and analysis;
- architectural schematic in the required editable/browser form and rendered image form;
- completion report; and
- all project-required canvas updates.

Use the project's diagram skill and palette rules for schematics. A phase is not complete merely because the prose exists: verify the artifacts, links, canvases, and required checks together.

## Migrating a completed implementation plan

When a plan is closed:

1. Copy the plan body verbatim into the numbered documentation archive.
2. Do not migrate the root plan's completion statement or instruction header into the archive body.
3. Replace the root plan body with a concise current-state summary and a relative link to the archive.
4. Use an assertion-gated exact-match split or equivalent sanctioned script; do not use a stale copy or an unbounded text replacement.
5. Verify the archived bytes, root link, and completion statement before reporting success.

## Required canvas updates

- Update the canonical task/status ledger with the phase state and unresolved work.
- Update the function inventory when functions change status or are newly exercised.
- Record the change, commands, files, and outcome in the append-only change log.
- Follow each canvas header and the `canvas-write-protocol` skill: acquire a fresh project timezone timestamp immediately before writing, re-read the head, append in the required position, and verify the persisted bytes.
- Keep failed, marginal, blocked, and pending gates visible; never smooth them into a success claim.

## Completion check

Before the project owner is asked to close the phase, confirm:

- every required artifact exists at the project-approved path;
- every cross-reference and archive link resolves;
- the detailed explanation has all four required parts;
- the schematic source and render agree;
- the ledger, function map, and change log contain the required evidence;
- the project's Verification Gate has run with honest results; and
- no unresolved `[PENDING]`, BLOCKED, or failed gate is being represented as complete.
