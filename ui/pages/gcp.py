import streamlit as st
from senior_nav.components.choice_chips import choice_single
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section
from senior_nav.components import buttons


def _init_state():
    st.session_state.setdefault("gcp_answers", {})
    st.session_state.setdefault("gcp_status", "in_progress")


def main():
    _init_state()
    gcp_header(0)           # section 1 of 5
    buttons.page_start()    # scope button CSS to this page

    answers = st.session_state["gcp_answers"]

    def form():
        with st.form("gcp_intro_form"):
            st.subheader("Financial Eligibility")
            medicaid_choice = choice_single(
                "Are you currently on Medicaid or receiving state long-term care assistance?",
                ["yes", "no", "unsure"],
                value=answers.get("medicaid_status", "no"),
                key="gcp_medicaid_status",
            )
            answers["medicaid_status"] = medicaid_choice

            if medicaid_choice != "yes":
                st.subheader("Financial Confidence")
                funding_choice = choice_single(
                    "How confident do you feel about paying for care?",
                    ["no_worries", "confident", "unsure", "not_confident"],
                    value=answers.get("funding_confidence", "unsure"),
                    key="gcp_funding_confidence",
                )
                answers["funding_confidence"] = funding_choice
            else:
                st.info(
                    "Medicaid changes how care is paid. We’ll still show a care recommendation, "
                    "then guide the next step."
                )
                funding_choice = answers.get("funding_confidence")

            # persist answers
            st.session_state["gcp_answers"] = answers

            start_disabled = (medicaid_choice is None) or (
                medicaid_choice != "yes" and not funding_choice
            )

            st.markdown('<div data-variant="primary">', unsafe_allow_html=True)
            go = st.form_submit_button(
                "Continue to Daily Life & Support",
                type="primary",
                use_container_width=True,
                disabled=start_disabled,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            if go:
                safe_switch_page("ui/pages/gcp_daily_life.py")

    gcp_section("Guided Care Plan", "Financial", form)

    # bottom nav rendered outside the section to keep button interactions working
    st.markdown('<div data-variant="secondary">', unsafe_allow_html=True)
    if st.button("Return to Hub", use_container_width=True, key="gcp_return_hub"):
        safe_switch_page("ui/pages/hub.py")
    st.markdown("</div>", unsafe_allow_html=True)

    buttons.page_end()


if __name__ == "__main__":
    main()