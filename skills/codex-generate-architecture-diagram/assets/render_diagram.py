#!/usr/bin/env python3
"""
render_diagram.py — deterministic HTML -> PNG renderer for house-style schematics.

WHY THIS EXISTS
    We no longer use any image-generation model. A schematic is now an
    HTML file using the house CSS (assets/diagram_house.css); this script screenshots it
    to a crisp 2x PNG with headless Chromium. Same input -> same pixels, every session.

USAGE
    uv run --with playwright python render_diagram.py INPUT.html OUTPUT.png [--scale 2] [--selector .page] [--full-page]

    - INPUT.html  : a self-contained house-style HTML (CSS inlined in <style>).
    - OUTPUT.png  : where to write the PNG.
    - --scale N   : device scale factor (default 2 -> retina-crisp, matches existing assets).
    - --selector  : CSS selector to screenshot (default ".page"). Tight crop around the diagram.
    - --full-page : screenshot the whole page incl. the gridded backdrop margin
                    (use this to match the older 2930px-wide assets exactly).

NOTES
    * Reuses the Chromium already cached by Playwright (~/.cache/ms-playwright); no download
      needed if a browser is present. If missing, run once:  uv run --with playwright playwright install chromium
    * `uv` provides the ephemeral env (project standard) so nothing pollutes the system Python.
    * Pure-stdlib argument handling; the only third-party import is playwright.
"""
import sys
import os


def parse_args(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    args = {"input": argv[1], "output": argv[2], "scale": 2, "selector": ".page", "full_page": False}
    i = 3
    while i < len(argv):
        a = argv[i]
        if a == "--scale":
            i += 1
            args["scale"] = float(argv[i])
        elif a == "--selector":
            i += 1
            args["selector"] = argv[i]
        elif a == "--full-page":
            args["full_page"] = True
        else:
            sys.exit(f"Unknown argument: {a}\n{__doc__}")
        i += 1
    return args


def render(args):
    from playwright.sync_api import sync_playwright

    in_path = os.path.abspath(args["input"])
    if not os.path.exists(in_path):
        sys.exit(f"Input HTML not found: {in_path}")
    out_path = os.path.abspath(args["output"])
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=args["scale"])
        page.goto("file://" + in_path)
        page.wait_for_timeout(350)  # let fonts/layout settle
        if args["full_page"]:
            page.screenshot(path=out_path, full_page=True)
        else:
            el = page.query_selector(args["selector"])
            if el is None:
                # graceful fallback: full page if the selector is absent
                page.screenshot(path=out_path, full_page=True)
            else:
                el.screenshot(path=out_path)
        browser.close()
    print(f"rendered -> {out_path}")


if __name__ == "__main__":
    render(parse_args(sys.argv))
