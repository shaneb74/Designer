
import streamlit as st
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

st.title("Call scheduled")
st.caption("Thanks - your call is on the calendar. You can get a head start while you wait.")

st.markdown('---')
col1, col2 = st.columns(2)
with col1:
    if st.button("Do Prep Now (Recommended)", key="ai_do_prep", type="primary"):
        st.switch_page("ui/pages/pfma_confirm_care_plan.py")
with col2:
    if st.button("Skip & Remind Me", key="ai_skip_prep"):
        st.switch_page("ui/pages/hub.py")

st.markdown('</div>', unsafe_allow_html=True)