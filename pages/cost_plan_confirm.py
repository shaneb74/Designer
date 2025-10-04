"""Final confirmation and PFMA handoff for Cost Planner."""
from __future__ import annotations

import json

import streamlit as st

from cost_planner_shared import ensure_core_state, format_currency, recompute_costs
from ui.cost_planner_template import (
    Metric,
    NavButton,
    apply_cost_planner_theme,
    cost_planner_page_container,
    render_app_header,
    render_metrics,
    render_nav_buttons,
    render_wizard_help,
    render_wizard_hero,
)


apply_cost_planner_theme()


ensure_core_state()
cp = st.session_state["cost_planner"]
aud_snapshot = st.session_state.get("audiencing_snapshot") or st.session_state.get("audiencing")

recompute_costs()


with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        "Confirm cost plan & handoff",
        "Lock in the current snapshot, export it, or share with an advisor.",
    )

    metrics = [
        Metric("Monthly costs", format_currency(cp["monthly_total"])),
        Metric("Offsets", format_currency(cp["subtotals"]["offsets"])),
        Metric("Net out-of-pocket", format_currency(cp["net_out_of_pocket"])),
    ]
    if cp.get("runway_months") is not None:
        metrics.append(Metric("Runway", f"{cp['runway_months']:.1f} months"))
    render_metrics(metrics)

    st.subheader("Ready to share?")
    confirm = st.checkbox("I reviewed these numbers and they reflect our plan.")

    snapshot_json = json.dumps(cp["snapshot_for_crm"], indent=2).encode("utf-8")
    st.download_button(
        "Download CRM snapshot",
        data=snapshot_json,
        file_name="cost_planner_snapshot.json",
        mime="application/json",
        disabled=not confirm,
    )

    col_share, col_tweak = st.columns(2)
    with col_share:
        if st.button("Share with Advisor / PFMA", type="primary", disabled=not confirm):
            st.session_state["last_event"] = {
                "type": "cost_planner_shared",
                "audiencing": aud_snapshot,
            }
            st.switch_page("ui/pages/pfma_confirm_cost_plan.py")
    with col_tweak:
        if st.button("Tweak estimate"):
            st.switch_page("ui/pages/cost_planner_estimate.py")

    render_wizard_help("Need to adjust anything? You can always jump back into modules before sharing.")

    clicked = render_nav_buttons(
        [
            NavButton("Return to Hub", "confirm_back_hub"),
            NavButton("Back to Summary", "confirm_back_summary"),
        ]
    )

    if clicked == "confirm_back_hub":
        st.switch_page("ui/pages/hub.py")
    elif clicked == "confirm_back_summary":
        st.switch_page("ui/pages/cost_planner_estimate_summary.py")