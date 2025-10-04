"""Navigation helpers for Streamlit multi-page experience."""
from __future__ import annotations

import streamlit as st


def safe_switch_page(target: str) -> None:
    """Attempt to navigate using ``st.switch_page`` with a graceful fallback."""
    candidates = [target]
    if target.startswith("ui/pages/"):
        candidates.append(target.replace("ui/pages/", "pages/"))
    elif target.startswith("pages/"):
        candidates.append(target.replace("pages/", "ui/pages/"))

    for candidate in candidates:
        try:
            st.switch_page(candidate)
            return
        except Exception:
            pass

    st.session_state["next_page"] = candidates[0]
    st.error(f"Couldn't find page: {candidates[0]}. Check registered pages.")
    st.experimental_rerun()
