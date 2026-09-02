---
name: compaction-required-greenlight
description: Gate context compaction or restart handoff by refreshing the live carrier, confirming append-only canvases, and giving the green light only last. Use before compaction or handoff.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: compaction-required-greenlight

> **Historical provenance (promoted, not invented):** this skill codifies an earlier estate-wide procedure for refreshing carrier memory before approving a compaction. It consolidates three project-local memories — `refresh-memory-before-compact-greenlight` (the ordered gate), `keep-handoff-carrier-lean` (the pruning/leanness clause), and the live carrier artifacts themselves (`live-runs-in-flight-handoff.md` / `cold-open-live-state.md`). Codified as a global skill 2026-07-24 on Ali's instruction so it binds every agent that shares the skills hub identically; current carrier handling is specified in §4. Since 2026-07-24 the always-loaded mandate also lives as global Session Hygiene rule #3 in `global/AGENTS.md`; the rule is stronger enforcement than a trigger-fired skill, and this skill is the procedure that rule points to.

## 1. What this is — the one invariant

**Compaction can silently drop working context. The refreshed re-attach memory is the SOLE guaranteed carry-over across that boundary.** Therefore:

> **Never green-light a compaction against stale memory.** Before you tell Ali "green light" / "ready to compact" — or before you initiate compaction yourself — the live re-attach carrier memory MUST already be a clean, current, self-contained snapshot. Refresh first, green-light strictly last. **Never invert this order.**

A green light against stale memory risks losing exactly the continuity a compact must preserve: live-run state (PIDs, service status, progress), completed-but-unlogged work, and open decisions live with Ali.

## 2. When to run it

- **Ali requests it:** "compaction required", "green light me to compact", "we'll compact now", "ready to compact?", or any hand-off across a compaction/restart boundary.
- **Self-triggered (mandatory):** when you approach the context ceiling (~80% of the window, per the global compaction-hygiene rule) and are about to recommend or run compaction yourself. The gate applies to self-initiated compaction exactly as to an Ali-requested one.
- Also applies before any deliberate session restart, fork boundary, or when handing live state to a successor session.

## 3. The green-light gate (green light is step 4 — never earlier)

1. **Verify live run state.** Do not report from memory — check the machine. Confirm any live PIDs/`systemd-run --user` services are alive and read their real progress from logs (e.g. `systemctl --user status`, `nvidia-smi`, `tail` the run log). Record current index/total, wall-clock, peak VRAM/RSS where relevant. A dead or finished run is itself state that must be written down.
2. **Update the LEDGER before compacting — and confirm the durable record is written NOW, not deferred.** The append-only canvases — `DYNAMIC_LEDGER.md`, `AGENT_CHANGES.md`, `COUNCIL.md` (whichever the project uses) — must already reflect everything that landed this session. **`DYNAMIC_LEDGER.md` is named first deliberately: writing the ledger is a mandatory pre-condition of every compaction, restart and hand-off, not a nice-to-have** (Ali, 2026-07-26). Where the session's state changed — a run finished, a decision landed, a blocker moved, a ruling was received — that change is a ledger entry *before* the boundary, never after it. If a completed action is unlogged, log it *before* compacting; never carry "I'll log it after the compact" across the boundary.
3. **Rewrite the carrier (and any relevant persistent memory) to current reality.** Make the re-attach carrier a self-contained snapshot (§4), updating any persistent memory whose facts changed this session. Prune as you go (§5).
4. **THEN give the green light — and freeze.** Only after 1–3 are true on disk do you say "green light" or initiate compaction yourself. After the green light, **stop state-mutating work until the compact lands**; any further work re-stales the carrier and re-arms the whole gate.
5. **On the far side of the boundary, run §7 before doing anything else.** The gate does not end at the green light — it ends when the successor context has re-grounded itself.

> Ordering note: steps 2–3 are deliberately sequenced canvases-then-carrier (the reverse of the source memory) so the carrier can cite the just-written canvas records, as the live carriers do. The hard invariant is only that the **green light comes strictly last**.

## 4. The carrier file — location per agent, and what it must contain

Each agent writes to its OWN memory store; the filename follows whatever the project already uses (naming grace — typically `live-runs-in-flight-handoff.md` or `cold-open-live-state.md`):

| Agent | Carrier write location |
|---|---|
| Codex/OpenAI seats (principal architect/lead; architecture reviewer; assurance reviewer) | `/home/az/.codex/memories/<current-project-namespace>/`, resolved by `codex-project-memory-protocol`; check and initialize the namespace plus `MEMORY.md` before writing |
| the external review seat | `/home/az/.local/share/opencode/memory/<project>/` |

- **Any other runtime or seat:** the gate binds you too, but no carrier path is specified here — **ask Ali or inspect the active runtime, never invent one.**
- If the current root, documented namespace, or destination index cannot be resolved and checked, do not rewrite or create a carrier: report `BLOCKED`. `extensions/ad_hoc/notes/` is never a carrier fallback, and a hook is only defense-in-depth.
- **Shared memory dir → agent-prefixed filename.** Where multiple agents share one project dir (the OpenCode case), each writes its OWN agent-prefixed carrier (`external-review-cold-open-live-state.md`, for example) so they never clobber each other.
- **No carrier yet?** Create one (typical name `cold-open-live-state.md`) and add its READ-FIRST pointer to the project's `MEMORY.md` index.

**The one surviving block must be self-contained** — readable cold by a fresh, context-light successor with zero prior turns:
- A `READ FIRST on re-attach` description line carrying a **fresh timestamp acquired live from the time MCP** (`get_current_time`, `Asia/Karachi`) — never guessed, never shell `date`, per Canvas Write Protocol #1 (the estate has a mis-stamped-carrier incident on record).
- Standing mission / the current pivot.
- Governance + operating mode (who holds command, what needs Ali, escalation triggers).
- Work / science state (frozen hashes, verdicts, what is decided).
- **Live run state:** PIDs / services, progress, watchers, log paths.
- **Pending actions + their exact procedures** (not just "do X" — how to do X).
- **Open decisions live with Ali.**
- **Standing constraints** carried across the boundary.
- **Relaunch / resume recipe** — the exact commands to pick up.

## 5. Keep the carrier LEAN (Ali's explicit requirement — prune deprecated things)

The carrier is a TRANSIENT snapshot of *current* state, not a history. On **every** refresh:

1. **Prune first.** Delete every superseded / deprecated / historical block (old cold-open `v` blocks, "CONSUMED", resolved-and-logged items). Keep exactly **one** authoritative current block.
2. **Rewrite, don't append.** Use native `Write` to replace the whole file with `[compressed frontmatter pointer] + [single current block]`. The frontmatter `description:` is a **tight pointer, NOT a duplicate of the block body.** Never stack a new block on top of the old ones.
3. **Leanness comes from dropping OLD blocks, never from thinning the CURRENT one** — the surviving block stays verbatim-complete (§4).
4. **Target a few-KB / one-screen file.** If it creeps back past ~2 stacked blocks or ~40 KB, prune again.
5. **This rewrite is a deliberate, narrow EXCEPTION to the non-destruction / mv-to-backup default** — scoped to *this carrier file only*. It is the agent's own transient working memory, lives outside git, and self-labels as transient. Dropping superseded-and-subsumed blocks is maintenance, not destruction. **If you are unsure which file is the carrier, rewrite nothing** and confirm first — the exception never licenses rewriting the wrong file.
6. **This NEVER applies to the append-only canvases.** `AGENT_CHANGES.md`, `DYNAMIC_LEDGER.md`, `COUNCIL.md` are strictly append-only — never pruned, rewritten, or truncated. Leanness is a carrier-only discipline.

## 7. ON RESUMING — the mandatory re-grounding read (Ali, 2026-07-26)

**The gate does not end at the green light. It ends when the successor context has re-grounded itself.** Compaction preserves a summary, and a summary of a research project silently loses the *goal* first — the founding design document is the least-quoted and most load-bearing artifact in any long program, so it is exactly what a summary drops.

**Immediately on resuming from a compaction, restart, fork or hand-off — BEFORE taking any other action, answering any question, or touching any file — read, in this order:**

1. **The project's founding design document, IN FULL.** The blueprint / charter / governing plan — whatever the project calls it (`BLUEPRINT.md`, `IMPLEMENTATION_PLAN.md`, the phase map). *In full* means end to end, not skimmed and not from a prior summary. **This is the GOAL**; every plan and scope decision is measured against it. For `local-mi-article` this is `docs/primitives/markdown/BLUEPRINT.md` (+ `DETAILED-EXPLANATION-BLUEPRINT.md`).
2. **The TOP 10 entries of `DYNAMIC_LEDGER.md`.** Newest-first, under the sentinel. This is where the project actually stands right now, and it is the counterpart to the blueprint: the blueprint is where we are going, the ledger head is where we are.
3. The re-attach carrier (§4) — for live PIDs, in-flight work and open decisions.

**Why in this order:** the carrier alone tells you what is *running*; it does not tell you what the project is *for*. A successor that reads only the carrier will faithfully continue the current task while having lost the standard it is supposed to meet. Reading the blueprint first, then the ledger head, restores goal-then-state before any judgement is made.

**Anti-pattern this closes:** treating the carrier as sufficient because it is the "guaranteed carry-over". It is guaranteed, but it is a *snapshot of motion*, not a statement of purpose — and a blueprint commitment that quietly went unmet will never surface from a carrier.

## 6. Quick checklist (before you say "green light")

- [ ] Live PIDs/services checked on the machine; progress read from logs.
- [ ] **DYNAMIC_LEDGER updated for this session's state changes** (mandatory pre-condition, §3.2); AGENT_CHANGES / COUNCIL also current on disk (nothing deferred).
- [ ] Carrier rewritten to a single, current, self-contained block (§4), fresh time-MCP timestamp.
- [ ] Carrier pruned of all superseded/deprecated blocks; still a few-KB/one-screen file.
- [ ] Relevant persistent memories updated; MEMORY.md pointer accurate.
- [ ] Only now: green light — then freeze state-mutating work until the compact lands.
