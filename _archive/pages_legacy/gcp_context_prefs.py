"""Guided Care Plan - Context & Preferences section."""
from __future__ import annotations

import streamlit as st

from guided_care_plan import ensure_gcp_session, get_question_meta, render_stepper
from senior_nav.components.choice_chips import choice_multi, normalize_none
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope gcp">', unsafe_allow_html=True)

SECTION_QUESTIONS = ["chronic", "preferences"]
NONE_EXCLUSIVE = {"chronic"}


def _ensure_widget_defaults(answers):
    for question_id in SECTION_QUESTIONS:
        default_value = answers.get(question_id) or []
        st.session_state.setdefault(f"gcp_{question_id}", list(default_value))


def _render_multiselect(question_id: str) -> list[str]:
    meta = get_question_meta(question_id)
    options = meta.get("options", [])
    option_map = {opt["value"]: opt.get("label", opt["value"]) for opt in options}
    values = list(option_map.keys())
    default = st.session_state.get(f"gcp_{question_id}", [])
    with st.container(border=True):
        selections = choice_multi(
            meta.get("label", question_id.replace("_", " ").title()),
            [(value, option_map.get(value, value)) for value in values],
            values=default,
            key=f"gcp_{question_id}",
        )
        if meta.get("description"):
            st.caption(meta["description"])
    return list(selections)


answers, _ = ensure_gcp_session()
_ensure_widget_defaults(answers)

st.title("Guided Care Plan — Context & Preferences")
st.caption("Section 5 of 5")

render_stepper(5)

with st.form("gcp_context_form"):
    selections = {qid: _render_multiselect(qid) for qid in SECTION_QUESTIONS}
    submitted = st.form_submit_button("Review recommendation", type="primary")

if submitted:
    processed = {}
    for qid, value in selections.items():
        processed[qid] = normalize_none(list(value or [])) if qid in NONE_EXCLUSIVE else list(value or [])
    for qid, value in processed.items():
        st.session_state[f"gcp_{qid}"] = list(value)
    answers.update(processed)
    st.switch_page("ui/pages/gcp_recommendation.py")

if st.button("Back to Health & Safety"):
    st.switch_page("ui/pages/gcp_health_safety.py")

st.markdown('</div>', unsafe_allow_html=True)
