
# Cost Planner · Income (v2)
from __future__ import annotations
import streamlit as st

# ---------------- Theme helpers (works with/without your PFMA CP template) ----------------
try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
        render_nav_buttons,
        Metric, NavButton,
    )
except Exception:
    # graceful fallbacks
    def apply_cost_planner_theme():
        st.markdown("""
        <style>
          :root{--brand:#0B5CD8;--surface:#f6f8fa;--ink:#111418}
          .sn-card{background:var(--surface);border:1px solid rgba(0,0,0,.08);
                   border-radius:14px;padding:clamp(1rem,2vw,1.5rem);}
        </style>
        """, unsafe_allow_html=True)
    from contextlib import contextmanager
    @contextmanager
    def cost_planner_page_container(): yield
    def render_app_header(): st.markdown("### Cost Planner")
    def render_wizard_hero(title: str, subtitle: str = ""):
        st.markdown(f"## {title}")
        if subtitle: st.caption(subtitle)
    def render_wizard_help(text: str): st.info(text)
    class Metric: 
        def __init__(self, title: str, value: str): self.title, self.value = title, value
    class NavButton:
        def __init__(self, label: str, key: str, type: str = "secondary", icon: str | None = None):
            self.label, self.key, self.type, self.icon = label, key, type, icon
    def render_nav_buttons(buttons=None, prev=None, next=None):
        cols = st.columns(2)
        if prev:
            with cols[0]:
                if st.button(prev.label, key=prev.key, type="secondary", use_container_width=True):
                    st.switch_page("pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        if next:
            with cols[-1]:
                if st.button(next.label, key=next.key, type="primary", use_container_width=True):
                    st.switch_page("pages/cost_planner_v2/cost_planner_expenses_v2.py")

# ---------------- State helpers ----------------
def _cp_get() -> dict:
    return st.session_state.setdefault("cost_planner", {})

def _qual_get() -> dict:
    cp = _cp_get()
    return cp.setdefault("qualifiers", {})  # has_partner, owns_home, etc.

def _income_get() -> dict:
    cp = _cp_get()
    return cp.setdefault("income", {
        "social_security_person_a": 0,
        "pension_person_a": 0,
        "other_income_monthly_person_a": 0,
        "social_security_person_b": 0,
        "pension_person_b": 0,
        "other_income_monthly_person_b": 0,
    })

def _set_income_total(total: float):
    cp = _cp_get()
    derived = cp.setdefault("derived", {})
    derived["income_total"] = float(total)

def _to_num(x) -> float:
    try:
        if x is None: return 0.0
        if isinstance(x, (int, float)): return float(x)
        s = str(x).strip().replace(",", "").replace("$", "")
        return float(s) if s else 0.0
    except Exception:
        return 0.0

def _partner_mode() -> str:
    # "No partner", "Unified household", "Split finances"
    q = _qual_get()
    return str(q.get("has_partner", "No partner"))

def _render_person_inputs(label: str, prefix: str, inc: dict) -> tuple[float, float, float]:
    with st.container(border=True):
        st.markdown(f"**{label}**")
        c1, c2, c3 = st.columns(3)
        with c1:
            a = st.text_input("Social Security ($/mo)", value=str(inc.get(f"social_security_{prefix}", 0)), key=f"ss_{prefix}")
        with c2:
            b = st.text_input("Pension ($/mo)", value=str(inc.get(f"pension_{prefix}", 0)), key=f"pension_{prefix}")
        with c3:
            c = st.text_input("Other income ($/mo)", value=str(inc.get(f"other_income_monthly_{prefix}", 0)), key=f"other_{prefix}")
        return _to_num(a), _to_num(b), _to_num(c)

def main():
    apply_cost_planner_theme()
    st.set_page_config(page_title="Cost Planner · Income", layout="wide")
    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero("Income", "What money comes in each month?")
        render_wizard_help("Ballpark your monthly income—rough numbers are fine. Include wages, rental, alimony, dividends—any steady cash.")

        inc = _income_get()
        has_partner = _partner_mode()  # "No partner" | "Unified household" | "Split finances"

        a_ss, a_pens, a_other = _render_person_inputs("Person A", "person_a", inc)

        b_ss = b_pens = b_other = 0.0
        if has_partner == "Unified household":
            st.caption("Since this is a unified household, include Person B as well.")
            b_ss, b_pens, b_other = _render_person_inputs("Person B", "person_b", inc)
        elif has_partner in ("Split finances", "No partner"):
            st.caption("We’ll only count Person A here.")

        total = a_ss + a_pens + a_other + b_ss + b_pens + b_other

        # persist to session
        inc["social_security_person_a"] = a_ss
        inc["pension_person_a"] = a_pens
        inc["other_income_monthly_person_a"] = a_other
        inc["social_security_person_b"] = b_ss
        inc["pension_person_b"] = b_pens
        inc["other_income_monthly_person_b"] = b_other
        _set_income_total(total)

        st.markdown("### ")
        st.metric("Total Monthly Income", f"${total:,.0f}")

        # nav
        render_nav_buttons(
            prev=NavButton("← Back to Modules", "income_back"),
            next=NavButton("Save & Continue → Expenses", "income_next", type="primary"),
        )

if __name__ == "__main__" or True:
    main()
