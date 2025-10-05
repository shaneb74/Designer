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

if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "gcp_answers": {},
        "decision_trace": [],
        "planning_mode": "estimating",
        "care_flags": {},
        "person_name": "Your Loved One",
    }

ctx = st.session_state.care_context
person_name = ctx.get("person_name", "Your Loved One")


with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        f"Cost Planner for {person_name}",
        "Choose the level of detail that fits your needs right now.",
    )

    st.markdown(
        """
Families can start light and go deeper when they're ready. Pick the path
that best fits the decisions you're making today. You can always return
to switch modes later.

- **Estimate Costs** - quick, high-level monthly estimate using a few
  selections.
- **Plan Costs** - full planning workflow with modules, offsets, and
  runway tracking.
"""
    )

    render_wizard_help(
        "You can switch between estimating and planning. We'll remember your progress in each path.",
    )

    clicked = render_nav([
            NavButton("Estimate Costs", "cp_estimate", type="primary"),
            NavButton("Plan Costs", "cp_plan", type="primary"),
            NavButton("Back to Hub", "cp_back_hub"),
        ]
    )

    if clicked == "cp_estimate":
        ctx["planning_mode"] = "estimating"
        st.switch_page("pages/cost_planner_estimate.py")
    elif clicked == "cp_plan":
        ctx["planning_mode"] = "planning"
        st.switch_page("pages/cost_planner_estimate.py")
    elif clicked == "cp_back_hub":
        st.switch_page("pages/hub.py")
