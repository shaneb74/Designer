
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

_debug_log('LOADED: household_legal.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Household & Legal Basics
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Household & Legal Basics for your loved one")
st.markdown("<h2>Confirm his living details.</h2>", unsafe_allow_html=True)
st.markdown("<p>Lock in key info for his plan.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Confirmation tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Household & Legal Basics", unsafe_allow_html=True)
st.markdown("<p>Marital: Married. Living: With spouse. Health: No smoking, mild hearing loss. Confirmed.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="household_legal_confirm")
st.button("Save Basics", key="save_household_legal", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Care Preferences", key="back_hl", type="secondary")
with col2:
    if st.button("Next: Benefits & Coverage", key="next_hl", type="primary"):
        st.switch_page('ui/pages/benefits_coverage.py')
        st.switch_page("ui/pages/benefits_coverage.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)