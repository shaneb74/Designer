
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

_debug_log('LOADED: personal_info.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Personal Info
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Personal Info for your loved one")
st.markdown("<h2>Confirm contact details.</h2>", unsafe_allow_html=True)
st.markdown("<p>Ensure your advisor can reach you.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Confirmation tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Personal Info", unsafe_allow_html=True)
st.markdown("<p>Name: your loved one Doe. Phone: 123-456-7890. Email: john@example.com. Confirmed.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="personal_info_confirm")
st.button("Save Info", key="save_personal_info", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Benefits", key="back_pi", type="secondary")
with col2:
    if st.button("Finish Prep", key="next_pi", type="primary"):
        st.switch_page('ui/pages/hub.py')
        st.switch_page("ui/pages/hub.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)