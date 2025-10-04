"""Runtime logging for rendered pages to protect legacy archiving."""
from __future__ import annotations

import inspect
import json
import pathlib
import time

_LOG_PATH = pathlib.Path("docs/rendered_pages.json")


def mark_render() -> None:
    """Record the ui/pages/*.py file that rendered, once per run segment."""
    try:
        for frame in inspect.stack():
            path = pathlib.Path(frame.filename).as_posix()
            if "/ui/pages/" in path:
                record = {"path": path, "ts": time.time()}
                try:
                    existing = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
                    if not isinstance(existing, list):
                        existing = []
                except Exception:
                    existing = []
                existing.append(record)
                _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
                _LOG_PATH.write_text(
                    json.dumps(existing, indent=2), encoding="utf-8"
                )
                break
    except Exception:
        pass
