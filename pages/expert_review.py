
import streamlit as st
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


# Guard
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if not st.session_state.is_authenticated:
    st.warning("Please log in to access the Expert Review page.")
    st.stop()

st.title("Expert Advisor Review")
st.write(
    "Great job completing your planning! Here, our expert advisor will review your Guided Care Plan, "
    "Cost Planner results, and personal information to ensure all modules were completed correctly. "
    "We'll highlight any missing steps or areas for you to revisit."
)

st.success("All required modules are complete.")
st.info("Optional: You may want to revisit the Benefits Check module to ensure coverage is maximized.")

if st.button("Back to Hub", key="expert_review_back"):
    st.switch_page("ui/pages/hub.py")

st.markdown('</div>', unsafe_allow_html=True)