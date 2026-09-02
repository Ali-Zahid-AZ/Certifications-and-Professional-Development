#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pydantic>=2,<3"]
# ///
"""arXiv scout helper for the mi-research-scout skill.

Progressive disclosure, deterministic, Pydantic-V2 validated output.

Two subcommands:
  search       Stage 1 — cheap. Returns Title/Authors/Abstract/categories for
               papers in the last N days. NEVER pulls full text.
  methodology  Stage 2 — only after an abstract aligns with a local axiom.
               Pulls the paper body (via ar5iv) and returns method/experiment
               sections only.

Governance: this tool sends only the DISTILLED KEYWORD QUERY it is given to
arXiv (public discovery API). It transmits no vault content. The caller is
responsible for passing keywords, never raw axiom/note text (vault rule §6).

All output is a single JSON object on stdout. Errors -> {"ok": false, "error": ...}.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator

ARXIV_API = "http://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
USER_AGENT = "mi-research-scout/1.0 (personal MI research; arXiv API)"
TIMEOUT = 30


# --------------------------------------------------------------------------- #
# Pydantic V2 models                                                          #
# --------------------------------------------------------------------------- #
class Paper(BaseModel):
    """Stage-1 abstract-level record. No full text."""

    arxiv_id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    published: str  # ISO date (submission)
    updated: str
    abstract: str
    categories: list[str] = Field(default_factory=list)
    primary_category: Optional[str] = None
    pdf_url: str
    abs_url: str
    comment: Optional[str] = None  # often contains GPU/hardware hints

    @field_validator("title", "abstract")
    @classmethod
    def _squash_ws(cls, v: str) -> str:
        return re.sub(r"\s+", " ", v).strip()


class SearchResult(BaseModel):
    ok: bool = True
    query: str
    days: int
    returned: int
    window_start: str
    papers: list[Paper]


class MethodologySection(BaseModel):
    heading: str
    text: str


class MethodologyResult(BaseModel):
    ok: bool = True
    arxiv_id: str
    source: str  # "ar5iv" | "abstract-fallback"
    title: Optional[str] = None
    sections: list[MethodologySection] = Field(default_factory=list)
    note: Optional[str] = None


# --------------------------------------------------------------------------- #
# Helpers                                                                      #
# --------------------------------------------------------------------------- #
def _fetch(url: str, retries: int = 3) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last = b""
    for attempt in range(retries):
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            last = resp.read()
        if last.strip():
            return last
        # arXiv intermittently returns an empty body on rapid calls; back off.
        time.sleep(2 * (attempt + 1))
    return last


def _parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _entry_to_paper(e: ET.Element) -> Paper:
    raw_id = e.findtext(f"{ATOM}id", "")
    arxiv_id = raw_id.rsplit("/abs/", 1)[-1]
    authors = [a.findtext(f"{ATOM}name", "") for a in e.findall(f"{ATOM}author")]
    cats = [c.attrib.get("term", "") for c in e.findall(f"{ATOM}category")]
    prim = e.find("{http://arxiv.org/schemas/atom}primary_category")
    pdf_url = ""
    for link in e.findall(f"{ATOM}link"):
        if link.attrib.get("title") == "pdf":
            pdf_url = link.attrib.get("href", "")
    comment = e.findtext("{http://arxiv.org/schemas/atom}comment")
    return Paper(
        arxiv_id=arxiv_id,
        title=e.findtext(f"{ATOM}title", ""),
        authors=[a for a in authors if a],
        published=e.findtext(f"{ATOM}published", ""),
        updated=e.findtext(f"{ATOM}updated", ""),
        abstract=e.findtext(f"{ATOM}summary", ""),
        categories=[c for c in cats if c],
        primary_category=prim.attrib.get("term") if prim is not None else None,
        pdf_url=pdf_url or f"https://arxiv.org/pdf/{arxiv_id}",
        abs_url=f"https://arxiv.org/abs/{arxiv_id}",
        comment=re.sub(r"\s+", " ", comment).strip() if comment else None,
    )


# --------------------------------------------------------------------------- #
# search                                                                       #
# --------------------------------------------------------------------------- #
def cmd_search(args: argparse.Namespace) -> dict:
    cats = [c.strip() for c in args.categories.split(",") if c.strip()]
    cat_clause = " OR ".join(f"cat:{c}" for c in cats)
    # Build a PROPER arXiv boolean: split the query on " OR " and field-qualify
    # each phrase as all:"phrase". A bare `all:(A OR B)` is mis-parsed by the API
    # (it silently degrades to a date-sorted dump), so we quote every term.
    phrases = [p.strip() for p in re.split(r"\s+OR\s+", args.query) if p.strip()]
    kw_clause = " OR ".join(f'all:"{p}"' for p in phrases) or f'all:"{args.query}"'
    search_q = f"({kw_clause})"
    if cat_clause:
        search_q = f"{search_q} AND ({cat_clause})"
    params = {
        "search_query": search_q,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        # over-fetch so client-side date window still yields enough
        "max_results": str(max(args.max * 6, 30)),
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    root = ET.fromstring(_fetch(url))

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    kept: list[Paper] = []
    for e in root.findall(f"{ATOM}entry"):
        p = _entry_to_paper(e)
        try:
            pub = _parse_dt(p.published)
        except ValueError:
            continue
        if pub >= cutoff:
            kept.append(p)
        if len(kept) >= args.max:
            break

    return SearchResult(
        query=args.query,
        days=args.days,
        returned=len(kept),
        window_start=cutoff.date().isoformat(),
        papers=kept,
    ).model_dump()


# --------------------------------------------------------------------------- #
# methodology                                                                  #
# --------------------------------------------------------------------------- #
_METH_KEYS = (
    "method",
    "approach",
    "experiment",
    "setup",
    "implementation",
    "training",
    "model",
    "evaluation",
    "data",
)
_TAG_RE = re.compile(r"<[^>]+>")
_SEC_RE = re.compile(
    r"<h[2-3][^>]*>(.*?)</h[2-3]>(.*?)(?=<h[2-3][^>]*>|</body>)",
    re.IGNORECASE | re.DOTALL,
)


def _clean(html: str) -> str:
    txt = _TAG_RE.sub(" ", html)
    txt = re.sub(r"&[a-z]+;", " ", txt)
    return re.sub(r"\s+", " ", txt).strip()


def cmd_methodology(args: argparse.Namespace) -> dict:
    aid = args.id.strip()
    bare = re.sub(r"v\d+$", "", aid)
    # Prefer arXiv native HTML (covers brand-new papers); fall back to ar5iv.
    sources = [
        ("arxiv-html", f"https://arxiv.org/html/{aid}"),
        ("arxiv-html", f"https://arxiv.org/html/{bare}"),
        ("ar5iv", f"https://ar5iv.labs.arxiv.org/html/{bare}"),
    ]
    html, source, last_exc = "", "", None
    for src, url in sources:
        try:
            body = _fetch(url).decode("utf-8", "ignore")
        except Exception as exc:  # noqa: BLE001 - try next source
            last_exc = exc
            continue
        # Reject abstract-landing redirects (no real body sections).
        if "ltx_title_section" in body or "<h2" in body.lower():
            html, source = body, src
            break
    if not html:
        return MethodologyResult(
            arxiv_id=aid,
            source="abstract-fallback",
            note=f"No HTML render available ({last_exc}); read the abstract from "
            f"`search`, or the PDF: https://arxiv.org/pdf/{aid}",
        ).model_dump()

    title_m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)

    # Collect every parsed section once, then rank.
    all_secs: list[MethodologySection] = []
    for heading_html, body_html in _SEC_RE.findall(html):
        heading = _clean(heading_html)
        body = _clean(body_html)
        if heading and len(body) > 40:
            all_secs.append(
                MethodologySection(heading=heading, text=body[: args.max_chars])
            )

    note = None
    matched = [s for s in all_secs if any(k in s.heading.lower() for k in _METH_KEYS)]
    if matched:
        sections = matched[: args.max_sections]
    elif all_secs:
        # Non-standard headings: return the first sections so structure is visible.
        sections = all_secs[: args.max_sections]
        note = "No method-keyword headings; returning leading sections instead."
    else:
        sections = []
        note = (
            "Body did not parse into sections (ar5iv may lack this paper or use an "
            f"atypical layout). Read the PDF directly: https://arxiv.org/pdf/{aid}"
        )
    return MethodologyResult(
        arxiv_id=aid,
        source=source,
        title=_clean(title_m.group(1)) if title_m else None,
        sections=sections,
        note=note,
    ).model_dump()


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="arXiv scout for mi-research-scout skill")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Stage 1: abstracts from the last N days")
    s.add_argument("--query", required=True, help="distilled MI keywords (NOT vault text)")
    s.add_argument("--days", type=int, default=14)
    s.add_argument("--max", type=int, default=8)
    s.add_argument(
        "--categories",
        default="cs.LG,cs.AI,cs.CL,cs.NE,stat.ML",
        help="comma-separated arXiv categories (empty string = no filter)",
    )
    s.set_defaults(func=cmd_search)

    m = sub.add_parser("methodology", help="Stage 2: method sections for one paper")
    m.add_argument("--id", required=True, help="arxiv_id, e.g. 2501.16496")
    m.add_argument("--max-sections", type=int, default=6)
    m.add_argument("--max-chars", type=int, default=2500)
    m.set_defaults(func=cmd_methodology)

    args = ap.parse_args()
    try:
        out = args.func(args)
    except Exception as exc:  # noqa: BLE001 - surface as structured error
        out = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if out.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
