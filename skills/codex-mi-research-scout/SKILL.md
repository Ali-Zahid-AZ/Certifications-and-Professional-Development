---
name: mi-research-scout
description: Autonomous mechanistic-interpretability research-direction finder for Ali's vault. Scans arXiv for the last ~14 days, aligns new papers against Ali's MI axioms and locked research directions, downscales 8xH100-class work to an 8GB-VRAM (RTX 4060) experiment, and assigns a cheapest-first compute tier from Cloud-Compute-Availability.md. Invoke when Ali says "scan arxiv", "find a research direction", "what's new in MI I could do", "weekly MI scan", or asks to extend/formulate an MI research idea against recent literature.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# MI Research Scout

Turn the last two weeks of arXiv into **one or more concrete, hardware-feasible MI experiments** that either *extend* a recent paper or *open a new direction*, each mapped to a costed compute tier. You are the reasoning engine; the script is only the arXiv fetcher. Bias every output toward weight/activation-level structural analysis over high-level theory.

## Canonical inputs (read live — never duplicate)
- **Axioms (hub):** `00-Personal/00-Admin/Trackers/00-Admin-Axiom-Tracker-DeepLearning-ALL.md` — this is a §4 privacy-zone file Ali has named; the named path is the *sole* permitted read there. Do **not** list or traverse `00-Personal/` otherwise. Axioms also live across the vault under the `#axiom` tag.
- **Directions (CANONICAL — read this FIRST):** `12-Agents/01-Research-Ideas/formal/research_directions.md`. Align every recommendation against this table so you do not re-propose something already locked, shelved, or pre-empted, and so you can say *which* track a new paper extends.
- **Compute tiers:** `Cloud-Compute-Availability.md` (vault root). Read at runtime so pricing/VRAM never goes stale; do not hardcode rates into output.
- **Hardware floor:** local = single **RTX 4060, 8GB VRAM**, one part-time researcher (GPU-serial, human-interleaved — no parallel-fleet assumptions).

## Governance (non-negotiable — vault rules win)
- **Read-only.** This skill never writes a vault note. Findings go to the user in chat; they reach `COUNCIL.md` only after Ali approves, via the normal council write mechanics (top-append below the sentinel, fresh tool-acquired PKT timestamp, provenance note).
- **§6 No external transmission.** Only *distilled MI keywords you compose* go to arXiv. NEVER pass raw axiom/note text, titles of private notes, or vault content into `--query` or any URL. Keywords are discovery; vault text is not.
- Use the native **Read** tool for all vault reads. Respect privacy zones §4.

## The script
`scripts/arxiv_scan.py` — runs via `uv run --script` (PEP-723, Pydantic V2, zero manual install). Emits one validated JSON object on stdout.

```
# Stage 1 (cheap — abstracts only, last N days):
uv run --script scripts/arxiv_scan.py search \
  --query "sparse autoencoder OR superposition OR persona vector OR induction head" \
  --days 14 --max 8 [--categories cs.LG,cs.AI,cs.CL,cs.NE,stat.ML]

# Stage 2 (only after an abstract aligns with an axiom):
uv run --script scripts/arxiv_scan.py methodology --id 2606.27321 [--max-sections 6] [--max-chars 2500]
```
Progressive disclosure is mandatory: **never** call `methodology` on a paper whose abstract has not already aligned with an axiom or direction — it wastes context.

## Procedure
1. **Load context (cheap first).** Read the axiom hub and `formal/research_directions.md` (the canonical tabulated index — your primary alignment surface); only drop into the `councils/` source docs for deeper prose when a paper looks like a genuine extension. Extract the active axioms (e.g. *"emergence is not summation"*, *"architecture determines the epistemology of its own interpretation"*, the archaeology/participation/collapse triad) and the locked portfolio.
2. **Compose queries.** From axioms+directions, write 1–3 keyword queries of MI terms (mechanisms, not your private phrasings). Run `search` for each.
3. **Triage abstracts** against axioms. For each paper, decide align / weak / skip. Read the `comment` field for GPU/scale hints.
4. **Deepen only the aligned.** Run `methodology` on those; read method/experiment sections.
5. **Downscale.** Isolate the paper's core mechanistic claim and design the smallest experiment that tests it on the 8GB floor — 4-bit quantized 1.5B–3B model, single layer/head, one SAE, a sub-circuit. If it cannot be downscaled, say so explicitly.
6. **Assign a compute tier** (cheapest-first heuristic, cross-referenced to the live compute file):
   - **Tier 0 — Local (≤8GB):** 4-bit 1.5B–3B, localized layer/head testing.
   - **Tier 1 — Free Cloud (≤16GB, hrs):** needs ~8B but finishes in hours → Colab T4 / Kaggle / Lightning.
   - **Tier 2 — ZeroGPU ($9/mo PRO):** bursty high-end validation.
   - **Tier 3 — Decoupled cheap (24–80GB):** sustained train / heavy logit-lens → Vast.ai / RunPod. ALWAYS prescribe the **network-volume workflow**: rent → attach volume → run → **terminate the pod (never pause)** to dodge idle-tax, data persists on cheap storage. Quote the live $/hr and a rough total.
   - **Tier 4 — Untenable:** ≥32GB for >40h with no downscaling path → reject or radically restructure; never silently recommend it.
7. **Verdict per finding:** is this an **EXTENSION** of the paper or a **NEW DIRECTION**? State which, and how it intersects the locked portfolio (does it feed P1/P2/P3, or open Direction A/B/C/D?).

## Output (one block per surviving paper)
```
### <short handle> — <EXTENSION | NEW DIRECTION>
- Paper: <title> (arXiv:<id>, <date>) — <one-line core mechanistic claim>
- Axiom alignment: <which axiom/direction it intersects, and why — first principles>
- Downscaled experiment: <the isolated 8GB-floor MI test: model, layer/head/SAE, signal, ~runtime>
- Compute tier: <Tier 0–4 + platform + live $/hr + rough total + network-volume/terminate note if Tier 3>
- Feasibility & risk: <contamination, confounds, what would falsify it>
```
End with a ranked shortlist (cheapest + highest-alignment first) and a one-line recommendation. Then ask Ali whether to draft any of these into `COUNCIL.md` — do not write the vault unprompted.

## Notes
- Default scan window 14 days; widen with `--days` if a window is thin.
- arXiv ids carry a version suffix (e.g. `...v1`); the script strips it for HTML.
- If `methodology` returns `abstract-fallback`, triage on the abstract; offer to read the PDF only if Ali wants the deep dive.
