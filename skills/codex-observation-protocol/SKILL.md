---
name: observation-protocol
description: Operating protocol for running long/compute (GPU) scripts under direct observation — the agent runs the job itself in bash with logging, arms a completion watcher, polls on a cache-aware sleep→wake→status cadence, restates results in text, records telemetry, and logs the outcome to AGENT_CHANGES.md + DYNAMIC_LEDGER.md. Invoke when starting any GPU/compute run, experiment, reproduction, or other long-running script that must be watched to completion (e.g. "run it under your observation protocol", "observe this run").
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: observation-protocol

## When to use
- Any GPU run, model-loading experiment, reproduction, activation-cache build, quantization run, or long script that must be watched to completion.
- Triggered by "run it under your observation protocol", "observe this run", "run + monitor", or any compute job that takes more than a few seconds.
- NOT for fast hardware-free checks (py_compile / ruff / radon / unit reads) — those run inline and finish immediately.

## Tooling constraints (inherit project rules)
- File reads/search/glob/diff → native tools (`Read`, `Grep`, `Glob`, `ls`, `git diff`/`diff`). For tailing a log use `tail -n N <log>` (or Read the file).
- Native `Write`/`Edit` for creating/editing files (Edit requires a prior native Read of the target range).
- AGENT_CHANGES.md / DYNAMIC_LEDGER.md writes: fresh PKT via `mcp__time__get_current_time(timezone="Asia/Karachi")`, re-read the head, chronological-inversion check, never delete/reorder, `sed -i` forbidden.

## The protocol (run every observed job)

### 1. Pre-flight (before launch)
1. **Live resource query — before EVERY model load, not just the first:** GPU util + free VRAM (`nvidia-smi`), free RAM, and load average. Free VRAM alone is NOT a go-signal: TransformerLens/HF loaders stage weights in CPU RAM first (transient ~4–5 GB spike), so BLOCK the load when free RAM is low even if the GPU is idle. On shared hardware (sibling sessions live), model loads are SEQUENTIAL — never parallel.
2. State the **residency strategy** (full-GPU / int8 / int4 / CPU-offload / streaming) and the expected peak VRAM vs the project's VRAM envelope, BEFORE launch. **No silent fallback:** on would-be OOM, switch lever AND log the trade-off — never silently fall back in a way that moves the mechanism.
3. Apply the **codex-engineering-standards** skill (the global rules name it; canonical ruff invocation is `uv run ruff check --select F821,F811 <files>` from the project root, plus Radon) on any code being run. Green before launch.
4. Decide the **output artifact path** (JSON/log) and a one-line **time estimate** (what/why).
5. **Crash-recovery pre-flight — MANDATORY before any multi-hour run:** (a) durable per-checkpoint state on disk (the science survives a dead process); (b) an idempotent resume driver (relaunch continues from the last checkpoint, never recomputes banked work); (c) a double-launch guard (relaunching while the original is alive must be refused or harmless); (d) a tested suspend/crash drill BEFORE the long run starts. Validated live (mi-article, 2026-07-06): a 16 h/seed crown-jewel run crashed on hibernation-resume and lost only ~6 h because the resume path pre-existed.

### 2. Launch (background + logging — the agent runs it itself)
- **Launch-path routing (sync note — mechanics owned by the sibling skills):** long/crown-jewel LOCAL runs launch as memory-protected `systemd-run --user` services per the **`protected-local-run`** skill (bare nohup dies with the terminal's cgroup under RAM pressure); CLOUD runs launch detached/fire-and-forget and are monitored server-side per the **`cloud-run-discipline`** skill. The nohup line below is the plain path for short local jobs only.
- Always background + unbuffered + logged; never block the session on a foreground GPU run:
  ```bash
  mkdir -p logs
  PYTHONUNBUFFERED=1 PYTHONPATH=. nohup uv run python -u -m <module> <args> > logs/<name>.log 2>&1 &
  echo "launched pid $!"
  ```
- Capture the **pid**. One job per log file (parallel bg jobs clobber a shared log).

### 3. Watch — sleep → wake → status cadence
- **Foreground bash waits cap at ~2 min.** For a quick first look, a bounded loop is fine:
  ```bash
  for i in $(seq 1 7); do kill -0 <pid> 2>/dev/null || { echo EXITED; break; }; sleep 15; done
  tail -n 20 logs/<name>.log
  ```
- **Any watch that must persist ACROSS turns MUST use a watcher mechanism actually exposed by the current Codex runtime.** Do NOT rely on a long-lived `nohup`/background bash loop (`pgrep`/`kill -0`/`sleep` watcher) as the cross-turn watch: the harness may reap idle background processes, so a bg watcher can silently die while the job keeps running. The bounded inline loop above is ONLY for a quick first look WITHIN the current turn; it is never the sole persistent watch.
- For longer jobs, **do not block** — use the current runtime's supported task wake, monitor, or automation mechanism when one is exposed, with a bounded status prompt and an explicit completion/crash condition. If no supported cross-turn watcher is available, leave checkpointed resume instructions and a cold-open carrier for the next session rather than inventing a tool.
  - **Intervals:** match the interval to how fast the watched state actually changes — 60–270 s when actively polling external state; **1200–1800 s** for idle heartbeats on a multi-minute job; up to the runtime's documented clamp for a long, self-checkpointed run whose next milestone is hours out. Do NOT tune intervals to prompt-cache TTL.
  - **Three independent layers, so a reaped watcher costs nothing:** (1) the science survives on the job's own on-disk checkpoints; (2) a supported runtime watcher, if available, carries the status loop; (3) a bounded inline check is disposable convenience only. Never let layer 3 be the thing the watch depends on.
- **Every status check** = (a) `kill -0 <pid>` alive/exited, (b) `tail -n N logs/<name>.log`, (c) optional phase-marker scan (`grep -E "DONE|Error|Traceback|<phase markers>" logs/<name>.log`). Confirm the log is still growing — a static log + live pid may mean a stall.
- **Watcher anti-pattern (two real incidents):** never build a completion watcher on `pgrep -f`/`pkill -f` with a pattern the watcher's own command line contains — the watcher matches its own argv, so the loop never exits (or SIGTERMs its own shell). Watch the LOG for the script's own completion marker (`=== DONE ===`) plus crash signatures (`Traceback|Error|Killed|OOM`) so crashes fire the alert too.
- **Restate** each checkpoint in your own text (the state classifier reads only message text, not tool output): what's happening, what's next.

### 4. On exit
1. Confirm clean exit (`=== DONE ===` marker / exit 0) — or capture the traceback and treat as a failure.
2. **Parse the artifact** (read the JSON, don't trust stdout alone) and build a **results table** (Ali prefers tables).
3. Record **telemetry**: peak VRAM, peak RAM, peak disk, wall-clock, seed/determinism — verify VRAM stayed within the project's VRAM envelope.
4. **Sanity check** before declaring done: re-read the ask, assert on the written artifact (shapes/counts/verdicts), confirm seeds. Non-destructive — never regenerate data "to verify".

### 5. Log the outcome
- Append to **AGENT_CHANGES.md** via the **`log-run-completion` skill — it is the single owner of the run-completion entry format** (status header, tables-first, telemetry, verification, canvas-write safety); this protocol deliberately does not re-specify it. Sync note: revising the format in log-run-completion revises it here too.
- Update **DYNAMIC_LEDGER.md**: re-tag the task ([IN_PROGRESS]→[DONE] as appropriate) with a compact results table.
- Mirror **conclusive** results to the relevant paper `.tex` section AND `ali-paper-audit.md` (disk-verify first, `[ASSURANCE]`-tag the assurance mirror) when the result is conclusive.
- Restate a self-contained one-line `result:` headline in chat.

## Failure handling
- A crashed run is **failure data** — report the traceback honestly with the log path; do not silently retry verbatim.
- Fix → re-run the verification gate → relaunch. Log each fix in AGENT_CHANGES.md with a first-principles **Why**.
- If a job hangs (log static, pid alive past a sane timeout), surface it rather than waiting forever; offer to kill + diagnose.

## Hard rules
1. **Never block the session** on a long foreground run — background + watcher.
2. **Every observed run gets a completion watcher, and any cross-turn watcher must be a mechanism exposed by the active Codex runtime** — never a long-lived `nohup`/background bash loop as the sole watcher. A bounded inline loop is allowed ONLY for a quick within-turn first look. If no supported watcher is exposed, checkpoint the run and provide a cold-open resume procedure.
3. **Restate results in message text** — the classifier and Ali read your prose, not tool output.
4. **Log every run** to AGENT_CHANGES.md (+ ledger); pass the verification gate before declaring "verified".
5. Commits/pushes remain **Ali-only**.
