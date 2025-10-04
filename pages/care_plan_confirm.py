
import streamlit as st
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: care_plan_confirm.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Care Plan Confirmation
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Confirm Care Plan for your loved one")
st.markdown("<h2>Is this right for him?</h2>", unsafe_allow_html=True)
st.markdown("<p>Check and lock in his guided care plan.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Confirmation tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Guided Care Plan", unsafe_allow_html=True)
st.markdown("<p>Plan summary: In-home care, 10 hours/week, light supervision. Matches your loved one's needs-safe, familiar.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="care_plan_confirm")
st.button("Save Confirmation", key="save_care_plan", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Booking", key="back_cpc", type="secondary")
with col2:
    if st.button("Next: Cost Plan", key="next_cpc", type="primary"):
        st.switch_page('ui/pages/cost_plan_confirm.py')
        st.switch_page("ui/pages/cost_plan_confirm.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)