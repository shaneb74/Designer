import streamlit as st
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


# CSS already injected by app.py

st.title("Sign in")
st.caption("Use a social account or your email to continue.")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("  Sign in with Apple"):
        st.session_state.is_authenticated = True
        st.switch_page("ui/pages/hub.py")
with col2:
    if st.button("G  Sign in with Google"):
        st.session_state.is_authenticated = True
        st.switch_page("ui/pages/hub.py")
with col3:
    if st.button("f  Continue with Facebook"):
        st.session_state.is_authenticated = True
        st.switch_page("ui/pages/hub.py")

st.divider()
st.subheader("Or use your email")
email = st.text_input("Email address", placeholder="you@example.com")
pwd = st.text_input("Password", type="password", placeholder="********")
agree = st.checkbox("I consent and have proper authorization if signing up for someone else.")

if st.button("Sign in", type="primary", disabled=not(email and pwd and agree)):
    st.session_state.is_authenticated = True
    st.success("Signed in.")
    st.switch_page("ui/pages/hub.py")

st.caption("By continuing you agree to our Terms & Privacy.")

st.markdown('</div>', unsafe_allow_html=True)