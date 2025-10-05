"""Expert review drawer for Cost Planner."""
from __future__ import annotations

import streamlit as st
from ui.cost_planner_template import render_nav
from ui.theme import inject_theme
inject_theme()

from cost_planner_shared import (
    ensure_core_state,
    expert_flag,
    format_currency,
    get_numeric,
    recompute_costs,
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
gcp = st.session_state.get("gcp", {})
aud = st.session_state.get("audiencing", {})

recompute_costs()
cp["expert_flags"] = []

chronic = gcp.get("chronic_conditions", [])
if chronic and get_numeric("medical_prescriptions") == 0:
    expert_flag("Medications listed but Rx cost is 0")

recommended = gcp.get("recommended_setting")
if recommended in {"assisted", "memory"} and get_numeric("housing_base_rent") == 0:
    expert_flag("Community setting selected without housing base rent")

if gcp.get("care_intensity") == "high" and get_numeric("care_base_rate") == 0:
    expert_flag("High care needs but care staffing cost missing")

if cp["mode"] == "planning" and cp.get("runway_months") is None:
    expert_flag("Planning mode without positive runway")


with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        "Expert review & decision trace",
        "Resolve any flagged inconsistencies before generating exports.",
    )

    if cp["expert_flags"]:
        for flag in cp["expert_flags"]:
            render_suggestion(flag, tone="warn")
    else:
        render_suggestion("No expert review flags at this time.", tone="info")

    st.subheader("Decision log")
    if cp["decision_log"]:
        for entry in cp["decision_log"]:
            st.write(f"* {entry}")
    else:
        render_wizard_help("No decisions logged yet. Notes will appear here as planners make updates.")

    st.subheader("Snapshot checks")
    metrics = [
        Metric("Monthly costs", format_currency(cp["monthly_total"])),
        Metric("Net out-of-pocket", format_currency(cp["net_out_of_pocket"])),
    ]
    if cp.get("runway_months") is not None:
        metrics.append(Metric("Runway (months)", f"{cp['runway_months']:.1f}"))
    render_metrics(metrics)

    clicked = render_nav([
            NavButton("Return to Hub", "evaluation_back_hub"),
            NavButton("Back: Debts & Other", "evaluation_back_debts"),
            NavButton("Next: Summary", "evaluation_next_summary", type="primary"),
        ]
    )

    if clicked == "evaluation_back_hub":
        st.switch_page("pages/hub.py")
    elif clicked == "evaluation_back_debts":
        st.switch_page("pages/cost_planner_freeform.py")
    elif clicked == "evaluation_next_summary":
        st.switch_page("pages/cost_planner_estimate_summary.py")
