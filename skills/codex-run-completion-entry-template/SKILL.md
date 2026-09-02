---
name: run-completion-entry-template
description: Write an evidence-backed completed-run entry in the project's append-only change log using tables first, honest gates, and mandatory verification, telemetry, output, and pending closers. Use when a run, experiment, ingestion, or long script finishes.
---

# Run Completion Entry

Use this skill after a run has finished with success, a marginal result, or failure. Before writing, read the project root's `agent_roles.md`; it determines the active lead, reviewers, and who may close the entry. The project's own template governs if it is more specific; otherwise use the format below.

## Write safely

1. Confirm the run is actually finished from on-disk artifacts, not memory or stdout alone.
2. Acquire the timestamp from the project's approved time source immediately before writing; use the project timezone and required format.
3. Re-read the change log head, verify its append anchor occurs exactly once, and abort/rebase if the head moved.
4. Insert the newest entry at the required position below the prohibited sentinel. Use the sanctioned assertion-gated write path; never use `sed -i` or a stale whole-file copy.
5. Update the task/status ledger in the same pass when the project protocol requires it.

## Entry skeleton

```markdown
### [YYYY-MM-DD HH:MM:SS TZ] | Agent: <agent> (<model>) | TASK <n> / <run-id> COMPLETE — <honest verdict and key numbers>

---

## Probe or stage name

| Metric | Configuration/strategy | Value | Gate/threshold | Verdict |
|---|---|---:|---:|---|
| ... | ... | ... | ... | ... |

1. Interpret the table without merely repeating it.

## Pipeline-integrity gates

| Gate | Assertion (read-only) | Expected | Observed | Pass/Fail |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Closers (all four are mandatory)

- **Verification gate:** name the project's Verification Gate and report the exact result.
- **Telemetry:** peak VRAM, peak RAM, peak disk, wall-clock, and seed(s), when applicable.
- **Output path:** exact artifact path(s) on disk.
- **Pending:** what awaits the project owner, council, or next phase, or `none`.
```

## Evidence and honesty rules

- Tables come before analysis; omit inapplicable sections rather than padding them.
- Every quantitative or verdict claim must trace to an on-disk artifact. Parse the artifact rather than trusting memory or terminal output.
- Tag estimates and reasoning-only values `[UNVERIFIED — reasoning only]`.
- Report FAILED, MARGINAL, BLOCKED, and crashed outcomes plainly; a crashed run still receives a completion entry with the traceback and log path.
- Tag each number with the configuration that produced it, such as quantization, residency, seed, or other relevant strategy.
- End with a concise chat update so the project owner can see what was logged.
