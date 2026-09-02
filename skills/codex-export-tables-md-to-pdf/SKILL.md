---
name: export-tables-md-to-pdf
description: "Render a table-heavy markdown doc to a share-ready landscape PDF with NO table-edge clipping (Ali's recurring failure mode) — pandoc → per-table colgroup → system-Chrome pipeline, shipped as a parameterized script in assets/. The clipping fix is CSS (`table-layout:fixed` + `width:100%`), never a bigger page; landscape is what rescues wide tables. Closes with a mandatory pdftoppm vision-verify (look at the edges, don't trust the exit code). Invoke when a markdown doc must become a PDF — \"export this to PDF\", \"make a share-ready PDF\", \"the table edges are cut off / clipped\", \"print this for the client/vendor\"."
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# Skill: export-tables-md-to-pdf

## What I do
Turn a table-heavy markdown document into a clean, share-ready **A4-landscape** PDF whose table edges sit inside the margins. The pipeline is deterministic — pandoc for the HTML, BeautifulSoup for column widths, headless system Chrome for the PDF. No image model, no API cost.

## When to use me
- A markdown doc (research write-up, vendor comparison, client report) must leave the estate as a PDF.
- **The symptom that names this skill: table edges are cut off / columns run off the page.**
- NOT for architecture/pipeline diagrams → `generate-architecture-diagram` (HTML→PNG, different job).
- NOT for a doc with no wide tables — pandoc alone is fine; this skill's whole value is the clipping guarantee.

## The load-bearing insight (do not re-derive this the hard way)
**The clipping fix is CSS, not page size.** With `table{width:100%; table-layout:fixed}` plus `th,td{overflow-wrap:anywhere; word-break:break-word}`, a table *cannot* overflow the printable box — fixed layout honours the colgroup widths instead of letting content dictate them. **Orientation (landscape), not a bigger page, is what rescues 7-column tables**; A3 was built and then dropped (2026-07-06) because A4-landscape already fits.

## Procedure
1. **Run the shipped script** (`assets/render_pdf.py`). It does pandoc → colgroup injection → Chrome PDF in one pass, printing a flushed marker per stage:
   ```bash
   uv run --with beautifulsoup4 --with playwright python \
     <skill-dir>/assets/render_pdf.py \
     --input doc.md --output doc.pdf --title "Project - Report"
   ```
   `bs4`/`playwright` are NOT in system python by design — `uv run --with` fetches them into a throwaway env, so there is nothing to install and nothing to maintain. `pandoc`, `google-chrome` and `pdftoppm` must be on PATH (all three are, on this box).
2. **Tune column widths only if a narrow column hogs space.** The script pins `#`/`type`/`rank`/`vendor`/`url` by default and splits the remainder equally; add per-doc pins with repeatable `--col`, e.g. `--col 'dimension=10' --col 'fixes=7.5'`. Do not hand-edit the CSS for this — that is what `--col` is for.
3. **★ Verify with vision — do not trust the exit code.** Rasterise a page and *look at both edges*:
   ```bash
   pdftoppm -png -r 150 -f 1 -l 1 doc.pdf /tmp/_chk          # full page
   pdftoppm -png -r 150 -f 1 -l 1 -x 0 -W 120 doc.pdf /tmp/_l # left edge strip
   ```
   Then Read the PNG. Confirm both borders sit inside the margin. A PDF that renders without error can still clip.

## Defaults (Ali's ratified choices — change only on his say-so)
| Setting | Value | Note |
|---|---|---|
| Page | **A4 landscape** | A3 built then dropped, 2026-07-06 |
| Body / table type | 8.5pt / 7.5pt | shrink table-pt before touching page size |
| Margins | 14/16/12/12 mm | bottom is larger to clear the footer |
| Header navy | `#243447` | a lighter navy + sage-green scheme was tried and **reverted by Ali** ("keep the one you produced"), 2026-07-06 |
| Panels / stripe / rule | `#f6f8fa` / `#f2f5f8` / `#9fb0c0` | |
| Browser | `channel="chrome"` | uses `/usr/bin/google-chrome`, sidestepping playwright-vs-cached-browser version drift |

## Gotchas
1. **Keep the PDF untracked** until Ali commits it — **in repos that run an auto-commit/format watcher** (a per-repo thing, not estate-wide; `local-persona-compositionality-article` has one on a ~3-minute timer, `agentic-coding` has it OFF), a *tracked* file can be committed or reformatted between your write and your next read, so "Edit succeeded" is not proof of persisted bytes there. Check the repo you are in first — this was mis-stated as an estate-wide "auto-commit cron" until 2026-07-17.
2. **`\$` unescaping is deliberate.** Estate markdown escapes currency as `\$` for the math-enabled HTML renderer (`markdown-dollar-escaping`); pandoc unescapes most, and the script's `.replace("\\$","$")` catches the rest — including inside code spans. Never blanket-replace `$` in the *source*.
3. **`<thead>` is why headers repeat** across page breaks — pandoc emits it from GFM pipe-tables, and `thead{display:table-header-group}` does the rest. Do not strip it.
4. `--wrap=none` on pandoc is load-bearing: without it, wrapped pipe-tables stop parsing.

## Sync note & provenance
Elevated to a global skill on Ali's instruction, 2026-07-17, from the `pdf-export-recipe` memory of the `p-ai-lead-qualification-automation` project (Aircall vendor research, 2026-07-06). The shipped `assets/render_pdf.py` is the **rescued original working script** (recovered from that job's tmp dir, where it was job-scoped and would have been lost), generalized: paths/stem/footer/column-map parameterized, Aircall-specific pins removed, flushed stage markers added per the global Script Observability rule. The origin memory stays a memory (it carries the client-specific column widths); this skill is the portable procedure.
