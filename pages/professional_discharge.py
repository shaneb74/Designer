from ui.ux_enhancements import apply_global_ux, render_stepper
import streamlit as st
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

apply_global_ux()
render_stepper('main')

st.header("Discharge Planner")
st.write("This is a placeholder screen. Routing and form will be wired later.")

if st.button("Back: Audiencing"):
    st.switch_page('ui/pages/01_audiencing.py')

st.markdown('</div>', unsafe_allow_html=True)