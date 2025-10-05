"""Housing drawer for the Cost Planner."""
from __future__ import annotations

import streamlit as st
from ui.cost_planner_template import render_nav
from ui.theme import inject_theme

from cost_planner_shared import ensure_core_state, format_currency, get_numeric, recompute_costs, set_numeric
inject_theme()

from ui.cost_planner_template import (

    Metric,
    NavButton,
    apply_cost_planner_theme,
    cost_planner_page_container,
    render_app_header,
    render_metrics,
    render_nav_buttons,
    render_suggestion,
    render_wizard_help,
    render_wizard_hero,
)


apply_cost_planner_theme()


ensure_core_state()
cp = st.session_state["cost_planner"]
aud = st.session_state["audiencing"]
quals = aud.get("qualifiers", {})


with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        "Housing and living costs",
        "Capture recurring housing payments before care or benefits.",
    )

    if not quals.get("owns_home"):
        render_suggestion(
            "Audiencing shows this household does not own a home. Home maintenance fields are hidden and treated as $0.",
            tone="info",
        )

    base_rent = st.number_input(
        "Monthly housing cost (rent, mortgage, or community fee)",
        min_value=0.0,
        step=50.0,
        value=float(get_numeric("housing_base_rent")),
        help="Include rent, mortgage, or assisted living base fees.",
    )
    set_numeric("housing_base_rent", base_rent)

    col_a, col_b = st.columns(2)
    with col_a:
        utilities = st.number_input(
            "Utilities & services",
            min_value=0.0,
            step=25.0,
            value=float(get_numeric("housing_utilities")),
            help="Electric, water, trash, cable, HOA dues.",
        )
        set_numeric("housing_utilities", utilities)

    with col_b:
        if quals.get("owns_home"):
            maintenance = st.number_input(
                "Maintenance or HOA",
                min_value=0.0,
                step=25.0,
                value=float(get_numeric("housing_maintenance")),
                help="Repairs, lawn care, or HOA assessments.",
            )
            set_numeric("housing_maintenance", maintenance)
        else:
            set_numeric("housing_maintenance", 0.0)

    recompute_costs()

    render_metrics(
        [
            Metric("Housing subtotal", format_currency(cp["subtotals"]["housing"]))
        ]
    )

    render_wizard_help("Include rent, mortgage, or assisted living base fees when estimating housing.")

    clicked = render_nav([
            NavButton("Return to Hub", "housing_back_hub"),
            NavButton("Back to Intro", "housing_back_intro"),
            NavButton("Next: Care", "housing_next_care", type="primary"),
        ]
    )

    if clicked == "housing_back_hub":
        st.switch_page("pages/hub.py")
    elif clicked == "housing_back_intro":
        st.switch_page("pages/cost_planner_estimate.py")
    elif clicked == "housing_next_care":
        st.switch_page("pages/cost_planner_home_care.py")
