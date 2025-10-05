import streamlit as st

# Try to use PFMA look & feel if available
try:
    from ui.pfma import apply_pfma_theme
except Exception:
    def apply_pfma_theme(): pass

apply_pfma_theme()

st.title("Cost Planner · Other Monthly Costs (v2)")

st.markdown("""<div class='pfma-card'>
  <h3>What do you pay monthly?</h3>
  <p class='pfma-note'>Stub page – we’ll wire inputs next:
  utilities, phone/internet, life insurance, transportation, auto,
  auto insurance, monthly debt payments, other. Includes the
  facility-move adjustment (~$500) when applicable.</p>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns([1,1])
with col1:
    if st.button("◀︎ Back to Modules"):
        st.switch_page("pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
with col2:
    st.button("Save & Continue", disabled=True, help="Coming soon")
