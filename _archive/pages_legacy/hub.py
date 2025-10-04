"""Care Planning Hub with three primary navigation tiles."""
from __future__ import annotations

import streamlit as st

from audiencing import apply_audiencing_sanitizer, ensure_audiencing_state, snapshot_audiencing
from ui.components import card_panel
from ui.theme import inject_theme


def safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()


def _ensure_care_context() -> dict[str, object]:
    return st.session_state.setdefault(
        "care_context",
        {
            "person_name": "Your Loved One",
            "gcp_answers": {},
            "gcp_recommendation": None,
            "gcp_cost": None,
        },
    )


def _determine_gcp_status() -> tuple[str, str, str]:
    answers = st.session_state.get("gcp_answers", {})
    gcp_state = st.session_state.get("gcp", {})
    recommendation = gcp_state.get("recommended_setting")

    if recommendation:
        return "✔ Complete", "Open summary", "primary"
    if answers:
        return "In progress", "Resume plan", "primary"
    return "Start here", "Begin plan", "primary"


def _determine_cost_status() -> tuple[str, str]:
    cost_planner = st.session_state.get("cost_planner", {})
    monthly_total = cost_planner.get("monthly_total")
    if monthly_total:
        return "In progress", "Review costs"
    return "Optional", "Explore costs"


def _determine_pfma_status() -> tuple[str, str]:
    pfma = st.session_state.get("pfma", {})
    if pfma.get("appointment_booked"):
        return "Scheduled", "View details"
    return "Next step", "Connect now"


def _render_tile(
    *,
    icon: str,
    title: str,
    description: str,
    status_label: str,
    cta_label: str,
    cta_kind: str,
    destination: str,
) -> None:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display:flex;flex-direction:column;gap:.8rem;min-height:220px;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <h3 style="margin:0;">{title}</h3>
                    <span style="font-size:0.85rem;color:var(--ink-muted);">{status_label}</span>
                </div>
                <p style="margin:0;color:var(--ink-muted);">{description}</p>
                <div style="margin-top:auto;">
                    {""}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(cta_label, type=cta_kind, use_container_width=True, key=f"hub_{destination}"):
            safe_switch_page(destination)


def render_hub() -> None:
    inject_theme()
    st.set_page_config(page_title="Care Planning Hub", layout="wide")
    st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    debug_flag = bool(st.session_state.get("dev_debug"))

    state = ensure_audiencing_state()
    apply_audiencing_sanitizer(state)
    snapshot = snapshot_audiencing(state)
    st.session_state["audiencing_snapshot"] = snapshot

    care_context = _ensure_care_context()
    person_name = care_context.get("person_name", "Your Loved One")

    with card_panel(padding="clamp(1.6rem, 3vw, 2.2rem)", gap="1.6rem"):
        st.markdown(
            f"""
            <div style="display:flex;flex-direction:column;gap:.5rem;">
                <div class="sn-hero-h1" style="font-size:2.2rem;">Care Planning Hub</div>
                <p style="margin:0;color:var(--ink-muted);font-size:1.05rem;">
                    This is your home base. Start with the Guided Care Plan, then explore cost planning and
                    advisor support when you're ready. Everything adapts as you learn more about {person_name}.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        gcp_status, gcp_cta, gcp_kind = _determine_gcp_status()
        cost_status, cost_cta = _determine_cost_status()
        pfma_status, pfma_cta = _determine_pfma_status()

        cols = st.columns(3, gap="large")
        with cols[0]:
            _render_tile(
                icon="🧭",
                title="Guided Care Plan",
                description="Answer step-by-step questions to understand needs, safety, and the best care setting.",
                status_label=gcp_status,
                cta_label=gcp_cta,
                cta_kind=gcp_kind,
                destination="pages/gcp.py",
            )
        with cols[1]:
            _render_tile(
                icon="💰",
                title="Cost Planner",
                description="Estimate monthly costs, compare scenarios, and see how benefits or savings play a role.",
                status_label=cost_status,
                cta_label=cost_cta,
                cta_kind="secondary",
                destination="pages/cost_planner.py",
            )
        with cols[2]:
            _render_tile(
                icon="🤝",
                title="Plan for My Advisor",
                description="Share your context with a concierge advisor who can help map the next moves.",
                status_label=pfma_status,
                cta_label=pfma_cta,
                cta_kind="secondary",
                destination="pages/pfma.py",
            )

    if debug_flag:
        with st.expander("Debug: Hub state", expanded=False):
            st.json(
                {
                    "audiencing": state,
                    "snapshot": snapshot,
                    "care_context": care_context,
                    "gcp": st.session_state.get("gcp", {}),
                    "cost_planner": st.session_state.get("cost_planner", {}),
                }
            )

    st.markdown("</div>", unsafe_allow_html=True)


render_hub()

