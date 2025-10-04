"""Guided Care Plan intro with financial context questions."""
from __future__ import annotations

import streamlit as st

from audiencing import (
    apply_audiencing_sanitizer,
    compute_audiencing_route,
    ensure_audiencing_state,
    snapshot_audiencing,
)
from guided_care_plan import ensure_gcp_session, render_stepper
from guided_care_plan.state import current_audiencing_snapshot
from ui.components import card_panel
from ui.theme import inject_theme


MEDICAID_OPTIONS = ("Yes", "No", "Unsure")
FUNDING_OPTIONS = ("No worries", "Confident", "Unsure", "Not confident")
MEDICAID_SESSION_KEY = "gcp_medicaid_choice"
FUNDING_SESSION_KEY = "gcp_funding_confidence"


def safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.rerun()


def _ensure_gate_state() -> dict[str, object]:
    return st.session_state.setdefault("gate", {})


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


def _persist_snapshot(state: dict[str, object]) -> None:
    apply_audiencing_sanitizer(state)
    compute_audiencing_route(state)
    snapshot = snapshot_audiencing(state)
    st.session_state["audiencing_snapshot"] = snapshot


def _persist_medicaid(state: dict[str, object], choice: str | None) -> None:
    qualifiers = state.setdefault("qualifiers", {})
    if choice == "Yes":
        qualifiers["on_medicaid"] = True
    elif choice in {"No", "Unsure"}:
        qualifiers["on_medicaid"] = False
    apply_audiencing_sanitizer(state)
    gate_state = _ensure_gate_state()
    gate_state["medicaid_offramp_shown"] = False


def _persist_gcp_context(choice: str | None, funding: str | None) -> None:
    _, gcp_state = ensure_gcp_session()
    if choice == "Yes":
        gcp_state["payment_context"] = "medicaid"
    elif choice in {"No", "Unsure"}:
        gcp_state["payment_context"] = "private" if choice == "No" else "unknown"

    if funding:
        gcp_state["funding_confidence"] = funding.lower().replace(" ", "_")
    elif funding is None:
        gcp_state["funding_confidence"] = None


def _render_funding_selector(current: str | None) -> str | None:
    st.markdown("**How confident do you feel about paying for care?**")
    cols = st.columns(len(FUNDING_OPTIONS), gap="small")
    selected = current
    for label, column in zip(FUNDING_OPTIONS, cols):
        with column:
            is_selected = selected == label
            pressed = st.button(
                label,
                key=f"funding_chip_{label.lower().replace(' ', '_')}",
                type="primary" if is_selected else "secondary",
                use_container_width=True,
            )
            if pressed:
                selected = None if is_selected else label
    return selected


def render_intro() -> None:
    inject_theme()
    st.set_page_config(page_title="Guided Care Plan", layout="centered")
    st.markdown('<div class="sn-scope gcp">', unsafe_allow_html=True)

    debug_flag = bool(st.session_state.get("dev_debug"))

    state = ensure_audiencing_state()
    answers, gcp_state = ensure_gcp_session()
    current_snapshot = current_audiencing_snapshot()
    care_context = _ensure_care_context()

    people = state.get("people", {}) or {}
    entry = state.get("entry")
    if entry == "self":
        person_name = people.get("recipient_name") or "you"
        possessive = "your"
    else:
        person_name = people.get("recipient_name") or "your loved one"
        possessive = "their"

    if MEDICAID_SESSION_KEY not in st.session_state:
        st.session_state[MEDICAID_SESSION_KEY] = None
    if FUNDING_SESSION_KEY not in st.session_state:
        st.session_state[FUNDING_SESSION_KEY] = None

    st.title("Guided Care Plan")
    st.caption("We'll gather context in five sections and build a DecisionTrace at the end.")
    render_stepper(0)

    with card_panel():
        st.markdown(
            f"""
            <div style="display:flex;flex-direction:column;gap:.4rem;">
                <div style="font-size:1.2rem;font-weight:600;color:var(--ink);">Financial context</div>
                <p style="margin:0;color:var(--ink-muted);">
                    Care options depend a lot on insurance. If {possessive} coverage includes Medicaid, we'll guide you to resources built for Medicaid families.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        medicaid_choice = st.radio(
            "Is your loved one currently on Medicaid?",
            options=MEDICAID_OPTIONS,
            index=None,
            key=MEDICAID_SESSION_KEY,
            horizontal=True,
            help="Medicaid is a state and federal program. If you're on it, your options and next steps are different. We'll point you to the right resources.",
        )

        _persist_medicaid(state, medicaid_choice)

        info_placeholder = st.empty()
        if medicaid_choice == "Yes":
            info_placeholder.info(
                "Because Medicaid changes the path, we'll highlight resources and keep the full plan available."
            )
        elif medicaid_choice == "Unsure":
            info_placeholder.info(
                "Medicaid is different from Medicare. Medicaid is needs-based and can cover long-term support; Medicare focuses on medical care."
            )

        funding_choice = None
        if medicaid_choice:
            current_funding = st.session_state.get(FUNDING_SESSION_KEY)
            funding_choice = _render_funding_selector(current_funding)
            st.session_state[FUNDING_SESSION_KEY] = funding_choice
        else:
            st.session_state[FUNDING_SESSION_KEY] = None

        _persist_gcp_context(medicaid_choice, funding_choice)

        st.markdown("<div class='sn-hr'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <p style="font-size:1rem;color:#475569;margin-bottom:0.6rem;">
                You're planning for <strong>{person_name.title()}</strong>. We'll guide you through daily life, health & safety, and preferences to recommend the right care setting.
            </p>
            <ul style="color:#475569;line-height:1.7;margin-left:1.2rem;">
                <li>Five sections with supportive, plain-language questions.</li>
                <li>Adapts to your answers and keeps everything in one DecisionTrace.</li>
                <li>Links directly to cost planning and advisor support when you're ready.</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

        start_disabled = medicaid_choice is None
        if st.button("Start Section 1", type="primary", use_container_width=True, disabled=start_disabled):
            _persist_snapshot(state)
            care_context["gcp_answers"] = answers
            st.session_state["gcp"] = gcp_state
            safe_switch_page("pages/gcp_daily_life.py")

        if st.button("Return to Hub", use_container_width=True):
            safe_switch_page("pages/hub.py")

    if debug_flag:
        with st.expander("Debug: GCP intro state", expanded=False):
            st.json(
                {
                    "answers": answers,
                    "gcp": gcp_state,
                    "audiencing": st.session_state.get("audiencing_snapshot", current_snapshot),
                    "medicaid_choice": medicaid_choice,
                    "funding_choice": funding_choice,
                }
            )

    st.markdown("</div>", unsafe_allow_html=True)


render_intro()

