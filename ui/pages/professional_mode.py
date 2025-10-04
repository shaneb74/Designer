"""Legacy shim that re-exports the canonical page from :mod:`pages` during migration."""
from __future__ import annotations

from pages.professional_mode import *  # type: ignore,F401,F403
