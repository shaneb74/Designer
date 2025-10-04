from ui.ux_enhancements import apply_global_ux, render_stepper
import streamlit as st
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

apply_global_ux()
render_stepper('main')
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'audience_type': None,
        'professional_role': None,
        'person_name': None,
        'care_flags': {},
        'derived_flags': {},
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'review_log': []
    }
ctx = st.session_state.care_context

st.header('Smart Review')
st.caption('AI advisor surfaces what an expert would flag. You decide what to keep.')
suspects = []
if ctx['gcp_answers'].get('Falls risk',0) >= 7:
    suspects.append(('Home seems unsafe', 'Home Mods'))
if ctx['gcp_answers'].get('Cognition',0) >= 7:
    suspects.append(('Memory concerns imply supervision', 'Housing Decisions'))
if ctx['care_flags'].get('is_veteran'):
    suspects.append(('Veteran might qualify for A&A', 'VA Aid & Attendance'))

for msg,drawer in suspects or [('No specific flags yet', None)]:
    cols = st.columns([6,1,1,2])
    with cols[0]: st.write('* ' + msg)
    with cols[1]:
        if st.button('Add', key=f'add_{msg}'):
            ctx['review_log'].append({'msg': msg, 'action': 'add'})
    with cols[2]:
        if st.button('Ignore', key=f'ignore_{msg}'):
            ctx['review_log'].append({'msg': msg, 'action': 'ignore'})
    with cols[3]:
        if drawer and st.button('Open drawer', key=f'open_{msg}'):
            st.session_state['open_drawer'] = drawer
            st.success(f'Related: {drawer}')

st.markdown('<div class="sn-sticky-bottom">', unsafe_allow_html=True)
c1,c2 = st.columns([1,1])
with c1:
    if st.button('Back: Cost Planner'):
        st.switch_page('ui/pages/03_cost_planner.py')
with c2:
    if st.button('Next: PFMA'):
        st.switch_page('ui/pages/pfma.py')
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)