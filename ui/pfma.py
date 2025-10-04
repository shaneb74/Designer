"""High-fidelity Plan for My Advisor layout helpers."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from io import BytesIO
from typing import Any, Callable, Dict, Iterable, List, Sequence

import streamlit as st

from ui.theme import inject_theme


PFMA_STEPS: List[tuple[str, str]] = [
    ("booking", "Booking"),
    ("care_plan", "Care Plan"),
    ("cost_plan", "Cost Planner"),
    ("care_needs", "Care Needs"),
    ("care_prefs", "Care Preferences"),
    ("household_legal", "Household & Legal"),
    ("benefits_coverage", "Benefits & Coverage"),
    ("personal_info", "Personal Info"),
    ("summary", "Summary & Exports"),
]


STEP_TO_PAGE = {
    "booking": "ui/pages/pfma.py",
    "care_plan": "ui/pages/pfma_confirm_care_plan.py",
    "cost_plan": "ui/pages/pfma_confirm_cost_plan.py",
    "care_needs": "ui/pages/pfma_confirm_care_needs.py",
    "care_prefs": "ui/pages/pfma_confirm_care_prefs.py",
    "household_legal": "ui/pages/pfma_confirm_household_legal.py",
    "benefits_coverage": "ui/pages/pfma_confirm_benefits_coverage.py",
    "personal_info": "ui/pages/pfma_confirm_personal_info.py",
    "summary": "ui/pages/pfma_summary.py",
}


DRAWER_KEYS = (
    "care_plan",
    "cost_plan",
    "care_needs",
    "care_prefs",
    "household_legal",
    "benefits_coverage",
    "personal_info",
)


DUCK_BADGES = (
    "Clarity",
    "Planner",
    "Care",
    "Joy",
    "Family",
    "Money",
    "You",
)


PFMA_SCOPE_CSS = """
<style>
.pfma-app {
  background: linear-gradient(135deg, #f9fafb 0%, #eef2ff 100%);
  min-height: 100vh;
  padding-bottom: 4rem;
}

.pfma-hero {
  position: relative;
  background: radial-gradient(160% 160% at 90% 0%, rgba(0, 87, 184, 0.15) 0%, rgba(0,87,184,0) 48%),
              linear-gradient(120deg, #ffffff 0%, #eef5ff 55%, #ffffff 100%);
  border-radius: var(--sn-radius-lg);
  padding: clamp(2.6rem, 5vw, 3.8rem) clamp(2.1rem, 5vw, 3.8rem);
  box-shadow: var(--shadow_1);
  margin-bottom: 1.6rem;
  overflow: hidden;
}

.pfma-hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(180% 180% at 15% 85%, rgba(251, 192, 45, 0.18) 0%, rgba(255,255,255,0) 48%);
  opacity: 0.7;
  pointer-events: none;
}

.pfma-hero h1 {
  font-size: clamp(32px, 4.4vw, 46px);
  font-weight: 800;
  color: var(--ink);
  margin: 0;
}

.pfma-hero p {
  margin: .7rem 0 0;
  color: var(--ink-muted);
  font-size: 1.05rem;
  max-width: 640px;
}

.pfma-progress {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
  margin-bottom: 2rem;
}

.pfma-progress__step {
  background: #e2e8f0;
  border-radius: 999px;
  padding: .55rem .9rem;
  font-weight: 600;
  font-size: .92rem;
  color: #475569;
  text-align: center;
  position: relative;
  transition: transform .18s ease, box-shadow .18s ease;
}

.pfma-progress__step.pfma-progress__step--active {
  background: linear-gradient(135deg, #0057b8 0%, #0b74d0 100%);
  color: white;
  box-shadow: 0 16px 30px -18px rgba(0, 87, 184, .7);
}

.pfma-progress__step.pfma-progress__step--done {
  background: rgba(0, 87, 184, 0.14);
  color: #0b3e91;
}

.pfma-section-grid {
  display: grid;
  gap: 1.4rem;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

.pfma-card {
  background: white;
  border-radius: var(--sn-radius-lg);
  border: 1px solid #d9e0ef;
  box-shadow: var(--shadow_1);
  padding: 1.6rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pfma-card h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 750;
  color: var(--ink);
}

.pfma-badge {
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  padding: .36rem .72rem;
  border-radius: 999px;
  background: rgba(251, 192, 45, 0.15);
  color: #8d5a00;
  font-weight: 600;
  font-size: .9rem;
}

.pfma-field-label {
  font-weight: 650;
  color: var(--ink);
  margin-bottom: .35rem;
}

.pfma-pill-group,
.pfma-chip-group {
  display: flex;
  gap: .5rem;
  flex-wrap: wrap;
}

.pfma-chip-group button,
.pfma-pill-group button {
  border-radius: 999px !important;
  padding: .52rem 1.15rem !important;
  font-weight: 600 !important;
}

.pfma-drawer {
  border-radius: var(--sn-radius-lg);
  background: white;
  border: 1px solid #d9e0ef;
  box-shadow: var(--shadow_1);
  padding: clamp(1.6rem, 3vw, 2.1rem);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.pfma-drawer__header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: flex-start;
}

.pfma-drawer__title {
  font-size: 1.35rem;
  font-weight: 760;
  margin: 0;
  color: var(--ink);
}

.pfma-drawer__badge {
  display: inline-flex;
  align-items: center;
  gap: .45rem;
  padding: .36rem .7rem;
  border-radius: 999px;
  background: #fef3c7;
  color: #8d5a00;
  font-weight: 650;
}

.pfma-banner {
  border-radius: var(--sn-radius);
  padding: .95rem 1.1rem;
  background: rgba(251, 192, 45, 0.16);
  border: 1px solid rgba(251, 192, 45, 0.45);
  color: #8d5a00;
  font-weight: 600;
}

.pfma-summary-grid {
  display: grid;
  gap: 1.4rem;
  grid-template-columns: minmax(280px, 1fr) minmax(260px, 320px);
}

.pfma-wheel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.pfma-wheel__duck {
  background: white;
  border-radius: var(--sn-radius);
  border: 1px solid #dce3f4;
  padding: 1rem;
  text-align: center;
  box-shadow: var(--shadow_1);
  position: relative;
  overflow: hidden;
}

.pfma-wheel__duck::after {
  content: "🦆";
  position: absolute;
  font-size: 2.2rem;
  top: 8px;
  right: 12px;
  opacity: .22;
}

.pfma-wheel__duck strong {
  display: block;
  font-size: 1.1rem;
  margin-bottom: .2rem;
}

.pfma-sticky-nav {
  position: sticky;
  bottom: 0;
  padding-top: 1.6rem;
  background: linear-gradient(180deg, rgba(249,250,251,0) 0%, rgba(249,250,251,0.92) 48%, rgba(249,250,251,1) 100%);
  backdrop-filter: blur(10px);
  margin-top: 2.2rem;
}

.pfma-sticky-nav .pfma-nav-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.pfma-nav-actions {
  display: flex;
  gap: .75rem;
}

.pfma-note {
  color: var(--ink-muted);
  font-size: .95rem;
}

.pfma-duck-parade {
  display: flex;
  gap: .6rem;
  flex-wrap: wrap;
  font-size: 1.65rem;
  margin-top: .8rem;
}

.pfma-duck-parade span {
  animation: pfmaFloat 0.7s ease-in-out;
}

@keyframes pfmaFloat {
  from { transform: translateY(8px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.pfma-download-card {
  background: white;
  border-radius: var(--sn-radius-lg);
  border: 1px solid #d9e0ef;
  box-shadow: var(--shadow_1);
  padding: 1.6rem;
  display: flex;
  flex-direction: column;
  gap: .9rem;
}

.pfma-download-card button[title] {
  width: 100%;
}

.pfma-summary-row {
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:.65rem 0;
  border-bottom:1px solid #e2e8f0;
}

.pfma-summary-row:last-child {
  border-bottom:none;
}

.pfma-summary-row .status {
  color: var(--ink-muted);
  font-weight: 600;
}

.pfma-fieldstack {
  display: grid;
  gap: 1.2rem;
}

.pfma-inline-fields {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

</style>
"""


def apply_pfma_theme() -> None:
    """Inject base theme + PFMA specific CSS."""

    st.set_page_config(page_title="Plan for My Advisor", layout="wide")
    inject_theme()
    if not st.session_state.get("_pfma_theme_injected"):
        st.markdown(PFMA_SCOPE_CSS, unsafe_allow_html=True)
        st.session_state["_pfma_theme_injected"] = True


def ensure_pfma_state() -> dict[str, Any]:
    """Return the pfma state block with defaults."""

    state = st.session_state.setdefault("pfma", {})
    state.setdefault("booking", {})
    sections = state.setdefault("sections", {})
    for key in DRAWER_KEYS:
        sections.setdefault(key, {"complete": False, "data": {}})
    state.setdefault("completed_steps", [])
    state.setdefault("last_completed", None)
    state.setdefault("badges", {duck: False for duck in DUCK_BADGES})

    dossier = st.session_state.setdefault("dossier", {})
    dossier.setdefault("pfma", {})
    return state


def step_index(step_key: str) -> int:
    for idx, (key, _) in enumerate(PFMA_STEPS):
        if key == step_key:
            return idx
    raise KeyError(step_key)


def mark_step_complete(step_key: str) -> None:
    state = ensure_pfma_state()
    completed = set(state.get("completed_steps", []))
    completed.add(step_key)
    ordered = [key for key, _ in PFMA_STEPS if key in completed]
    state["completed_steps"] = ordered
    state["last_completed"] = datetime.utcnow().isoformat()


def step_status(current_step: str, step_key: str) -> str:
    state = ensure_pfma_state()
    completed = set(state.get("completed_steps", []))
    current_idx = step_index(current_step)
    idx = step_index(step_key)
    if step_key in completed and idx <= current_idx:
        return "done"
    if idx == current_idx:
        return "active"
    return "upcoming"


def render_header(subtitle: str | None = None) -> None:
    st.markdown('<div class="pfma-hero">', unsafe_allow_html=True)
    st.markdown("<h1>Plan for My Advisor</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p>Get your ducks in a row 🦆 before your concierge call. We’ll gather the essentials so your advisor can jump straight into solutions.</p>",
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(f"<p style='margin-top:1.2rem;color:var(--ink);font-weight:600;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_progress(current_step: str) -> None:
    st.markdown('<div class="pfma-progress">', unsafe_allow_html=True)
    for key, label in PFMA_STEPS:
        status = step_status(current_step, key)
        cls = "pfma-progress__step"
        if status == "active":
            cls += " pfma-progress__step--active"
        elif status == "done":
            cls += " pfma-progress__step--done"
        st.markdown(f'<div class="{cls}">{label}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def go_to_step(step_key: str) -> None:
    target = STEP_TO_PAGE.get(step_key)
    if not target:
        return
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()


def next_step_key(current_step: str) -> str | None:
    idx = step_index(current_step)
    if idx + 1 < len(PFMA_STEPS):
        return PFMA_STEPS[idx + 1][0]
    return None


def prev_step_key(current_step: str) -> str | None:
    idx = step_index(current_step)
    if idx > 0:
        return PFMA_STEPS[idx - 1][0]
    return None


def segmented_control(label: str, options: Sequence[str], *, key: str, default: str | None = None) -> str | None:
    state_key = f"pfma_segment_{key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = default
    st.markdown(f'<div class="pfma-field-label">{label}</div>', unsafe_allow_html=True)
    st.markdown('<div class="pfma-pill-group sn-segmented">', unsafe_allow_html=True)
    choice = st.radio("", options, index=None, key=state_key, horizontal=True, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    return choice


def chip_multiselect(
    label: str,
    options: Sequence[str],
    *,
    key: str,
    default: Iterable[str] | None = None,
) -> list[str]:
    state_key = f"pfma_chip_{key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = list(default or [])
    selected = list(st.session_state[state_key])
    st.markdown(f'<div class="pfma-field-label">{label}</div>', unsafe_allow_html=True)
    chips = st.multiselect("", options, selected, key=state_key + "_multi", label_visibility="collapsed")
    st.session_state[state_key] = chips
    return chips


def ensure_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            return None
    return None


@dataclass
class DrawerResult:
    saved: bool
    payload: Dict[str, Any]
    next_step: str | None
    previous_step: str | None


def render_drawer(
    *,
    step_key: str,
    title: str,
    badge: str,
    description: str,
    body: Callable[[dict[str, Any]], Dict[str, Any]],
    footer_note: str | None = None,
) -> DrawerResult:
    apply_pfma_theme()
    state = ensure_pfma_state()
    render_header()
    render_progress(step_key)

    st.markdown('<div class="pfma-drawer">', unsafe_allow_html=True)
    st.markdown('<div class="pfma-drawer__header">', unsafe_allow_html=True)
    st.markdown(f'<div class="pfma-drawer__title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pfma-drawer__badge">{badge}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="margin:0;color:var(--ink-muted);">{description}</p>', unsafe_allow_html=True)

    why_state_key = f"pfma_why_{step_key}"
    if why_state_key not in st.session_state:
        st.session_state[why_state_key] = False
    if st.button("Why this?", key=f"pfma_why_button_{step_key}"):
        st.session_state[why_state_key] = not st.session_state[why_state_key]

    advisor_toggle_key = f"pfma_sidebar_{step_key}"
    ask = st.sidebar.checkbox("Ask Advisor", key=advisor_toggle_key, help="Get a warm nudge on why this info matters.")
    if ask:
        st.sidebar.info(
            f"Your advisor uses the {title.split(' ')[0].lower()} details to spot safety or planning opportunities early."
        )

    if st.session_state[why_state_key]:
        st.info(
            "Our AI Advisor says: capturing this section means your concierge can personalize next steps and avoid duplicate"
            " questions on the call."
        )

    container = st.container()
    with container:
        payload = body(state)

    saved = False
    next_key = next_step_key(step_key)
    prev_key = prev_step_key(step_key)

    st.markdown('<div class="pfma-sticky-nav">', unsafe_allow_html=True)
    st.markdown('<div class="pfma-nav-inner">', unsafe_allow_html=True)

    if footer_note:
        st.markdown(f'<div class="pfma-note">{footer_note}</div>', unsafe_allow_html=True)
    else:
        st.empty()

    st.markdown('<div class="pfma-nav-actions">', unsafe_allow_html=True)
    if prev_key:
        if st.button("Back", key=f"pfma_prev_{step_key}"):
            go_to_step(prev_key)
    save_label = "Save + Continue" if next_key else "Save"
    save_button = st.button(save_label, key=f"pfma_save_{step_key}", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if save_button:
        saved = True

    return DrawerResult(saved=saved, payload=payload, next_step=next_key, previous_step=prev_key)


def update_section(step_key: str, payload: Dict[str, Any]) -> None:
    state = ensure_pfma_state()
    section = state["sections"].setdefault(step_key, {"complete": False, "data": {}})
    section["data"] = payload
    section["complete"] = True
    dossier = st.session_state.setdefault("dossier", {})
    dossier.setdefault("pfma", {})[step_key] = payload
    mark_step_complete(step_key)
    set_badges_from_progress()


def set_badges_from_progress() -> None:
    state = ensure_pfma_state()
    completion_ratio = sum(1 for key in DRAWER_KEYS if state["sections"].get(key, {}).get("complete")) / max(
        len(DRAWER_KEYS), 1
    )
    unlocked = int(round(completion_ratio * len(DUCK_BADGES)))
    for idx, duck in enumerate(DUCK_BADGES):
        state["badges"][duck] = idx < unlocked


def build_export_payloads() -> tuple[BytesIO, BytesIO]:
    state = ensure_pfma_state()
    dossier = st.session_state.get("dossier", {}).get("pfma", {})
    csv_lines = ["section,key,value"]
    for section, payload in dossier.items():
        for key, value in payload.items():
            sanitized = str(value).replace('"', '""')
            csv_lines.append(f'{section},{key},"{sanitized}"')
    csv_bytes = "\n".join(csv_lines).encode("utf-8")
    csv_buffer = BytesIO(csv_bytes)

    pdf_text = ["Plan for My Advisor", "----------------------", ""]
    for section, payload in dossier.items():
        pdf_text.append(section.replace("_", " ").title())
        for key, value in payload.items():
            pdf_text.append(f" - {key}: {value}")
        pdf_text.append("")
    pdf_buffer = BytesIO("\n".join(pdf_text).encode("utf-8"))
    return pdf_buffer, csv_buffer


def duck_parade() -> None:
    state = ensure_pfma_state()
    st.markdown('<div class="pfma-duck-parade">', unsafe_allow_html=True)
    for duck in DUCK_BADGES:
        icon = "🟡" if state["badges"].get(duck) else "⚪"
        st.markdown(f"<span title='{duck}'>{icon}</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

