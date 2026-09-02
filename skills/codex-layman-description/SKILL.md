---
name: layman-description
description: Explain project status in plain, non-technical English with an answer-first summary, decisions needed from Ali, honest risks, and next steps. Use when Ali asks for a layman or simple description.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: layman-description

> **Why this exists (Ali, in his words):** *"I get overwhelmed with so much going on. Unlike you, I am human and my organic brain can only take in a certain amount of information at a time, so I need to be given the main points in easy terms so that I can be aware of where we stand."* This skill is the standing translation layer between the agent's technical work and a human under real cognitive load. It is not optional politeness — it is how Ali stays oriented and in command.

## 1. What this is

A pass that converts the technical firehose (change logs, council debates, code, run state, decisions) into a short, plain-English briefing a non-coder can absorb in about a minute. It answers four questions, every time: **What just happened? Where do we stand? What needs YOU? What's next?**

**Simple is not the same as dumbed-down or sugar-coated.** Plain language is a precision tool, not "talking down" — the goal is that Ali understands *accurately*, including the bad news, the risks, and the open questions. Never trade honesty for comfort to make the summary feel tidy.

## 2. When to invoke

Trigger on any request for a simple/human-readable account, e.g.: "layman description", "in simple terms", "simple/plain English", "explain simply", "dumb it down", "ELI5", "break it down for me", "catch me up", "where do we stand", "what's going on", "non-technical summary", or "I'm overwhelmed / lost." Also invoke proactively when you're about to hand Ali a dense technical result and he has signalled overload — offer the layman version alongside it.

## 3. The output template (use these sections, in this order)

Answer-first, then detail. Keep the whole thing to roughly one screen.

1. **The one line (bottom line up front).** If Ali reads nothing else: the single most important thing right now, in one sentence.
2. **Where we stand.** 2–4 plain sentences, or a tiny status table, describing the current state like a status light — *on track · waiting on something · stuck · decision needed.*
3. **What happened** *(over the window — default ~last 2 hours; state the window you used).* 3–6 bullets, most important first. Each bullet = *what we did* + *why it matters to you*, in everyday words. No file names, no jargon, analogy where it helps.
4. **What it means / what was decided.** The implication of the above, and any decision that got made, in plain terms.
5. **What needs YOU.** The specific things only Ali can decide or do (approvals, choices, an action on another system). Flag these clearly — they are the action items. If nothing needs him, say so.
6. **Next immediate steps.** The very next 1–3 actions (who does what, in order). Concrete, not vague.
7. *(optional)* **The big picture in one analogy.** A single metaphor for the whole situation, if it genuinely helps.
8. **Want more?** One line inviting him to zoom in on any point ("say the word and I'll go deeper on any of these"). This is deliberate progressive disclosure — headline now, detail on demand.

Scale to the ask: a quick "catch me up" may need only sections 1–2 and 6; a full "where do we stand and what's next" uses all of them.

## 4. The craft rules (how to write each line)

Grounded in established communication frameworks (sources at the bottom):

- **Answer first (BLUF / Minto Pyramid Principle).** Lead with the conclusion, then support it. Never make Ali wade through background to reach the point. [BLUF; Minto]
- **Plain-language mechanics (Plain Writing Act / plainlanguage.gov).** Short sentences (aim <~20 words). Common everyday words. **Active voice** — name who does what ("we froze the design", not "the design was frozen"). Personal pronouns (you/we). One idea per sentence. [OPM / plainlanguage.gov]
- **The Feynman test — Ali's own calibration.** Explain it so a **sharp, highly-educated non-specialist** fully understands. Ali's concrete benchmark is his wife, a **medical doctor** — brilliant and highly educated, but outside physics / maths / LLMs / AgentOps: if she would get it, it's clear enough. Gloss every domain term, but keep the underlying reasoning **fully rigorous** — a hollowed-out "simple" version that quietly drops the real logic fails the test (she, and he, will notice). If you can't say it without jargon, you don't yet understand it well enough — simplify again, bridging from what he already knows via analogy. [Feynman technique; see the [[ali-explains-to-doctor-wife]] memory]
- **Beat the curse of knowledge.** You know the internals; he doesn't, and expertise makes you blind to that gap. Assume zero shared jargon; if a technical term is unavoidable, gloss it in the same breath. [Heath, *Made to Stick*]
- **Respect working-memory limits (cognitive load / chunking).** People hold only ~5–9 things at once — keep each list to ≤~7 items, group related points, and cut anything that isn't load-bearing. Fewer, sharper points beat a complete inventory. [Miller 7±2; Sweller cognitive load]
- **Progressive disclosure.** Show the essential layer; offer the rest on demand. Don't pre-dump every detail "just in case." [Nielsen Norman Group]
- **Concrete and quantified.** "3 of 5 steps done", "about 2 hours", "one file left" — numbers and objects anchor understanding better than adjectives.
- **Tables for status** when 2+ items share fields (per Ali's presentation standard), kept small.
- **Honesty over reassurance.** Surface risks, blockers, and uncertainty in plain words. A calm "we hit a snag and here's what it means" is the job; false cheer is a failure.

## 5. How to gather the material (so the summary is true, not invented)

Before writing, pull the actual record for the window — don't summarize from memory:
- **`AGENT_CHANGES.md`** entries whose timestamps fall in the window (what was actually done).
- **`COUNCIL.md`** for decisions/debates; **`DYNAMIC_LEDGER.md`** for task status; the **cold-open/live-state carrier** for current run state and open Ali-decisions.
- **`git log --since=...`** and this session's own actions.
- For each technical item ask: *"What would Ali care about here, in one plain sentence — and why does it matter to him?"* Keep the meaning, drop the mechanism.
- **Claim→artifact discipline still applies:** every "done" in the layman summary must trace to a real logged artifact. Simplifying the language never licenses inventing or inflating progress.

## 6. Time-window handling

Default to **~the last 2 hours**. Honor whatever Ali specifies instead — "the last hour", "today", "this week", "since we last spoke", "since the last compaction", "the whole project so far", or an explicit range. **Always state the window you actually used** ("Here's the last ~2 hours:") so he knows the scope.

## 7. Worked example (technical → layman)

**Technical (as logged):** *"Promoted the compaction gate to global Session Hygiene rule #3 (tri-file parity, AGENTS≡project-rules); thinned 6 per-project rule sections plus the research-lifecycle session-hygiene section to pointers; slimmed 4 drifted memory files (4 distinct md5s) to provenance-pointers; anchor-gated splice, 18 files, 18 backups; zero health-check regressions."*

**Layman:** *"We had one important safety habit — 'always save a fresh summary before wiping the AI's short-term memory' — written down in about a dozen scattered places, and the copies had quietly started to disagree with each other. I moved it into one master rulebook that every AI reads, turned the detailed how-to into a single reusable checklist, and changed all the scattered copies into short 'see the master' notes. Nothing was deleted, and every file was backed up first. The result: one source of truth instead of twelve drifting ones. Think of it as replacing twelve dog-eared photocopies of a recipe with a single laminated card on the fridge that everyone uses."*

Notice: no file names, no hashes, no "md5/parity/splice"; one analogy; the reassurance ("nothing deleted, backed up") is true and load-bearing, not filler.

## 8. What NOT to do

- Don't dump jargon, file names, function names, hashes, or command lines. If Ali wants that, he'll ask for the technical version.
- Don't bury the lede — the most important thing is sentence one, never paragraph four.
- Don't list *everything*; list what **matters to him**. Completeness is the technical log's job, not this.
- Don't write a wall of text. If it's more than ~one screen, you haven't finished simplifying.
- Don't sugar-coat, over-reassure, or hide a blocker inside soft language.
- Don't invent or round-up progress to make the picture look cleaner than the artifacts support.

## 9. Close every layman briefing by

Naming **what (if anything) needs Ali's decision**, stating **the next step**, and **offering to go deeper** on any point. He should finish it knowing exactly where things stand and what, if anything, is now in his court.

---

## Sources (discovery-sourced; frameworks described in my own words)
- BLUF — Bottom Line Up Front: https://en.wikipedia.org/wiki/BLUF_(communication)
- Minto Pyramid Principle (answer-first): https://www.betterup.com/blog/minto-pyramid
- Plain language / Plain Writing Act of 2010: https://www.opm.gov/information-management/plain-language · https://www.plainlanguage.gov
- Feynman technique (explain simply, analogies, find the gaps): https://modelthinkers.com/mental-model/the-feynman-technique
- Curse of knowledge (Heath, *Made to Stick*): https://maestrogroup.co/curse-of-knowledge
- Cognitive load & chunking (Sweller 1988; Miller 7±2, 1956) + progressive disclosure (NN/g lineage): https://www.linkedin.com/pulse/progressive-disclosure-ux-reducing-cognitive-load-one-margub-alam-sc38c · https://www.interaction-design.org/literature/topics/progressive-disclosure
