# pages/hub.py
import streamlit as st

# ---------- Session guard ----------
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "person_name": "Your Loved One",
        "gcp_answers": {},
        "gcp_recommendation": None,   # 'In-home care' | 'Assisted living' | 'Memory care' | None
        "gcp_cost": None,             # e.g., '$5,200/mo'
    }

ctx = st.session_state.care_context
person_name = ctx.get("person_name", "Your Loved One")

st.title("Your Concierge Care Hub")
st.caption("Everything in one place. Start with the Guided Care Plan, then explore costs, or connect with an advisor.")

# ---------- Scoped styles (won't clobber your global theme) ----------
st.markdown(
    """
    <style>
      .sn-card {
        background: #ffffff;
        border: 1px solid rgba(2, 6, 23, 0.08);
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(2, 6, 23, 0.04);
        padding: 20px 22px;
        margin: 22px 0;
      }
      .sn-row {
        display: flex;
        gap: 16px;
        align-items: center;
        justify-content: space-between;
      }
      .sn-left { flex: 1 1 auto; min-width: 0; }
      .sn-mid { flex: 0 0 auto; }
      .sn-right { flex: 0 0 auto; text-align: right; }
      .sn-title { font-weight: 700; font-size: 20px; margin: 0 0 6px 0; }
      .sn-subtle { color: #475569; margin: 0; }
      .sn-status {
        font-size: 13px;
        padding: 6px 10px;
        border-radius: 999px;
        border: 1px solid rgba(2, 6, 23, 0.06);
        background: #F8FAFC;
        display: inline-block;
      }
      .sn-spacer { height: 2px; background: transparent; margin: 6px 0 0 0; }
      /* make streamlit buttons look decent without fighting theme */
      .sn-card .stButton>button {
        padding: 10px 14px;
        border-radius: 10px;
        font-weight: 600;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

def card(title: str, subtitle: str, cta_label: str, cta_key: str, on_click_page: str, status: str | None = None):
    """Render a self-contained card with left/mid/right sections."""
    with st.container():
        st.markdown('<div class="sn-card">', unsafe_allow_html=True)
        # Row content (use Streamlit columns to keep responsive sizing, but CSS ensures it stays inside)
        c1, c2, c3 = st.columns([6, 2, 2], vertical_alignment="center")
        with c1:
            st.markdown(f'<p class="sn-title">{title}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="sn-subtle">{subtitle}</p>', unsafe_allow_html=True)
        with c2:
            if st.button(cta_label, key=cta_key):
                st.switch_page(on_click_page)
        with c3:
            if status:
                st.markdown(f'<span class="sn-status">{status}</span>', unsafe_allow_html=True)
            else:
                st.markdown("&nbsp;", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Guided Care Plan tile ----------
gcp_completed = bool(ctx.get("gcp_recommendation")) or bool(ctx.get("gcp_answers"))
rec_text = ctx.get("gcp_recommendation") or "Recommendation here"
cost_text = ctx.get("gcp_cost") or "Cost TBD"

card(
    title="Guided Care Plan",
    subtitle=(f"{rec_text} • {cost_text}" if gcp_completed
              else "Answer 12 simple questions to get a personalized recommendation."),
    cta_label=("Open" if gcp_completed else "Start Plan"),
    cta_key="hub_gcp_start",
    on_click_page="pages/gcp.py",
    status=("Completed ✅" if gcp_completed else "Not started"),
)

# ---------- Cost Planner ----------
card(
    title="Cost Planner",
    subtitle=f"Estimate costs quickly, or build a detailed plan with modules for {person_name}.",
    cta_label="Open Planner",
    cta_key="hub_open_cp",
    on_click_page="pages/cost_planner.py",
    status=None,
)

# ---------- Plan for My Advisor ----------
card(
    title="Plan for My Advisor",
    subtitle="Book time with a concierge advisor and share your plan.",
    cta_label="Get Connected",
    cta_key="hub_pfma",
    on_click_page="pages/pfma.py",
    status=None,
)

# ---------- Medication Management ----------
card(
    title="Medication Management",
    subtitle="Keep meds on track with simple reminders and checks.",
    cta_label="Open",
    cta_key="hub_meds",
    on_click_page="pages/medication_management.py",
    status=None,
)

# ---------- Risk Navigator ----------
card(
    title="Risk Navigator",
    subtitle="Quick safety check to reduce avoidable risks at home.",
    cta_label="Run Check",
    cta_key="hub_risk",
    on_click_page="pages/risk_navigator.py",
    status=None,
)

# ---------- Assessment (last) ----------
card(
    title="Assessment",
    subtitle="Additional screening tools and forms.",
    cta_label="Open Assessment",
    cta_key="hub_assess",
    on_click_page="pages/care_plan_confirm.py",
    status=None,
)
