---
name: generate-platform-health-protocol
description: Author a cadence-tiered platform health protocol for a data/ML/agent platform — a single master runner (tests/health/check_platform_health.py --tier N | --tiers | --all) with tiers organized by execution cadence (per-ingestion → daily/weekly → monthly → quarterly), a "When to Run What" scenario table, and per-tier checks tables, Failure Interpretation tables (Result → Meaning → Action), standalone commands, and "What FAILURE Looks Like" sample output. All checks are read-only assertions per the Non-Destructive Testing Mandate. Invoke when a platform needs a health battery or its verification doc ("build the health checks", "platform health protocol", "how do we know the stack is healthy").
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: generate-platform-health-protocol

## When to use
- A platform with stateful stores (DBs, vector stores, parquet/caches, containers, models) needs a standing health battery and its operating document.
- An existing ad-hoc pile of checks needs consolidating into one runner + one protocol doc.
- Output: `tests/health/check_platform_health.py` (master runner) + `docs/overview/markdown/combined-platform-health-protocol.md` (the protocol doc).

## Design principles
1. **Read-only, always.** Every check asserts properties of EXISTING artifacts (presence, hashes, schema, row counts, uniqueness, container liveness, port response). NEVER regenerate, re-ingest, re-download, or write to a store "to verify" (global Non-Destructive Testing Mandate). Anything loading a model or allocating GPU memory is not a health check.
2. **Tiers = cadence.** Organize by how often each battery runs, mapped to the platform layer it validates.
3. **Graceful degradation.** When infrastructure is offline (container down, DB unreachable), a check reports SKIPPED-with-reason, not a crash.
4. **Deterministic + flushed.** Same inputs → same verdicts; flushed prints at every check boundary (global observability rule).

## The master runner
```
uv run python tests/health/check_platform_health.py --tier N   # one tier
                                              ... --tiers 1,2  # subset
                                              ... --all        # full battery
```
- Exit code 0 only if all executed checks pass; per-check PASS/FAIL/SKIP lines, flushed.
- Each check: name, target artifact, assertion, expected, observed, verdict.

## The protocol doc structure
1. **Tier table** — columns: Flag | Tier name | What it validates (platform layer) | Est. time | Cadence. Example cadence ladder: Tier 1 Post-Ingestion Smoke ("every ingestion") → mid tiers daily/weekly → Graceful Degradation (quarterly) → MLOps Health (monthly).
2. **Quick Reference — When to Run What**: scenario → exact command table ("just ingested", "before a demo", "container restarted", "monthly review").
3. **Per tier**:
   - Checks table (check | artifact | assertion | threshold).
   - **Failure Interpretation table** — Result → Meaning → Action (e.g. "Gate = ITERATE → expected if X not yet built → check <path> for <columns>").
   - Standalone commands (each check runnable alone).
   - **"What FAILURE Looks Like"** — a literal sample of failing output, so operators recognize it.
4. Footer: governance cross-references (where results are logged, who owns thresholds).

## Workflow
1. Inventory the platform's layers and artifacts (stores, caches, containers, models, reports).
2. Define tiers by cadence; place every artifact in exactly one tier (log anything deliberately uncovered — no silent gaps).
3. Write the runner with per-check functions (CC ≤ 10 each; Radon-clean); thresholds in one table/constant block, not scattered.
4. Author the protocol doc from the runner (doc mirrors code — regenerate the doc when checks change).
5. Verify: run `--all` against the live platform once; paste real output into the "What FAILURE Looks Like"/sample sections; log the addition in AGENT_CHANGES.md and the logs/reports inventory doc if the project keeps one.

## Hard rules
1. Read-only assertions only — a health check that mutates state is a defect, full stop.
2. Every tier has a Failure Interpretation table — a red check without a documented meaning/action is not operational.
3. Thresholds are explicit and centralized; changing one is a logged change.
4. Expensive regeneration scripts stay OUT of the battery (manual, developer-facing, explicitly invoked).
