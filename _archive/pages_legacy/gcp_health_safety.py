"""Guided Care Plan - Health & Safety section."""
from __future__ import annotations



import streamlit as st

from guided_care_plan import ensure_gcp_session, get_question_meta, render_stepper
from guided_care_plan.state import current_audiencing_snapshot
from senior_nav.components.choice_chips import choice_multi, choice_single, normalize_none
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope gcp">', unsafe_allow_html=True)


SECTION_QUESTIONS = [
    "cognition",
    "behavior_risks",
    "falls",
    "med_mgmt",
    "home_safety",
    "supervision",
]

MULTI_QUESTIONS = {"behavior_risks"}


def _ensure_widget_defaults(answers):
    for question_id in SECTION_QUESTIONS:
        meta = get_question_meta(question_id)
        options = [option["value"] for option in meta["options"]]
        if question_id in MULTI_QUESTIONS:
            default_value = answers.get(question_id) or []
            st.session_state.setdefault(f"gcp_{question_id}", list(default_value))
        else:
            default_value = answers.get(question_id) or options[0]
            if default_value not in options:
                default_value = options[0]
            st.session_state.setdefault(f"gcp_{question_id}", default_value)


def _render_question(question_id: str, owns_home: bool | None):
    meta = get_question_meta(question_id).copy()
    if question_id == "home_safety" and owns_home is False:
        meta = dict(meta)
        meta["label"] = "Is their living setup safe?"

    options = meta.get("options", [])
    option_map = {opt["value"]: opt.get("label", opt["value"]) for opt in options}
    values = list(option_map.keys())

    with st.container(border=True):
        if question_id in MULTI_QUESTIONS:
            default = st.session_state.get(f"gcp_{question_id}", [])
            if not isinstance(default, list):
                default = list(default or [])
            choice = choice_multi(
                meta.get("label", question_id.replace("_", " ").title()),
                [(value, option_map.get(value, value)) for value in values],
                values=default,
                key=f"gcp_{question_id}",
            )
            if meta.get("description"):
                st.caption(meta["description"])
        else:
            selected_value = st.session_state.get(f"gcp_{question_id}", values[0])
            if selected_value not in values:
                selected_value = values[0]
            choice = choice_single(
                meta.get("label", question_id.replace("_", " ").title()),
                [(value, option_map.get(value, value)) for value in values],
                value=selected_value,
                key=f"gcp_{question_id}",
                help_text=meta.get("description"),
            )
    return choice


answers, _ = ensure_gcp_session()
snapshot = current_audiencing_snapshot()
owns_home = snapshot.get("qualifiers", {}).get("owns_home")

_ensure_widget_defaults(answers)

st.title("Guided Care Plan — Health & Safety")
st.caption("Section 4 of 5")

render_stepper(4)

error_placeholder = st.empty()

with st.form("gcp_health_safety_form"):
    selections = {qid: _render_question(qid, owns_home) for qid in SECTION_QUESTIONS}
    submitted = st.form_submit_button("Continue to Context & Preferences", type="primary")

if submitted:
    processed = {}
    missing = []
    for qid, value in selections.items():
        if qid in MULTI_QUESTIONS:
            processed[qid] = normalize_none(list(value or []))
        else:
            if value is None:
                missing.append(qid)
            processed[qid] = value
    if missing:
        error_placeholder.error("Answer each question before moving on.")
    else:
        for qid, value in processed.items():
            if qid in MULTI_QUESTIONS:
                st.session_state[f"gcp_{qid}"] = list(value)
        answers.update(processed)
        st.switch_page("ui/pages/gcp_context_prefs.py")

if st.button("Back to Daily Life & Support"):
    st.switch_page("ui/pages/gcp_daily_life.py")

st.markdown('</div>', unsafe_allow_html=True)