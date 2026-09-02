---
name: "session-closeout-reflection"
description: Run a four-question blind-spot audit before closing a substantial task or session, covering confidence, missing context, decision-critical assumptions, and next verification. Use for closeout or final sanity checks.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: session-closeout-reflection

> Historical provenance: a two-question closeout ritual — Q1 asked for least confidence; Q2 is attributed to Sam Altman. Extended to four questions on 2026-07-06 with Ali's blind-spot-audit block: Q3 (pivotal assumption), Q4 (verification handoff), and the closing "do not reassure me" directive. Used together they consistently catch load-bearing things that were skipped. This skill turns that ritual into an explicit, repeatable pass.

## 1. What this is
A short, honest reflection pass run at the **end** of work — not during it. Four questions, asked in order. The value is in answering them *without flattering yourself*: the point is to find what was missed, not to confirm the work is fine.

## 2. When to run it
- **Human-invoked:** whenever Ali says "end session", "wrap up", "closeout", "final pass", "blind-spot audit", "what are you least confident about", "what am I missing", "check my assumptions", "what should I verify", or similar.
- **Self-triggered (mandatory gate):** before declaring **substantial multi-step work** `complete` / `verified` / done, run this pass on yourself first and fold the result into the completion summary. "Substantial" = anything that touched multiple files, made a non-trivial decision, ran an experiment, or changed system state. Skip the self-trigger only for genuinely trivial turns (a one-line fix, a lookup, a greeting) — forcing it there is noise.
- Do **not** run it mid-task as a substitute for actually doing the investigation. It is a closeout, not a planning tool.

## 3. The four questions (ask in this order)

### Q1 — Least confident (historical prompt)
> **"What are you least confident about right now?"**

Answer protocol:
1. Enumerate honestly — aim for **6–7 concrete items** you did NOT properly investigate, verify, or that rest on an assumption. Do not pad with fake confidence and do not stop at one or two; the useful items are usually the ones you're tempted not to list.
2. For each item, state *why* it's uncertain (untested path, unread file, assumed contract, skipped edge case, external system not confirmed).
3. Triage: mark any item that is **load-bearing** — where being wrong would break the result or means you acted without understanding something first.
4. For each load-bearing item, **investigate it thoroughly and exhaustively to root cause** before calling the work done — or, if investigation is out of scope for now, surface it explicitly to Ali as an open risk rather than burying it.

### Q2 — Biggest blind spot (Sam Altman's)
> **"What's the biggest thing I'm missing about the situation right now? What don't I realize?"**

Answer protocol:
1. Step back from the task mechanics to the *situation* — the goal behind the task, the context, the human's actual intent.
2. Name the single biggest unstated assumption or framing that, if wrong, changes everything — the thing outside the current frame, not just an unchecked detail inside it.
3. If it exists, say it plainly even if it undercuts the work just completed. A finding that "this whole approach may be solving the wrong problem" is exactly what this question exists to catch.

### Q3 — Pivotal assumption (Ali's blind-spot audit, 2026-07-06)
> **"What assumption would most change your recommendation if it were wrong?"**

Answer protocol:
1. List the premises the delivered result/recommendation actually rests on — data assumptions, environment assumptions, readings of Ali's intent, "this tool/file behaves the way I remember" beliefs.
2. For each, ask: if this were wrong, would the conclusion flip, or merely wobble? Discard the wobblers.
3. Name the ONE premise with the highest chance-of-being-wrong × impact-if-wrong, stated as a falsifiable sentence — not a vague caution.
4. State the evidence that would discriminate: the observation that would confirm it or kill it.

Scope note vs Q2: Q2 attacks the *frame* (is this the right problem/approach at all?); Q3 stays inside the frame and stress-tests the single load-bearing premise of the specific answer given. If your Q3 answer restates Q2, you have not found the premise yet — dig into the mechanics of the recommendation itself.

### Q4 — Verification handoff (Ali's blind-spot audit, 2026-07-06)
> **"What should I verify with a human, source, log, or test before acting?"**

Answer protocol:
1. Collect every load-bearing item from Q1 and the pivotal assumption from Q3 that was not resolved to root cause in-session.
2. For each, name the cheapest discriminating check AND its channel: a **human** (who, asked what), a **source** (which document/URL, read raw), a **log** (which artifact, looking for what), or a **test** (which command, expecting what).
3. Phrase each as an actionable next check ("run X and expect Y", "ask Ali whether Z") — never a vague "double-check the config".
4. If genuinely nothing needs verification before acting, say so explicitly and why — silence is not an acceptable answer.

## 4. Output shape
Report concisely (respect Ali's <4-line completion-summary rule for the wrap-up itself, but this reflection may add a short block above it):
- **Least confident:** the triaged list; load-bearing items flagged and either resolved-to-root-cause or surfaced as open risks.
- **Biggest blind spot:** one sharp sentence, or an explicit "nothing material surfaced — checked the frame, the intent, and the assumptions."
- **Pivotal assumption:** the single premise that would flip the recommendation if wrong, stated falsifiably, with the discriminating evidence named.
- **Verify before acting:** the concrete next checks, each with its channel (human / source / log / test) and expected result.
- Then the normal completion summary / `result:` line.
- If a load-bearing item or a blind spot is genuinely material, do NOT silently declare done — raise it first.
- Closing discipline for the whole block: **be specific; do not reassure; give the risk, the evidence gap, and the next check.**

## 5. Discipline
1. **Honesty over reassurance.** If the honest answer to Q1 is a long list, that's the useful outcome, not a failure. Never shrink the list to look finished.
2. **No theater.** Don't fabricate uncertainties to look thorough, and don't rubber-stamp "nothing missing" to look done. Both defeat the purpose.
3. **Act on what surfaces.** A flagged load-bearing item that you then ignore is worse than not asking. Investigate to root cause or escalate — never note-and-drop.
4. **Closeout only.** This does not replace planning, the verification gate, or actually doing the work. It is the last honest look before signing off.
5. **Risk, evidence gap, next check.** Every surfaced item carries all three; a named risk without a concrete next check is note-and-drop by another name.

## 6. When NOT to use
1. Trivial single-step turns (one-line fix, a lookup, a greeting) — the self-trigger is skipped there by design.
2. Mid-task, as a stand-in for real investigation.
3. As a planning or scoping tool — it is retrospective, run at the end.
