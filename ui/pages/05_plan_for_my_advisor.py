"""Placeholder for the Plan for My Advisor page."""
from __future__ import annotations

import streamlit as st

from senior_nav.components import buttons
from senior_nav.components.nav import safe_switch_page

st.set_page_config(layout="wide")
buttons.page_start()

st.title("Plan for My Advisor")
st.info("Advisor plan UI will be implemented in a later milestone.")

with buttons.scope("link"):
    if buttons.secondary("Refresh", key="pfma_refresh"):
        st.rerun()

back_col, next_col = st.columns([1, 1])
with back_col:
    with buttons.variant("secondary"):
        if buttons.secondary("Back", key="pfma_back"):
            safe_switch_page("ui/pages/gcp_recommendation.py")
with next_col:
    if buttons.primary("Book Time with an Advisor", key="pfma_next"):
        st.info("Booking flow coming soon.")

buttons.page_end()
