
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

_debug_log('LOADED: care_prefs.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Care Preferences
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Care Preferences for your loved one")
st.markdown("<h2>Choose what suits him best.</h2>", unsafe_allow_html=True)
st.markdown("<p>Personalize his care settings.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Preference tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Care Preferences", unsafe_allow_html=True)
st.markdown("<p>Pets: Yes (dog). Activities: Gardening. Radius: 10 miles. Setting: Quiet, private.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="care_prefs_confirm")
st.button("Save Preferences", key="save_care_prefs", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Care Needs", key="back_cp", type="secondary")
with col2:
    if st.button("Next: Household & Legal", key="next_cp", type="primary"):
        st.switch_page('ui/pages/household_legal.py')
        st.switch_page("ui/pages/household_legal.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)