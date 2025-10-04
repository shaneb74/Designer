"""Bridge page that welcomes users based on their entry role."""
from __future__ import annotations

import streamlit as st

from audiencing import ensure_audiencing_state, snapshot_audiencing
from ui.components import card_panel
from ui.theme import inject_theme


ENTRY_COPY = {
    "self": {
        "headline": "Welcome, let's walk through a plan together",
        "body": (
            "We'll start with a few questions to understand your care needs and how you"
            " feel about covering the costs. Then we'll craft a roadmap you can revisit"
            " anytime."
        ),
        "accent": "We'll focus on what matters most for you-clarity, confidence, and next steps.",
    },
    "proxy": {
        "headline": "We're here to support you and your loved one",
        "body": (
            "First we'll learn a bit about their needs and your comfort with planning."
            " From there, we'll recommend options and resources to help you feel ready."
        ),
        "accent": "We're alongside you with guidance that keeps family conversations warm and grounded.",
    },
    "pro": {
        "headline": "Let's prepare a plan you can share",
        "body": (
            "We'll gather context quickly, then assemble guidance you can review with the"
            " families you support. Everything stays clear, actionable, and advisor-friendly."
        ),
        "accent": "Keep it collaborative-tailor the plan and export highlights whenever you need.",
    },
}


def safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()


def _ensure_care_context() -> dict[str, object]:
    return st.session_state.setdefault(
        "care_context",
        {"person_name": "Your Loved One", "gcp_answers": {}, "gcp_recommendation": None},
    )


def _render_cards(accent: str) -> None:
    columns = st.columns(3, gap="large")
    card_specs = (
        {
            "title": "Personalized guidance",
            "copy": "Answer a few context questions and we'll highlight the first moves to make.",
        },
        {
            "title": "Care Planning Hub",
            "copy": "Navigate between the Guided Care Plan, Cost Planner, and Advisor handoff easily.",
        },
        {
            "title": "Ready for handoff",
            "copy": accent,
        },
    )

    for column, spec in zip(columns, card_specs):
        with column:
            with st.container(border=True):
                st.markdown(f"**{spec['title']}**")
                st.caption(spec["copy"])


def render_contextual_welcome() -> None:
    inject_theme()
    st.set_page_config(page_title="Welcome to your Care Planning Hub", layout="centered")
    st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    debug_flag = bool(st.session_state.get("dev_debug"))

    state = ensure_audiencing_state()
    entry = state.get("entry") or "proxy"
    copy = ENTRY_COPY.get(entry, ENTRY_COPY["proxy"])

    _ensure_care_context()

    with card_panel():
        st.markdown(
            f"""
            <div class="sn-hero-h1" style="margin-bottom:.4rem;">{copy['headline']}</div>
            <p style="margin:0;color:var(--ink-muted);font-size:1.05rem;">{copy['body']}</p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='sn-hr'></div>", unsafe_allow_html=True)

        _render_cards(copy["accent"])

        st.markdown("<div class='sn-hr'></div>", unsafe_allow_html=True)

        cta_col, helper_col = st.columns([2, 1])
        with cta_col:
            if st.button(
                "Continue to Care Planning Hub →",
                type="primary",
                use_container_width=True,
            ):
                safe_switch_page("pages/hub.py")
        with helper_col:
            st.caption(
                "What is the Care Planning Hub? It's your home base for guided plans, cost tools, and advisor handoffs."
            )

    if debug_flag:
        with st.expander("Debug: Contextual welcome", expanded=False):
            st.json({
                "audiencing": state,
                "snapshot": st.session_state.get("audiencing_snapshot", snapshot_audiencing(state)),
            })

    st.markdown("</div>", unsafe_allow_html=True)


render_contextual_welcome()

