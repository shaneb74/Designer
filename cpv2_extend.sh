#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"
CP_DIR="pages/cost_planner_v2"
mkdir -p "$CP_DIR"

echo "➡️  Extending Cost Planner v2 under: $CP_DIR"

create_if_absent () {
  # Guard against missing args while set -u is on
  local argc=$#
  if (( argc < 2 )); then
    echo "❌ create_if_absent requires 2 args (path, contents). Got: $argc"
    return 1
  fi
  local path="$1"
  local contents="$2"
  if [[ -e "$path" ]]; then
    echo "ℹ️  Exists (skipped): $path"
  else
    printf "%s" "$contents" > "$path"
    echo "✅ Created: $path"
  fi
}

read -r -d '' PFMA_STUB_HEADER <<'PY'
"""Cost Planner v2 — PFMA-styled module stub."""
from __future__ import annotations
import streamlit as st

try:
    from ui.pfma import apply_pfma_theme
except Exception:
    def apply_pfma_theme():
        st.markdown("""
        <style>
          :root{
            --brand:#0B5CD8; --paper:#ffffff; --surface:#f6f8fa;
            --ink:#111418; --ink-muted:#6b7280; --radius:14px;
          }
          .block-container{max-width:1160px;padding-top:8px;}
          .pfma-card{
            background: var(--surface);
            border: 1px solid rgba(0,0,0,.08);
            border-radius: var(--radius);
            padding: clamp(1rem, 2vw, 1.5rem);
          }
          .pfma-note{font-size:.9rem;color:var(--ink-muted);margin:.25rem 0 0;}
        </style>
        """, unsafe_allow_html=True)

apply_pfma_theme()
PY

read -r -d '' MODULES_HUB_PAGE <<PY
${PFMA_STUB_HEADER}
st.title('Cost Planner · Modules')
st.markdown(
    """<div class='pfma-card'>
    <h3>Pick a module to update</h3>
    <p class='pfma-note'>This hub adapts to your Qualifiers (partner, home ownership, veteran status, care setting).</p>
    </div>""", unsafe_allow_html=True
)
st.info('TODO: add dynamic navigation between Income, Expenses, Benefits, Home, Assets, and Caregiver modules.')
PY

read -r -d '' CAREGIVER_PAGE <<PY
${PFMA_STUB_HEADER}
st.title('Cost Planner · Caregiver Support (v2)')
st.markdown("""<div class='pfma-card'>
  <h3>Who’ll help with in-home care?</h3>
  <p class='pfma-note'>Optional for in-home care with higher needs. Adds caregiver_cost to monthly all-in.</p>
</div>""", unsafe_allow_html=True)
st.info('TODO: inputs for caregiver_type, include_caregiver_cost, caregiver_cost (default 3600 if included).')
PY

read -r -d '' BENEFITS_PAGE <<PY
${PFMA_STUB_HEADER}
st.title('Cost Planner · Benefits (v2)')
st.markdown("""<div class='pfma-card'>
  <h3>Any benefits to lower your costs?</h3>
  <p class='pfma-note'>VA, Medicaid status, and LTC insurance are summarized here.</p>
</div>""", unsafe_allow_html=True)
st.info('TODO: build inputs for: va_estimate_(A/B), ltc_daily_benefit_(A/B), medicaid_status → benefits_total')
PY

read -r -d '' HOME_PAGE <<PY
${PFMA_STUB_HEADER}
st.title('Cost Planner · Home Decisions (v2)')
st.markdown("""<div class='pfma-card'>
  <h3>What’s the plan for your home?</h3>
  <p class='pfma-note'>Estimate sale proceeds, rental income, or a simple reverse mortgage monthly amount (no fee modeling).</p>
</div>""", unsafe_allow_html=True)
st.info('TODO: add inputs for sale_price (one-time), rental_income (monthly), reverse_mortgage_income (monthly) → home_monthly_total.')
PY

read -r -d '' ASSETS_PAGE <<PY
${PFMA_STUB_HEADER}
st.title('Cost Planner · Assets (v2)')
st.markdown("""<div class='pfma-card'>
  <h3>What savings or assets can you tap?</h3>
  <p class='pfma-note'>Simple: cash, brokerage, IRA/401k combined, home equity, other assets, plus any one-time liquidity nudge.</p>
</div>""", unsafe_allow_html=True)
st.info('TODO: inputs for cash_savings, brokerage_taxable, ira_total, home_equity (if owner), other_assets, liquidity_total → assets_total_effective')
PY

# Create all missing stubs safely
create_if_absent "$CP_DIR/cost_planner_modules_hub_v2.py" "$MODULES_HUB_PAGE"
create_if_absent "$CP_DIR/cost_planner_caregiver_v2.py" "$CAREGIVER_PAGE"
create_if_absent "$CP_DIR/cost_planner_benefits_v2.py" "$BENEFITS_PAGE"
create_if_absent "$CP_DIR/cost_planner_home_v2.py" "$HOME_PAGE"
create_if_absent "$CP_DIR/cost_planner_assets_v2.py" "$ASSETS_PAGE"

# Update .gitignore (idempotent)
if ! grep -q '^pages/cost_planner_legacy/$' .gitignore 2>/dev/null; then
  {
    echo ""
    echo "# Archived legacy Cost Planner files"
    echo "pages/cost_planner_legacy/"
  } >> .gitignore
  echo "✅ Updated .gitignore"
else
  echo "ℹ️  .gitignore already includes pages/cost_planner_legacy/"
fi

# Commit (only if there are changes)
git add -A
if git diff --cached --quiet; then
  echo "ℹ️  Nothing to commit."
else
  git commit -m "feat: scaffold Cost Planner v2 modules (hub, caregiver, benefits, home, assets)"
  git push || true
fi

echo "🎯 Cost Planner v2 module expansion complete."
