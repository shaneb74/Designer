#!/usr/bin/env python3
"""Inventory scripts for duplicate and orphan Streamlit pages."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
from collections.abc import Iterator

CANONICAL_ROOT = "ui/pages"
LEGACY_ROOT = "pages"
ENTRYPOINTS = ["app.py", "run.py"]

LINK_PATTERNS = [
    re.compile(r'safe_switch_page\(["\']([^"\']+)["\']\)'),
    re.compile(r'st\.switch_page\(["\']([^"\']+)["\']\)'),
    re.compile(r'st\.page_link\(["\']([^"\']+)["\'])'),
]


def file_hash(path: str) -> str:
    """Return the SHA-1 hash of the file at *path*."""
    digest = hashlib.sha1()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(8192)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def walk_py(root: str) -> Iterator[str]:
    """Yield Python file paths rooted at *root*."""
    for dirpath, _, files in os.walk(root):
        for filename in files:
            if filename.endswith(".py"):
                yield os.path.join(dirpath, filename).replace("\\", "/")


def collect_links(paths: list[str]) -> set[str]:
    """Collect page link targets referenced in the provided *paths*."""
    links: set[str] = set()
    for path in paths:
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for pattern in LINK_PATTERNS:
            for match in pattern.finditer(text):
                links.add(match.group(1))
    return links


def resolve_target(target: str, all_files: set[str]) -> str | None:
    """Resolve a page link *target* to a file path if present."""
    if not target.endswith(".py"):
        return None
    if target.startswith("ui/pages/") or target.startswith("pages/"):
        return target if target in all_files else None
    canonical_candidate = f"{CANONICAL_ROOT}/{target}"
    if canonical_candidate in all_files:
        return canonical_candidate
    legacy_candidate = f"{LEGACY_ROOT}/{target}"
    if legacy_candidate in all_files:
        return legacy_candidate
    return None


def main() -> None:
    """Generate a report describing duplicate and orphaned pages."""
    seen: dict[str, list[dict[str, str]]] = {}
    for root in (CANONICAL_ROOT, LEGACY_ROOT):
        if not os.path.isdir(root):
            continue
        for path in walk_py(root):
            basename = os.path.basename(path)
            record = {"path": path, "hash": file_hash(path)}
            seen.setdefault(basename, []).append(record)
    duplicates = {name: items for name, items in seen.items() if len(items) > 1}

    all_files: set[str] = set()
    for root in (CANONICAL_ROOT, LEGACY_ROOT):
        if not os.path.isdir(root):
            continue
        for path in walk_py(root):
            all_files.add(path)

    seeds = [path for path in ENTRYPOINTS if os.path.exists(path)] + list(all_files)
    referenced: set[str] = set()
    for path in seeds:
        for target in collect_links([path]):
            resolved = resolve_target(target, all_files)
            if resolved:
                referenced.add(resolved)

    orphans = sorted(path for path in all_files if path not in referenced)

    report = {
        "canonical_root": CANONICAL_ROOT,
        "legacy_root": LEGACY_ROOT,
        "duplicates_by_basename": duplicates,
        "orphans": orphans,
        "entrypoints_present": [path for path in ENTRYPOINTS if os.path.exists(path)],
    }
    pathlib.Path("docs").mkdir(exist_ok=True)
    output = pathlib.Path("docs/pages_issues_report.json")
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        "Wrote docs/pages_issues_report.json.",
        "Dupes:",
        len(duplicates),
        "Orphans:",
        len(orphans),
    )


if __name__ == "__main__":
    main()
