# Cost Planner v2 · Landing
from __future__ import annotations

import streamlit as st

# If you want the PFMA look & feel on CPv2 pages:
try:
    # These helpers exist in your project; if not, you can remove this block safely.
    from ui.pfma import apply_pfma_theme
    apply_pfma_theme()
except Exception:
    pass

st.markdown(
    """
    <div class="pfma-card">
      <h3>Cost Planner</h3>
      <p class="pfma-note">
        A simple, conversational way to estimate care costs or plan your budget in detail.
        You can start light and add more later.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pfma-card" style="margin-top:0.75rem">
      <h4 style="margin:0 0 .25rem 0;">How do you want to start?</h4>
      <ul style="margin:.25rem 0 0 1rem;">
        <li><b>Estimate</b> — quick monthly care cost using a few inputs (pulls from Guided Care Plan if available).</li>
        <li><b>Plan</b> — detailed modules (income, expenses, benefits, home, assets) to see your runway.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 1])

with col1:
    # This is the one you asked about — it sends people to the CPv2 Modules Hub
    if st.button("Start planning", type="primary", use_container_width=True):
        st.switch_page("pages/cost_planner_v2/cost_planner_modules_hub_v2.py")

with col2:
    # Optional: quick peek at the results page (useful during development)
    if st.button("Jump to Timeline (dev)", use_container_width=True):
        st.switch_page("pages/cost_planner_v2/cost_planner_timeline_v2.py")