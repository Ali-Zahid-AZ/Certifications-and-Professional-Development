#!/usr/bin/env python3
"""Render a table-heavy markdown doc to a print-clean landscape PDF.

The no-clipping guarantee is CSS, not page size: `table-layout:fixed` + `width:100%`
means a table mathematically cannot overflow the printable box. Landscape (not a
bigger page) is what rescues 7-column tables.

Run (no install needed — uv fetches the two deps into a throwaway env):

    uv run --with beautifulsoup4 --with playwright python render_pdf.py \
        --input doc.md --output doc.pdf --title "Project - Report"

Requires on PATH: pandoc, google-chrome. Verify output per the skill's vision-check step.
"""
import argparse
import html
import pathlib
import subprocess
import sys

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# House palette (Ali's ratified scheme; a sage-green variant was tried and reverted 2026-07-06).
NAVY, PANEL, STRIPE, RULE = "#243447", "#f6f8fa", "#f2f5f8", "#9fb0c0"

# Narrow columns that must not hog width, as % of table width. Extend per-doc with --col.
DEFAULT_COL_PCT = {"#": 3.0, "type": 4.5, "rank": 5.0, "vendor": 11.0, "url": 16.0}

CSS_TEMPLATE = f"""
* {{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
html {{ font-size:__BODYPT__pt; }}
body {{ font-family:'Helvetica Neue',Arial,'Segoe UI','Noto Sans','Noto Color Emoji',sans-serif;
       color:#1c2530; line-height:1.42; margin:0; }}
h1 {{ font-size:1.85rem; color:{NAVY}; margin:0 0 .3rem; }}
h2 {{ font-size:1.32rem; color:{NAVY}; border-bottom:2px solid {NAVY}; padding-bottom:2px;
     margin:1.3rem 0 .5rem; break-after:avoid; }}
h3 {{ font-size:1.1rem; color:#2f4256; margin:.9rem 0 .35rem; break-after:avoid; }}
p,li {{ margin:.28rem 0; }}
blockquote {{ border-left:3px solid {RULE}; background:{PANEL}; margin:.5rem 0;
             padding:.35rem .8rem; color:#38414c; }}
blockquote p, blockquote li {{ margin:.14rem 0; }}
code {{ font-family:'SF Mono',Menlo,Consolas,monospace; background:#eef1f4; color:#0b3d63;
       padding:0 .18em; border-radius:2px; font-size:.9em; overflow-wrap:anywhere; }}
a {{ color:#1f5fa8; text-decoration:none; overflow-wrap:anywhere; word-break:break-word; }}
strong {{ color:#17212c; }}
table {{ width:100%; table-layout:fixed; border-collapse:collapse; margin:.5rem 0 1rem;
        font-size:__TABLEPT__pt; }}
thead {{ display:table-header-group; }}
th,td {{ border:1px solid #b9c2cb; padding:3px 5px; text-align:left; vertical-align:top;
        overflow-wrap:anywhere; word-break:break-word; line-height:1.3; }}
th {{ background:{NAVY}; color:#fff; font-weight:600; }}
tbody tr:nth-child(even) td {{ background:{STRIPE}; }}
tr {{ break-inside:avoid; }}
hr {{ border:0; border-top:1px solid #d5dce2; margin:1rem 0; }}
"""

FOOTER_TEMPLATE = (
    '<div style="font-size:8px;width:100%;text-align:center;color:#777;'
    'font-family:sans-serif;padding:0 8mm;">__TITLE__ &middot; '
    '<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
)


def md_to_html(md_path):
    """pandoc GFM -> html5 fragment. --wrap=none keeps pipe-tables intact; <thead> repeats headers."""
    try:
        result = subprocess.run(
            ["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none", str(md_path)],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as exc:  # check=True hides captured stderr in its message
        sys.exit(f"pandoc failed (exit {exc.returncode}):\n{exc.stderr}")
    # Source docs escape currency as \$ for the math-enabled renderer; pandoc leaves some literal.
    fragment = result.stdout.replace("\\$", "$")  # not `html` — that shadows the stdlib import
    print(f"[1/4] pandoc -> {len(fragment)} chars of HTML", flush=True)
    return fragment


def _widths(headers, col_pct):
    """Fixed % for known narrow columns; the remainder split equally across the rest."""
    fixed = {i: col_pct[h.strip().lower()] for i, h in enumerate(headers)
             if h.strip().lower() in col_pct}
    free = [i for i in range(len(headers)) if i not in fixed]
    remaining = 100.0 - sum(fixed.values())
    if remaining < 0:  # over-pinned via --col: negative widths are silently dropped by the browser
        print(f"WARNING: pinned columns total {sum(fixed.values()):.1f}% (>100%) — free columns "
              f"clamped to 0; lower your --col values", flush=True)
        remaining = 0.0
    each = remaining / len(free) if free else 0.0
    return [fixed.get(i, each) for i in range(len(headers))]


def inject_colgroups(html, col_pct):
    """Give every table explicit per-column widths so fixed layout has something to honour."""
    soup = BeautifulSoup(html, "html.parser")
    count = 0
    for table in soup.find_all("table"):
        thead = table.find("thead")
        if not thead:
            continue
        headers = [th.get_text() for th in thead.find_all("th")]
        if not headers:
            continue
        colgroup = soup.new_tag("colgroup")
        for width in _widths(headers, col_pct):
            col = soup.new_tag("col")
            col["style"] = f"width:{width:.2f}%"
            colgroup.append(col)
        table.insert(0, colgroup)
        count += 1
    print(f"[2/4] colgroups injected into {count} tables", flush=True)
    return str(soup)


def build_page(body_html, body_pt, table_pt):
    css = CSS_TEMPLATE.replace("__BODYPT__", str(body_pt)).replace("__TABLEPT__", str(table_pt))
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<style>{css}</style></head><body>{body_html}</body></html>")


def render(page_html, out_path, title, page_format, tmp_dir):
    """channel='chrome' uses the system browser, sidestepping playwright-vs-cached-browser drift."""
    html_path = tmp_dir / "_render.html"
    html_path.write_text(page_html, encoding="utf-8")
    print("[3/4] launching system chrome", flush=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(out_path), format=page_format, landscape=True, print_background=True,
            margin={"top": "14mm", "bottom": "16mm", "left": "12mm", "right": "12mm"},
            display_header_footer=True, header_template="<div></div>",
            footer_template=FOOTER_TEMPLATE.replace("__TITLE__", html.escape(title)),
        )
        browser.close()
    print(f"[4/4] WROTE {out_path} ({out_path.stat().st_size // 1024} KB)", flush=True)


def parse_args():
    ap = argparse.ArgumentParser(description="Table-heavy markdown -> clean landscape PDF")
    ap.add_argument("--input", required=True, type=pathlib.Path)
    ap.add_argument("--output", required=True, type=pathlib.Path)
    ap.add_argument("--title", default="", help="footer text, left of the page numbers")
    ap.add_argument("--format", default="A4", help="A4 (Ali's default) or A3")
    ap.add_argument("--body-pt", type=float, default=8.5)
    ap.add_argument("--table-pt", type=float, default=7.5)
    ap.add_argument("--col", action="append", default=[], metavar="HEADER=PCT",
                    help="pin a column width, e.g. --col 'vendor=11'. Repeatable.")
    return ap.parse_args()


def main():
    args = parse_args()
    if not args.input.is_file():
        sys.exit(f"input not found: {args.input}")
    # as_uri() below rejects relative paths, so a relative --output must be resolved first.
    args.output = args.output.resolve()
    col_pct = dict(DEFAULT_COL_PCT)
    for spec in args.col:
        header, sep, pct = spec.partition("=")
        if not sep or not header.strip():
            sys.exit(f"--col expects HEADER=PCT, got: {spec!r}")
        try:
            col_pct[header.strip().lower()] = float(pct)
        except ValueError:
            sys.exit(f"--col percentage must be a number, got {pct!r} in {spec!r}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    body_html = inject_colgroups(md_to_html(args.input), col_pct)
    page_html = build_page(body_html, args.body_pt, args.table_pt)
    render(page_html, args.output, args.title or args.input.stem, args.format, args.output.parent)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
