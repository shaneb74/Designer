
import streamlit as st
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


# Auth guard for professional-only space
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if not st.session_state.is_authenticated:
    st.warning("Please log in to access Professional Mode.")
    st.stop()

st.title("Professional Mode")
st.write("You are signed in as a professional user. Future workflow will go here.")

if st.button("Back to Hub", key="prof_back_hub"):
    st.switch_page("ui/pages/hub.py")

st.markdown('</div>', unsafe_allow_html=True)