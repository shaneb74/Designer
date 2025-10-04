"""Ensure there are no duplicate page filenames in the canonical tree."""

from __future__ import annotations

import os


def test_no_duplicate_page_basenames() -> None:
    root = "ui/pages"
    if not os.path.isdir(root):
        return
    names: dict[str, str] = {}
    for dirpath, _, files in os.walk(root):
        for filename in files:
            if filename.endswith(".py"):
                assert (
                    filename not in names
                ), f"Duplicate page filename: {filename} in {dirpath} and {names[filename]}"
                names[filename] = dirpath
