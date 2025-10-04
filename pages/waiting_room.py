
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

_debug_log('LOADED: waiting_room.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Waiting Room Page
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Your Waiting Room")
st.markdown("<h2>Relax, explore, get ready.</h2>", unsafe_allow_html=True)
st.markdown("<p>While you wait for your call, check out these options.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Content cards
st.markdown('<div style="display: flex; gap: 2rem; flex-wrap: wrap; justify-content: center; padding: 1.5rem;">', unsafe_allow_html=True)

# Trivia Card
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; min-height: 200px; width: 300px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Trivia Time")
st.markdown("<p>Fun fact: Did you know 1 in 5 seniors miss a med dose? Click for a tip!</p>", unsafe_allow_html=True)
st.button("Get Tip", key="trivia_tip", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

# Partner Spot Card
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; min-height: 200px; width: 300px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Partner Spotlight")
st.markdown("<p>Explore our trusted partners-vetted for your peace of mind.</p>", unsafe_allow_html=True)
if st.button("See All Partners", key="partner_spotlight", type="secondary"):
    st.switch_page("ui/pages/trusted_partners.py")
st.markdown('</div>', unsafe_allow_html=True)

# Second Opinion Card
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; min-height: 200px; width: 300px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Second Opinion")
st.markdown("<p>Get a quick geriatrics review before your call-no cost.</p>", unsafe_allow_html=True)
st.button("Chat Now", key="second_opinion", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_wait", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)