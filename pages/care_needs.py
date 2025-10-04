
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

_debug_log('LOADED: care_needs.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Care Needs & Daily Support
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Care Needs & Support for your loved one")
st.markdown("<h2>Tailor his daily care.</h2>", unsafe_allow_html=True)
st.markdown("<p>Share details to match his needs.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Confirmation tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Care Needs & Daily Support", unsafe_allow_html=True)
st.markdown("<p>Behavioral notes: Wandering, mild confusion. Diet: Low salt. Cognition: Moderate. Mental health: Stable.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="care_needs_confirm")
st.button("Save Needs", key="save_care_needs", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Cost Plan", key="back_cn", type="secondary")
with col2:
    if st.button("Next: Care Preferences", key="next_cn", type="primary"):
        st.switch_page('ui/pages/care_prefs.py')
        st.switch_page("ui/pages/care_prefs.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)