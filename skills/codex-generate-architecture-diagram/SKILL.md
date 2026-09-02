---
name: generate-architecture-diagram
description: Produce a professional house-style architecture, pipeline, lifecycle, build-sequence, flow-canvas, or status-board diagram as BOTH an HTML file and a rendered PNG. Use when asked to "make/generate an architecture diagram", "draw a schematic", produce a system diagram for a deck/director, or turn a written design into a polished visual. This skill renders real pixels deterministically from HTML+CSS via headless Chromium — no image-generation model is used.
---

## Project role assignment

Before assigning authority, selecting a seat, or interpreting a role-specific instruction, read the project root's `agent_roles.md`. It is the source of truth for the active roster, responsibilities, permissions, model routing, and review requirements.

# House-Style Schematic Protocol (HTML + CSS → PNG)

You author a **self-contained HTML file** using the shared house CSS, then render it to a crisp PNG with **headless Chromium**. This replaces the old image-model workflow (a separate image-model workflow etc.) entirely: the output is deterministic, version-controllable, editable, and identical across sessions. **Always produce BOTH artifacts: the `.html` (source of truth) and the `.png` (the shareable raster).**

> The house look is a **near-monochrome "paper-figure"** style — it should read like a panel in a journal, **not** a slide deck. Warm ivory paper, one teal accent, structure carried by typography and layout. If the user only wants a quick text-editable graph and not this polished look, a **Mermaid** or **Graphviz/DOT** block is fine instead.

---

## What this skill ships (in `assets/`)

| File | Purpose |
|---|---|
| `diagram_house.css` | **Canonical** house style — warm paper, single teal accent, clay break, umber connectors, flat number badges, cards, legend. Single source of truth for the look. |
| `template-architecture.html` | Vertical **bands** (layers/zones, left label + cards). For "how the system is structured". |
| `template-build-sequence.html` | **Axis + columns** (phase axis · tool lane · cards · aside). For "how it was built, phase by phase". |
| `template-flow-canvas.html` | **Node graph / spine** (start → action/decision/update/fault → end). For "how a Flow/Apex path executes". |
| `template-board.html` | **Status cards** (pass/warn/defer badges). For "test results / readiness boards". |
| `render_diagram.py` | HTML → PNG renderer (headless Chromium, 2× scale). |

`sample/` holds a rendered reference (`sample-architecture.html` + `.png`) so you can see the target look before you start.

Each template **inlines a copy of the CSS** in its `<style>` block so a single `.html` renders anywhere via `file://`. `diagram_house.css` is the canonical copy — if you change the look, change it there and re-sync the inlined copies.

---

## The one governing principle

**Hue encodes MEANING, not category.** Near-monochrome on warm paper; structure is carried by **typography and layout**, not by colour. Colour is spent only where it means something.

## Palette tokens (verbatim — use ONLY these)

```css
--paper:#faf7f1;      /* warm ivory canvas — plain, NO grid lines */
--ink:#272320;        /* warm near-black — titles, card titles */
--soft:#6f665b;       /* warm muted — body / secondary text */
--faint:#a89f91;      /* hairline + italic lead text */
--rule:#e3dccf;       /* hairline rules, default card border */
--conn:#6e5747;       /* warm dark umber — flow connectors with visual weight */
--accent:#2f6f6b;     /* petrol/teal — THE single accent (badges + ground truth) */
--accent-d:#1f4f4c;   /* deep accent — accent text */
--accent-wash:#eef4f2;/* faint teal tint — ground-truth card fill + code chips */
--break:#b5482e;      /* clay-red — reserved for the ONE mechanism break, nothing else */
--break-wash:#f7ece7;
--card:#fffdf9;       /* card fill (warm white) */
```

### Colour discipline — the only legitimate uses

| Colour | Used for, and ONLY for |
|--------|------------------------|
| **Teal `--accent`** | filled number badges; the **ground-truth** anchor card (`.card.gt`, ◆); accent text / `code` chips |
| **Clay `--break`** | exactly ONE thing per figure — the mechanism that **breaks** (`.card.brk`, ⚠). Never decorative. |
| **Umber `--conn`** | flow connectors / arrows only (warm-dark, visually weighted) |
| **Warm neutrals** | everything else — paper, ink, hairlines, card borders |

Never reintroduce green, amber, orange, periwinkle, lavender as *category* labels. If a new semantic truly needs a colour, add it to this table first.

## The five governing rules (what makes it look "house")

1. **Warm paper, no chrome.** Background is plain `--paper` — **no grid lines, no filled banner bars, no navy blocks.** Sans font only (`"Segoe UI", Inter, Arial, sans-serif`); titles `font-weight:800`; emphasis via italic + `--accent-d`.
2. **Spatial skeleton before content.** Pick a layout archetype (band / build-sequence / flow-canvas / board) and lay the empty grid first, then fill cards. Don't free-place boxes.
3. **Cards hold terse technical terms, not prose.** A card = a bold `.t`/`.ct` title + a few comma/`<br>`-separated terms, `code` for API names. Coloured rounded border ONLY on the ground-truth card (`.gt`, teal) and the single break card (`.brk`, clay). Keep ≤ ~5 cards per band.
4. **Flat teal badges + umber arrows show flow.** `.num`/`.badge` are **flat** filled teal circles with a white numeral — no gradient, no shadow, no outlined ring. Connectors are warm-dark umber arrows (`.arrow`/`.farrow`/`.down`) with rounded caps and filled-triangle heads; use the **fork SVG** (below) where a node genuinely branches. `.elbl.yes`→accent, `.elbl.no`→clay.
5. **Anchor with TYPE, not bars.** Header = uppercase letter-spaced teal **kicker** → bold **title** (one italic accent phrase allowed) → muted italic **sub** → small-caps **breadcrumb sequence** (`.seq`, last item bold accent) → hairline. Asides/invariants are editorial italic lines with a short accent rule above (`.invariant` / `.callout`), never filled boxes. Close with a hairline-framed type-led **headline** (`.bottom`, key phrases in `--accent-d` "holds" / `--break` "breaks"), a **dot legend** (mandatory — states what each colour means), and the italic **thesis tagline** (`.tagline`).

### Fork connector SVGs (copy verbatim)

```html
<!-- single connector between stages -->
<svg width="46" height="70" viewBox="0 0 46 70" fill="none">
  <path d="M5 35 H30" stroke="#6e5747" stroke-width="6" stroke-linecap="round"/>
  <path d="M29 27 L44 35 L29 43 Z" fill="#6e5747"/></svg>

<!-- one-to-two fork -->
<svg width="124" height="74" viewBox="0 0 124 74" fill="none">
  <g stroke="#6e5747" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14 28 Q7 28 7 37 Q7 46 14 46"/>
    <path d="M10 37 H30 Q40 37 40 28 V22 Q40 14 50 14 H98"/>
    <path d="M10 37 H30 Q40 37 40 46 V52 Q40 60 50 60 H98"/></g>
  <path d="M97 7 L116 14 L97 21 Z" fill="#6e5747"/>
  <path d="M97 53 L116 60 L97 67 Z" fill="#6e5747"/></svg>
```

---

## Workflow (do this every time)

1. **Gather inputs:** title + one-line subtitle; audience (exec → fewer cards; engineering → detailed); layout archetype; the zones/phases and their cards; the flow/numbering; the ground-truth anchor (if any) and the single break (if any); the breadcrumb stages; the closing headline + thesis line. Anchor to a prior diagram if matching a set.
2. **Pick the closest template** in `assets/` and copy it to the target location (e.g. the project's `docs/architectural-diagrams/html/<name>.html`). Keep the `<style>` block; replace ALL body content.
3. **Author the body** following the five rules. Use real names/`code` from the codebase, not placeholders. Spend teal only on badges + the ground-truth card; spend clay on at most one break.
4. **Render to PNG:**
   ```bash
   uv run --with playwright python <skill>/assets/render_diagram.py \
       docs/architectural-diagrams/html/<name>.html \
       docs/architectural-diagrams/<name>.png
   ```
   - Default crop is the `.page` element at 2× scale (crisp, tight). `--scale 3` for extra-large prints.
   - Reuses the Chromium in `~/.cache/ms-playwright`. If none is installed: `uv run --with playwright playwright install chromium` (one time).
5. **Verify the PNG** by viewing it. Check: warm paper with NO grid; teal only on badges + ground truth; at most one clay break; umber arrows; flat badges (no shadow/ring); kicker→title→sub→breadcrumb header; dot legend present; thesis tagline present. Re-edit the HTML and re-render — the cheapest iteration is a precise delta.
6. **Save BOTH** next to the project's existing diagrams: `.html` under `…/html/`, `.png` one level up. Reference the `.png` from markdown with a correct relative path and **verify the link resolves**.

---

## Layout archetypes (pick one, state it explicitly)

| Archetype | Template | Use for | Skeleton |
|---|---|---|---|
| **Architecture — vertical bands** | `template-architecture.html` | system structure / layers | `.band` rows (`.lbl` left + `.cells` cards); footer `.foot` with `.panel.boundary` + `.panel.guard`; `.bottom` close |
| **Build sequence** | `template-build-sequence.html` | phased build, who-does-what | `.bband` (axis · `.col.head` · `.cards` · `.callout` aside); `.gate` per phase; `.nonneg` non-negotiables strip |
| **Flow canvas** | `template-flow-canvas.html` | Flow/Apex execution path | `.flow`/`.canvas` rows of `.node`(`.start/.action/.update/.create/.fault/.end`) + `.decision`; `.farrow` + `.elbl` branches; `.legend` |
| **Board** | `template-board.html` | test/readiness status | `.board` grid of `.tcard`(`.pass`→teal/`.warn`→clay/`.defer`→neutral) with `.badge`; `.emcallout` summary |

---

## Quality checklist (run before declaring done)

- [ ] BOTH `.html` and `.png` produced and saved in the repo's diagram folders.
- [ ] Only the palette tokens used — warm paper, NO grid lines, NO filled banner/navy bars.
- [ ] Teal spent only on badges + ground-truth card; clay on **at most one** break; umber only on connectors.
- [ ] Flat teal number badges (no gradient/shadow/ring); sans font throughout.
- [ ] Header = kicker → title (≤1 italic accent phrase) → italic sub → small-caps breadcrumb → hairline.
- [ ] Asides/invariants are editorial italic lines with an accent rule, NOT filled boxes.
- [ ] Closing block = hairline + type-led headline ("holds"/"breaks") + **dot legend** + italic **thesis tagline**.
- [ ] Spatial skeleton laid before content; ≤ ~5 cards per band; terse term-clusters, not sentences.
- [ ] PNG viewed and verified (no clipping/overflow); markdown link to it resolves.
- [ ] Real codebase names/`code` used; matches the existing diagram set's look.

---

## Maintenance: HTML is the source of truth

- **Never hand-edit a PNG.** Edit the `.html` source and re-render — the HTML is the single source of truth; the PNG is only the shareable raster.
- **A stale PNG is a documentation defect.** Re-render whenever the diagram's facts change, and save both artifacts together so they never diverge.
- Project-level palette overrides (e.g. a journal-locked variant) must be declared in a project palette-rules file — never improvised per figure.

---

## Pitfalls & fallbacks

- **Reintroducing rainbow/category colour:** the single biggest regression. If a card "needs" green/amber/orange, it almost certainly doesn't — use a neutral card and let typography carry it. Only teal (badge/ground-truth), clay (the one break), and umber (arrows) are coloured.
- **Filled banners / navy bars:** the old style used navy `.banner`/`.bottom` bars — the house style replaces these with type under a hairline. Don't fill them.
- **Clipping at the right edge:** the page is `width:1400px`; keep content within it. Use `.cards.c3`/`.c2` (fewer columns) rather than overflowing.
- **Blurry PNG:** ensure `--scale 2` (default). Render large and let the viewer shrink.
- **Chromium missing:** `uv run --with playwright playwright install chromium` once; thereafter renders are offline.
- **CSS drift:** if a generated HTML looks off, diff its inlined `<style>` against `assets/diagram_house.css` — re-sync from the canonical copy.

---

## Worked reference

`sample/sample-architecture.html` + `sample/sample-architecture.png` are a full rendered example. Open the PNG to see the target look, read the HTML to see how bands/cards/badges/legend/close are assembled, then adapt for the new diagram.
