---
name: canvas-write-protocol
description: Safely append to the estate's timestamped canvases with tool-acquired time, head re-read, conflict detection, and no stale or destructive edits. Use before writing a project canvas or rotating one.
---

# Skill: canvas-write-protocol

> **Origin (relocated, not invented):** the procedure behind the global *Canvas Write Protocol* section, the *Standing Canvases* entry formats, and *Documentation Lifecycle* item 1 (rotation, the estate sweep, the killed-claims registry). Relocated into a skill on 2026-07-30 under the estate's progressive-disclosure guidance, so the always-loaded rule files carry the mandate and the pointer while the step-by-step procedure loads when a canvas is actually being written. **Nothing was dropped in the move.** The rules remain the enforcement; this skill is the procedure they point to. Two of the clauses below were bought by real incidents, marked ★ where they appear.

## 1. What this governs

A **canvas** is an append-only, timestamped, newest-at-top file of record. Every project root carries the set:

| Canvas | Is | Written by |
|---|---|---|
| `AGENT_CHANGES.md` | The comprehensive code-change log — *what was changed* | Every agent, after every change |
| `DYNAMIC_LEDGER.md` | The single canonical task/status ledger — *what to do*; it supersedes the deprecated `STATUS.md` + `TO-DO.md` | Every agent, on every state change |
| `COUNCIL.md` | The cross-agent dialectic canvas for architectural debate *before* code changes; obey the protocol in its own header | Council participants |
| `FUNCTION_MAP.md` | Canonical inventory of operational functions grouped by source file | On gate pass / deliverable close |

**Naming grace:** legacy projects use hyphen spellings — `AGENT-CHANGES.md`, `FUNCTION-MAP.md`, `IMPLEMENTATION-PLAN.md`, `agent-roles.md`. **Use whichever spelling already exists in the project root; never create a duplicate under the other spelling.** The protocol is identical either way.

`agent_roles.md` is a standing canvas but is **not** agent-writable: only Ali defines or edits it. `COUNCIL.md` is likewise never *created* by an agent — if it is absent, ask Ali to create it from the template.

## 2. Timestamps are TOOL-ACQUIRED — never guessed

> **Acquire the time from the time MCP immediately before the write. Never hardcode it, never estimate it, never reuse an earlier one, never derive it from context.**

| Harness | Tool name | Argument |
|---|---|---|
| Codex/OpenAI seats (principal architect/lead; architecture reviewer; assurance reviewer) | `mcp__time__get_current_time` | timezone `Asia/Karachi` |
| the external review seat | `time_get_current_time` | timezone `Asia/Karachi` |

Format written into the canvas: **`YYYY-MM-DD HH:MM:SS PKT`**.

**If the time MCP is down: HOLD the write and tell Ali.** Do not substitute shell `date`. Do not substitute an estimated timestamp. Do not write the entry with a placeholder intending to fix it later. A canvas whose timestamps are sometimes real and sometimes invented has no ordering guarantee at all — and ordering is the entire value of a newest-at-top append-only file.

**Reuse is the quiet failure mode.** Acquiring the time once and stamping three entries with it destroys the ordering between those three. One write, one acquisition.

### ★ The incident that bought this — suspect yourself before the machine

An agent mis-stamped a canvas, attributed the error to clock skew in the environment, and wrote that confabulated root cause into memory **as "verified"**. It was then measured: **35 samples, zero skew.** The machine's clock was never wrong. The agent had guessed a timestamp and blamed the environment for its own shortcut.

Three lessons, all load-bearing:

1. **The clock is not the suspect.** When a timestamp is wrong, the overwhelmingly likely cause is that it was not acquired from the tool.
2. **Never record a root cause you have not measured.** "Verified" is a claim about evidence, not a confidence level.
3. **Mutable-state records need a verified-at stamp.** An observation of a changeable system silently becomes a lie once reality moves — which is exactly why the canvases are timestamped in the first place.

## 3. The append algorithm

Canvases are written concurrently by multiple agents and multiple sessions on one shared machine. **Assume a concurrent writer; do not assume you are alone.**

1. **Re-read the head, fresh.** Read the **TOP 5 entries** of the target canvas from disk right now. Not from memory, not from earlier in this session, not from a summary.
2. **Acquire the time** (§2) — *after* the re-read, so the acquisition is as close to the write as possible.
3. **Compare against the head.** If your newly acquired timestamp is **OLDER than the head entry's timestamp**, a concurrent writer has landed an entry after your read: **HOLD → re-read the head → re-acquire the time → retry.** Never write an entry that would sit above a newer one.
4. **Write only against the freshly re-read head.** The bytes you splice into must be the bytes you just read.

### ★ Abort-and-rebase is the correct behavior when the head has moved

The house pattern is an **assertion-gated splice that aborts on a moved head**: the writer asserts the head it read is still the head at write time, and **aborts rather than writing** if it is not. A failed write that aborted cleanly is a *success* of this protocol — you then re-read, re-acquire, and rebase your entry onto the new head.

The anti-pattern is the opposite instinct: seeing the head has moved and writing anyway, or force-writing a whole-file replacement built from a stale copy. That silently deletes the other writer's entry. **A canvas write must never be able to lose someone else's entry.**

## 4. Forbidden mechanics

| Forbidden | Why |
|---|---|
| `sed -i` on a canvas | In-place stream editing has no head assertion and no concurrency awareness; it will happily rewrite a file that moved under it |
| **Stale-temp-copy editors** — read to a temp file, edit the temp, write it back | The write-back is a whole-file replacement built from a snapshot that is already out of date; every entry landed in between is destroyed |
| Writing **at or above** the `STRICTLY PROHIBITED to write above this line` sentinel | Everything above the sentinel is the canvas's own header/protocol. It is not content |
| **Deleting** an entry | Canvases are append-only. Corrections are new entries, never edits to old ones |
| **Reordering** entries | Order is the record |
| **Truncating** `>` redirection onto a canvas | Same failure as the temp-copy, with no read at all |
| Rewriting a canvas to make it "lean" | Leanness is a **re-attach carrier** discipline, and it is explicitly carrier-only. It never applies to a canvas |

**Where to write:** append **newest-at-top, directly below the sentinel.**

### Stamping authority

| Stamp / action | Who |
|---|---|
| `[CONVERGED — RECOMMEND CLOSE]` | **Any agent** may stamp this |
| `[CLOSED]` | **Ali only** |
| Purge / prune / rotate-in-place | **Ali only** |
| `git commit` / `git push` of a canvas | **Ali only** |

An agent that believes a council is finished stamps `[CONVERGED — RECOMMEND CLOSE]` and stops. Closing is Ali's ruling, not a conclusion an agent reaches on its own.

## 5. Entry formats, per canvas

### `DYNAMIC_LEDGER.md`

```
### [YYYY-MM-DD HH:mm:SS PKT] | [TAG] | [Brief Topic]
```

| Tag | Means |
|---|---|
| `[PENDING]` | Not started; queued |
| `[IN_PROGRESS]` | Actively being worked |
| `[BLOCKED]` | Waiting on Ali, an external system, or a gate |
| `[DONE]` | Complete, with the outcome recorded |

**On a state change, RE-TAG the existing entry — never delete it, never write a duplicate entry for the same item.** The tag history is how a dormant project explains itself months later.

Two standing obligations that land here:

- **Every P0/P1 finding from any audit becomes its own `[PENDING]` entry at audit close.** Findings that live only in a report's prose fall off the moment a project goes dormant.
- **Destructive commands and human-only SaaS-console actions are recorded here, not executed.** Record the exact command plus a one-line rationale as `[PENDING]`; Ali runs it; on his confirmation re-tag `[DONE]` with the timestamp and the outcome.

### `AGENT_CHANGES.md`

Five fields, every entry:

| Field | Content |
|---|---|
| **Timestamp** | `[YYYY-MM-DD HH:MM:SS]` PKT, tool-acquired (§2) |
| **Action** | Brief description of what was installed / changed |
| **Commands Executed** | The exact terminal commands used |
| **Files Modified** | Absolute paths to every file altered |
| **Outcome** | Success / Failure, plus relevant output metrics — and the verification-gate result where code changed |

Log **every** change: system change, installation, permission modification, configuration update, code edit. The ledger says what to do; `AGENT_CHANGES.md` says what was done.

### `COUNCIL.md`

Append-only, newest-at-top below the sentinel, and **obey the protocol in the file's own header** — it may add project-specific turn structure on top of this skill. Every factual claim in a council turn carries its exact source URL, raw-read (never from a summarizer, never quoted out of a search result).

### `FUNCTION_MAP.md`

Canonical inventory of operational functions, **grouped by source file**, append-only — no deletion without Ali. Two-tier status legend, and the tiers are not interchangeable:

| Status | Means |
|---|---|
| `PLANNED` | Reserved by the implementation plan; not yet built |
| `CODE-COMPLETE` | Past the Verification Gate, **not yet exercised** |
| `OPERATIONAL` | Past the Verification Gate **AND** exercised end-to-end by a DONE deliverable |

Passing the gate alone never earns `OPERATIONAL`. (Gate procedure: the `codex-engineering-standards` skill.)

## 6. Rotation into the archive tree

**The root canvas is always the LIVE file.** It is the one agents read and append to.

When a phase closes, or the file grows large:

1. **Rotate the content** into the append-only archive tree: `docs/documentation/.../NN-<name>.md`, with **zero-padded** `NN` so lexical order is chronological order.
2. **The root restarts fresh** — the live file continues from empty (below its sentinel/header).
3. **Archives are immutable, citable sources of record.** They are never edited, never re-stamped, never corrected in place. A superseded gate string, a retired canvas name, or a killed doctrine claim found inside an archive is **not a finding** — it is the record of what was true when written. Rewriting it would violate the append-only and plan-freeze doctrines.
4. Closed councils may be archived as `NN-COUNCIL.md`.

### Rotation triggers — a trigger, not a vibe

**Propose rotation as a `[PENDING]` ledger item when either fires:**

- A council is stamped `[CLOSED]`, or
- **a live canvas exceeds ~150 KB.**

The threshold applies to **every** standing canvas, not only `COUNCIL.md` — `AGENT_CHANGES.md` is the one that grows fastest and it is the one a council-shaped filter misses. "May be archived" with no trigger means it never is; that is why the trigger is written down and why rotation goes into the ledger as a tracked item rather than a good intention. Rotation itself is Ali's action (§4).

## 7. The estate sweep — when a name or a claim dies

This is the highest-cost failure mode in the whole protocol, because the cost is paid later, by someone else.

**Trigger the sweep on either event:**

- A **Standing-Canvas rename or consolidation** (a canvas name changes, two canvases merge, a file is retired), **or**
- **any time a doctrine claim is proven false.**

**The procedure:**

1. **Sweep the whole estate for the dead string.** Use a python `os.walk` sweep for exhaustive recursion into **nested and hidden directories** — so that a MISS actually proves absence. A shallow or glob-based search that skips dotted directories returns "not found" for a string that is still live in three files, which is worse than not searching.
2. **Fix every live cross-reference** before declaring the change done. Rule files, skills, project instruction files, playbooks, deploy templates, `verify.sh` scripts — estate-wide. Deliberately **skip** the exempt classes: archives, rotated docs, councils, audits, append-only canvases, backups, dated memos.
3. **Register the killed claim** in `system-level/KILLED-CLAIMS.md` — the registry's ruled home since 2026-07-18, and where `estate_health_check.py` **check 12** reads it. Bring: the claim as doctrine actually phrases it, a signature matching the **assertion** rather than merely its vocabulary, disk-verifiable evidence with the date it was checked, and a **revisit trigger naming an observable event** (never a mechanism). Agents **propose** rows; **only Ali confirms, amends, or removes them.**
4. **Run the health check** and confirm no live rule file re-asserts the claim.

**Why both the sweep and the registry exist, in that order:** *the sweep is the control; the registry is the backstop.* On 2026-07-17 the estate disproved a doctrine claim and corrected the three global rule files — and the same claim **survived for hours** in the playbook that seeds every new research project, found by a sibling project rather than by any check. **A claim killed in one rule file survives in every other until swept.** The registry is for the day someone forgets, which is the day it will matter — it does not license skipping the sweep.

Corollary from the same doctrine: **a fix that makes doctrine LONGER is a restatement, not a fix.** When you kill a claim, delete it — do not append a correction beside the surviving copy and call it swept. A true copy rots exactly like the false one did.

## 8. When NOT to use this

1. **The re-attach carrier memory file.** It is a transient snapshot, deliberately rewritten and pruned on every refresh — the narrow, explicitly-scoped exception to append-only discipline. See the `compaction-required-greenlight` skill. If you are unsure which file is the carrier, **rewrite nothing** and confirm first.
2. **Ordinary source files, configs and documentation.** Normal editing rules apply there.
3. **`agent_roles.md`** and the creation of `COUNCIL.md` — Ali's, not yours.
4. **Reading** a canvas. This protocol governs writes; reading the head is encouraged, and re-reading the top entries at session start is required.

## 9. Quick checklist (before every canvas write)

- [ ] Correct canvas identified, in the correct spelling that **already exists** in this project root.
- [ ] TOP 5 entries re-read **from disk, just now**.
- [ ] Timestamp acquired live from the time MCP, `Asia/Karachi`, immediately before the write — not reused, not guessed, not shell `date`.
- [ ] New timestamp is **newer** than the head; if not, HOLD → re-read → re-acquire → retry.
- [ ] Write is an append **below the sentinel**, newest-at-top; nothing at or above it touched.
- [ ] No `sed -i`, no temp-copy write-back, no truncating redirect; head-assertion aborts rather than clobbers.
- [ ] Entry matches this canvas's format (§5); a state change **re-tags** the existing entry rather than deleting or duplicating it.
- [ ] Stamping stayed within authority — `[CONVERGED — RECOMMEND CLOSE]` at most; `[CLOSED]` / purge / commit is Ali's.
- [ ] Canvas over ~150 KB or council `[CLOSED]`? Rotation proposed as a `[PENDING]` ledger item.
- [ ] Did this write kill a name or a claim? Then the §7 sweep + `KILLED-CLAIMS.md` row are part of "done".
