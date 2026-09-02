---
name: protected-local-run
description: "Launch long LOCAL compute/experiment runs as memory-PROTECTED transient `systemd-run --user` services (own cgroup, systemd-oomd opted out, MemoryMin reclaim protection, Linger survival past logout) — NEVER as bare `nohup … &` under the terminal, which dies when systemd-oomd culls the terminal's cgroup under RAM pressure. Owns the LAUNCH mechanics only; the watch/telemetry/logging protocol stays with observation-protocol. Invoke when launching any multi-hour, model-loading, or crown-jewel LOCAL run (\"launch it protected\", \"start the long local run\", \"run the sweep locally overnight\"), or when a local run must survive terminal death, desktop crash, logout, or RAM-pressure kills. Skip for trivial/short scripts."
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: protected-local-run

## When to use
- Any LOCAL run that is long (≳30 min), loads a model, or is crown-jewel (its loss costs days): launch it via the recipe below.
- NOT for short scripts (plain background + log is fine) and NOT for cloud runs (→ the `cloud-run-discipline` skill).
- This skill owns the **launch**; the **watch** (runtime-supported cadence, status restates, run logging) remains the `observation-protocol` skill — run both together.

## The failure this prevents (incident-bought, 2026-07-12)
A ~2.5-day CPU-resident model run launched as bare `nohup … &` lived inside the terminal's cgroup scope. Under RAM pressure, **systemd-oomd** (userspace memory-pressure killer; Ubuntu defaults: kill at 60% pressure / 30 s) killed the terminal scope — reaping the agent session, the run (mid-record), and the session-scoped watchers in one shot. `journalctl -b 0 | grep "systemd-oomd killed"` is the forensic source for this failure shape. A bare nohup only blocks SIGHUP; it does NOT survive a cgroup-scope kill or a desktop teardown.

## Pre-req probes (once per box; all must hold)
1. `systemd-run --user` works.
2. `loginctl show-user <user> -p Linger` → `Linger=yes` (services survive logout).
3. The user slice delegates the `memory` cgroup controller (so `MemoryMin` binds).

## The recipe
```bash
systemd-run --user --unit=<run-name> \
  --working-directory=<project-dir> \
  -p ManagedOOMMemoryPressure=auto \   # opt OUT of oomd pressure-kill → run is a non-victim
  -p ManagedOOMSwap=auto \             # opt OUT of oomd swap-kill
  -p MemoryMin=<N>G \                  # reclaim-protect the model resident set (tune to workload)
  -p OOMScoreAdjust=-500 \             # bias the kernel OOM killer away from the run
  -p OOMPolicy=continue \              # don't tear the unit down if one proc is OOM-killed
  -p "Environment=PATH=$PATH" \        # pass the known-good PATH (uv lives in ~/.local/bin)
  -p StandardOutput=append:<abs-log> -p StandardError=append:<abs-log> \
  bash <wrapper-or-driver>
```

## Driver requirements (non-negotiable before launch)
1. **Idempotent/resumable** — skip-if-record-exists, so a relaunch re-runs only unfinished work. This is what makes the protected relaunch safe.
2. **Double-launch guard** — relaunching while the unit is active must be refused (`systemd-run` errors on a duplicate unit; do not work around it).
3. **Flushed stage markers + in-loop progress** per the global Script Observability rule (cited by name, not re-typed).
4. Pass the global **Verification Gate** (by name) on any code being run, before launch.

## Health check & relaunch
- Alive: `systemctl --user is-active <run-name>`; process view: `pgrep -af "<driver>" | grep -v shell-snapshot | grep -v "bin/bash -c"`.
- Logs: the append-log file (`tail -n N <log>`) or `journalctl --user -u <run-name>`.
- Relaunch only if dead: `systemctl --user reset-failed <run-name>` first (clears the old unit), then the same `systemd-run` line. **Verify the banked-artifact count is unchanged after a kill before relaunching.**

## Why it works (both failure modes closed)
1. oomd fires again → the run's service is opted out; oomd kills disposable desktop cgroups instead.
2. Terminal/desktop crash or logout → the run is its OWN cgroup under `user@.service` and `Linger=yes` keeps it alive.
3. Kernel OOM → `OOMScoreAdjust=-500` + `MemoryMin` bias/protect the run.

## Trade-offs & caveats
- An aggressive `MemoryMin` reserves RAM and can push oomd onto desktop apps (acceptable — they're disposable — but don't over-reserve). The oomd opt-out is the real protection; `MemoryMin` is bonus.
- **Watchers may die with the agent session** — but the RUN now survives; on re-attach, re-arm a watcher exposed by the active runtime, or follow the checkpointed resume procedure, and re-verify the service. Point watcher prompts at the `systemctl` commands, not at a pid.
- Complements — never replaces — the shared-hardware resource pre-flight (RAM, not VRAM, is usually the contended resource on CPU-resident runs; sequential loads only). Keep terminal verbosity minimal: scrollback RAM fed the original incident.

## Sync note & provenance
Elevated from the standing project memory `run-local-experiments-as-systemd-user-service` (Ali, 2026-07-12; present in two research projects) into a global skill on Ali's instruction, 2026-07-12. Doctrine synced with `codex-research-lifecycle` and with `observation-protocol` (launch here, watch there) — revising any copy revises the others.
