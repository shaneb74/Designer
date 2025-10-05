from __future__ import annotations
import streamlit as st
from ui.pfma import apply_pfma_theme, render_drawer

apply_pfma_theme()

def _body(_):
    st.metric("Monthly All-In", "$—")
    st.metric("Income + Benefits", "$—")
    st.metric("Monthly Gap", "$—")
    st.metric("Runway", "—")
    st.info("This is the final results page. We’ll compute after modules are filled.")
    return {"ok": True}

res = render_drawer(
    step_key="timeline",
    title="Your Money Timeline",
    badge="Results",
    description="Here’s how long your money lasts at the current settings.",
    body=_body,
)
if res.ok:
    if st.button("Expert Review", type="primary"):
        st.switch_page("pages/expert_review.py")
