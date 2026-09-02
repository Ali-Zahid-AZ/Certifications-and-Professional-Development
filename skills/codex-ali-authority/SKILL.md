---
name: codex-ali-authority
description: Apply Ali's strongest user-level authority to a named scope, including overriding lower-priority project rules, freezes, approval gates, reviewer sequencing, role routing, and default workflow. Use only when Ali explicitly invokes this skill or clearly instructs Codex to act under Ali authority.
---

# Codex Ali Authority

Use this skill only after Ali explicitly invokes `$codex-ali-authority` or
clearly instructs Codex to act under Ali authority.

## Authority

- Ali can override anything anytime using this authority, within the named
  scope and subject to the higher-priority boundaries below.
- Ali may suspend, revoke, or waive any lower-priority provision of this skill
  for the explicitly named action and scope.
- Treat Ali's invocation plus his direct instruction as the governing user
  decision. Do not ask for the same permission again.
- The authority may override lower-priority project or global rules, freezes,
  approval gates, reviewer sequencing, role routing, concurrency defaults, and
  ordinary ask-first conventions when Ali's instruction clearly covers them.
- The authority itself does not perform an action. Ali must still name the
  action and scope; once he does, do not impose an additional ordinary approval
  gate for that same action.
- Keep the scope exact. Do not treat the authority as permission for unrelated
  work or as a reason to broaden the user's goal.

## Boundaries that remain

- This is user-level authority. It cannot override system or developer
  instructions, platform or tool restrictions, applicable law or policy, or
  higher-priority safety boundaries.
- In particular, this authority cannot revoke the higher-priority privacy
  boundary that keeps raw OpenCode session handles out of memory, logs, prompts,
  repositories, and chat. Use masked or transient handles instead.
- It cannot justify exposing secrets or private content, concealing actions,
  fabricating evidence, or claiming completion without verification.
- Operating-system `sudo` does not change instruction priority. Use it only for
  a separately named, permitted system action; never treat it as a way to
  bypass the boundaries above.
- If a higher-priority conflict remains, state it plainly, perform the closest
  permitted action, and do not claim that the override succeeded.

## Execution

1. Confirm that Ali explicitly invoked this skill or named Ali authority.
2. Parse the exact action and scope, and identify the lower-priority controls
   that Ali is overriding.
3. State the material effect, risks, and any irreversible or external impact
   briefly before acting.
4. Execute only within the named scope, preserving unrelated work and the
   evidence trail required by the active project.
5. Verify the actual result and report what changed, what did not change, and
   any remaining evidence gap.
6. Record the change where the active project rules require it; do not create a
   new standing exception unless Ali explicitly asks for one.

## Ambiguous invocations

If Ali invokes the authority without naming an action or scope, ask one concise
question rather than inferring broad permission. If the action is clear but a
target is not, resolve the target from live project state only when doing so is
unambiguous; otherwise ask Ali.
