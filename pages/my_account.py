
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

_debug_log('LOADED: my_account.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# My Account Page
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("My Account")
st.markdown("<h2>Your profile & access</h2>", unsafe_allow_html=True)
st.markdown("<p>Manage your details and resources for your loved one.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Account tiles
st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; justify-items: center; padding: 2rem;">', unsafe_allow_html=True)

# Edit Info
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 200px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Edit Info")
st.markdown("<p>Update your name, email, or phone number.</p>", unsafe_allow_html=True)
st.button("Edit Details", key="edit_info", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# My Documents
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 200px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### My Documents")
st.markdown("<p>View and manage your loved one's stored documents.</p>", unsafe_allow_html=True)
if st.button("Go to Documents", key="go_docs", type="primary"):
    st.switch_page("ui/pages/my_documents.py")
st.markdown('</div>', unsafe_allow_html=True)

# Export Results
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 200px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Export Results")
st.markdown("<p>Download your care plan and cost summary.</p>", unsafe_allow_html=True)
if st.button("Export Now", key="go_export", type="primary"):
    st.switch_page("ui/pages/export_results.py")
st.markdown('</div>', unsafe_allow_html=True)

# Change Password
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 200px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Change Password")
st.markdown("<p>Update your account password securely.</p>", unsafe_allow_html=True)
st.button("Change Password", key="change_pass", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Logout
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 200px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Log Out")
st.markdown("<p>Sign out of your account when you're done.</p>", unsafe_allow_html=True)
st.button("Log Out", key="logout", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_account", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)