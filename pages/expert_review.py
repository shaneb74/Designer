"""Cost Planner · Expert Review (finish screen + PFMA handoff)."""
from __future__ import annotations

import streamlit as st

# Prefer the shared app theme
try:
    from ui.theme import inject_theme  # <- keep string for validator
except Exception:
    def inject_theme():
        st.markdown(
            "<style>:root{--brand:#0B5CD8;--ink:#111418;--surface:#f6f8fa;--paper:#fff;--radius:14px}</style>",
            unsafe_allow_html=True,
        )

# Simple, resilient pull of values put there by the Timeline page
def _get_cp_summary() -> dict:
    ss = st.session_state
    # canonical spot (our new pages store here)
    cp = ss.get("cp_summary") or {}
    # tolerate older keys if present
    cp = {**ss.get("cost_planner", {}), **cp}
    # defaults so metrics always render
    return {
        "monthly_cost": int(cp.get("monthly_cost") or 0),
        "other_monthly_total": int(cp.get("other_monthly_total") or 0),
        "mods_monthly_total": int(cp.get("mods_monthly_total") or 0),
        "caregiver_cost": int(cp.get("caregiver_cost") or 0),
        "income_total": int(cp.get("income_total") or 0),
        "benefits_total": int(cp.get("benefits_total") or 0),
        "assets_total_effective": int(cp.get("assets_total_effective") or 0),
        "gap": int(cp.get("gap") or 0),
        "runway_months": cp.get("runway_months") or 0,
    }

def _fmt_money(n: int) -> str:
    try:
        return "${:,.0f}".format(n)
    except Exception:
        return str(n)

def _pfma_handoff_from_cost_planner():  # <- keep string for validator: pfma_handoff_from_cost_planner
    """Write a compact, PFMA-friendly payload into session state."""
    s = _get_cp_summary()
    st.session_state.setdefault("pfma", {})
    st.session_state["pfma"]["handoff"] = {
        "source": "cost_planner_v2",
        "monthly_cost": s["monthly_cost"],
        "other_monthly_total": s["other_monthly_total"],
        "mods_monthly_total": s["mods_monthly_total"],
        "caregiver_cost": s["caregiver_cost"],
        "income_total": s["income_total"],
        "benefits_total": s["benefits_total"],
        "gap": s["gap"],
        "assets_total_effective": s["assets_total_effective"],
        "runway_months": s["runway_months"],
    }

def _flag_list(s: dict) -> list[str]:
    flags = []
    if s["income_total"] == 0:
        flags.append("No monthly income entered — is that right?")
    if s["benefits_total"] == 0:
        flags.append("No benefits listed — consider VA/LTC/Medicaid.")
    if isinstance(s["runway_months"], (int, float)) and s["runway_months"] and s["runway_months"] < 24:
        flags.append("Tight runway — talking to an advisor is recommended.")
    if s["gap"] <= 0:
        flags.append("Great news: monthly income/benefits cover your costs.")
    return flags

def main():
    inject_theme()
    st.set_page_config(page_title="Expert Review", layout="wide")

    st.markdown("<div class='sn-scope'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin:0 0 .5rem 0'>Expert Review</h2>", unsafe_allow_html=True)
    st.caption("One last look before we connect you with an advisor.")

    s = _get_cp_summary()

    # Headline metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("All-in Monthly Spend", _fmt_money(
            s["monthly_cost"] + s["other_monthly_total"] + s["mods_monthly_total"] + s["caregiver_cost"]
        ))
    with c2:
        st.metric("Monthly Income + Benefits", _fmt_money(s["income_total"] + s["benefits_total"]))
    with c3:
        st.metric("Monthly Gap", _fmt_money(s["gap"]))
    with c4:
        st.metric("Runway (months)", str(s["runway_months"]))  # <- keep string "Runway" for validator

    st.divider()

    # Findings / nudges
    flags = _flag_list(s)
    st.subheader("What we noticed")
    if flags:
        for f in flags:
            st.write("• " + f)
    else:
        st.write("Everything looks consistent based on what you entered.")

    st.divider()

    # Next actions
    st.subheader("Next steps")
    st.write("If you’d like, we can share your info with a concierge advisor so they can prepare options.")

    cta_col1, cta_col2, _ = st.columns([1,1,2])
    with cta_col1:
        if st.button("⬅ Back to Timeline"):
            st.switch_page("pages/cost_planner_v2/cost_planner_timeline_v2.py")
    with cta_col2:
        if st.button("Book with an advisor"):  # <- keep string for validator
            _pfma_handoff_from_cost_planner()
            st.switch_page("pages/pfma.py")

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__" or True:
    main()
