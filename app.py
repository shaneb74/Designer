from __future__ import annotations

# app.py - Senior Navigator bootstrap (cleaned)

from pathlib import Path
import io
import tokenize
import streamlit as st

# --- Streamlit rerun: back-compat shim ---
if not hasattr(st, "rerun"):
    # Older Streamlit exposed experimental_rerun
    st.rerun = getattr(st, "experimental_rerun")

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
# ==========================================
def _syntax_preflight(paths=("pages",), stop_on_error=True):
    errors = []
    for root in paths:
        for p in Path(root).rglob("*.py"):
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

# (Optional) enable locally; comment in prod if you want
# _syntax_preflight()

# ==========================================
# Session bootstrap (prototype auth flag)
# ==========================================
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

# ==========================================
# First-load boot redirect (force Welcome once per session)
# ==========================================
def _force_welcome_once() -> None:
    """On first run of a new session, clear query params so router lands on Welcome."""
    if st.session_state.get("_boot_forced_welcome"):
        return
    st.session_state["_boot_forced_welcome"] = True
    try:
        st.query_params.clear()  # Streamlit ≥ 1.33
    except Exception:
        try:
            st.experimental_set_query_params()  # older API
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
        if default
        else st.Page(path, title=title, icon=icon)
    )

# ==========================================
# Pages to register (controls nav order)
# NOTE: All former tell_us_* flows now point to contextual_welcome
# ==========================================
INTENDED = [
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Your Concierge Care Hub", "🏠", False),
    ("pages/contextual_welcome.py", "Contextual Welcome - For You", "ℹ️", False),
    ("pages/contextual_welcome.py", "Contextual Welcome - For Loved Ones", "ℹ️", False),
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
    ("pages/expert_review.py", "Expert Review", "🔎", False),
    ("pages/cost_planner_evaluation.py", "Cost Planner: Evaluation", "🔍", False),
    ("pages/cost_planner_skipped.py", "Cost Planner: Skipped", "⚠️", False),
    ("pages/pfma.py", "Plan for My Advisor", "🧭", False),
    ("pages/appointment_booking.py", "Appointment Booking", "📞", False),
    ("pages/appointment_interstitial.py", "Call Scheduled", "⏰", False),
    ("pages/pfma_confirm_care_plan.py", "PFMA • Care Plan", "✅", False),
    ("pages/pfma_confirm_cost_plan.py", "PFMA • Cost Plan", "💰", False),
    ("pages/pfma_confirm_care_needs.py", "PFMA • Care Needs", "🩺", False),
    ("pages/pfma_confirm_care_prefs.py", "PFMA • Care Preferences", "🎯", False),
    ("pages/pfma_confirm_household_legal.py", "PFMA • Household & Legal", "🏠", False),
    ("pages/pfma_confirm_benefits_coverage.py", "PFMA • Benefits & Coverage", "💳", False),
    ("pages/pfma_confirm_personal_info.py", "PFMA • Personal Info", "👤", False),
    ("pages/login.py", "Login", "🔐", False),
    ("pages/ai_advisor.py", "AI Advisor", "🤖", False),
    ("pages/waiting_room.py", "Waiting Room", "⏳", False),
    ("pages/trusted_partners.py", "Trusted Partners", "🤝", False),
    ("pages/export_results.py", "Export Results", "📥", False),
    ("pages/my_documents.py", "My Documents", "📁", False),
    ("pages/my_account.py", "My Account", "👤", False),
]

# Build final page list (quietly skip any missing files)
pages = []
for path, title, icon, *rest in INTENDED:
    default = bool(rest[0]) if rest else False
    page = ensure_page(path, title, icon, default)
    if page:
        pages.append(page)

# Kick the session back to Welcome on first load
_force_welcome_once()

if pages:
    pg = st.navigation(pages)
    pg.run()
else:
    st.error("No pages available. Check file paths in app.py.")

# ==========================================
# Sidebar auth toggle (prototype)
# ==========================================
with st.sidebar:
    st.markdown("---")
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