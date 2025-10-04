
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

_debug_log('LOADED: benefits_coverage.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Benefits & Coverage
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Benefits & Coverage for your loved one")
st.markdown("<h2>Unlock savings for his care.</h2>", unsafe_allow_html=True)
st.markdown("<p>Confirm eligibility details.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Confirmation tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Benefits & Coverage", unsafe_allow_html=True)
st.markdown("<p>Insurance: Blue Cross. LTC: No. Medicaid: In process. VA: Yes. Confirmed.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="benefits_coverage_confirm")
st.button("Save Coverage", key="save_benefits_coverage", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Household", key="back_bc", type="secondary")
with col2:
    if st.button("Next: Personal Info", key="next_bc", type="primary"):
        st.switch_page('ui/pages/personal_info.py')
        st.switch_page("ui/pages/personal_info.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)