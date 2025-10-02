import streamlit as st
from pathlib import Path

CSS = '''<style>
/* Focus outlines for accessibility */
*:focus { outline: 2px solid rgba(0,0,0,0.25) !important; outline-offset: 2px !important; }
a:focus, button:focus { outline: 3px solid rgba(0,0,0,0.35) !important; }

/* Stepper container */
.sn-stepper { display:flex; gap:6px; align-items:center; flex-wrap:wrap; margin: 8px 0 16px 0; }
.sn-step { padding:4px 10px; border-radius: 999px; background: #eef2ff; color:#1e3a8a; font-size: 13px; max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sn-step.sn-active { background:#1e3a8a; color:#fff; }
.sn-step.sn-done { background:#c7d2fe; color:#1e3a8a; opacity:0.95; }

/* Sticky nav helper if used */
.sn-sticky-bottom { position: sticky; bottom: 0; background: rgba(255,255,255,0.92); backdrop-filter: saturate(1.2) blur(6px); padding: 8px 0; border-top: 1px solid rgba(0,0,0,0.06); z-index: 5; }

/* Print friendliness */
@media print {
  [data-testid="stSidebar"] { display: none !important; }
  .block-container { max-width: 100% !important; padding: 0 !important; }
  h1,h2 { page-break-after: avoid; }
  .sn-stepper { display:none !important; }
}
</style>'''

def apply_global_ux():
    st.markdown(CSS, unsafe_allow_html=True)

# Ordered flows. File stems must match your pages/*.py filenames.
FLOW_MAIN = [
  'audiencing', 'care_needs', 'care_prefs',
  'household_legal', 'benefits_coverage', 'personal_info',
  'care_plan_confirm', 'appointment_booking', 'pfma',
  'hub'
]

FLOW_COST = [
  'cost_planner', 'cost_planner_modules', 'cost_planner_home_care',
  'cost_planner_evaluation', 'cost_plan_confirm', 'hub'
]

def _labelize(stem: str) -> str:
    return stem.replace('_', ' ').title()

def _infer_current_from_script():
    import inspect
    frm = inspect.stack()[2]
    f = frm.filename or ''
    return Path(f).stem

def _render_pills(flow, current):
    cols = st.columns(len(flow) if len(flow)<=8 else 8, gap='small')
    for i, step in enumerate(flow):
        style = 'sn-step'
        if step == current:
            style += ' sn-active'
        elif flow.index(current) > i:
            style += ' sn-done'
        with cols[i % len(cols)]:
            st.markdown(f'<div class="{style}">{_labelize(step)}</div>', unsafe_allow_html=True)

def render_stepper(flow_hint: str = 'auto'):
    """Render a tiny stepper based on filename in known flows. No layout changes to content."""
    apply_global_ux()
    current = _infer_current_from_script()
    flows = []
    if flow_hint == 'main': flows = [FLOW_MAIN]
    elif flow_hint == 'cost': flows = [FLOW_COST]
    else: flows = [FLOW_MAIN, FLOW_COST]

    chosen = None
    for f in flows:
        if current in f:
            chosen = f
            break
    if chosen:
        with st.container():
            st.markdown('<div class="sn-stepper">', unsafe_allow_html=True)
            _render_pills(chosen, current)
            st.markdown('</div>', unsafe_allow_html=True)
