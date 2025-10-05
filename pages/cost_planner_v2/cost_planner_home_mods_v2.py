import streamlit as st

# PFMA theme (fallback-safe)
try:
    from ui.pfma import apply_pfma_theme
except Exception:
    def apply_pfma_theme(): pass

apply_pfma_theme()

# ---- session scaffolding ----
cp = st.session_state.setdefault("cost_planner", {})
qual = cp.setdefault("qualifiers", {})  # owns_home, care_setting, etc.
home_mods = cp.setdefault("home_mods", {})

owns_home = bool(qual.get("owns_home", True))
care_setting = str(qual.get("care_setting", "Home")).lower()

st.title("Cost Planner · Home Modifications (v2)")

if not owns_home or care_setting != "home":
    st.info(
        "This module applies mainly to **age-in-place at home**. "
        "If you rent or you're moving to a facility, you can skip it."
    )

st.markdown("""<div class='pfma-card'>
  <h3>Here’s what home safety upgrades might cost</h3>
  <p class='pfma-note'>Use this if you plan to stay at home and may need accessibility upgrades. You can optionally spread the cost over 5 years to see a monthly equivalent.</p>
  <ul>
    <li>Grab bars: $300–$800</li>
    <li>Ramps: $1,000–$5,000</li>
    <li>Walk-in shower: $3,000–$10,000</li>
    <li>Stairs/lighting: $500–$1,200</li>
  </ul>
</div>""", unsafe_allow_html=True)

colA, colB = st.columns([1, 1], gap="large")
with colA:
    needed = st.radio(
        "Do you plan any accessibility upgrades?",
        options=["None", "Planning upgrades"],
        index=0 if home_mods.get("home_mods_needed") in (None, "None") else 1,
        key="cp_hm_needed",
    )
with colB:
    amort = st.checkbox(
        "Spread cost over 5 years?",
        value=bool(home_mods.get("amortize_mods", False)),
        help="This will convert your one-time budget into a monthly amount (budget ÷ 60).",
        key="cp_hm_amortize",
    )

budget = 0
if needed == "Planning upgrades":
    budget = st.number_input(
        "Upgrade budget (one-time, $)",
        min_value=0,
        step=500,
        value=int(home_mods.get("home_mods_budget", 0)) or 0,
        key="cp_hm_budget",
        help="Enter your total estimated budget for home modifications.",
        format="%d",
    )

mods_monthly_total = 0
if needed == "Planning upgrades" and budget and amort:
    mods_monthly_total = int(round(budget / 60.0))  # 5 years → 60 months

st.markdown("---")
mcol1, mcol2, mcol3 = st.columns([1,1,1])
with mcol1:
    st.metric("One-time budget", f"${budget:,}" if budget else "$0")
with mcol2:
    st.metric("Amortize over 5 years?", "Yes" if amort else "No")
with mcol3:
    st.metric("Monthly Mod Costs", f"${mods_monthly_total:,}")

st.markdown("---")

c1, c2, c3 = st.columns([1,1,1])
with c1:
    if st.button("◀︎ Back to Modules", key="hm_back"):
        st.switch_page("pages/cost_planner_v2/cost_planner_modules_hub_v2.py")

def _save_to_state():
    home_mods["home_mods_needed"] = needed
    home_mods["home_mods_budget"] = int(budget or 0)
    home_mods["amortize_mods"] = bool(amort)
    home_mods["mods_monthly_total"] = int(mods_monthly_total or 0)
    cp["home_mods"] = home_mods

with c2:
    if st.button("Save", key="hm_save"):
        _save_to_state()
        st.success("Home modification choices saved.")

with c3:
    if st.button("Save & Continue → Assets", key="hm_next"):
        _save_to_state()
        st.switch_page("pages/cost_planner_v2/cost_planner_assets_v2.py")
