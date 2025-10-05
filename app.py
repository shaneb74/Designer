from __future__ import annotations

# app.py - Senior Navigator bootstrap with safe, persistent debug + guardrails

import os
import sys
import inspect
from pathlib import Path
import streamlit as st

def register_pages(*args, **kwargs):
    # disabled: we register pages solely via INTENDED + st.navigation
    return None

from pathlib import Path

# (removed) legacy auto-registration of subfolder pages
# =========================

# Debug / guardrail toggles
# =========================
def _debug_enabled() -> bool:
    # Enable via URL ?debug=1 or env SN_DEBUG_PAGES=1
    try:
        qp_flag = str(st.query_params.get("debug", "")).lower() in ("1", "true", "yes")
    except Exception:
        qp_flag = False
    env_flag = os.environ.get("SN_DEBUG_PAGES", "") == "1"
    return qp_flag or env_flag

def _design_mode_enabled() -> bool:
    try:
        qp_flag = str(st.query_params.get("dev", "")).lower() in ("1", "true", "yes")
    except Exception:
        qp_flag = False
    env_flag = os.environ.get("SN_DEV", "") == "1"
    ss_flag = bool(st.session_state.get("dev_design_mode"))
    return qp_flag or env_flag or ss_flag

# ==========================================
# Guard: exactly one active ./pages directory
# ==========================================
# in app.py, replace _enforce_single_pages_dir with this version:


def _enforce_single_pages_dir() -> None:
    from pathlib import Path
    roots = []
    for d in Path(".").glob("**/pages"):
        sd = str(d.resolve()).replace("\\","/").lower()
        if not d.is_dir(): 
            continue
        if ("_graveyard" in sd) or ("/.venv/" in sd) or ("/.git/" in sd):
            continue
        if not any(d.rglob("*.py")):
            continue
        roots.append(d)
    expected = (Path.cwd() / "pages").resolve()
    if len(roots) != 1 or roots[0].resolve() != expected:
        raise RuntimeError(f"❌ Invalid pages directories detected: {roots}\n"
                           f"Expected exactly one at {expected}")
_enforce_single_pages_dir()


# ==========================================
# Sys.path hygiene: keep repo clean & stable
# ==========================================
def _sanitize_sys_path() -> None:
    bad_markers = ("/_graveyard/", "/Designer-Development-8/", "/designer-development-8/", "/ui/pages/")
    keep: list[str] = []
    for p in sys.path:
        s = p.replace("\\", "/")
        if any(m in s for m in bad_markers):
            continue
        keep.append(p)
    sys.path[:] = keep
_sanitize_sys_path()

# ==========================================
# Live import logger (kept on; lightweight)
# Logs any module imported from /pages/ at runtime
# ==========================================
class _PageImportLogger:
    def find_spec(self, fullname, path=None, target=None):  # type: ignore[override]
        from importlib.machinery import PathFinder
        spec = PathFinder.find_spec(fullname, path)
        if spec and getattr(spec, "origin", None):
            origin = str(spec.origin).replace("\\", "/")
            if "/pages/" in origin:
                print(f"📄 import: {origin}")
        return spec

# Insert logger only once and only when debug is enabled
if _debug_enabled():
    # place before default PathFinder so it sees imports
    sys.meta_path.insert(0, _PageImportLogger())

# ===============================
# Theme import with safe fallback
# ===============================
try:
    from ui.theme import inject_theme  # preferred path
except Exception:
    def inject_theme() -> None:
        st.markdown(
            """
            <style>
              .block-container{max-width:1160px;padding-top:8px;}
              header[data-testid="stHeader"]{background:transparent;}
              footer{visibility:hidden;}
            </style>
            """,
            unsafe_allow_html=True,
        )

# ==========================================
# Global CSS injection (theme comes in last)
# ==========================================
def _inject_global_css() -> None:
    css_path = Path("static/style.css")
    if css_path.exists():
        try:
            extra = css_path.read_text(encoding="utf-8").strip()
        except Exception:
            extra = css_path.read_bytes().decode(errors="ignore").strip()
        v = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{extra}</style><!-- v:{v} -->", unsafe_allow_html=True)
    inject_theme()
_inject_global_css()

# ==========================================
# Pre-flight syntax check for page modules
# (kept: catches bad edits before navigation)
# ==========================================
def _syntax_preflight(paths=("pages",), stop_on_error=True):
    import pathlib, io, tokenize
    errors = []
    for root in paths:
        for p in pathlib.Path(root).rglob("*.py"):
            try:
                src = p.read_text(encoding="utf-8")
            except Exception as e:
                errors.append((p, 0, 0, f"read error: {e}", ""))
                continue
            try:
                tokenize.generate_tokens(io.StringIO(src).readline)
                compile(src, str(p), "exec", dont_inherit=True)
            except SyntaxError as e:
                errors.append((p, e.lineno or 0, e.offset or 0, e.msg, e.text or ""))
            except Exception as e:
                errors.append((p, 0, 0, f"{type(e).__name__}: {e}", ""))
    if errors:
        st.error("Syntax/parse error(s) found. Fix these before running pages.")
        for p, line, col, msg, txt in errors:
            pointer = " " * (max((col or 1) - 1, 0)) + "^" if txt else ""
            st.write(f"**{p}**")
            st.code(f"line {line}, col {col}: {msg}\n{(txt or '').rstrip()}\n{pointer}")
            st.markdown("---")
        if stop_on_error:
            st.stop()
_syntax_preflight()

# ==========================================
# Session bootstrap (prototype auth flag)
# ==========================================
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

# ==========================================
# Design mode helpers
# ==========================================
def _force_welcome_once() -> None:
    """On first run of a session, bounce to Welcome unless in design mode."""
    if _design_mode_enabled():
        return
    if st.session_state.get("_boot_forced_welcome"):
        return
    st.session_state["_boot_forced_welcome"] = True
    try:
        st.query_params.clear()  # Streamlit >= 1.33
    except Exception:
        try:
            st.experimental_set_query_params()
        except Exception:
            pass
    st.rerun()

# ==========================================
# Page registration helpers
# ==========================================
def ensure_page(path: str, title: str, icon: str, default: bool = False):
    p = Path(path)
    if not p.exists():
        return None
    return (
        st.Page(path, title=title, icon=icon, default=True)
        if default else st.Page(path, title=title, icon=icon)
    )

# ==========================================
# Pages to register (controls nav order)
# ==========================================
INTENDED = [

    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Your Concierge Care Hub", "🏠", False),

    # contextual welcome wrappers
    ("pages/contextual_welcome_self.py", "Contextual Welcome - For You", "ℹ️", False),
    ("pages/contextual_welcome_loved_one.py", "Contextual Welcome - For Loved Ones", "ℹ️", False),

    ("pages/professional_mode.py", "Professional Mode", "🧑", False),
    ("pages/gcp.py", "Guided Care Plan", "🗺️", False),
    ("pages/gcp_daily_life.py", "GCP - Daily Life & Support", "🗺️", False),
    ("pages/gcp_health_safety.py", "GCP - Health & Safety", "🗺️", False),
    ("pages/gcp_context_prefs.py", "GCP - Context & Preferences", "🗺️", False),
    ("pages/gcp_recommendation.py", "GCP Recommendation", "🗺️", False),

    ("pages/cost_planner.py", "Cost Planner: Mode", "💰", False),
    ("pages/cost_planner_estimate.py", "Cost Planner: Estimate", "💰", False),
    ("pages/cost_planner_estimate_summary.py", "Cost Planner: Quick Summary", "💰", False),
    ("pages/cost_planner_modules.py", "Cost Planner: Modules", "📊", False),
    ("pages/cost_planner_home_care.py", "Home Care Support", "🏠", False),
    ("pages/cost_planner_daily_aids.py", "Daily Living Aids", "🛠️", False),
    ("pages/cost_planner_housing.py", "Housing Path", "🏡", False),
    ("pages/cost_planner_benefits.py", "Benefits Check", "💳", False),
    ("pages/cost_planner_mods.py", "Age-in-Place Upgrades", "🔧", False),
    # --- Cost Planner v2 (PFMA-style UI) ---
                                        ("pages/expert_review.py", "Expert Review", "🔎", False),
        ("pages/cost_planner_evaluation.py", "Cost Planner: Evaluation", "🔍", False),
    ("pages/cost_planner_skipped.py", "Cost Planner: Skipped", "⚠️", False),

    ("pages/pfma.py", "Plan for My Advisor", "🧭", False),

    ("pages/pfma_confirm_care_plan.py", "PFMA * Care Plan Confirmer", "✅", False),
    ("pages/pfma_confirm_cost_plan.py", "PFMA * Cost Plan Confirmer", "💰", False),
    ("pages/pfma_confirm_care_needs.py", "PFMA * Care Needs", "🩺", False),
    ("pages/pfma_confirm_care_prefs.py", "PFMA * Care Preferences", "🎯", False),
    ("pages/pfma_confirm_household_legal.py", "PFMA * Household & Legal", "🏠", False),
    ("pages/pfma_confirm_benefits_coverage.py", "PFMA * Benefits & Coverage", "💳", False),
    ("pages/pfma_confirm_personal_info.py", "PFMA * Personal Info", "👤", False),

    ("pages/login.py", "Login", "🔐", False),
    ("pages/ai_advisor.py", "AI Advisor", "🤖", False),
    ("pages/waiting_room.py", "Waiting Room", "⏳", False),
    ("pages/trusted_partners.py", "Trusted Partners", "🤝", False),
    ("pages/export_results.py", "Export Results", "📥", False),
    ("pages/my_documents.py", "My Documents", "📁", False),
    ("pages/my_account.py", "My Account", "👤", False),

    # --- Cost Planner v2 (PFMA style) ---
    ("pages/cost_planner_v2/cost_planner_landing_v2.py", "Cost Planner v2 · Landing", "💰", False),
    ("pages/cost_planner_v2/cost_planner_modules_hub_v2.py", "Cost Planner v2 · Modules", "🧰", False),
    ("pages/cost_planner_v2/cost_planner_income_v2.py", "Cost Planner v2 · Income", "🧾", False),
    ("pages/cost_planner_v2/cost_planner_expenses_v2.py", "Cost Planner v2 · Expenses", "🧮", False),
    ("pages/cost_planner_v2/cost_planner_benefits_v2.py", "Cost Planner v2 · Benefits", "🎖️", False),
    ("pages/cost_planner_v2/cost_planner_home_v2.py", "Cost Planner v2 · Home", "🏠", False),
    ("pages/cost_planner_v2/cost_planner_home_mods_v2.py", "Cost Planner v2 · Home Mods", "🔧", False),
    ("pages/cost_planner_v2/cost_planner_liquidity_v2.py", "Cost Planner v2 · Liquidity", "💵", False),
    ("pages/cost_planner_v2/cost_planner_caregiver_v2.py", "Cost Planner v2 · Caregiver", "👥", False),
    ("pages/cost_planner_v2/cost_planner_assets_v2.py", "Cost Planner v2 · Assets", "🏦", False),
    ("pages/cost_planner_v2/cost_planner_timeline_v2.py", "Cost Planner v2 · Timeline", "📈", False),
]
# Build the Page objects (ignore missing silently)
pages = []
for path, title, icon, default in INTENDED:
    page = ensure_page(path, title, icon, default)
    if page:
        pages.append(page)

# Kick the session back to Welcome on first load (disabled in design mode)
_force_welcome_once()

# Render navigation (always sidebar, expanded)
if pages:
    pg = st.navigation(pages, position="sidebar", expanded=True)
    pg.run()
else:
    st.error("No pages available. Check file paths in app.py.")

# ==========================================
# Sidebar tools (Design mode + Auth)
# ==========================================
with st.sidebar:
    st.markdown("---")
    # Design mode toggle
    st.checkbox(
        "Design mode (keep nav visible; skip welcome redirect)",
        key="dev_design_mode",
        help="Enable with ?dev=1 in the URL or SN_DEV=1 in env.",
    )
    # Lightweight pages debug toggle
    st.checkbox(
        "Debug: log page imports (?debug=1)",
        value=_debug_enabled(),
        key="dbg_pages_enabled",
        help="Prints a line in the terminal whenever a /pages/ module is imported.",
        disabled=True,  # state is controlled by query param/env for reproducibility
    )
    st.markdown("---")
    # Prototype auth toggle
    st.caption("Authentication")
    if st.session_state.is_authenticated:
        st.success("Signed in")
        if st.button("Log out", key="sidebar_logout"):
            st.session_state.is_authenticated = False
            st.rerun()
    else:
        st.info("Not signed in")
        if st.button("Log in", key="sidebar_login"):
            st.session_state.is_authenticated = True
            st.rerun()
