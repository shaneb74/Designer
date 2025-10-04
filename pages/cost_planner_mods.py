
from __future__ import annotations

import streamlit as st

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


_debug_log("LOADED: cost_planner_mods.py")


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
        "Age-in-place upgrades",
        "Capture accessibility improvements that keep the home safe and comfortable.",
    )

    st.subheader("Upgrade options")
    grab_bars = st.checkbox("Grab bars and bathroom supports")
    stair_lift = st.checkbox("Stair lift or ramp installation")
    lighting = st.checkbox("Smart lighting and fall prevention sensors")

    selected = [
        label
        for label, checked in [
            ("Grab bars", grab_bars),
            ("Stair lift", stair_lift),
            ("Smart lighting", lighting),
        ]
        if checked
    ]

    if selected:
        render_wizard_help(
            "We'll translate selected upgrades into estimated project budgets during implementation.",
        )
    else:
        render_wizard_help("Not ready to choose upgrades? You can revisit this later.")

    clicked = render_nav_buttons(
        [
            NavButton("Back to Modules", "mods_back_modules"),
            NavButton("Next Option", "mods_next_option", type="primary"),
        ]
    )

    if clicked == "mods_back_modules":
        st.switch_page("ui/pages/cost_planner_modules.py")
    elif clicked == "mods_next_option":
        st.switch_page("ui/pages/cost_planner_skipped.py")