#!/usr/bin/env python3
"""Archive safe legacy pages into the _archive/pages_legacy directory."""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import sys

ARCHIVE_DIR = pathlib.Path("_archive/pages_legacy")


def load_rendered() -> set[str]:
    """Load runtime-rendered page paths from the log file."""
    log_path = pathlib.Path("docs/rendered_pages.json")
    if not log_path.exists():
        return set()
    try:
        entries = json.loads(log_path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    rendered: set[str] = set()
    for entry in entries:
        path = entry.get("path") if isinstance(entry, dict) else None
        if path:
            rendered.add(path)
    return rendered


def main() -> None:
    """Move eligible legacy pages into the archive directory."""
    issues_path = pathlib.Path("docs/pages_issues_report.json")
    if not issues_path.exists():
        print("Run tools/find_pages_issues.py first.")
        sys.exit(1)

    data = json.loads(issues_path.read_text(encoding="utf-8"))
    duplicates = data.get("duplicates_by_basename", {})
    orphans = set(data.get("orphans", []))

    rendered = load_rendered()
    to_archive: set[str] = set()

    for entries in duplicates.values():
        for record in entries:
            path = record.get("path")
            if isinstance(path, str) and path.startswith("pages/") and path not in rendered:
                to_archive.add(path)

    for path in orphans:
        if path.startswith("pages/") and path not in rendered:
            to_archive.add(path)

    if not to_archive:
        print("Nothing to archive.")
        return

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(to_archive):
        destination = ARCHIVE_DIR / pathlib.Path(path).name
        print(f"Archiving {path} -> {destination}")
        shutil.move(path, destination)

    print("Done. Review git status, run the app, and commit the changes.")


if __name__ == "__main__":
    main()
