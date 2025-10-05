import streamlit as st
from ui.cost_planner_template import render_nav
from ui.theme import inject_theme
inject_theme()

from ui.cost_planner_template import (

    NavButton,
    apply_cost_planner_theme,
    cost_planner_page_container,
    render_app_header,
    render_module_cards,
    render_nav_buttons,
    render_wizard_help,
    render_wizard_hero,
)


apply_cost_planner_theme()


if "care_context" not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context
person_name = ctx.get("person_name", "Your Loved One")
estimate = ctx.get("cost_estimate", {})
est_completed = bool(estimate.get("completed"))
est_setting = estimate.get("setting_label") or estimate.get("setting") or ""
est_zip = estimate.get("zip", "")
est_monthly = estimate.get("estimate_monthly")


with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        f"Recommended Cost Modules for {person_name}",
        "Work through the modules below. You can return to any module at any time.",
    )

    summary = "Get a quick monthly estimate based on setting, ZIP, and a few simple details."
    if est_completed and est_monthly:
        summary = f"{est_setting or 'In-home care'} • ${est_monthly:,}/mo"
        if est_zip:
            summary += f" • ZIP {est_zip}"

    cards = [
        {
            "title": "Cost of Care Planner",
            "description": summary,
            "status": "Completed" if est_completed else "Not started",
            "status_class": "positive" if est_completed else "",
            "actions": [
                {"label": "Open", "key": "open_quick_estimate", "type": "primary"},
            ],
        },
        {
            "title": "Home Care Support",
            "description": "Hourly in-home caregiving and companion support.",
            "actions": [
                {"label": "Open", "key": "open_home_care", "type": "secondary"},
            ],
        },
        {
            "title": "Daily Living Aids",
            "description": "Equipment and supplies that support daily safety and independence.",
            "actions": [
                {"label": "Open", "key": "open_daily_aids", "type": "secondary"},
            ],
        },
        {
            "title": "Housing Path",
            "description": "Assisted living, memory care, or other residential options.",
            "actions": [
                {"label": "Open", "key": "open_housing", "type": "secondary"},
            ],
        },
        {
            "title": "Benefits Check",
            "description": "VA, Medicaid, LTC insurance, and other offsets.",
            "actions": [
                {"label": "Open", "key": "open_benefits", "type": "secondary"},
            ],
        },
        {
            "title": "Age-in-Place Upgrades",
            "description": "Home safety modifications and accessibility improvements.",
            "actions": [
                {"label": "Open", "key": "open_mods", "type": "secondary"},
            ],
        },
    ]

    triggered = render_module_cards(cards)

    if triggered == "open_quick_estimate":
        st.switch_page("pages/cost_planner_estimate.py")
    elif triggered == "open_home_care":
        st.switch_page("pages/cost_planner_home_care.py")
    elif triggered == "open_daily_aids":
        st.switch_page("pages/cost_planner_daily_aids.py")
    elif triggered == "open_housing":
        st.switch_page("pages/cost_planner_housing.py")
    elif triggered == "open_benefits":
        st.switch_page("pages/cost_planner_benefits.py")
    elif triggered == "open_mods":
        st.switch_page("pages/cost_planner_mods.py")

    render_wizard_help("You can revisit modules any time-progress saves automatically.")

    clicked = render_nav([
            NavButton("Back to Mode", "mods_back_mode"),
            NavButton("Expert Review", "mods_expert_review", type="primary"),
        ]
    )

    if clicked == "mods_back_mode":
        st.switch_page("pages/cost_planner.py")
    elif clicked == "mods_expert_review":
        st.switch_page("pages/expert_review.py")
