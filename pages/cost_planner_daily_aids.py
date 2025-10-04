"""Medical and daily aids drawer."""
from __future__ import annotations

import streamlit as st

from cost_planner_shared import ensure_core_state, format_currency, get_numeric, recompute_costs, set_numeric
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
gcp = st.session_state.get("gcp", {})


with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        "Medical and daily living aids",
        "Capture medication costs, supplies, and transport to appointments.",
    )

    chronic = gcp.get("chronic_conditions", [])
    if chronic:
        render_suggestion(
            "Chronic conditions noted in the Guided Care Plan: " + ", ".join(chronic),
            tone="info",
        )

    rx = st.number_input(
        "Prescription medications",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("medical_prescriptions")),
        help="Monthly prescription spending across retail and mail order.",
    )
    set_numeric("medical_prescriptions", rx)

    supplies = st.number_input(
        "Medical supplies & equipment",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("medical_supplies")),
        help="Incontinence products, DME rentals, batteries, and similar.",
    )
    set_numeric("medical_supplies", supplies)

    transport = st.number_input(
        "Medical transportation",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("medical_transport")),
        help="Ambulance subscriptions, paratransit, or rides to medical appointments.",
    )
    set_numeric("medical_transport", transport)

    recompute_costs()

    render_metrics(
        [
            Metric("Medical subtotal", format_currency(cp["subtotals"]["medical"]))
        ]
    )

    render_wizard_help("Capture recurring prescriptions separately from one-time equipment purchases.")

    clicked = render_nav_buttons(
        [
            NavButton("Return to Hub", "medical_back_hub"),
            NavButton("Back: Care", "medical_back_care"),
            NavButton("Next: Insurance", "medical_next_insurance", type="primary"),
        ]
    )

    if clicked == "medical_back_hub":
        st.switch_page("ui/pages/hub.py")
    elif clicked == "medical_back_care":
        st.switch_page("ui/pages/cost_planner_home_care.py")
    elif clicked == "medical_next_insurance":
        st.switch_page("ui/pages/cost_planner_benefits.py")