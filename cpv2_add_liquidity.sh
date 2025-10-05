#!/usr/bin/env bash
set -euo pipefail

CP_DIR="pages/cost_planner_v2"
TARGET="$CP_DIR/cost_planner_liquidity_v2.py"
HUB="$CP_DIR/cost_planner_modules_hub_v2.py"

echo "➡️  Creating Liquidity Nudge module at: $TARGET"

mkdir -p "$CP_DIR"

# 1) Write the Liquidity module (PFMA style, consistent with other stubs)
cat > "$TARGET" <<'PY'
"""Cost Planner · Liquidity Nudge (v2)
Collect simple one-time sale proceeds (car, furniture, other) and an optional 'keeping_car' toggle.
Stores values under st.session_state.cost_planner['liquidity'].
"""

from __future__ import annotations
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
              .pfma-hstack{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}
              .pfma-actions{display:flex;gap:.5rem;justify-content:flex-end;margin-top:10px}
            </style>
            """,
            unsafe_allow_html=True,
        )

# Simple nav helpers
def goto(page: str) -> None:
    st.switch_page(f"pages/cost_planner_v2/{page}")

def back_to_hub() -> None:
    goto("cost_planner_modules_hub_v2.py")

def _cp() -> dict:
    """Get or init cost_planner state bucket."""
    return st.session_state.setdefault("cost_planner", {})

def _ensure_bucket() -> dict:
    cp = _cp()
    return cp.setdefault("liquidity", {
        "planning_to_sell": False,
        "keeping_car": True,
        "car_sale_value": 0,
        "furniture_sale_value": 0,
        "other_sale_value": 0,
        "liquidity_total": 0,
    })

def _save_to_state(vals: dict) -> None:
    cp = _cp()
    liq = cp.setdefault("liquidity", {})
    liq.update(vals)
    # Derive total
    liq["liquidity_total"] = max(0, int(liq.get("car_sale_value", 0))) \
                           + max(0, int(liq.get("furniture_sale_value", 0))) \
                           + max(0, int(liq.get("other_sale_value", 0)))
    # Surface a convenience flag other modules can read
    if "flags" not in cp:
        cp["flags"] = {}
    cp["flags"]["keeping_car"] = bool(liq.get("keeping_car", True))

apply_pfma_theme()

st.title("Cost Planner · Liquidity (v2)")
st.markdown(
    """<div class='pfma-card'>
        <span class='pfma-badge'>Optional</span>
        <h3 style="margin:.3rem 0 0;">Moving to care? Selling anything?</h3>
        <p class='pfma-note' style="margin:.25rem 0 0;">
          Quick way to add one-time cash from selling a car, furniture, or other items.
          We’ll roll this into your <em>Total Assets Available</em>.
        </p>
      </div>""",
    unsafe_allow_html=True,
)

bucket = _ensure_bucket()
planning = st.toggle("Planning to sell big things?", value=bool(bucket.get("planning_to_sell", False)), key="liq_planning")

keeping_car = st.toggle("Keeping the car?", value=bool(bucket.get("keeping_car", True)), key="liq_keep_car",
                        help="If you won’t keep the car, other modules can reduce auto + insurance costs.")

car_sale = 0
furn_sale = 0
other_sale = 0

if planning:
    st.markdown("<div class='pfma-card'>", unsafe_allow_html=True)
    st.subheader("Sale estimates")
    col1, col2, col3 = st.columns(3)
    with col1:
        car_sale = st.number_input("Car sale value ($ one-time)", min_value=0, step=500, value=int(bucket.get("car_sale_value", 0)))
    with col2:
        furn_sale = st.number_input("Furniture / personal items ($ one-time)", min_value=0, step=100, value=int(bucket.get("furniture_sale_value", 0)))
    with col3:
        other_sale = st.number_input("Other (RV, boat, etc.) ($ one-time)", min_value=0, step=250, value=int(bucket.get("other_sale_value", 0)))
    st.caption("Tip: rough numbers are fine — we’ll treat these as one-time inflows.")
    st.markdown("</div>", unsafe_allow_html=True)

# Preview total
preview_total = (car_sale if planning else 0) + (furn_sale if planning else 0) + (other_sale if planning else 0)
st.info(f"**Cash from Sales (preview):** ${preview_total:,}")

# Actions
c1, c2, c3 = st.columns([1,1,1])
with c1:
    if st.button("← Back to Modules", key="liq_back"):
        _save_to_state({
            "planning_to_sell": planning,
            "keeping_car": keeping_car,
            "car_sale_value": car_sale if planning else 0,
            "furniture_sale_value": furn_sale if planning else 0,
            "other_sale_value": other_sale if planning else 0,
        })
        back_to_hub()

with c2:
    if st.button("Save", key="liq_save"):
        _save_to_state({
            "planning_to_sell": planning,
            "keeping_car": keeping_car,
            "car_sale_value": car_sale if planning else 0,
            "furniture_sale_value": furn_sale if planning else 0,
            "other_sale_value": other_sale if planning else 0,
        })
        st.success("Liquidity saved.")

with c3:
    if st.button("Save & Continue → Home Mods", key="liq_next"):
        _save_to_state({
            "planning_to_sell": planning,
            "keeping_car": keeping_car,
            "car_sale_value": car_sale if planning else 0,
            "furniture_sale_value": furn_sale if planning else 0,
            "other_sale_value": other_sale if planning else 0,
        })
        st.switch_page("pages/cost_planner_v2/cost_planner_home_mods_v2.py")
PY

# 2) Ensure Modules Hub links to Liquidity
if [[ -f "$HUB" ]]; then
  if ! grep -q 'cost_planner_liquidity_v2\.py' "$HUB"; then
    # Try to insert into MODULES list right after 'Home Decisions' if present, else append
    if grep -q 'MODULES\s*=' "$HUB"; then
      python3 - <<'PY' "$HUB"
from pathlib import Path
hub = Path(__import__('sys').argv[1])
s = hub.read_text(encoding="utf-8")
lines = s.splitlines()
out = []
inserted = False
for ln in lines:
    out.append(ln)
    if not inserted and ("cost_planner_home_v2.py" in ln or "Home Decisions" in ln):
        out.append('    ("Liquidity", "cost_planner_liquidity_v2.py"),')
        inserted = True
if not inserted:
    # fall back: try to find start of MODULES list
    new = s.replace("MODULES = [", "MODULES = [\n    (\"Liquidity\", \"cost_planner_liquidity_v2.py\"),", 1)
    if new != s:
        Path(hub).write_text(new, encoding="utf-8")
        print("🧩 Added Liquidity after MODULES header.")
    else:
        # last resort: append a new entry near top
        out.insert(0, 'MODULES = [("Liquidity", "cost_planner_liquidity_v2.py"),]')
        Path(hub).write_text("\n".join(out), encoding="utf-8")
        print("🧩 Created MODULES with Liquidity as first entry (fallback).")
else:
    hub.write_text("\n".join(out), encoding="utf-8")
    print("🧩 Inserted Liquidity after Home Decisions.")
PY
  else
    echo "ℹ️ Modules Hub already references Liquidity."
  fi
else
  echo "⚠️ Modules Hub not found at: $HUB (skipping link insertion)"
fi

# 3) Compile check
echo "🧪 Compile checking Liquidity module…"
python3 - <<'PY'
import py_compile, sys
try:
    py_compile.compile("pages/cost_planner_v2/cost_planner_liquidity_v2.py", doraise=True)
    print("✅ cost_planner_liquidity_v2.py compiles")
except Exception as e:
    print("❌ Compile failed:", e)
    sys.exit(1)
PY

# 4) Optional commit (only if changes staged)
git add -A >/dev/null 2>&1 || true
if git diff --cached --quiet; then
  echo "ℹ️  Nothing to commit."
else
  git commit -m "feat: add Cost Planner v2 Liquidity module and link from Modules Hub" >/dev/null 2>&1 || true
  git push >/dev/null 2>&1 || true
  echo "📦 Changes committed."
fi

echo "🎯 Liquidity module ready. Open Modules Hub and click “Liquidity”."
