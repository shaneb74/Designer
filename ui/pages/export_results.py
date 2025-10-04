"""Legacy shim that re-exports the canonical page from :mod:`pages` during migration."""
from __future__ import annotations

from pages.export_results import *  # type: ignore,F401,F403
