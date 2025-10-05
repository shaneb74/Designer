"""Care Planning Hub — PFMA-styled, no spacer bars"""
from __future__ import annotations
import streamlit as st

try:
    from ui.theme import inject_theme as _pfma_theme
except Exception:
    def _pfma_theme():
        st.markdown("<style>.block-container{max-width:1160px}</style>", unsafe_allow_html=True)

def _goto(path: str) -> None:
    try:
        st.switch_page(path)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = path
        st.experimental_rerun()

def _tile(*, icon: str, status: str, title: str, desc: str, cta: str, dest: str, key: str) -> None:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display:flex;flex-direction:column;gap:.5rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:1.4rem">{icon}</div>
                <div style="font-size:.9rem;color:var(--ink-muted)">{status}</div>
              </div>
              <h3 style="margin:0">{title}</h3>
              <p style="margin:.2rem 0 0;color:var(--ink-muted)">{desc}</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button(cta, type="secondary", use_container_width=True, key=key):
            _goto(dest)

def render_hub() -> None:
    _pfma_theme()
    st.set_page_config(page_title="Care Planning Hub", layout="wide")
    st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="display:flex;flex-direction:column;gap:.5rem;margin-bottom:1rem;">
          <div class="sn-hero-h1" style="font-size:2.0rem;">Care Planning Hub</div>
          <p style="margin:0;color:var(--ink-muted);font-size:1.02rem;">
            Start with the Guided Care Plan, then explore the Cost Planner, and connect with your advisor when ready.
          </p>
        </div>
        """, unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        _tile(
            icon="🧭",
            status="Start here",
            title="Guided Care Plan",
            desc="Answer step-by-step to understand needs, safety, and the right care setting.",
            cta="Begin plan",
            dest="pages/gcp.py",
            key="hub_gcp"
        )
    with c2:
        _tile(
            icon="💰",
            status="Optional",
            title="Cost Planner",
            desc="Estimate monthly care costs and see how income, benefits, and savings fit.",
            cta="Explore costs",
            dest="pages/cost_planner_v2/cost_planner_landing_v2.py",
            key="hub_cp"
        )
    with c3:
        _tile(
            icon="🤝",
            status="Next step",
            title="Plan for My Advisor",
            desc="Share your context so a concierge advisor can help map next moves.",
            cta="Connect now",
            dest="pages/pfma.py",
            key="hub_pfma"
        )

    st.markdown('</div>', unsafe_allow_html=True)

render_hub()
