---
name: seed-statistics-protocol
description: Author a project's seed and statistics protocol with correct input-sampling framing, n and sigma discipline, stability analysis, sensitivity disclosure, and reproducible sweep rules. Use when designing a seed sweep or statistics protocol.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: seed-statistics-protocol

## When to use
- A research project is approaching its first (or full) multi-seed sweep and needs a ratified seed/statistics protocol-of-record before launch.
- An existing single-seed/pilot result must be hardened to publication standard.
- NOT for ops/data projects without experimental claims.

## The deliverable
One document — conventionally `full-10-seed-sweep.md` at the project root — that becomes the project's **seed/statistics protocol of record** once Ali ratifies it (strict adherence thereafter). Ratified exemplars: `local-mi-article/full-10-seed-sweep.md` and `local-persona-compositionality-article/full-10-seed-sweep.md` (the second is the ported-and-re-targeted pattern: statistical spine preserved, every experiment reference replaced with the new project's).

## Contents checklist (every § required)
1. **Status header** — PLANNED/RULED status, council provenance, Ali's directives verbatim, HOLD-for-go clause.
2. **Purpose** — which headline verdicts acquire CIs/trend tests and why.
3. **The framing correction (load-bearing, first):** frozen pretrained checkpoints + no training loop ⇒ seeds perturb **input sampling and stochastic ordering only**. The training-centric vocabulary ("initialization sensitivity", "lucky seed", "N independent training runs") is a **category error** — rejected explicitly, with the correct language pinned: *"input-sampling robustness on frozen checkpoints."*
4. **Seed-perturbation design:** audit the pipeline for σ=0-by-construction metrics (deterministic extraction over a fixed corpus, greedy decoding, deterministic quantization). Where the headline metric is deterministic, DEFINE what the seed perturbs (per-seed corpus resample/subsample/fold) so n=10 is a genuine distribution, and pin per-stage seed semantics (which RNG each seed feeds).
5. **Seed count + citation:** n=10 {0..9} default; Henderson et al. (arXiv:1806.08295) cited ONLY with the mandatory frozen-checkpoint caveat attached everywhere it appears.
6. **σ=0 honesty rule:** deterministic fixed-input metrics reported as **exact determinism** (`σ=0` across `r=10` repeats, `n_eff=1` unless distinct input draws exist — stronger than any box plot); the battery is explicitly DECLINED for them.
7. **Field best-practice alignment (raw-read per the global web rule; re-confirm every quote before paper insertion):** bootstrap-over-input as PRIMARY stability instrument (arXiv:2510.00845 — ≥100 resamples, avg pairwise stability + CV, ≥0.8 bar; adopt stricter where the project already has one; never conflate fidelity-vs-reference with stability-vs-itself); the trained-instances seed axis the project *lacks* named explicitly (arXiv:2501.16496); methodology-sensitivity disclosure + robustness check on behavioral/faithfulness-style metrics (arXiv:2407.08734).
8. **The conditional statistics battery** — the per-metric instrument table (BCa bootstrap CI · Wilson CI for proportions · exact Page's L / Jonckheere–Terpstra for ordered trends · Holm-corrected paired Wilcoxon (seeds are PAIRED — unpaired tests are wrong) · exact permutation (2¹⁰ enumerable) · regime-boundary crossing probability · σ/input-null ratio · TOST exploratory-only), each row stating what it applies to and why.
9. **Operations:** tiering by per-seed cost, cheap tiers to full n FIRST, expensive tier LAST against frozen cheap results; incremental distribution figures as seeds land; **HOLD for Ali's explicit launch go**; no resource contention between tiers.
10. **Determinism seal + diagnostic gate:** seal hardening for new seeds (documented per-item as precision vs determinism choices); **same-seed-twice bit-identity diagnostic** per varying metric BEFORE invalidating already-written results — bit-identical ⇒ results stand (record the proof); leaking ⇒ hardened seal + re-run that experiment only.
11. **Per-seed audit catalogue** (one row per seed × experiment: metrics, verdicts, peak VRAM/RAM/disk, wall-clock, anomaly) + **boundary-condition rule:** a verdict-flipping seed is a FINDING written up mechanistically, never discarded.
12. **Unified visualization standard:** strip/swarm of raw seed points + overlaid box-whisker (collapses to the median line at σ=0) + `(σ=0, n=10)` annotations + capstone experiment × seed heatmap.
13. **Deliverables checklist** with checkbox state, and provenance (council rounds, Ali rulings, raw-read sources).

## Definition of done (disk-asserted)
- [ ] The document exists at the project root with the status header and HOLD-for-go clause.
- [ ] Every σ=0-by-construction metric in the pipeline is enumerated with its code-level reason (file:symbol), disk-verified.
- [ ] Every battery instrument names its target metric — no orphan statistics, no metric without an instrument or an explicit determinism exemption.
- [ ] The three best-practice sources carry the raw-read/re-verify flag.
- [ ] Council ratification is recorded (or the [PENDING — Ali] row exists in DYNAMIC_LEDGER).

## Sync note & provenance
Generalized from the two ratified sweep protocols named above on Ali's instruction, 2026-07-12. The `codex-research-lifecycle` skill carries the cross-project invariants; THIS skill authors the full per-project document — revising the doctrine revises both.
