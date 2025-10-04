import streamlit as st

ROUTES = ("guided_care_plan", "medicaid_off_ramp", "plan_for_my_advisor")

def _route_hint(entry: str, q: dict) -> str:
    if q.get("on_medicaid"):
        return "medicaid_off_ramp"
    if q.get("urgent"):
        return "plan_for_my_advisor"
    return "guided_care_plan"

def get_audience() -> dict:
    return st.session_state.get("audiencing", {
        "entry": "self",
        "qualifiers": {
            "is_veteran": False,
            "has_partner": False,
            "owns_home": False,
            "on_medicaid": False,
            "urgent": False,
        },
        "route": {"next": "guided_care_plan"},
    })

def render():
    st.header("Audiencing - quick setup")

    entry = st.segmented_control(
        "Who are you planning for?",
        options=["self", "proxy", "pro"],
        default=get_audience().get("entry", "self"),
        help="Self, someone else (proxy), or a professional/referral partner."
    )

    with st.form("audiencing_form", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            is_veteran  = st.toggle("Veteran / surviving spouse", value=get_audience()["qualifiers"]["is_veteran"])
            has_partner = st.toggle("Has spouse/partner", value=get_audience()["qualifiers"]["has_partner"])
        with col2:
            owns_home   = st.toggle("Owns a home", value=get_audience()["qualifiers"]["owns_home"])
            on_medicaid = st.toggle("On/applying for Medicaid", value=get_audience()["qualifiers"]["on_medicaid"])
        with col3:
            urgent      = st.toggle("Urgent (need help ASAP)", value=get_audience()["qualifiers"]["urgent"])
        submitted = st.form_submit_button("Continue")

    if submitted:
        qualifiers = {
            "is_veteran": bool(is_veteran),
            "has_partner": bool(has_partner),
            "owns_home": bool(owns_home),
            "on_medicaid": bool(on_medicaid),
            "urgent": bool(urgent),
        }
        st.session_state["audiencing"] = {
            "entry": entry,
            "qualifiers": qualifiers,
            "route": {"next": _route_hint(entry, qualifiers)},
        }
        st.session_state.setdefault("event_log", []).append({
            "kind": "audiencing_set",
            "data": st.session_state["audiencing"],
        })
        st.rerun()

    if get_audience()["qualifiers"]["on_medicaid"]:
        st.info("Medicaid path noted. We'll show Medicaid-aligned guidance and planners.")

    with st.expander("Debug · Audiencing JSON", expanded=False):
        st.json(get_audience())
