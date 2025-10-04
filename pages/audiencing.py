"""Streamlit page shim that redirects to the Welcome flow."""

import streamlit as st
from ui.theme import inject_theme

from audiencing import *  # noqa: F401,F403


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


st.switch_page("ui/pages/00_welcome.py")

st.markdown('</div>', unsafe_allow_html=True)