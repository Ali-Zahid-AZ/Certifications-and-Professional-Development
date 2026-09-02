---
name: cloud-run-discipline
description: Enforce detached, server-side monitoring and resource discipline for paid cloud GPU runs. Use when launching or checking a cloud run.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: cloud-run-discipline

## When to use
- Any paid cloud/serverless-GPU run: single experiments, multi-spawn grids, long ladders.
- NOT for local runs (→ `protected-local-run`). The watch cadence and run logging remain `observation-protocol` + `log-run-completion`.
- Every rule below is incident-bought (dates given); keep the incidents in the text — they are the load-bearing part.

## Launch rules
1. **Always detached + fire-and-forget, by default, no per-run instruction needed.** A blocking client call (`.remote()`/`.map()` or an undetached streamer) is **cancelled when the client stops polling — EVEN in a `--detach`'d app**. `.spawn()` (fire-and-forget) is the fix even for a SINGLE function. Incidents: a run was lost when wifi dropped mid-ladder (2026-07-08) and again when the laptop client was killed (2026-07-10) — the verdict was never committed.
2. **Orchestration loops live server-side:** put the loop inside a cheap CPU-container function that dispatches each GPU step via nested remote calls; the local entrypoint only spawns that orchestrator. Each step commits its artifact to the platform volume independently.
3. **NEVER wrap the launch in a shell `timeout <N>`** — it SIGTERM-kills the client at the wall-clock limit mid-run → no artifact (two runs died this way, rc=124, 2026-07-10). The remote function's own `timeout=` parameter, sized to the job, is the correct and only ceiling.
4. **Stage multi-spawn grids strictly** within the account's concurrent-container cap — **10 concurrent containers PER ACCOUNT on Modal** (Ali-flagged 2026-07-12; this is **account-level state, not a platform constant** — re-verify against the live plan rather than trusting this line. One 27B on an A100-80GB still counts as one of the 10). Excess spawns are **not an error**: Modal QUEUES them (Pending → Running as slots free; pending containers don't cost). But two concurrent stages competing for the same slots deepen the queue and muddy monitoring: let one stage DRAIN before launching the next; never run two grid stages concurrently on one account. If parallelism is genuinely needed, spread stages across accounts — each still ≤10 live containers.

## Pre-flight (before any paid run)
1. **Standalone load-check for EVERY new/gated model:** a cheap mode on the CHEAPEST GPU tier that calls the SAME loader the experiment uses + one forward pass, then exits — no pipeline, no volume writes. A PASS certifies auth + gated-license acceptance + the loader path for the whole model family (test the smallest scale; siblings share the license). Incident (2026-07-08): three gated models 401'd only AFTER the full multi-GPU ladder launched — a rotated platform secret cannot be read back, so **a live load succeeding is the ONLY confirmation the rotation landed.**
2. **Spend authorization is Ali's per-project Phase-0 ruling** (per `codex-research-lifecycle`) — never inherit a spend grant from another project; track per-run cost for planning either way.
3. Global Verification Gate (by name) green on the code being shipped to the container.

## During the run
1. **VRAM check on every cloud model load:** capture peak VRAM (dual-method: allocator max + memory-stats peak, larger binds), assert within the card with headroom; on overfill risk, switch residency lever (quantize / offload / stream) and log the trade-off — never silently fall back in a way that changes the mechanism.
2. **Monitor server-side, never a local pid/log:** (a) platform app-state listing → running-vs-stopped + task count; (b) volume/artifact listing → which steps have COMMITTED (the real progress signal); (c) for detail, a **bounded** log snapshot only — `timeout 25 <platform> app logs <app-id> > snap.txt` then filter the file. NEVER stream live logs unbounded on a running app (it hangs the tool). The local streamer exiting while the app keeps running is EXPECTED — it is the proof the detach worked.
3. Cross-turn watching: use a watcher exposed by the active Codex runtime per `observation-protocol`, with the status prompt pointing at the server-side commands; if none is available, leave a checkpointed resume procedure.

## After the run
- Pull artifacts from the volume (prefer per-file gets if recursive volume download is flaky on the installed client version); disk-verify before quoting any number; log via `log-run-completion`.

## Sync note & provenance
Elevated from five standing project memories (`modal-runs-server-side-detached`, `no-timeout-wrapper-on-modal-runs`, `modal-10-container-limit`, `preflight-model-access-check`, `cloud-vram-check`; Ali rulings 2026-07-06 → 2026-07-12) into a global skill on Ali's instruction, 2026-07-12. Platform-generic; Modal is the reference implementation. Doctrine synced with `codex-research-lifecycle` and with `observation-protocol` (launch/monitor mechanics here, watch cadence there) — revising any copy revises the others.
