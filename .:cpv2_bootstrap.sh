#!/usr/bin/env bash
set -euo pipefail

echo "➡️  Cost Planner v2 bootstrap starting…"

# --- sanity: ensure we're at repo root
if [ ! -d ".git" ]; then
  echo "❌ Please run from your repo root (where .git exists)."
  exit 1
fi

# --- branch
BRANCH="feat/cost-planner-v2-bootstrap"
if ! git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
  git checkout -b "$BRANCH"
else
  git checkout "$BRANCH"
fi

# --- archive old pages
ARCHIVE_DIR="archive/cost_planner_old_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ARCHIVE_DIR"

echo "🔎 Archiving old Cost Planner pages to $ARCHIVE_DIR …"
shopt -s nullglob
moved=0
for f in pages/cost_planner*.py pages/*cost_planner* pages/*/cost_planner*.py; do
  # Skip v2 paths
  case "$f" in
    pages/cost_planner_v2/*) continue ;;
  esac
  if [ -f "$f" ]; then
    mkdir -p "$ARCHIVE_DIR/$(dirname "$f")"
    git mv "$f" "$ARCHIVE_DIR/$(dirname "$f")/" || mv "$f" "$ARCHIVE_DIR/$(dirname "$f")/"
    echo "  • archived: $f"
    moved=1
  fi
done
shopt -u nullglob
if [ $moved -eq 0 ]; then
  echo "ℹ️  No old Cost Planner files found to archive (that’s fine)."
fi

# --- scaffold new v2 folders
mkdir -p pages/cost_planner_v2
mkdir -p cost_planner_v2

# --- helpers (state + nav)
cat > cost_planner_v2/cp_state.py << 'PY'
from __future__ import annotations
from typing import Any, Dict
import streamlit as st

CP_KEY = "cp"

DEFAULTS = {
    "meta": {"planner_mode": None, "authed": False},
    "qualifiers": {
        "has_partner": "No partner",
        "owns_home": False,
        "is_veteran": False,
        "care_setting": None,
        "partner_maintaining_home": False,
    },
    "setting_cost": {
        "care_setting": None,
        "home_hours": 4,
        "room_type": "Studio",
        "care_level": "Low",
        "chronic_conditions": [],
        "mobility": "Low",
        "monthly_cost": 0,
    },
    "income": {
        "social_security_person_a": 0,
        "pension_person_a": 0,
        "other_income_monthly_person_a": 0,
        "social_security_person_b": 0,
        "pension_person_b": 0,
        "other_income_monthly_person_b": 0,
        "income_total": 0,
    },
    "expenses": {
        "optional_utilities": 0,
        "optional_phone_internet": 0,
        "optional_life_insurance": 0,
        "optional_transportation": 0,
        "optional_auto": 0,
        "optional_auto_insurance": 0,
        "monthly_debt_payments": 0,
        "optional_other": 0,
        "facility_move_adjustment": True,
        "other_monthly_total": 0,
    },
    "caregiver": {
        "caregiver_type": "None",
        "include_caregiver_cost": True,
        "caregiver_cost": 0,
    },
    "benefits": {
        "va_estimate_person_a": 0,
        "va_estimate_person_b": 0,
        "ltc_daily_benefit_person_a": 0,
        "ltc_daily_benefit_person_b": 0,
        "medicaid_status": "Unsure",
        "benefits_total": 0,
    },
    "home": {
        "sale_price": 0,
        "home_monthly_total": 0,
        "reverse_mortgage_active": False,
        "reverse_mortgage_income": 0,
    },
    "liquidity": {
        "planning_to_sell": False,
        "car_sale_value": 0,
        "furniture_sale_value": 0,
        "other_sale_value": 0,
        "keeping_car": True,
        "liquidity_total": 0,
    },
    "home_mods": {
        "home_mods_needed": "None",
        "home_mods_budget": 0,
        "amortize_mods": False,
        "mods_monthly_total": 0,
    },
    "assets": {
        "cash_savings": 0,
        "brokerage_taxable": 0,
        "ira_total": 0,
        "home_equity": 0,
        "other_assets": 0,
        "assets_total_effective": 0,
    },
    "timeline": {
        "monthly_all_in": 0,
        "gap": 0,
        "runway_months": None,
    },
    "progress": {
        "landing_complete": False,
        "income_complete": False,
        "expenses_complete": False,
        "caregiver_complete": False,
        "benefits_complete": False,
        "home_complete": False,
        "liquidity_complete": False,
        "home_mods_complete": False,
        "assets_complete": False,
        "timeline_ready": False,
    },
}

def ensure_cp() -> Dict[str, Any]:
    cp = st.session_state.setdefault(CP_KEY, {})
    def deepseed(dst, src):
        for k, v in src.items():
            if isinstance(v, dict):
                deepseed(dst.setdefault(k, {}), v)
            else:
                dst.setdefault(k, v)
        return dst
    return deepseed(cp, DEFAULTS)

def cp_get(*path, default=None):
    cp = ensure_cp()
    cur = cp
    for p in path:
        cur = cur.get(p, {})
    return cur if cur != {} else default

def cp_set(path, value):
    cp = ensure_cp()
    cur = cp
    for p in path[:-1]:
        cur = cur.setdefault(p, {})
    cur[path[-1]] = value
PY

cat > cost_planner_v2/cp_nav.py << 'PY'
import streamlit as st
def goto(page: str):
    st.switch_page(f"pages/cost_planner_v2/{page}")
PY

# --- minimal PFMA-styled page stub builder
stub_page () {
  local file="$1"
  local title="$2"
  cat > "pages/cost_planner_v2/$file" << PY
from __future__ import annotations
import streamlit as st
from ui.pfma import apply_pfma_theme, render_drawer
from cost_planner_v2.cp_state import ensure_cp

apply_pfma_theme()
ensure_cp()

def _body(_):
    st.caption("TODO: ${title} form and logic.")
    return {"ok": True}

res = render_drawer(
    step_key="${title.lower().replace(' ','_')}",
    title="${title}",
    badge="v2",
    description="Stub page — to be implemented.",
    body=_body,
)

# Navigate back to Modules Hub after save
if res.ok:
    st.switch_page("pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
PY
}

# --- landing (slightly richer stub that points to hub)
cat > pages/cost_planner_v2/cost_planner_landing_v2.py << 'PY'
from __future__ import annotations
import streamlit as st
from ui.pfma import apply_pfma_theme, render_drawer, segmented_control
from cost_planner_v2.cp_state import ensure_cp, cp_get, cp_set
from cost_planner_v2.cp_nav import goto

apply_pfma_theme()
ensure_cp()

def _body(_):
    mode = segmented_control(
        "Are you just curious about care costs, or ready to plan your budget?",
        ("Estimate", "Plan"),
        key="cp_mode",
        default=cp_get("meta","planner_mode"),
    )
    if mode:
        cp_set(["meta","planner_mode"], mode)

    st.caption("Setting & Cost (quick preview)")
    cs = segmented_control("Care setting", ("Home","Assisted Living","Memory Care","Skilled"), key="cp_sc_care_setting",
                           default=cp_get("setting_cost","care_setting") or "Home")
    if cs == "Home":
        st.number_input("In-home care hours per day", min_value=0, max_value=24,
                        value=int(cp_get("setting_cost","home_hours",default=4)), key="cp_sc_home_hours")

    st.success("Estimated Care Cost: (placeholder)")

    return {"ok": True}

res = render_drawer(
    step_key="landing",
    title="Cost Planner",
    badge="v2",
    description="Pick a mode, set context, and see an immediate care-cost estimate. Then continue in Plan to build your budget.",
    body=_body,
)
if res.ok:
    goto("cost_planner_modules_hub_v2.py")
PY

# --- modules hub stub
cat > pages/cost_planner_v2/cost_planner_modules_hub_v2.py << 'PY'
from __future__ import annotations
import streamlit as st
from ui.pfma import apply_pfma_theme
from cost_planner_v2.cp_state import ensure_cp
from cost_planner_v2.cp_nav import goto

apply_pfma_theme()
ensure_cp()

st.markdown("<div class='pfma-card'>", unsafe_allow_html=True)
st.markdown("### Your Plan Modules (v2)")
st.caption("Work through modules in any order. Then view Your Money Timeline.")

modules = [
    ("Income", "cost_planner_income_v2.py"),
    ("Other Monthly Costs", "cost_planner_expenses_v2.py"),
    ("Caregiver Support", "cost_planner_caregiver_v2.py"),
    ("Benefits", "cost_planner_benefits_v2.py"),
    ("Home Decisions", "cost_planner_home_v2.py"),
    ("Liquidity Nudge", "cost_planner_liquidity_v2.py"),
    ("Home Modifications", "cost_planner_home_mods_v2.py"),
    ("Assets", "cost_planner_assets_v2.py"),
]

for label, page in modules:
    cols = st.columns([3,1])
    with cols[0]: st.write(f"**{label}**")
    with cols[1]:
        if st.button("Open", key=f"open_{label}"): goto(page)
    st.divider()

if st.button("View Money Timeline", type="primary"):
    goto("cost_planner_timeline_v2.py")

st.markdown("</div>", unsafe_allow_html=True)
PY

# --- timeline stub (result page)
cat > pages/cost_planner_v2/cost_planner_timeline_v2.py << 'PY'
from __future__ import annotations
import streamlit as st
from ui.pfma import apply_pfma_theme, render_drawer

apply_pfma_theme()

def _body(_):
    st.metric("Monthly All-In", "$—")
    st.metric("Income + Benefits", "$—")
    st.metric("Monthly Gap", "$—")
    st.metric("Runway", "—")
    st.info("This is the final results page. We’ll compute after modules are filled.")
    return {"ok": True}

res = render_drawer(
    step_key="timeline",
    title="Your Money Timeline",
    badge="Results",
    description="Here’s how long your money lasts at the current settings.",
    body=_body,
)
if res.ok:
    if st.button("Expert Review", type="primary"):
        st.switch_page("pages/expert_review.py")
PY

# --- create module stubs
stub_page "cost_planner_income_v2.py"        "Income"
stub_page "cost_planner_expenses_v2.py"      "Other Monthly Costs"
stub_page "cost_planner_benefits_v2.py"      "Benefits"
stub_page "cost_planner_home_v2.py"          "Home Decisions"
stub_page "cost_planner_assets_v2.py"        "Assets"
stub_page "cost_planner_caregiver_v2.py"     "Caregiver Support"
stub_page "cost_planner_liquidity_v2.py"     "Liquidity Nudge"
stub_page "cost_planner_home_mods_v2.py"     "Home Modifications"

# --- quick compile check (optional)
echo "🧪 Byte-compiling new pages…"
python3 - <<'PY'
import pathlib, py_compile, sys
ok=True
for f in pathlib.Path("pages/cost_planner_v2").glob("*.py"):
    try: py_compile.compile(str(f), doraise=True)
    except Exception as e:
        ok=False; print("❌", f, ":", e)
for f in pathlib.Path("cost_planner_v2").glob("*.py"):
    try: py_compile.compile(str(f), doraise=True)
    except Exception as e:
        ok=False; print("❌", f, ":", e)
if not ok: sys.exit(1)
print("✅ compile ok")
PY

# --- commit
git add -A
git commit -m "feat(cp-v2): archive old cost planner pages; scaffold PFMA-styled v2 stubs + helpers"

echo "🎉 Cost Planner v2 bootstrap complete on branch: $BRANCH"
echo "👉 Next: open pages/cost_planner_v2/* and implement modules incrementally."