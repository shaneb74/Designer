"""Medicaid off-ramp page with curated resource links."""
from __future__ import annotations

import streamlit as st

from ui.components import card_panel
from ui.theme import inject_theme


inject_theme()
st.set_page_config(page_title="Medicaid Resources", layout="centered")
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

with card_panel():
    st.markdown(
        """
        <div class="sn-hero-h1" style="margin-bottom:.4rem;">Medicaid Resources for Your Loved One</div>
        <p style="margin:0;color:var(--ink-muted);font-size:1.05rem;">
          Because your loved one is on Medicaid, there are special programs and benefits you may qualify for.
          Medicaid has federally and state-supported options that can help with senior living, long-term care, and related services.
          While our direct resources are limited in this area, we've included information and links to trusted organizations that can guide you to the right support.
        </p>
        """,
        unsafe_allow_html=True,
    )

    resources = [
        ("State Medicaid Office", "Visit State Directory →"),
        ("Area Agencies on Aging", "Find an Agency →"),
        ("National Council on Aging", "Explore Resources →"),
        ("Community Health Centers", "Search Centers →"),
    ]

    cols = st.columns(2, gap="large")
    for idx, (title, cta) in enumerate(resources):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="sn-field-card" style="display:flex;flex-direction:column;gap:.5rem;min-height:150px;">
                    <div style="font-weight:700;color:var(--ink);font-size:1.05rem;">{title}</div>
                    <a href="#" target="_blank" style="font-weight:600;">{cta}</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='sn-hr'></div>", unsafe_allow_html=True)

    st.link_button("Explore Resources", "#", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
