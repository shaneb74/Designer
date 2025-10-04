"""Guided Care Plan recommendation page with Medicaid-aware off-ramp."""
from __future__ import annotations

import streamlit as st

from audiencing import ensure_audiencing_state
from guided_care_plan import ensure_gcp_session, evaluate_guided_care, get_question_meta, render_stepper
from guided_care_plan.state import current_audiencing_snapshot
from ui.theme import inject_theme


def _safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()


inject_theme()
st.markdown('<div class="sn-scope gcp">', unsafe_allow_html=True)


def _ensure_care_context():
    return st.session_state.setdefault(
        "care_context",
        {
            "person_name": "Your Loved One",
            "gcp_answers": {},
            "gcp_recommendation": None,
            "gcp_cost": None,
        },
    )


def _render_chronic_selector(current_values):
    meta = get_question_meta("chronic")
    options = meta.get("options", [])
    option_map = {opt["value"]: opt.get("label", opt["value"]) for opt in options}
    values = list(option_map.keys())
    default = current_values or (["none"] if "none" in values else [])
    with st.form("gcp_chronic_conditions_form"):
        selections = st.multiselect(
            meta.get("label", "Any chronic conditions?"),
            options=values,
            default=default,
            format_func=lambda value: option_map.get(value, value),
            help=meta.get("description"),
        )
        submitted = st.form_submit_button("Refresh recommendation", type="primary")
    return submitted, selections


answers, gcp_result = ensure_gcp_session()
care_context = _ensure_care_context()
aud_state = ensure_audiencing_state()
snapshot = current_audiencing_snapshot()

answers.pop("chronic_conditions", None)

has_result = bool(gcp_result.get("recommended_setting"))
stepper_placeholder = st.empty()
with stepper_placeholder.container():
    render_stepper(5 if has_result else 4)

st.title("Guided Care Plan - Recommendation")
st.caption("Confirm medical context so we can finalize the guidance and directional next steps.")

submitted, selections = _render_chronic_selector(answers.get("chronic"))

if submitted:
    chosen = list(selections or [])
    if "none" in chosen:
        if len(chosen) == 1:
            answers["chronic"] = ["none"]
        else:
            answers["chronic"] = []
    else:
        answers["chronic"] = chosen
    result = evaluate_guided_care(answers, aud_state)
    gcp_result.update(result)
    gcp_result["audiencing_snapshot"] = snapshot
    st.session_state["gcp"] = gcp_result
    care_context["gcp_answers"] = answers
    care_context["gcp_recommendation"] = result["recommended_setting"]
    care_context["gcp_cost"] = result.get("care_intensity")
    st.success("Recommendation updated.")
    has_result = True
    stepper_placeholder.empty()
    with stepper_placeholder.container():
        render_stepper(5)

if has_result:
    recommendation = gcp_result["recommended_setting"]
    intensity = gcp_result.get("care_intensity")
    safety_flags = gcp_result.get("safety_flags", [])
    chronic_conditions = gcp_result.get("chronic_conditions", [])
    decision_trace = gcp_result.get("DecisionTrace", []) or []
    payment_context = gcp_result.get("payment_context") or "private"
    funding_choice = answers.get("funding_confidence")
    chronic_labels = {
        opt["value"]: opt.get("label", opt["value"])
        for opt in get_question_meta("chronic").get("options", [])
    }

    friendly_setting = {
        "home": "Stay at home with in-home support",
        "assisted": "Assisted living support",
        "memory": "Memory care support",
    }.get(recommendation, recommendation)

    intensity_copy = {
        "low": "Low support needs",
        "med": "Moderate support needs",
        "high": "High support needs",
    }.get(intensity, intensity)

    st.markdown("---")

    if payment_context == "medicaid":
        st.markdown(
            """
            <div style="background:#e0f2fe;border:1px solid #bae6fd;padding:1rem;border-radius:12px;margin-bottom:1.2rem;">
                <strong>Medicaid/state assistance detected.</strong>
                Medicaid changes how care is paid for. We'll point you to advisor support designed for Medicaid families.
            </div>
            """,
            unsafe_allow_html=True,
        )
        gate_state = st.session_state.setdefault("gate", {})
        gate_state["medicaid_offramp_shown"] = True

    st.subheader("Your personalized recommendation")
    st.markdown(f"### {friendly_setting}")
    if intensity_copy:
        st.caption(intensity_copy)

    if safety_flags:
        st.markdown("#### Safety watchpoints")
        for flag in safety_flags:
            label = flag.replace("_", " ").title()
            st.write(f"⚠️ {label}")

    if chronic_conditions:
        st.markdown("#### Chronic conditions to plan for")
        if chronic_conditions == ["none"]:
            st.write("No chronic conditions noted.")
        else:
            friendly = [
                chronic_labels.get(cond, cond.replace("_", " ").title())
                for cond in chronic_conditions
            ]
            st.write(", ".join(friendly))

    if decision_trace:
        st.markdown("#### DecisionTrace")
        for step in decision_trace:
            st.write(f"• {step}")

    st.markdown("---")

    if payment_context == "medicaid":
        primary_label = "Continue to Plan for My Advisor →"
        primary_destination = "pages/pfma.py"
        primary_type = "primary"
        secondary_label = "View Cost Planner (optional, private-pay only)"
        secondary_destination = "pages/cost_planner.py"
        secondary_type = "secondary"
    else:
        primary_label = "Continue to Cost Planner →"
        primary_destination = "pages/cost_planner.py"
        primary_type = "primary"
        secondary_label = "Connect with an advisor"
        secondary_destination = "pages/pfma.py"
        secondary_type = "secondary"

    if payment_context == "private" and funding_choice in {"unsure", "not_confident"}:
        st.markdown(
            """
            <div style="background:#fef3c7;border:1px solid #facc15;padding:1rem;border-radius:12px;margin-bottom:1.2rem;">
                <strong>Not sure about paying for care?</strong>
                We can walk through funding strategies in the Cost Planner before you make any commitments.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button(primary_label, type=primary_type, use_container_width=True):
        _safe_switch_page(primary_destination)

    if st.button(secondary_label, type=secondary_type, use_container_width=True):
        _safe_switch_page(secondary_destination)

with st.expander("Debug: GCP snapshot", expanded=False):
    st.json({"answers": answers, "gcp": gcp_result})

st.markdown('</div>', unsafe_allow_html=True)

