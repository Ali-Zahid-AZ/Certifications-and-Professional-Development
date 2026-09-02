---
name: codex-research-lifecycle
description: "Govern research-project initialization, design, experimentation, review, handoff, and closeout with evidence-bounded science, project-local authority, and reproducible operations. Use when starting, planning, running, reviewing, handing off, or closing a research project."
---

# Codex Research Lifecycle

This is the self-contained research-lifecycle doctrine for Codex. Use it as the
entry point for research work; invoke the specialized skills named below for
their exact procedures. It is agent-agnostic: the active project's rules and
`agent_roles.md` supply the project-specific authority and roster.

## Authority and operating ethos

Apply sources in this order: Ali's current instruction and global rules, the
active project's `AGENTS.md` and `agent_roles.md`, then this skill and the
specialized skills it routes to. A stricter project rule may narrow permission
but may not loosen global safety. If a conflict cannot be resolved by that
ordering, stop and ask Ali.

Ali is the research owner and final authority over scope, publication,
spending, secrets, destructive actions, and outward-facing impact. Work as a
peer: state assumptions, surface risks and uncertainty, and report evidence
gaps plainly. Confidence is the deadline; compute time, wall-clock pressure,
hardware limits, and convenience never justify a proxy, silent scope cut, or
weakened method. Prefer deterministic behavior, observability, reversibility,
and systems that fail loudly.

Every plan, artifact, log, memory note, and handoff must pass the capable-
stranger test: a capable successor holding the artifact and applicable rules
can continue without guessing. Memory, handovers, and other agents' reports
are dated evidence, not authority; verify live disk, git, runtime, and service
state before acting.

## Stage 0: idea, arming, and cold open

Recording an idea or proposal is not authorization to run it. A project starts
only on Ali's explicit live instruction to arm it. The idea pipeline is in the
Obsidian vault:

- `/home/az/GitHub-Repositories/obsidian-knowledge-base/12-Agents/01-Research-Ideas/formal/research_directions.md` is the canonical index.
- `detailed-project-proposals/` contains cold-open project proposals.
- `councils/` contains the dated council source of record; a dated council
  wins over an index on conflict.

At a cold open, read the selected proposal, its cited council documents, the
index row, live project rules, `agent_roles.md`, standing-canvas heads, and
current disk/git/runtime state. If an inherited claim comes from a primary
source, re-derive or re-verify it from that primary source before building on
it. Code belongs in its own repository under
`/home/az/GitHub-Repositories/`; vault writes obey the vault rules and
`codex-vault-safe-note-editing`.

Before scaffolding, ask Ali these Phase-0 questions in plain chat, one focused
question at a time:

1. What is the compute envelope: shared local hardware or named cloud
   platform/account, with its VRAM/RAM/CPU limits?
2. Is spend authorized, within what pool, or must every paid run be flagged?
   Never inherit spend authorization from another project.
3. What is the deliverable and venue: article, position piece, or report?
4. Are private data, client material, or gated models involved?
5. Is any standing autonomous/council authority armed now, later, or not at
   all? Never assume a grant.
6. What exact project/repository/hub name should be used?

## Initiation sequence

1. Invoke `codex-project-scaffold-init`. Use the canonical template layer at
   `/home/az/GitHub-Repositories/agentic-coding/project-rules-skills/templates/`:
   `for-new-projects-deploy/` for the base set, `research-project-variant/`
   for research, and `data-project-variant/` when structured or PII data is in
   scope. Keep project configuration in the hub and symlink it into the repo;
   never create a shadow local copy or break a hub link.
2. Verify the scaffold: non-empty mission, resolved symlinks, consistent
   active/hub rules, complete documentation tree, required cited paths, active
   `.env` exclusions, and no leaked handles, hardware strings, old project
   names, or other template contamination.
3. The normal project set is `AGENTS.md`, `agent_roles.md`, `COUNCIL.md`,
   `AGENT_CHANGES.md`, `DYNAMIC_LEDGER.md`, `FUNCTION_MAP.md`,
   `IMPLEMENTATION_PLAN.md`, `documentation-rules.md`,
   `SCHEMATIC-PALETTE-RULES.md`, `.agents/`, `scripts/verify.sh`, the
   `docs/documentation/` archive tree, and the research primitives:
   `BLUEPRINT.md`, `DETAILED-EXPLANATION-BLUEPRINT.md`,
   `initiation-COUNCIL.md`, `literature-for-the-project.md`,
   `ledger.schema.json`, `llm-models-used-in-this-study.md`, and the article
   skeleton. Add the data-project bundle and reports/testing directories when
   applicable. Do not invent optional files; report missing ones.
4. Seed memory using the protocol below before the initiation council.
5. Convene the initiation council on phases, owners/auditors, exit gates,
   envelope, hypotheses, kill criteria, and GO/NO-GO tiers. Populate
   `docs/primitives/BLUEPRINT.md` from the converged design and archive the
   initiation council as permitted by the project rules.
6. Run the pre-mortem: answer the blind-spot question “it is three months
   later and this design failed; what assumption caused it?” and check sibling
   projects for already-ratified corrections.
7. Freeze Phase 0 before Phase 1. After the P0 freeze, annotate or calibrate;
   do not adjudicate the frozen apparatus. Amendments are versioned, never
   edited in place. Author the per-version plan with
   `codex-author-implementation-plan` when a build phase opens.

## Memory porting and namespaces

Use `codex-project-memory-protocol`. Codex memories live under
`/home/az/.codex/memories/`, and a project's namespace is separate from every
other project. Resolve a documented alias or the exact repository-root
basename, check `/home/az/.codex/memories/<namespace>/` before the first
project-memory read or write, and create only that namespace plus its
`MEMORY.md` index in the canonical sibling format if absent. Write
project-specific memories directly there; `/home/az/.codex/memories/extensions/ad_hoc/notes/`
is reserved for genuinely global or cross-project policy. The shared
`CROSS-PROJECT-MEMORY-DOCTRINE.md` is an orientation source, not authority.
Do not enumerate or read other project namespaces unless Ali explicitly names
the source and destination for an import. If the live root, documented alias,
namespace, or index cannot be resolved and checked, stop the memory operation
and report `BLOCKED`; `extensions/ad_hoc/notes/` is not a project-memory
fallback. Hooks are defense-in-depth only.

At project start, after the namespace preflight, read only the destination
`MEMORY.md`, the shared doctrine, and live project rules before seeding.
Classify explicitly named material:

- Portable doctrine: methodology, interaction preferences, epistemics, run
  discipline, and other durable principles; candidate for adapted seeding.
- Project state: handovers, live runs, phase results, and session-mode notes;
  never port.
- Credentials, client data, private payloads, raw transcripts, session
  handles, generated internals, and mutable run state; never port.
- Hardware/platform-specific procedure; port only when the Phase-0 envelope
  matches, otherwise retain a pointer and exclusion note.

Seed only applicable durable principles with adapted copies, provenance, and
same-namespace relative links. Record exclusions and quarantine ambiguity.
Keep the live re-attach memory current, reference successful runs and durable
decisions there, and refresh it before every compact/restart green-light.

## Roster, council, and delivery loop

The active project's `agent_roles.md` is the sole source of truth for the
human owner, lead, workers, reviewers, model IDs, transports, reasoning,
depth, concurrency, write permissions, review completion, convergence, and
escalation. This skill defines no default roster. If the file is absent,
stale, ambiguous, or contradictory, stop and ask Ali. Missing or unavailable
required seats are incomplete review, not agreement.

Councils are dialectic, not majority vote. Roles provide lenses, not votes;
Ali closes councils and remains final authority unless he explicitly grants a
bounded action. The lead must consider bounded parallel work before sizeable
implementation, using only assigned seats and disjoint write scopes. Review
roles remain read-only unless the roster explicitly assigns implementation.
Do not nest delegation when the active rules prohibit it, do not launch
multiple agents on the same unresolved question, and do not delegate compute
or model/data-generation runs out of the lead session.

Before any external feedback, consultation, or audit dispatch in this loop,
apply `$codex-external-agent-availability-preflight`. The current project's
root `external-agent-availability.md` is re-read immediately before the hello
and before the substantive dispatch; missing, stale, malformed, or unverified
status is incomplete availability and never agreement. Use the transport skill
for the handshake and keep session handles transient.

The standard delivery loop is:

`council design → lead implementation/integration → first-party verification → independent architecture/assurance/scientific review → synthesis → Ali authorization`

Apply these optimizations: freeze before build; use the deterministic code
gate and Radon loop; run a cheap exact-path canary before expensive work; seek
adversarial disconfirmation; use diverse independent lenses; keep permitted
work concurrent without idle review windows; and leave an append-only audit
trail. Changes spanning more than two files receive an independent adversarial
audit. Check every applicable council ruling separately and record PASS,
FAIL, or unresolved evidence. A lead never self-certifies independent quality
or convergence.

For Python changes, invoke `codex-engineering-standards`. For non-Python
documentation or configuration work, state why the Python gate is not
applicable; still run the relevant structural and persisted-byte checks.

## Research epistemics

Before execution, preregister the claim and its alternatives: H1, H2, and H0,
the measured construct, estimator, input-sampling unit, analysis, thresholds,
kill criteria, and GO/NO-GO rule. The freeze is a gate, not decoration. After
freezing, distinguish annotation/calibration from adjudication and version any
amendment.

Every claim maps to an artifact, configuration, and provenance record. Tag
estimates and reasoning products `[UNVERIFIED — reasoning only]`; distinguish
exploratory, single-seed, model/corpus-specific, and confirmatory evidence.
Separate instrument behavior from the phenomenon, test construct validity,
calibration, causal direction, and measurement-versus-mechanism mismatch.
Harden the design against impact and selection bias: held-out inputs, negative
controls, nulls, alternate plausible mechanisms, reward hacking, leakage,
confounds, multiple comparisons, and the temptation to select a seed or
condition because it improves the headline. Report boundary cases and
failed/marginal gates rather than hiding them.

Use `codex-scientific-claim-soundness-audit` for claim, framing, preregistration,
or verdict review and `codex-citation-faithfulness-audit` for references.
Literature discovery is not evidence: every quote or citation must be
reconfirmed verbatim from the raw source before entering a paper or claim.

## Seed and statistics doctrine

Frozen checkpoints isolate input-sampling variance; they are not training
variance. Define what the seed changes. If seeds only repeat a deterministic
fixed input, report `r` repeats and `n_eff=1`, not `n=10` independent samples.
To estimate an input-sampling distribution, wire each seed to a distinct
prespecified input draw/resample/fold, quantify overlap/dependence, and report
the resulting `n` and `n_eff`.

- When input sampling is the estimand, default to ten distinct units `{0..9}`.
  The Henderson et al. reference (arXiv:1806.08295) motivates 5–10 seeds for
  training stochasticity; cite it only with the explicit caveat that this
  protocol estimates input sampling and can have exactly zero variance.
- `σ=0` on fixed inputs is an exact-determinism finding, not a failed test.
  Decline significance tests for those values and report, for example,
  `σ=0; r=10; n_eff=1`. If distinct input units also yield zero variance,
  report their valid `n`/`n_eff` separately.
- Use input bootstrap as the primary stability instrument: at least 100
  resamples, average pairwise stability and error CV, with a field bar such as
  0.8 only when appropriate. Keep fidelity-to-reference and stability-under-
  resampling on separate axes. The relevant reference is arXiv:2510.00845.
- Where variance exists, choose the instrument per metric: BCa bootstrap CI
  for bounded continuous values; Wilson CI for pass/fail proportions; Page's
  L and/or Jonckheere–Terpstra for ordered trends; Holm-corrected paired
  Wilcoxon for adjacent paired conditions; exact permutation tests for local
  non-monotone contrasts; regime-boundary crossing probability for threshold
  calls; condition/input-null variance ratios; and TOST only for declared-
  epsilon exploratory equivalence claims at small n. Never use unpaired tests
  for paired seeds or Wald intervals near 0/1.
- Disclose configuration sensitivity (ablation type, positions, readout,
  coefficients, and similar choices) and run a small robustness check across
  plausible alternatives. The relevant methodology-sensitivity reference is
  arXiv:2407.08734.
- Run cheap tiers to full n before expensive tiers, regenerate distributions
  incrementally, and hold every sweep launch for Ali's explicit go. Never
  create resource contention between tiers.
- Harden deterministic execution for new seeds: deterministic algorithms,
  documented TF32 precision choices, math-only attention paths where needed,
  `PYTHONHASHSEED`, and explicitly accepted residual nondeterminism. For old
  results, run only a same-seed-twice bit-identity diagnostic (`r=2`,
  `n_eff=1`); rerun that experiment only if leakage is found.
- Keep one audit row per seed × experiment with metrics, verdicts, peak VRAM,
  RAM, disk, wall-clock, and anomalies. Never cherry-pick: a verdict flip is
  a boundary-condition analysis. Visualize all valid points with a jittered
  strip/swarm, an overlaid box plot where variance exists, explicit
  determinism annotations, and an experiment × sampling-unit pass/fail heatmap.

Use `codex-seed-statistics-protocol` to author the project's full protocol;
this section supplies the cross-project invariants.

## Execution, observability, and run logging

Before every model load, query GPU, RAM, CPU, and disk on the shared machine;
RAM/CPU pressure can matter even when VRAM is free, and stall rate is more
informative than swap-used. Declare full-GPU, quantized, CPU-offload, or
streaming residency before running. Record peak VRAM/RAM/disk and wall-clock
for every run. Run a cheap exact-path canary first; for paid/gated cloud
models, use a standalone cheap access/load check before the pipeline.

For every multi-hour run, require durable checkpoints, an idempotent/resumable
driver, a double-launch guard, a tested resume path, and a banked-artifact
count check. Use `codex-protected-local-run` for long local runs: do not use
bare `nohup`; launch in a user systemd service with the required memory
protection, OOM behavior, append-only logs, and explicit working directory.
Verify user service/linger/cgroup prerequisites and relaunch only after
`reset-failed`, never while the unit is active.

Use `codex-cloud-run-discipline` for cloud work: launch detached/server-side,
keep orchestration off the local client, never wrap the client in shell
`timeout`, monitor platform state plus committed artifacts with bounded log
snapshots, stage work within the platform concurrency cap, check VRAM with
headroom on every load, and track cost according to the Phase-0 ruling.

Every runnable script prints flushed gateway/checkpoint messages and periodic
`index/total + rate + elapsed` progress. Use only watcher mechanisms exposed
by the active runtime; a watcher is convenience, never the load-bearing
science. Check completion markers and crash signatures without watcher-self-
matching process patterns. The job's own checkpoints must survive watcher
failure.

Log completed runs with `codex-log-run-completion` in the project's canonical
tables-first `AGENT_CHANGES.md` format and reference every successful run in
project memory. Health checks may inspect existing artifacts and assert cheap
deterministic properties, but may not regenerate data, redownload weights,
recompute caches, rerun pipelines, or allocate GPU merely to verify.

## Documentation, paper, and closeout

Standing canvases follow their own headers and `canvas-write-protocol`; read
live heads at session start and load full history only when needed. Use
`$documentation-rules` and `$codex-phase-closeout-documentation` skills for the
per-phase set: archived plan plus Completion Statement, playbook/detailed
explanation, results, analysis, schematic, completion report, and updated
canvases. Do not polish phase deliverables mid-phase. Keep working numbers in
the ledger/audit records, write a story only after all inputs are final, and
place conclusive disk-verified results in both the deliverable and its review
mirror with `[AGENT]` provenance. Use tables, honest estimates, and explicit
`[UNVERIFIED]` labels; never hand-maintain derived counts or duplicate a value
without a sync note. Every audit P0/P1 becomes its own pending ledger entry.

For article projects, create the skeleton early, author natively in the target
format, and draft Methods → Results → Related Work → Introduction →
Discussion/Limitations → Conclusion/Abstract → Appendices → full review.
Maintain one literature index, log negative searches for absence claims, run
the citation-faithfulness gate before the references freeze, and include the
input-sampling caveat, determinism reporting, configuration sensitivity, and
boundary analyses in the methods. Ali controls venue, timing, and upload.

Maintain a lean cold-open carrier with current state, live runs, landed/logged
work, pending decisions, and the first objectively incomplete task. Refresh
it and all required durable canvases before compaction, restart, or handoff;
use `codex-compaction-required-greenlight` and `codex-session-recovery` when
those triggers apply. Verify disk before acting on any memory or handover,
run `codex-session-closeout-reflection` before substantial completion, and
compact manually near 80% context use.

## Skill routing and interaction

Discover live Codex skills from the real directories under
`/home/az/.codex/skills/`; use the formal OpenCode discovery route for
OpenCode skills. Do not rely on a hand-maintained count, duplicate specialized
procedures here, or invent a provider-specific roster. Relevant routes include
onboarding, memory, scaffolding, planning, orchestration, code standards,
protected/cloud runs, observation, seed/statistics, claim/citation audits,
documentation, recovery, compaction, and vault-safe editing.

Ask only focused questions when ambiguity, risk, or approval is material.
Announce the target/effect before using standing permission; irreversible,
external, production, spending, secret, and disclosure boundaries retain their
explicit authorization gates. Report status answer-first with verified facts,
estimates, reasoning products, and unresolved gaps clearly separated.
