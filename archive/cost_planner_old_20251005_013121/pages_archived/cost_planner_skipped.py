from __future__ import annotations


import streamlit as st
from ui.cost_planner_template import render_nav
from ui.theme import inject_theme
inject_theme()

from ui.cost_planner_template import (

    NavButton,
    apply_cost_planner_theme,
    cost_planner_page_container,
    render_app_header,
    render_nav_buttons,
    render_wizard_help,
    render_wizard_hero,
)


apply_cost_planner_theme()


def _debug_log(msg: str) -> None:
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass


_debug_log("LOADED: cost_planner_skipped.py")


if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "gcp_answers": {},
        "decision_trace": [],
        "planning_mode": "exploring",
        "care_flags": {},
    }


with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        "Skipped modules",
        "Review what you skipped and reopen them when you're ready.",
    )

    skipped_modules = ["Housing Path", "Benefits Check"]
    st.subheader("Skipped items")
    for module in skipped_modules:
        st.write(f"• {module}")

    render_wizard_help("You can revisit these modules any time from the Cost Planner dashboard.")

    clicked = render_nav([
            NavButton("Back to Evaluation", "skipped_back_evaluation"),
            NavButton("Revisit Modules", "skipped_revisit", type="primary"),
        ]
    )

    if clicked == "skipped_back_evaluation":
        st.switch_page("pages/cost_planner_evaluation.py")
    elif clicked == "skipped_revisit":
        st.switch_page("pages/cost_planner_modules.py")
