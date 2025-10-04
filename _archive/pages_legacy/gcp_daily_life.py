"""Guided Care Plan - Daily Life & Support section."""
from __future__ import annotations



import streamlit as st

from guided_care_plan import ensure_gcp_session, get_question_meta, render_stepper
from senior_nav.components.choice_chips import choice_single
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope gcp">', unsafe_allow_html=True)


SECTION_QUESTIONS = [
    "who_for",
    "living_now",
    "caregiver_support",
    "adl_help",
]


def _ensure_widget_defaults(answers):
    for question_id in SECTION_QUESTIONS:
        meta = get_question_meta(question_id)
        options = [option["value"] for option in meta["options"]]
        default_value = answers.get(question_id) or options[0]
        if default_value not in options:
            default_value = options[0]
        st.session_state.setdefault(f"gcp_{question_id}", default_value)


def _render_radio(question_id: str) -> str:
    meta = get_question_meta(question_id)
    option_map = {opt["value"]: opt["label"] for opt in meta["options"]}
    values = list(option_map.keys())
    selected_value = st.session_state.get(f"gcp_{question_id}", values[0])
    if selected_value not in values:
        selected_value = values[0]
    with st.container(border=True):
        choice = choice_single(
            meta["label"],
            [(value, option_map[value]) for value in values],
            value=selected_value,
            key=f"gcp_{question_id}",
            help_text=meta.get("description"),
        )
        if meta.get("description"):
            st.caption(meta["description"])
    return choice


answers, _ = ensure_gcp_session()
_ensure_widget_defaults(answers)

st.title("Guided Care Plan — Daily Life & Support")
st.caption("Section 3 of 5")

render_stepper(3)

error_placeholder = st.empty()

with st.form("gcp_daily_life_form"):
    selections = {qid: _render_radio(qid) for qid in SECTION_QUESTIONS}
    submitted = st.form_submit_button("Continue to Health & Safety", type="primary")

if submitted:
    missing = [qid for qid, value in selections.items() if value is None]
    if missing:
        error_placeholder.error("Answer each question before moving on.")
    else:
        answers.update(selections)
        st.switch_page("ui/pages/gcp_health_safety.py")

if st.button("Back to financial questions"):
    st.switch_page("ui/pages/gcp.py")

st.markdown('</div>', unsafe_allow_html=True)