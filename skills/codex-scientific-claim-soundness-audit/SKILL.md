---
name: scientific-claim-soundness-audit
description: Audit whether an empirical claim is established by its method and evidence, using adversarial claim, design, statistics, scope, and reporting checks. Use when drafting, reviewing, or freezing a claim, verdict, framing, or preregistration.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: scientific-claim-soundness-audit

## When to use
- **Automatically, as a MANDATORY embedded lens in every evaluative Codex/OpenCode sub-agent prompt** — any feedback, opinion, audit, verification, design sanity-check, or council deliberation (wired by `codex-subagent-orchestration`, cited by name). Purely mechanical delegations that produce no claim (bulk reformatting, file moves, scaffolding, mechanical bulk edits) are the sole exemption.
- Whenever a **claim, verdict, framing, or pre-registration** is being drafted, reviewed, ruled, or frozen — a BLUEPRINT section, a paper claim, a council ruling, a Gate rubric, an abstract sentence, a client-deliverable conclusion, an ops post-mortem root cause.
- Before any design-of-record freeze or claim sign-off — this is the last adversarial pass a claim gets before it becomes a commitment.
- **Domain-general.** The gate applies to any empirical claim: research findings, ML-based science (model performance as evidence), analytics/BI conclusions, LLM/agent eval verdicts, ops root-cause claims. §Domain adapters supplies per-field vocabulary; the dimensions themselves never change.
- NOT a substitute for: mechanical code correctness (→ the global Verification Gate), citation faithfulness (→ `citation-faithfulness-audit`), or literature discovery (→ scouting). It COMPOSES with all three; it targets the claim↔method↔evidence relationship those gates do not check.

> **Why this skill exists (the incident that bought it).** A research direction was once drafted to claim two modalities' concepts live in **"superposition / a shared subspace"** — an **ontological** claim — while the proposed measurement was **passive representational geometry** (cosine alignment, MDS). An external referee (the architecture reviewer, GPT-5.6 Codex, 2026-07-15) flagged that a passive snapshot cannot establish a shared-subspace claim — two things looking aligned is not two things being the same; only a **causal interchange test** ("intervene on one, does the other move?") licenses the stronger word. Every code-correctness gate had PASSED — they test whether the *machinery* works, never whether the *claim* is sound. The fix was a cheap document edit at pre-registration; without this lens it would have surfaced at peer review, **after** the compute was spent measuring the wrong thing. This skill is that referee lens made standing, so it fires **before** the commitment, on every claim, without waiting for an external reviewer.

## The one load-bearing question (and its severity twin)
> **Can the method actually ESTABLISH the claim — or only something weaker?**
> And the severity check (Mayo): **would the claim have passed this test just as well even if it were false?** A test the claim could not have failed is no test at all.
> If only something weaker: (1) restate the claim to *exactly* what the method establishes, and (2) name the additional test (typically a causal/interventional manipulation) that would license the stronger claim, and make that test — not the weaker evidence — the deciding artifact.

Everything below operationalizes this question. A claim that survives it is SOUND; a claim that needs (1)/(2) is an OVERCLAIM until narrowed or re-instrumented.

## The design-class certainty ladder (GRADE-adapted)
Before running the dimensions, grade the evidence's **starting certainty from its design class** — the claim's verb may never demand more certainty than its design class can supply:

| Design class | Starting certainty | Can it ever carry a causal/mechanistic verb? |
|---|---|---|
| Causal intervention with pre-registered prediction (interchange/patching, randomized experiment, switchback/holdout) | **HIGH** | Yes — this is the only class that earns one |
| Controlled manipulation without pre-registration (post-hoc ablation, A/B without frozen hypothesis) | **MODERATE** | Only with narrowed scope + disclosed post-hocness |
| Passive/correlational observation (geometry, probes, dashboards, correlations, attention weights) | **LOW** | Never on its own |
| Anecdote, demo, single case, cherry-picked example | **VERY LOW** | Never |

Each dimension FAIL downgrades one level; a large pre-registered effect surviving an adversarial control may upgrade one level (never into a causal verb). The final grade **annotates** the claim in the audit table; the three verdicts below remain the only freeze gate. Rationale (GRADE's core move): certainty is set first by *what kind of study you ran*, not by how impressive the numbers are.

## The 13-dimension gate (a single hit on ANY dimension = the claim is not yet sound)

**Cluster A — claim ↔ method**

| # | Dimension | FAILED when |
|---|---|---|
| 1 | **METHOD-CLAIM GAP** ★ | the method cannot establish the claim's CATEGORY — correlational/associational evidence advanced for a **causal** or **mechanistic** claim; a passive **snapshot** advanced for a claim about **function, routing, or dynamics**; observational co-occurrence advanced for **necessity/sufficiency**. The most common and most damaging failure. |
| 2 | **MEASUREMENT-CONSTRUCT MISMATCH** | the metric does not operationalize the construct the claim names — a proxy measured perfectly is still not the thing ("engagement" ≠ clicks, "reasoning" ≠ benchmark accuracy, "concept presence" ≠ probe accuracy). The claim inherits the proxy's gap, silently. |
| 3 | **ONTOLOGICAL OVERREACH** | a loaded theoretical term is asserted where only an operational measurement exists — *superposition, represents, encodes, understands, knows, plans, causes, drives* — none of which a correlational or geometric measurement can bear. Prefer the operational restatement (doctrine below). |
| 4 | **SEVERITY** (subsumes FALSIFIABILITY) | the claim would have passed this test even if false — no pre-registered null, no stated observation that would REFUTE it, or a test so weak that passing carries no information. A design that can only confirm is not a finding. |

**Cluster B — design integrity**

| # | Dimension | FAILED when |
|---|---|---|
| 5 | **CIRCULARITY** | the measurement presupposes the conclusion — the metric, threshold, or contrast is constructed so the hypothesis structurally cannot lose (defining the "X circuit" as whatever moves the X readout, then reporting that it moves the readout). |
| 6 | **EVIDENCE CONTAMINATION** | the evidence was shaped by information it must be independent of — train/test leakage, temporal leakage (future information in features), duplicate or near-duplicate records across the split, benchmark contamination in a model's training data, double-dipping (same data selects the hypothesis and confirms it). The dominant *empirical* claim-killer in ML-based science. |
| 7 | **DESIGN THREATS** (broadened from CONFOUND LEAKAGE) | the contrast varies more than the thing under test, or the sample was shaped by the outcome — confounds/nuisance variables not held fixed or regressed out; selection and survivorship effects; attrition; regression to the mean; instrumentation drift (the measure changed meaning mid-study); testing effects. The effect could be the nuisance, not the target. |
| 8 | **INSTRUMENT SANITY** | the measuring instrument was never shown to discriminate — no negative control (run it on a randomized/null target: if the probe, saliency map, metric, or dashboard reports the same "finding" on noise, the instrument is broken) and no positive control (it detects a known-planted effect). A positive result from an unvalidated instrument is uninterpretable. |

**Cluster C — statistics & scope**

| # | Dimension | FAILED when |
|---|---|---|
| 9 | **STATISTICAL DISCIPLINE** | a single-metric or single-threshold "win" with no effect size, no cross-seed/resample variance, no multiple-comparison correction across everything actually tried; a threshold chosen after looking; **forking paths** — analysis choices (subsets, exclusions, metrics) made after seeing the data, which inflates false positives even when only ONE analysis is run. Repair: pre-registration or a multiverse/specification-curve disclosure. |
| 10 | **SCOPE INFLATION** | the claim's scope exceeds the evidence's scope — N=1 model/system → universal claim; single-modality → cross-modal; single-seed → "robust"; one architecture/market/quarter → "X does Y". An instance-specific result licenses only an instance-specific claim. |
| 11 | **CORRELATED-BET** | multiple "independent" confirmations sharing one common cause are counted as N independent shots — one model's many metrics/layers/probes, one dataset's many slices, one pipeline's many dashboards are **one correlated bet**, not N. Robustness across a shared confound is not robustness. |

**Cluster D — reporting**

| # | Dimension | FAILED when |
|---|---|---|
| 12 | **CLAIM-BOUNDARY DRIFT** | the verbal claim's **VERB / TYPE / PRECISION / SCOPE** exceeds the artifact — "proves"/"causes"/"shows" where the artifact is only "consistent with"; a mechanistic verb on associational data; a precision the artifact did not isolate; **spin** — rhetoric that survives verb-checking: *promising, encouraging, striking, clearly, trend toward significance, considerably, novel* — and favorable framing of a secondary outcome when the primary failed. Every spin word is either deleted or backed by a named artifact. |
| 13 | **NULL-AS-INFORMATIVE** | a null or negative result is reframed as failure, hidden, or quietly dropped, rather than reported as the informative instance-specific negative it is; or the desired conclusion is smuggled in as an "expected result." |

Report per-dimension PASS/FAIL with file:line (or claim-locator) evidence — never a blanket verdict.

## The operational-over-ontological doctrine
When a claim uses a theoretical/ontological construct the method cannot directly observe, **restate it as the operational claim the method CAN establish, then (optionally) add the causal test that would earn the ontological word.**

| Ontological claim (needs a mechanism the method can't see) | Operational restatement (what a measurement establishes) | The test that would earn the ontological word |
|---|---|---|
| "A and B concepts are in **superposition** / share a subspace" (the founding incident) | "under representation R and decomposition S, A and B route through features that are {shared / separable} by metric M, with null N" | **causal interchange**: patch A's feature into a B run — does the B readout move as predicted? |
| "this component **represents** X" | "ablating/patching this component changes the X readout by Δ, matching the pre-registered Δ" | pre-registered ablation Δ == observed Δ (resample/interchange patching, never zero-ablation) |
| "the system **understands** X" | "output behavior on X-contrast stimuli differs by ..." | a behavioral + causal manipulation that dissociates understanding from surface correlation |
| "the campaign/change **caused** the lift" | "metric M moved by Δ coincident with X, under holdout/baseline H" | randomized holdout, geo-split, or switchback whose pre-registered prediction matches |

Doctrine: **operational is always safe to claim from a matching measurement; ontological/causal is earned only by an intervention whose result matches a pre-registered prediction.** Name the metric, the representation, and the null in the claim itself — an unnamed theoretical construct is an overclaim by construction.

## Domain adapters (vocabulary only — the 13 dimensions never change)
| Domain | Typical DESIGN THREATS (dim 7) | Typical CONTAMINATION (dim 6) | The canonical severe test |
|---|---|---|---|
| **Mechanistic interpretability** | stimulus confounds (lexical content, speaker, pitch, energy, spectral envelope, length), layer/position imbalance | probe train/eval overlap; SAE trained on the eval distribution | causal interchange / resample patching with pre-registered Δ; negative control = randomized-model probe |
| **ML-based science** (model performance as evidence) | cohort selection, label shift, class imbalance | the 8 leakage types: no split, preprocessing on full data, feature leakage, duplicates, temporal leakage, non-independence, sampling bias, illegitimate features | out-of-distribution / temporal-holdout validation; negative control = shuffled labels |
| **Analytics / BI / ops** | seasonality, mix shift, survivorship in retained cohorts, regression to the mean after an extreme period, metric definition drift | pre-period contaminated by the change; selection on the dependent variable | holdout market / switchback / difference-in-differences with pre-registered direction |
| **LLM / agent evals** | prompt-template sensitivity, judge-model bias, position bias | benchmark items in training data; judge sees the candidate's identity | held-out paraphrase set + judge blinding + a null system scoring baseline |

An adapter row is a *starting checklist*, not a ceiling — the auditor names the domain's nuisances explicitly per claim.

## The audit procedure (how a Codex/OpenCode reviewer runs this lens)
1. **Extract every load-bearing CLAIM** from the artifact under review (blueprint section, paper sentence, council ruling, Gate rubric, pre-registration, client conclusion). A load-bearing claim is one a reader would cite or a reviewer would attack.
2. **Classify each claim's TYPE** — descriptive / correlational / causal / mechanistic / existential / universal — and its **design class** (certainty ladder above); name the method that would be required to establish that type.
3. **Run the 13-dimension gate** on each claim; per-dimension PASS/FAIL with evidence; downgrade the certainty grade per hit.
4. **For each FAIL, produce the minimal repair**: the narrowed restatement the current evidence licenses, PLUS the additional test (usually causal/interventional) that would license the original claim. Repairs are concrete edits, not "consider revising."
5. **Verdict** (per claim and overall):
   - **SOUND** — method establishes the claim; verb/scope match the artifact.
   - **SOUND-WITH-NARROWING** — sound after the named restatement; no re-instrumentation needed.
   - **OVERCLAIM-BLOCK** — the claim requires evidence the design does not produce; blocks any freeze/sign-off of that claim until narrowed or re-instrumented.
6. **Emit the per-claim audit table** (the mandatory artifact — coverage is provable, not asserted):
   `| # | Claim (verbatim) | Type | Design class → start certainty | Dimensions hit | Certainty after | Verdict | Repair |`
7. **Log** the audit entry per the target project's Canvas Write Protocol (`AGENT_CHANGES.md`; and `COUNCIL.md` when one is open) — fresh PKT via the time tool, head re-read + inversion check, assertion-gated splice below the sentinel, `sed -i`/stale-copy editors forbidden. A read-only auditor's ONLY write is its audit entry.

## Definition of done (assert each — do not claim from memory)
- [ ] Every load-bearing claim in the artifact has a ROW in the per-claim audit table (count claims vs rows — 100% coverage, not sampled; an unaudited claim is an unguarded claim).
- [ ] Every FAIL carries a concrete repair (narrowed restatement + the licensing test), not a vague flag.
- [ ] Every claim carries a design-class certainty grade, and no verb demands more certainty than its grade supplies.
- [ ] Overall verdict is one of SOUND / SOUND-WITH-NARROWING / OVERCLAIM-BLOCK, with the OVERCLAIM-BLOCK claims enumerated.
- [ ] For a pre-registration/freeze context: no claim is frozen while any of its dimensions is OVERCLAIM-BLOCK (the gate blocks the freeze, exactly as the citation gate blocks the references freeze).
- [ ] Audit close logged in `AGENT_CHANGES.md`; any OVERCLAIM-BLOCK gets its own `[PENDING]` `DYNAMIC_LEDGER.md` row.

## Hard rules
1. **Method before verb, always.** A claim's verb may never exceed what its method establishes — compute time, deadline pressure, and a compelling narrative are never valid reasons to keep the stronger word (the faithful-over-convenient ethos, cited by name).
2. **Ontological and causal words are earned by interventions, not by observation.** Passive similarity, probe accuracy, dashboards, and attention weights are correlational; they never on their own license *represents / encodes / causes / understands*.
3. **No positive result from an unvalidated instrument.** An instrument that has not passed a negative control (silent on a null target) has not yet measured anything.
4. **A test the claim could not fail is no test** (Mayo's severity). Passing it adds zero certainty.
5. **N=1 licenses only an instance-specific claim.** A single model's/system's/quarter's result — however clean — is one correlated bet; the honest claim names the instance.
6. **The null is a finding.** A pre-registered null that fires is reported as the instance-specific negative it is, never hidden or reframed as failure.
7. **This lens does not rubber-stamp.** It is adversarial by construction — the auditor's job is to REFUTE the claim's soundness and default to the weaker reading when uncertain; a clean pass is earned, not assumed.
8. **Coverage is 100%, never sampled.** Every load-bearing claim is audited; a sampled pass can only say "sound in the fraction we checked."

## Delineation from adjacent gates (so they don't drift into each other)
| Gate | Audits | Direction |
|---|---|---|
| **Verification Gate** (global) | does the CODE compile / import / have no undefined names | machinery correctness |
| **codex-subagent-orchestration §Audit-gate** | does the code match the COUNCIL RULINGS (spec-drift) | code ↔ ruling fidelity |
| **citation-faithfulness-audit** | do our CITATIONS faithfully represent their SOURCES | our text ↔ external sources |
| **scientific-claim-soundness-audit** (this) | do our OWN CLAIMS follow from our OWN methods/evidence | our claims ↔ our methods |

All four compose; none subsumes another. This one is the only gate that checks the claim↔method relationship — the axis on which top-venue papers are most often rejected.

## Sources (raw-read 2026-07-18; each dimension traces to an established framework)
- **SEVERITY** — Mayo, *Statistical Inference as Severe Testing*: data warrant H only if "(S-1) H agrees with the data" AND "(S-2) with high probability, H would not have passed the test so well, were H false" — https://faculty.washington.edu/conormw/Papers/Mayo_Review_Preprint.pdf
- **MEASUREMENT-CONSTRUCT MISMATCH** — Jacobs & Wallach, *Measurement and Fairness* (construct vs operationalization) — https://arxiv.org/abs/1912.05511
- **EVIDENCE CONTAMINATION** — Kapoor & Narayanan, *Leakage and the Reproducibility Crisis in ML-based Science* (8-type leakage taxonomy; ≥294 affected studies across 17 fields) — https://arxiv.org/abs/2207.07048 · https://reproducible.cs.princeton.edu
- **DESIGN THREATS** — Shadish/Cook/Campbell validity-threat taxonomy via Matthay & Glymour, *A Graphical Catalog of Threats to Validity* — https://pmc.ncbi.nlm.nih.gov/articles/PMC7144753
- **INSTRUMENT SANITY** — Adebayo et al., *Sanity Checks for Saliency Maps* (randomization/negative-control tests for instruments) — https://arxiv.org/abs/1810.03292
- **STATISTICAL DISCIPLINE (forking paths)** — Gelman & Loken, *The Garden of Forking Paths* — https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf
- **CLAIM-BOUNDARY DRIFT (spin)** — Boutron et al. via Catalogue of Bias, *Spin Bias* — https://catalogofbias.org/biases/spin-bias
- **Certainty ladder** — GRADE (evidence starts at a design-class level; named domains downgrade/upgrade) — https://www.cdc.gov/acip-grade-handbook/hcp/chapter-7-grade-criteria-determining-certainty-of-evidence/index.html
- **Checklist-as-artifact & cross-discipline generalization** — REFORMS: 32-item consensus checklist for ML-based science — https://pmc.ncbi.nlm.nih.gov/articles/PMC11092361

## Sync note & provenance
Elevated from the S5-reframe incident in `local-omni-audio-mi-research` (external referee catch by the architecture reviewer/GPT-5.6 Codex, 2026-07-15; original draft and historical review provenance retained) into a global skill on Ali's instruction, 2026-07-15. **v2 (2026-07-19):** generalized beyond the founding MI context and hardened against the surveyed frameworks above — 10→13 dimensions (new: MEASUREMENT-CONSTRUCT MISMATCH, EVIDENCE CONTAMINATION, INSTRUMENT SANITY; FALSIFIABILITY upgraded to SEVERITY; CONFOUND LEAKAGE broadened to DESIGN THREATS; spin folded into CLAIM-BOUNDARY DRIFT), design-class certainty ladder added (annotates claims; the three verdicts remain the sole freeze gate), domain adapters replace project-specific vocabulary, per-claim audit table made the mandatory artifact. Historical audits citing "the 10-dimension gate" in append-only canvases remain correct as written (archives are exempt from sweeps). Wired as a MANDATORY embedded lens by `codex-subagent-orchestration` (revising the wiring revises the current orchestration contract — this skill cites the gate WITHOUT a hardcoded dimension count, deliberately). Doctrine is consistent with `codex-research-lifecycle`'s epistemics/pre-registration sections and with the global Output & Research Epistemics rules (claim→artifact, epistemic tags, instance-specific nulls, correlated-bet) — revising the doctrine revises every copy.
