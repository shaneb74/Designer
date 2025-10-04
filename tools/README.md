# Tools

This folder contains small maintenance utilities used by pre-commit and local dev.

## Scripts

- `sanitize_ascii.py` - replaces smart quotes, em dashes, NBSP, zero‑width chars.
- `check_future_imports.py` - verifies `from __future__ import annotations` is right after the module docstring (or top) and before other imports.
- `fix_future_imports.py` - auto-moves that import to the correct position.
- `compile_pages.py` - compiles `pages/*.py` to catch syntax errors quickly.
- `dead_imports.py` - AST-based detector for unused imports.
- `lint.py` - lightweight linter (tabs, long lines, trailing spaces, final newline, mixed line endings).
- `fix_scopes.py` / `finish_scope_insertion.py` - placeholders kept for future theming migrations.

## Typical usage

```bash
python3 tools/sanitize_ascii.py --write
python3 tools/check_future_imports.py
python3 tools/fix_future_imports.py
python3 tools/compile_pages.py
python3 tools/dead_imports.py
python3 tools/lint.py
```

## Pre-commit

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: sanitize-ascii
        name: Sanitize ASCII punctuation
        entry: python3 tools/sanitize_ascii.py --ext .py --write
        language: system
        types: [python]
        pass_filenames: false

      - id: check-future-imports
        name: Check __future__ import placement
        entry: python3 tools/check_future_imports.py
        language: system
        types: [python]
        pass_filenames: false

      - id: compile-pages
        name: Compile pages/*.py
        entry: python3 tools/compile_pages.py
        language: system
        types: [python]
        pass_filenames: false
```
