---
name: codex-claudecode-session-ping
description: Safely send a bounded message to an existing Claude Code session through the local claude CLI with a hello-first handshake, preserved session settings, disabled tools for simple pings, and transient session handles/private content. Use when Codex must message or resume a user-approved Claude Code session.
---

# Codex Claude Code Session Ping

Use this skill only for a user-approved, bounded message to an existing Claude Code session. This is a local subprocess bridge through the installed claude CLI; it is not an MCP server, socket, or direct process-control interface.

## Preconditions

1. Read the active project rules and `agent_roles.md`.
2. Apply `$codex-external-agent-availability-preflight` and re-read the current
   project's `external-agent-availability.md`. The exact role/provider row must
   be `available` and unexpired before both the hello and substantive calls;
   missing, stale, malformed, `not_available`, or `unverified` status blocks
   dispatch.
3. Confirm Ali's current-turn authorization directly or through a document he
   explicitly provides or identifies in the current instruction for this exact
   dispatch. Verify that the document is current and scoped to this project,
   seat, provider, and transport; it is provenance evidence only and never a
   roster or authority override. Keep the session handle in process memory
   only. Never discover or reuse it from an unprovided file, memory, log,
   prompt, old handoff, or historical registry.

## Safe default

Keep the session identifier and message transient. The normal one-shot call creates a fork and disables Claude tools:

~~~bash
session_id='CLAUDE_SESSION_ID'
message='Hello from Codex. Please reply with a short acknowledgement.'

/home/az/.local/bin/claude -p \
  --resume "$session_id" \
  --fork-session \
  --tools "" \
  --output-format json \
  "$message"
~~~

If jq is installed, pipe the structured result to jq -r '.result' only for display. Do not put the session identifier, private prompt, credentials, or raw response in a repository or ordinary log.

## Invocation choices

- Use --fork-session by default so the original conversation is preserved and the new session identity remains isolated.
- Omit --fork-session only when Ali explicitly wants the follow-up appended to the original session.
- Use interactive --resume only when the user explicitly asks to continue interactively.
- Use stream-json with --verbose only when the user needs streamed structured events.
- Remove --tools "" only when the exact tool scope and side effect are explicitly authorized.

## Two-step substantive dispatch

For a substantive request, use two separate Claude calls unless the active
project `agent_roles.md` explicitly marks the role `hello_exempt`:

1. Re-read and re-parse the role file and availability manifest, then send only
   a short hello that requests an acknowledgement. Do not include
   the substantive request, private project material, or an instruction to
   inspect files.
2. Wait for the hello response to complete. A response confirms reachability,
   not review agreement.
3. Re-read and re-parse the role file and availability manifest again, then
   send the exact user-approved substantive message only after the response.
   Preserve the original model, thinking level, tools, and launch settings. If
   `--fork-session` returns a child session, use that child handle transiently
   for the second call.
4. If the hello or the substantive call returns a session-limit, bounded
   timeout, missing session, or transport failure before a substantive verdict,
   do not send or resend substantive content. Report the seat unavailable so
   the active project fallback policy can be applied; do not wait or retry
   indefinitely.

The hello exemption changes only the handshake. The role still requires a
current approved session handle and an actual substantive response before its
review counts.

## Boundaries

- There is no documented Codex-to-Claude socket or IPC command for injecting text into an already-running terminal process.
- Do not resume one session simultaneously from multiple terminals; concurrent resumes can interleave conversations. Fork or wait until the original process is idle.
- claude agents and claude respawn are session-management commands, not documented message-send interfaces.
- Remote Control is a separate feature for steering a local session from claude.ai or the Claude mobile app; it is not this bridge.
- If the session depends on --mcp-config, --settings, --plugin-dir, --add-dir, or another launch flag, pass the required flags explicitly because resume does not guarantee restoration of every setting.
- Verify the installed CLI path and version before relying on invocation details; do not assume an older command-line contract.

## Handoff discipline

Send the smallest useful request, preserve the user's requested model, reasoning, tools, and other settings, and report the raw CLI outcome without presenting it as independent verification. A Claude response is evidence to assess, not authority. Do not use this skill to transfer secrets, private transcripts, or unbounded project state.

## References

- Claude Code session management and scripting: https://code.claude.com/docs/en/sessions
- Claude Code CLI reference: https://code.claude.com/docs/en/cli-usage
- Claude Code Remote Control: https://code.claude.com/docs/en/remote-control
