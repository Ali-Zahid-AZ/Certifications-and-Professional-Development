#!/usr/bin/env python3
"""Read-only inventory of AGENT_CHANGES.md and COUNCIL.md files."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TARGET_NAMES = ("AGENT_CHANGES.md", "COUNCIL.md")
CONTROL_DIRECTORIES = {".git", ".hg", ".svn"}


def repo_root_for(path: Path, scan_root: Path) -> str | None:
    """Return the nearest lexical repository root, if one is visible."""

    candidate = path.parent
    root = scan_root
    while True:
        if (candidate / ".git").exists() or (candidate / ".hg").exists():
            return str(candidate)
        if candidate == root or candidate.parent == candidate:
            return None
        candidate = candidate.parent


def count_logical_lines(path: Path) -> int:
    """Count lines without decoding or loading the whole file into memory."""

    with path.open("rb") as handle:
        return sum(1 for _ in handle)


def scan_documents(scan_root: Path, threshold: int) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Walk the tree without following directory symlinks and collect evidence."""

    documents: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    def record_walk_error(error: OSError) -> None:
        errors.append({"path": error.filename or str(scan_root), "error": str(error)})

    for directory, dirnames, filenames in os.walk(
        scan_root,
        topdown=True,
        followlinks=False,
        onerror=record_walk_error,
    ):
        dirnames[:] = sorted(
            name
            for name in dirnames
            if name not in CONTROL_DIRECTORIES
            and not (Path(directory) / name).is_symlink()
        )
        for filename in sorted(filenames):
            if filename not in TARGET_NAMES:
                continue

            path = Path(directory) / filename
            record: dict[str, Any] = {
                "path": str(path),
                "name": filename,
                "is_symlink": path.is_symlink(),
                "resolved_path": str(path.resolve(strict=False)),
                "repository": repo_root_for(path, scan_root),
            }
            try:
                stat_result = path.stat()
                line_count = count_logical_lines(path)
                record.update(
                    {
                        "bytes": stat_result.st_size,
                        "mtime_utc": datetime.fromtimestamp(
                            stat_result.st_mtime, tz=timezone.utc
                        ).isoformat(),
                        "lines": line_count,
                        "exceeds_threshold": line_count > threshold,
                    }
                )
            except (OSError, ValueError) as error:
                record["error"] = str(error)
                errors.append({"path": str(path), "error": str(error)})
            documents.append(record)

    documents.sort(key=lambda item: (item["name"], item["path"]))
    return documents, errors


def summarize_name(documents: list[dict[str, Any]], name: str) -> dict[str, Any]:
    """Summarize one target filename without hiding unreadable entries."""

    found = 0
    readable = 0
    over_threshold = 0
    max_lines = 0
    for item in documents:
        if item["name"] != name:
            continue
        found += 1
        if "lines" not in item:
            continue
        readable += 1
        max_lines = max(max_lines, item["lines"])
        if item.get("exceeds_threshold"):
            over_threshold += 1
    return {
        "found": found,
        "readable": readable,
        "over_threshold": over_threshold,
        "max_lines": max_lines,
    }


def build_report(scan_root: Path, threshold: int) -> dict[str, Any]:
    documents, errors = scan_documents(scan_root, threshold)
    by_name = {name: summarize_name(documents, name) for name in TARGET_NAMES}
    oversized = [item for item in documents if item.get("exceeds_threshold")]
    unreadable = [item for item in documents if "error" in item]
    if errors or unreadable:
        decision = "UNVERIFIED"
    elif oversized:
        decision = "NEEDS_ALI_ACTION"
    else:
        decision = "PASS"

    return {
        "schema_version": 1,
        "scan_started_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(scan_root),
        "threshold": threshold,
        "threshold_rule": "strictly greater than threshold",
        "excluded_directory_names": sorted(CONTROL_DIRECTORIES),
        "target_names": list(TARGET_NAMES),
        "inventory": by_name,
        "total_documents": len(documents),
        "oversized_documents": oversized,
        "unreadable_documents": unreadable,
        "errors": errors,
        "decision": decision,
        "documents": documents,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("/home/az/GitHub-Repositories"),
        help="root directory to scan",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=2000,
        help="strict line threshold; files above it are escalated",
    )
    parser.add_argument(
        "--format",
        choices=("json",),
        default="json",
        help="output format (JSON is intentionally the stable machine format)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="indent JSON for human inspection",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.threshold < 0:
        print("--threshold must be non-negative", file=sys.stderr)
        return 2
    if not args.root.is_dir():
        print(f"scan root is not a directory: {args.root}", file=sys.stderr)
        return 2

    report = build_report(args.root, args.threshold)
    indent = 2 if args.pretty else None
    print(json.dumps(report, indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
