---
name: schematic-palette-rules
description: Apply project-specific palette and layout rules to architecture schematics while preserving the shared diagram house style. Use when creating, reviewing, or rendering an architecture, pipeline, lifecycle, or system-boundary diagram.
---

# Schematic Palette and Diagram Rules

Use this skill together with the project's `SCHEMATIC-PALETTE-RULES.md` and the shared `generate-architecture-diagram` skill. Before acting, read the project root's `agent_roles.md`; it determines who may approve or review the diagram. The project palette file is authoritative for local overrides.

## Authority

- Treat the project palette file as a controlled protocol.
- Only the project owner may edit or unlock palette rules unless the project explicitly grants narrower authority.
- Do not invent a new visual language when the shared house style already supplies the structure.
- Declare every project-specific override in the source so another agent can reproduce the render.

## Palette

- Keep the neutral house palette unless the project file declares an override.
- Define CSS variables for each override and map colors to semantic roles, not arbitrary individual nodes.
- Typical variables include an accent for the primary thesis or pathway and a break color for warnings, boundaries, or disallowed transitions. Use the project file's exact names when present.
- Every color must have one documented meaning and must remain legible against the paper/background color.

## Structural rules

- Use the declared paper/background treatment and a readable sans-serif typeface.
- Preserve a clear header hierarchy, card/group structure, and unambiguous connectors.
- Keep system boundaries visible and do not let decorative styling obscure data or control flow.
- Include a legend whenever color or line style carries meaning.
- Include the project-required thesis tagline or explanatory caption when the palette file requires one.
- Keep the diagram understandable in the first viewport before relying on interaction or a high-resolution render.

## Render and verify

1. Render the browser artifact and image with the project-approved renderer. The common command is `uv run --with playwright python <path-to-render_diagram.py>`; use the actual project path and declared overrides.
2. Save the source HTML and rendered PNG at the project-approved locations.
3. Use the required viewport and scale; the default is 1400px wide at 2x unless the project file overrides it.
4. Inspect the render for clipping, contrast, unreadable labels, crossing connectors, missing legend, and boundary ambiguity.
5. Verify that the render matches the source after any change and record the command and outcome in the project change log.
