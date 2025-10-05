#!/usr/bin/env bash
set -euo pipefail

CP_DIR="pages/cost_planner_v2"
TARGET="$CP_DIR/cost_planner_timeline_v2.py"

echo "➡️  Writing $TARGET (full, safe replacement)…"
mkdir -p "$CP_DIR"

cat > "$TARGET" <<'PY'
"""Cost Planner · Your Money Timeline (v2)

Final readout that combines monthly care costs, expenses, home mods, caregiver adders,
compares to income + benefits, and estimates runway using total assets.

Rules:
- monthly_all_in = monthly_cost + other_monthly_total + mods_monthly_total + caregiver_cost
- gap = monthly_all_in - (income_total + benefits_total)
- effective_assets = assets_total_effective (preferred) else liquidity_total (fallback so users see impact even if they skipped Assets)
- runway_months = effective_assets / gap if gap > 0, else "Unlimited"
"""

from __future__ import annotations
import math
import streamlit as st

# PFMA theme (safe fallback if unavailable)
try:
    from ui.pfma import apply_pfma_theme
except Exception:
    def apply_pfma_theme():
        st.markdown(
            """
            <style>
              .pfma-card{background:#fff;border:1px solid #e5e7eb;border-radius:16px;padding:16px;margin:0 0 12px;}
              .pfma-note{color:#6b7280;font-size:0.92rem;}
              .pfma-badge{display:inline-block;background:#eef2ff;color:#1f3bb3;border-radius:999px;padding:2px 10px;font-size:12px;font-weight:600;}
              .pfma-summary dd{margin:0 0 6px 0}
              .pfma-summary dt{color:#6b7280;font-size:.9rem;margin-top:4px}
              .pfma-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
              @media (max-width: 900px){.pfma-grid{grid-template-columns:1fr}}
            </style>
            """,
            unsafe_allow_html=True,
        )

def _cp() -> dict:
    return st.session_state.setdefault("cost_planner", {})

def _get(path: str, default=0):
    """
    Small helper to fetch nested cp keys like 'income.income_total'.
    """
    d = _cp()
    for part in path.split("."):
        if not isinstance(d, dict):
            return default
        d = d.get(part, {})
    return d if isinstance(d, (int, float)) else (default if d in (None, "", False) else d)

def _fmt_money(v: float | int) -> str:
    try:
        return f"${int(v):,}"
    except Exception:
        return "$0"

def goto(page: str) -> None:
    st.switch_page(f"pages/cost_planner_v2/{page}")

apply_pfma_theme()

st.title("Cost Planner · Your Money Timeline")

st.markdown(
    """<div class='pfma-card'>
        <h3 style="margin:.3rem 0 0;">Here’s how long your money lasts</h3>
        <p class='pfma-note' style="margin:.25rem 0 0;">
          We total your monthly costs and compare them to your monthly income & benefits.
          Then we estimate how long your assets could cover the gap.
        </p>
      </div>""",
    unsafe_allow_html=True,
)

# --- Pull inputs (robust defaults) ---
monthly_cost          = int(_get("setting_cost.monthly_cost", 0))             # from Setting & Cost
other_monthly_total   = int(_get("expenses.other_monthly_total", 0))          # from Other Monthly Costs
mods_monthly_total    = int(_get("home_mods.mods_monthly_total", 0))          # from Home Mods
income_total          = int(_get("income.income_total", 0))                   # from Income
benefits_total        = int(_get("benefits.benefits_total", 0))               # from Benefits
assets_total_effective= int(_get("assets.assets_total_effective", 0))         # from Assets

# Caregiver Support (include if user added it)
caregiver_cost        = 0
caregiver_type        = _get("caregiver.caregiver_type", "")
include_caregiver     = bool(_get("caregiver.include_caregiver_cost", False))
if str(caregiver_type).lower() == "hired aide" and include_caregiver:
    caregiver_cost = int(_get("caregiver.caregiver_cost", 3600))

# Liquidity (one-time) for display + fallback assets if assets not entered
liquidity_total       = int(_get("liquidity.liquidity_total", 0))
keeping_car           = bool(_get("flags.keeping_car", True))

# --- Calculations ---
monthly_all_in = monthly_cost + other_monthly_total + mods_monthly_total + caregiver_cost
inflows = income_total + benefits_total
gap = monthly_all_in - inflows

# Prefer assets_total_effective (assets page already absorbs liquidity). If assets missing, fall back to liquidity.
effective_assets = assets_total_effective if assets_total_effective > 0 else liquidity_total

if gap <= 0:
    runway_label = "Unlimited"
    runway_detail = "Monthly income + benefits cover your monthly costs."
else:
    months = math.floor(effective_assets / gap) if effective_assets > 0 else 0
    runway_label = f"{months} months"
    runway_detail = "Based on current assets divided by your monthly shortfall (gap)."

# --- Summary cards ---
left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.markdown("<div class='pfma-card'>", unsafe_allow_html=True)
    st.subheader("Monthly snapshot")
    st.markdown(
        f"""
        <div class='pfma-grid pfma-summary'>
          <div>
            <dt>Total monthly care cost</dt><dd><strong>{_fmt_money(monthly_cost)}</strong></dd>
            <dt>Other monthly expenses</dt><dd><strong>{_fmt_money(other_monthly_total)}</strong></dd>
            <dt>Home mods (monthly)</dt><dd><strong>{_fmt_money(mods_monthly_total)}</strong></dd>
            <dt>Caregiver add-on</dt><dd><strong>{_fmt_money(caregiver_cost)}</strong></dd>
          </div>
          <div>
            <dt>Monthly income</dt><dd><strong>{_fmt_money(income_total)}</strong></dd>
            <dt>Monthly benefits</dt><dd><strong>{_fmt_money(benefits_total)}</strong></dd>
            <dt><span class='pfma-badge'>All-in monthly</span></dt><dd><strong>{_fmt_money(monthly_all_in)}</strong></dd>
            <dt>Monthly gap</dt><dd><strong>{_fmt_money(gap)}</strong></dd>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='pfma-card'>", unsafe_allow_html=True)
    st.subheader("One-time funds (assets)")
    assets_line = f"<strong>{_fmt_money(assets_total_effective)}</strong> <span class='pfma-note'>(from Assets)</span>"
    liq_line = f"<strong>{_fmt_money(liquidity_total)}</strong> <span class='pfma-note'>(Liquidity Nudge)</span>"
    # Clarify which value is driving the runway calc
    if assets_total_effective > 0:
        driving = "Assets entered are used for runway; Liquidity is already included if you added it on the Assets page."
    elif liquidity_total > 0:
        driving = "No Assets entered—using Liquidity Nudge amount for runway."
    else:
        driving = "Add Assets or Liquidity to see your runway."
    st.markdown(
        f"""
        <div class='pfma-grid pfma-summary'>
          <div>
            <dt>Assets total</dt><dd>{assets_line}</dd>
            <dt>Liquidity (one-time)</dt><dd>{liq_line}</dd>
          </div>
          <div>
            <dt><span class='pfma-badge'>Assets used in calc</span></dt>
            <dd><strong>{_fmt_money(effective_assets)}</strong></dd>
            <dt>Car kept?</dt><dd><strong>{'Yes' if keeping_car else 'No'}</strong></dd>
          </div>
        </div>
        <p class='pfma-note' style='margin:.5rem 0 0;'>{driving}</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='pfma-card'>", unsafe_allow_html=True)
    st.subheader("Runway estimate")
    st.markdown(
        f"""
        <p style="font-size:1.1rem;margin:.4rem 0;">
          <strong>{runway_label}</strong>
        </p>
        <p class='pfma-note' style="margin:.2rem 0 0;">{runway_detail}</p>
        """,
        unsafe_allow_html=True,
    )

    if gap > 0 and (effective_assets <= 0 or effective_assets / gap < 24):
        st.warning("Tight runway — consider talking to an advisor.")

    st.markdown("</div>", unsafe_allow_html=True)

# Actions
c1, c2 = st.columns([1,1])
with c1:
    if st.button("← Back to Modules", key="tm_back"):
        goto("cost_planner_modules_hub_v2.py")
with c2:
    if st.button("Continue → Expert Review", key="tm_next"):
        st.switch_page("pages/expert_review.py")
PY

# compile check
python3 - <<'PY'
import py_compile,sys
try:
    py_compile.compile("pages/cost_planner_v2/cost_planner_timeline_v2.py", doraise=True)
    print("✅ cost_planner_timeline_v2.py compiles")
except Exception as e:
    print("❌ Compile failed:", e)
    sys.exit(1)
PY

echo "✅ Timeline updated with Liquidity badge + caregiver costs + safe assets fallback."
