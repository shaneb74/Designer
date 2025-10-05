"""Cost Planner v2 — PFMA-styled module stub."""
from __future__ import annotations

import streamlit as st

try:
    from ui.pfma import apply_pfma_theme
except Exception:
    def apply_pfma_theme():
        st.markdown("""
        <style>
          :root{
            --brand:#0B5CD8; --paper:#ffffff; --surface:#f6f8fa;
            --ink:#111418; --ink-muted:#6b7280; --radius:14px;
          }
          .block-container{max-width:1160px;padding-top:8px;}
          .pfma-card{
            background: var(--surface);
            border: 1px solid rgba(0,0,0,.08);
            border-radius: var(--radius);
            padding: clamp(1rem, 2vw, 1.5rem);
          }
          .pfma-note{font-size:.9rem;color:var(--ink-muted);margin:.25rem 0 0;}
        </style>
        """, unsafe_allow_html=True)

apply_pfma_theme()

st.title('Cost Planner · Caregiver Support (v2)')
st.markdown("""<div class='pfma-card'>
  <h3>Who’ll help with in-home care?</h3>
  <p class='pfma-note'>Optional but helpful for in-home care with high needs. Adds caregiver_cost to monthly all-in.</p>
</div>""", unsafe_allow_html=True)
st.info('TODO: inputs for caregiver_type, include_caregiver_cost, caregiver_cost (default 3600 if included).')
