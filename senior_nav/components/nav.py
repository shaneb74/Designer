"""Navigation helpers for Streamlit multi-page experience."""
from __future__ import annotations

import streamlit as st


def safe_switch_page(target: str) -> None:
    """Navigate to ``target`` and fail fast if it cannot be found."""
    try:
        st.switch_page(target)
    except Exception:
        st.error(f"Page not found: {target}")
        raise
