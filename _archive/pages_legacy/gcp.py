"""Guided Care Plan intro with financial context questions."""
from __future__ import annotations

import streamlit as st

from audiencing import (
    apply_audiencing_sanitizer,
    compute_audiencing_route,
    ensure_audiencing_state,
    snapshot_audiencing,
)
from guided_care_plan import ensure_gcp_session, get_question_meta, render_stepper
from guided_care_plan.state import current_audiencing_snapshot
from senior_nav.components.choice_chips import choice_single
from ui.components import card_panel
from ui.theme import inject_theme

MEDICAID_SESSION_KEY = "gcp_medicaid_choice"
FUNDING_SESSION_KEY = "gcp_funding_confidence"


def safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()


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


def _question_config(question_id: str) -> tuple[dict[str, object], list[str], dict[str, str]]:
    meta = get_question_meta(question_id)
    option_map: dict[str, str] = {}
    values: list[str] = []
    for option in meta.get("options", []):
        if isinstance(option, dict):
            value = option.get("value")
            label = option.get("label", str(value))
        else:
            value = str(option)
            label = str(option)
        if value is None:
            continue
        values.append(value)
        option_map[value] = label
    return meta, values, option_map


def _persist_medicaid(state: dict[str, object], choice: str | None) -> None:
    qualifiers = state.setdefault("qualifiers", {})
    if choice == "yes":
        qualifiers["on_medicaid"] = True
    elif choice in {"no", "unsure"}:
        qualifiers["on_medicaid"] = False
    apply_audiencing_sanitizer(state)
    gate_state = _ensure_gate_state()
    gate_state["medicaid_offramp_shown"] = False

    context_state = st.session_state.setdefault("context", {})
    if choice is None:
        context_state.pop("medicaid_unsure_flag", None)
    else:
        context_state["medicaid_unsure_flag"] = choice == "unsure"


def _persist_gcp_context(choice: str | None, funding: str | None) -> None:
    _, gcp_state = ensure_gcp_session()
    if choice == "yes":
        gcp_state["payment_context"] = "medicaid"
    elif choice in {"no", "unsure"}:
        gcp_state["payment_context"] = "private"
    else:
        gcp_state.pop("payment_context", None)

    if funding:
        gcp_state["funding_confidence"] = funding
    elif funding is None:
        gcp_state["funding_confidence"] = None


def render_intro() -> None:
    inject_theme()
    st.set_page_config(page_title="Guided Care Plan", layout="centered")
    st.markdown('<div class="sn-scope gcp">', unsafe_allow_html=True)

    debug_flag = bool(st.session_state.get("dev_debug"))

    state = ensure_audiencing_state()
    answers, gcp_state = ensure_gcp_session()
    current_snapshot = current_audiencing_snapshot()
    care_context = _ensure_care_context()

    medicaid_meta, medicaid_values, medicaid_labels = _question_config("medicaid_status")
    funding_meta, funding_values, funding_labels = _question_config("funding_confidence")

    people = state.get("people", {}) or {}
    entry = state.get("entry")
    if entry == "self":
        person_name = people.get("recipient_name") or "you"
        possessive = "your"
    else:
        person_name = people.get("recipient_name") or "your loved one"
        possessive = "their"

    stored_medicaid = answers.get("medicaid_status")
    if stored_medicaid not in medicaid_values:
        stored_medicaid = None
    st.session_state.setdefault(MEDICAID_SESSION_KEY, stored_medicaid)
    if stored_medicaid is not None:
        st.session_state[MEDICAID_SESSION_KEY] = stored_medicaid

    stored_funding = answers.get("funding_confidence")
    if stored_funding not in funding_values:
        stored_funding = None
    st.session_state.setdefault(FUNDING_SESSION_KEY, stored_funding)
    if stored_funding is not None:
        st.session_state[FUNDING_SESSION_KEY] = stored_funding

    current_step = 1
    if stored_medicaid:
        current_step = 2

    st.title("Guided Care Plan")
    st.caption("We'll gather context in five sections and build a DecisionTrace at the end.")
    render_stepper(current_step)

    with card_panel():
        st.markdown(
            f"""
            <div style=\"display:flex;flex-direction:column;gap:.4rem;\">
                <div style=\"font-size:1.2rem;font-weight:600;color:var(--ink);\">Financial context</div>
                <p style=\"margin:0;color:var(--ink-muted);\">
                    Care options depend a lot on insurance. If {possessive} coverage includes Medicaid, we'll guide you to resources built for Medicaid families.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Section 1 — Financial Eligibility")
        medicaid_default = st.session_state.get(MEDICAID_SESSION_KEY)
        if medicaid_default not in medicaid_values:
            medicaid_default = medicaid_values[0]
        medicaid_choice = choice_single(
            medicaid_meta.get("label", "Are you currently on Medicaid?"),
            [(value, medicaid_labels.get(value, value)) for value in medicaid_values],
            value=medicaid_default,
            key=MEDICAID_SESSION_KEY,
            help_text=medicaid_meta.get("description"),
        )

        if medicaid_choice in medicaid_values:
            answers["medicaid_status"] = medicaid_choice
        else:
            answers.pop("medicaid_status", None)

        _persist_medicaid(state, medicaid_choice)

        info_placeholder = st.empty()
        helper_copy = medicaid_meta.get("helper_copy")
        if medicaid_choice == "yes":
            info_placeholder.info(
                "Because Medicaid changes the path, we'll highlight resources and keep the full plan available."
            )
        elif medicaid_choice == "unsure" and helper_copy:
            info_placeholder.info(helper_copy)
        else:
            info_placeholder.empty()

        funding_choice = None
        if medicaid_choice and medicaid_choice != "yes":
            st.markdown("### Section 2 — Financial Confidence")
            funding_default = st.session_state.get(FUNDING_SESSION_KEY)
            if funding_default not in funding_values:
                funding_default = funding_values[0]
            funding_choice = choice_single(
                funding_meta.get(
                    "label", "How confident do you feel about paying for care?"
                ),
                [(value, funding_labels.get(value, value)) for value in funding_values],
                value=funding_default,
                key=FUNDING_SESSION_KEY,
                help_text=funding_meta.get("description"),
            )
            if funding_choice in funding_values:
                answers["funding_confidence"] = funding_choice
            else:
                answers.pop("funding_confidence", None)
        else:
            answers.pop("funding_confidence", None)
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

        start_disabled = medicaid_choice is None or (
            medicaid_choice != "yes" and not funding_choice
        )
        if st.button(
            "Continue to Daily Life & Support",
            type="primary",
            use_container_width=True,
            disabled=start_disabled,
        ):
            _persist_snapshot(state)
            care_context["gcp_answers"] = answers
            st.session_state["gcp"] = gcp_state
            safe_switch_page("ui/pages/gcp_daily_life.py")

        if st.button("Return to Hub", use_container_width=True):
            safe_switch_page("ui/pages/hub.py")

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

