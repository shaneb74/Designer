import streamlit as st
from pathlib import Path

# Set page config for centered layout
st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

# CSS Injection for Streamlit Cloud
def inject_css(path: str):
    css_path = Path(path)
    if css_path.exists():
        mtime = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{css_path.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)
    else:
        st.warning(f"Missing CSS: {path}")

# Load CSS
inject_css("static/style.css")

# Define pages
welcome = st.Page("pages/welcome.py", title="Welcome", icon="👋")
tell_us = st.Page("pages/tell_us_about_john.py", title="Tell Us About John", icon="ℹ️")
hub = st.Page("pages/hub.py", title="Hub", icon="🏠")
gcp = st.Page("pages/gcp.py", title="Guided Care Plan", icon="🗺️")
cost_planner_mode = st.Page("pages/cost_planner.py", title="Cost Planner: Mode", icon="💰")
cost_planner_modules = st.Page("pages/cost_planner_modules.py", title="Cost Planner: Modules", icon="📊")
cost_planner_home_care = st.Page("pages/cost_planner_home_care.py", title="Home Care Support", icon="🏠")
cost_planner_daily_aids = st.Page("pages/cost_planner_daily_aids.py", title="Daily Living Aids", icon="🛠️")
cost_planner_housing = st.Page("pages/cost_planner_housing.py", title="Housing Path", icon="🏡")
cost_planner_benefits = st.Page("pages/cost_planner_benefits.py", title="Benefits Check", icon="💳")
cost_planner_mods = st.Page("pages/cost_planner_mods.py", title="Age-in-Place Upgrades", icon="🔧")
cost_planner_evaluation = st.Page("pages/cost_planner_evaluation.py", title="Cost Planner: Evaluation", icon="🔍")
cost_planner_skipped = st.Page("pages/cost_planner_skipped.py", title="Cost Planner: Skipped", icon="⚠️")
appointment_booking = st.Page("pages/appointment_booking.py", title="Appointment Booking", icon="📞")
care_plan_confirm = st.Page("pages/care_plan_confirm.py", title="Care Plan Confirmation", icon="✅")
cost_plan_confirm = st.Page("pages/cost_plan_confirm.py", title="Cost Plan Confirmation", icon="💰")
care_needs = st.Page("pages/care_needs.py", title="Care Needs & Support", icon="🩺")
care_prefs = st.Page("pages/care_prefs.py", title="Care Preferences", icon="🎯")
household_legal = st.Page("pages/household_legal.py", title="Household & Legal", icon="🏠")
benefits_coverage = st.Page("pages/benefits_coverage.py", title="Benefits & Coverage", icon="💳")
personal_info = st.Page("pages/personal_info.py", title="Personal Info", icon="👤")
appointment_interstitial = st.Page("pages/appointment_interstitial.py", title="Call Scheduled", icon="⏰")
ai_advisor = st.Page("pages/ai_advisor.py", title="AI Advisor", icon="🤖")
waiting_room = st.Page("pages/waiting_room.py", title="Waiting Room", icon="⏳")
exports = st.Page("pages/exports.py", title="Exports", icon="📤")

# Configure navigation
pages = [welcome, tell_us, hub, gcp, cost_planner_mode, cost_planner_modules, cost_planner_home_care, cost_planner_daily_aids, cost_planner_housing, cost_planner_benefits, cost_planner_mods, cost_planner_evaluation, cost_planner_skipped, appointment_booking, care_plan_confirm, cost_plan_confirm, care_needs, care_prefs, household_legal, benefits_coverage, personal_info, appointment_interstitial, ai_advisor, waiting_room, exports]
pg = st.navigation(pages)

# Run the selected page
pg.run()

# Common elements: AI Advisor in sidebar
with st.sidebar:
    st.subheader("AI Advisor")
    st.write("Ask me anything about your plan...")
    st.text_input("Your question", key="ai_question")
    if st.button("Ask", key="ai_ask", type="primary"):
        st.info("Placeholder response: Here's some advice...")
