"""Care drawer for Cost Planner."""
from __future__ import annotations

import streamlit as st

from cost_planner_shared import (
    ensure_core_state,
    format_currency,
    get_numeric,
    recompute_costs,
    set_numeric,
)
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
gcp = st.session_state.get("gcp", {})
quals = aud.get("qualifiers", {})


with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        "Care staffing and services",
        "Estimate care staffing, second person support, and supplemental services.",
    )

    recommended = gcp.get("recommended_setting")
    if recommended:
        render_suggestion(
            f"Guided Care Plan suggested {recommended.title()} with {gcp.get('care_intensity', 'unknown')} care intensity.",
            tone="info",
        )

    base_rate = st.number_input(
        "Primary care or staffing cost",
        min_value=0.0,
        step=50.0,
        value=float(get_numeric("care_base_rate")),
        help="Monthly base rate for in-home staffing or community care.",
    )
    set_numeric("care_base_rate", base_rate)

    col_left, col_right = st.columns(2)
    with col_left:
        addon = st.number_input(
            "Level-of-care add-ons",
            min_value=0.0,
            step=25.0,
            value=float(get_numeric("care_level_addon")),
            help="Medication management, behavior support, or acuity fees.",
        )
        set_numeric("care_level_addon", addon)

    with col_right:
        supplemental = st.number_input(
            "Supplemental support services",
            min_value=0.0,
            step=25.0,
            value=float(get_numeric("care_support_services")),
            help="Adult day, respite, transportation, or wellness memberships.",
        )
        set_numeric("care_support_services", supplemental)

    if cp.get("household") == "split" and quals.get("has_partner"):
        second_person = st.number_input(
            "Second person care add-on",
            min_value=0.0,
            step=25.0,
            value=float(get_numeric("care_second_person")),
            help="Care costs for a partner or second person in the household.",
        )
        set_numeric("care_second_person", second_person)
    else:
        set_numeric("care_second_person", 0.0)

    recompute_costs()

    render_metrics(
        [
            Metric("Care subtotal", format_currency(cp["subtotals"]["care"]))
        ]
    )

    render_wizard_help("Capture all ongoing staffing commitments before layering on medical costs.")

    clicked = render_nav_buttons(
        [
            NavButton("Return to Hub", "care_back_hub"),
            NavButton("Back: Housing", "care_back_housing"),
            NavButton("Next: Medical", "care_next_medical", type="primary"),
        ]
    )

    if clicked == "care_back_hub":
        st.switch_page("ui/pages/hub.py")
    elif clicked == "care_back_housing":
        st.switch_page("ui/pages/cost_planner_housing.py")
    elif clicked == "care_next_medical":
        st.switch_page("ui/pages/cost_planner_daily_aids.py")