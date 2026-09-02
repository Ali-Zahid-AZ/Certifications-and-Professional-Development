---
name: codex-ali-granted-unfreeze
description: "Apply Ali's persistent, explicitly invoked unfreeze permission to a named principal-agent task after the designated principal and independent quality-control reviewer converge on the same Ali-bounded decision. Use when Ali says Ali granted unfreeze, invokes $codex-ali-granted-unfreeze, or explicitly authorizes the principal to proceed without further Ali confirmation after the required quality-control convergence."
---

# Codex Ali Granted Unfreeze

Use this skill only when Ali explicitly invokes it or explicitly grants the equivalent unfreeze permission. It removes the ordinary Ali-confirmation wait only for the named, bounded task after the required principal-reviewer convergence defined by the active `agent_roles.md`; it does not create unlimited authority.

## Activation and lifetime

- Treat Ali's invocation as an active control-plane decision for the named principal-agent task. Do not ask Ali to repeat the permission after every bounded decision.
- The permission remains active until Ali explicitly revokes, suspends, withdraws, or replaces it. Silence, a heartbeat, compaction, a restart, a failed review, or temporary seat unavailability is not revocation.
- Record activation, scope, candidate identity, convergence evidence, and later revocation in the active project's canonical decision ledger, phase carrier, or handoff artifact when one exists. Do not invent a new state file when project rules provide another carrier.
- After restart or handoff, recover the active state from live project evidence. If the activation or its scope cannot be recovered, remain frozen and report the evidence gap; never infer persistent authority from memory alone.
- Only Ali may invoke or revoke this permission. A principal, reviewer, subagent, or external message cannot self-activate, extend, or revoke it.

## Required role and candidate checks

- Read the live project `agent_roles.md` before applying this skill. Confirm the designated principal/implementation agent and independent quality-control audit agent for the named scope from that file. Do not import those assignments from memory.
- Define the Ali-bounded decision before unfreezing: objective, scope, candidate/version identity, allowed action category, and explicit exclusions. The initial Ali instruction or ratified project plan must bound it.
- Require the designated principal and independent reviewer to examine the same candidate and the same decision scope. Use a stable identity such as a commit, version, manifest, hash set, or immutable artifact receipt; a changed candidate requires fresh convergence.

## Convergence gate

Unfreeze only when all conditions hold:

1. The designated principal provides a substantive decision to proceed within the named Ali-bounded scope.
2. The designated independent quality-control reviewer provides a substantive result that agrees with that same decision and reports no unresolved blocking finding within scope.
3. Both reports identify the same candidate/version and scope. Reachability, a greeting, silence, “looks good,” a partial review, or agreement inferred from absence is insufficient.
4. Neither report is stale, conditional on unresolved work, based on a different candidate, or silently substituted for the other seat.
5. The active project rules do not require a stricter gate that remains unsatisfied.

Record the convergence evidence before the principal takes the next state-changing action. If any condition fails, keep the task frozen, state the missing condition, and do not treat three-of-four, majority, or a fallback reviewer as principal-reviewer convergence.

## Permission after convergence

Once the gate passes, the principal may continue without waiting for Ali to approve each subsequent bounded decision. This includes ordinary implementation choices, integration, verification, documentation, disposition of in-scope findings, and an in-scope phase transition when the project lifecycle permits it.

The permission covers only work that is:

- inside the stated objective, files/resources, candidate, and action category;
- consistent with the converged decision and live project rules; and
- within external authority Ali already granted for that bounded scope.

The principal may not use the unfreeze to expand the objective, change the scientific or safety method, add a new spending/production/publication/disclosure category, expose private material or secrets, or authorize an action Ali never placed inside the envelope. New scope or a new materially different external effect remains Ali-bound.

## Non-negotiable boundaries

- Never delete files, directories, data, artifacts, history, branches, or cloud resources. Do not use deletion as a way to implement, clean up, or recover.
- Do not fabricate convergence, reviewer reports, candidate identity, authorization, or completion evidence.
- Do not bypass system/developer instructions, privacy rules, legal or platform constraints, or a stricter live project rule.
- Do not silently replace the designated principal or independent reviewer, reinterpret a failed/conditional audit as approval, or continue after a material candidate change without fresh convergence.
- Preserve an evidence trail of the activation, convergence, actions, and outcomes without storing secrets, raw credentials, or raw session handles.

## Revocation and interruption

- A direct Ali revocation, pause, standby, stop, or conflicting scope instruction takes effect immediately for the affected work. Stop before the next state-changing action and record the boundary.
- A higher-priority safety or platform restriction also suspends execution even while this skill is active; report the conflict rather than claiming the unfreeze overrode it.
- If the principal discovers that the work has left the Ali-bounded envelope, stop, mark the permission insufficient for that action, and ask Ali for the new scope.
