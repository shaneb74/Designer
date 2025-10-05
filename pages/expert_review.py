"""Cost Planner · Expert Review (finish screen + PFMA handoff)."""
from __future__ import annotations

import streamlit as st

# --- Theme / CP template hooks (works with your shim) ---
try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
        render_nav_buttons,
        render_metrics,
        Metric,
        NavButton,
        card,  # optional; present in your shim
    )
except Exception:
    # Minimal fallbacks so this page never crashes if helpers move
    def apply_cost_planner_theme() -> None:
        st.markdown(
            """
            <style>
              :root{
                --brand:#0B5CD8; --paper:#fff; --surface:#f6f8fa;
                --ink:#111418; --ink-muted:#6b7280; --radius:14px;
              }
              .sn-card{background:var(--surface);border:1px solid rgba(0,0,0,.08);
                       border-radius:var(--radius);padding:clamp(1rem,2vw,1.5rem);}
            </style>
            """,
            unsafe_allow_html=True,
        )
    from contextlib import contextmanager
    @contextmanager
    def cost_planner_page_container():
        yield
    def render_app_header(): st.markdown("### Expert Review")
    def render_wizard_hero(title: str, subtitle: str = ""):
        st.markdown(f"## {title}")
        if subtitle: st.caption(subtitle)
    def render_wizard_help(text: str): st.info(text)
    def render_metrics(items): 
        cols = st.columns(len(items))
        for col, m in zip(cols, items):
            with col: st.metric(m.title, m.value)
    class Metric: 
        def __init__(self, title: str, value: str): self.title, self.value = title, value
    class NavButton:
        def __init__(self, label: str, key: str, type: str = "secondary", icon: str | None = None):
            self.label, self.key, self.type, self.icon = label, key, type, icon
    def render_nav_buttons(buttons=None, prev=None, next=None):
        # simple 2-button layout fallback
        if buttons is None:
            buttons = [prev, next]
        try:
            seq = [b for b in buttons if b]
        except Exception:
            seq = [buttons]
        clicked = None
        cols = st.columns(len(seq)) if seq else []
        for i, nb in enumerate(seq):
            if not nb: continue
            label = (nb.icon + " " if getattr(nb, "icon", None) else "") + nb.label
            args = {}
            if getattr(nb, "type", "") == "primary": args["type"] = "primary"
            with cols[i]:
                if st.button(label, key=nb.key, **args):
                    clicked = nb.key
        return clicked
    @contextmanager
    def card(**style):
        st.markdown('<div class="sn-card">', unsafe_allow_html=True)
        try: yield
        finally: st.markdown("</div>", unsafe_allow_html=True)

# --- Begin page ---
apply_cost_planner_theme()

# Expect Cost Planner state already set up by prior pages;
# keep this page resilient if user lands here directly.
cp = st.session_state.setdefault("cost_planner", {
    "monthly_total": 0,
    "subtotals": {"offsets": 0},
    "net_out_of_pocket": 0,
    "notes": "",
})

with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        "Expert Review",
        "Double-check the plan, then book your concierge advisor to walk the plan into action."
    )

    # Optional: top-line metrics (safe placeholders if numbers missing)
    mt = cp.get("monthly_total", 0)
    offs = cp.get("subtotals", {}).get("offsets", 0)
    oop = cp.get("net_out_of_pocket", 0)
    try:
        mt_val = f"${mt:,.0f}"
        offs_val = f"-${offs:,.0f}"
        oop_val = f"${oop:,.0f}"
    except Exception:
        mt_val, offs_val, oop_val = str(mt), str(offs), str(oop)

    render_metrics([
        Metric("Monthly costs", mt_val),
        Metric("Offsets", offs_val),
        Metric("Net out-of-pocket", oop_val),
    ])

    # Summary card (feel free to customize with real content)
    with card():
        st.markdown("#### Summary & notes")
        st.write(
            cp.get("notes") or
            "This section can show key assumptions, services, and any offsets applied. "
            "You can edit modules or go back to adjust inputs before booking."
        )

    render_wizard_help(
        "Happy with the numbers? Book your concierge call. "
        "You'll get a confirmation and your advisor will call within 24 hours."
    )

    st.markdown("---")

    # Final CTA: review vs. book
    clicked = render_nav_buttons(
        [
            NavButton("Review again", "cp_review_again"),
            NavButton("Book my advisor call", "cp_to_pfma", type="primary", icon="📞"),
        ]
    )

    if clicked == "cp_review_again":
        # Point to your "overview" page for deeper edits.
        st.switch_page("pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
    elif clicked == "cp_to_pfma":
        # Definitive handoff to PFMA flow
        st.switch_page("pages/pfma.py")