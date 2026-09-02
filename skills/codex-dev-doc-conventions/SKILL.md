---
name: dev-doc-conventions
description: Prepare shareable development documentation by removing private internals, normalizing style, and passing the project's readiness scan. Use when editing external-facing developer documents or sending selected documentation outside the private project.
---

# Shareable Development-Document Conventions

This skill applies to documents intended for readers outside the private working context. Before editing, read the project root's `agent_roles.md`; it determines approval and review responsibilities. Keep the internal source as the safety net, edit only the approved shareable copy, and do not claim readiness until the project's scan and manual checks pass.

## Content boundary

Before editing, identify the approved shareable files and the private/internal twins. Remove or generalize:

- agent names, model identifiers, seat labels, and internal governance wording;
- canvas names, private repository paths, internal tooling, and session details;
- client or employer internals, implementation-specific systems, PII, phone numbers, and real staff names;
- secrets, tokens, credentials, raw transcripts, and private logs; and
- emojis or other project-internal presentation cues that are not part of the target style.

Do not silently remove information that changes the technical meaning. If a judgment, unresolved decision, or private dependency matters, flag it for the project owner instead of leaking it or inventing a neutral substitute.

## Editing workflow

1. Edit the shareable development copy only; preserve the internal twin as the source of truth and safety net.
2. Run the project's `send_readiness_scan` or equivalent scanner after the edit.
3. Confirm every prohibited-content axis is clean; in the supplied project this includes an Axis-1 tooling scan of zero, but use the project's current axis definitions.
4. Review the rendered or plain-text output for leakage, broken links, unreadable tables, and meaning-changing sanitization.
5. Send only the explicitly named, approved files, individually. Do not bulk-send a documentation directory.

## Formatting

- Write a spaced em dash as a colon when the target convention requires it.
- Do not put a space before a colon.
- Convert explanatory parentheticals to the target project's colon-based explanatory style where required.
- Use the project's callout convention consistently.
- Do not use emojis in shareable developer documents.
- Escape `$` as `\$` where the target renderer interprets it as markup.
- Prefer tables first for repeated structured information, then explain the implications in prose.
- Expect an approved formatter to retouch the file; inspect its diff and revert only changes outside the requested scope.
