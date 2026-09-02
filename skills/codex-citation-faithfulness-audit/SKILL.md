---
name: citation-faithfulness-audit
description: Portable 100%-coverage citation-integrity gate for research manuscripts — a six-dimension audit (DEAD_LINK, QUOTE_MISMATCH, OVERCLAIM_VERB, TAXONOMY_AMBIGUITY, MATH_MISALIGNMENT, FRAMING-FIDELITY) that blocks every reference from the frozen references file (references.bib) until it passes BOTH the claim-side audit and the source-side verbatim backstop. Invoke when a paper approaches its references freeze ("audit the citations", "run the literature audit", "verify the bibliography", "freeze references.bib"), or whenever any citation's faithfulness is questioned. Generalized from local-mi-article's LITERATURE-AUDIT-PROTOCOL.md; where a project ships its own protocol doc, that doc governs and this skill is the portable fallback.
---

# Skill: citation-faithfulness-audit

## When to use
- A manuscript is approaching its references freeze — no entry reaches the frozen references file (`references.bib` or equivalent) until it passes this gate.
- A specific citation's faithfulness is challenged (by a reviewer, an audit, or a doubt).
- NOT for literature *discovery* (that is mining/scouting); this gate audits what discovery already captured.

> **Sync note:** generalized from `local-mi-article/LITERATURE-AUDIT-PROTOCOL.md` (the proven original — it caught a real methodological flaw pre-manuscript). If either that doc or this skill is revised, check the other. In local-mi-article, the project doc governs.

## The integrity guarantee
**Zero fabricated or distorted citations.** A sampled check can only ever say "no fabrication in the X% we checked" — which is NOT "zero fabrication". The mechanical verbatim check therefore runs at **100% coverage, never sampled**.

## Inputs (per reference R)
- `verbatim_extract` — the exact source passage captured at mining time.
- `triggered_claims[]` — every manuscript sentence citing R.
- The live source URL/DOI. All source fetches follow the global **Raw Web Reading** rule (cited by name — raw body only, never a summarizer middleman).

## The 6-dimension gate (a single hit on ANY dimension = FAILED)
| # | Dimension | FAILED when |
|---|---|---|
| 1 | **DEAD_LINK** | URL/DOI unreachable or does not resolve |
| 2 | **QUOTE_MISMATCH** | `verbatim_extract` not found in the normalized raw source body |
| 3 | **OVERCLAIM_VERB** | attribution verb exceeds the source ("proves"/"shows" where the source "reports"/"suggests") |
| 4 | **TAXONOMY_AMBIGUITY** | the branch/category the manuscript files R under is unsupported by the source |
| 5 | **MATH_MISALIGNMENT** | method/metric attribution wrong (cites a metric or setup the source did not use) |
| 6 | **FRAMING-FIDELITY** | the citing sentence is not logically supported by R's `verbatim_extract` |

## FRAMING-FIDELITY in detail (the most common overclaim vector)
A reference can pass resolvability + quote + verb checks and still be cited for a claim its source never substantiated. For each citing sentence, check the extract supports the claim's **TYPE** (empirical / historical / methodological), **PRECISION** (the exact quantization level, model, technique named), and **SCOPE** (hardware, metric, population).
- METHODOLOGICAL ("the method introduced by X") → PASS if the extract describes that method.
- HISTORICAL ("prior work includes") → PASS if the extract establishes field presence.
- EMPIRICAL ("X showed A survives B") → PASS only if the extract reports A + B + the survival.
- Precision misclassification (claim says int4, source tested int8) → FAILED.
- Method-to-result confusion (cite a method, claim a result it never produced) → FAILED.

## Two independent passes (both run, never merged)
1. **Claim-side audit** — reads the captured `verbatim_extract` against `triggered_claims[]`: does the CLAIM's language match what the extract says? FRAMING-FIDELITY on 100% of citations (cheap; uses the already-captured extract).
2. **Source-side backstop** — independent verbatim re-fetch of the actual source: does the SOURCE contain the evidence? Tiered:

| Tier | Check | Coverage | Catches |
|---|---|---|---|
| **T1 mechanical** | URL resolves + verbatim parity in normalized raw body | **100% (ALL refs)** | DEAD_LINK, QUOTE_MISMATCH |
| **T2 framing** | re-read source abstract/intro against the claim | ~30–40%, risk-stratified (strong-claim / non-arXiv / codename-derived) | source-side FRAMING-FIDELITY |
| **T3 full** | full 6-dimension audit + source Methods read | FAIL/contested only (~5–10%) | all dimensions |

Assign the two passes to two independent auditor seats per `agent_roles.md` where the project has them; a single-agent project runs them as two SEPARATE passes (claim-side fully before any source-side re-fetch) — never one combined read. Report coverage transparently: "T1 = 100%; T2 deep-checked N of M (the high-risk subset); the remaining M−N passed mechanical T1."

## Re-mine policy
A FAILED reference triggers **one** re-mine cycle (cap = 1). Still FAILING → **BLOCKED** → escalate to Ali. Dropped references land in `references_dropped.jsonl` with the reason (scientific honesty: explored, not citably usable). Hallucinated-citation flags stay inline ("⚠ hallucinated — do not cite"); never silently dropped.

## Definition of done (disk-asserted — check each on disk, not from memory)
- [ ] Every entry in the frozen references file has a PASSED audit record (100% — count entries vs verdicts).
- [ ] `references_dropped.jsonl` (or equivalent) exists and holds every FAILED/dropped ref with reasons.
- [ ] Annotated bibliography present: each entry carries branch, intended use, and its supporting verbatim extract.
- [ ] The coverage sentence (T1/T2/T3 numbers) appears in the audit report and matches the verdict counts.
- [ ] Audit close logged in AGENT_CHANGES.md; any BLOCKED refs have their own [PENDING] DYNAMIC_LEDGER rows.

## Hard rules
1. 100% mechanical coverage is non-negotiable — no sampling shortcut, ever (compute time is never a valid reason for a proxy).
2. Every quote confirmed verbatim in the raw source body before it is written anywhere (global Raw Web Reading + claim-level-citation rules, cited by name).
3. The gate BLOCKS the references freeze — no PASS, no `.bib` entry, no exceptions without an explicit, logged Ali override.
4. Verdicts trace to recorded artifacts (audit rows), tagged per producing pass; on prose-vs-data conflict, data wins.
