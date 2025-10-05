import streamlit as st
def goto(page: str):
    st.switch_page(f"pages/cost_planner_v2/{page}")
