from __future__ import annotations
from typing import Any, Dict
import streamlit as st

CP_KEY = "cp"

DEFAULTS = {
    "meta": {"planner_mode": None, "authed": False},
    "qualifiers": {
        "has_partner": "No partner",
        "owns_home": False,
        "is_veteran": False,
        "care_setting": None,
        "partner_maintaining_home": False,
    },
    "setting_cost": {
        "care_setting": None,
        "home_hours": 4,
        "room_type": "Studio",
        "care_level": "Low",
        "chronic_conditions": [],
        "mobility": "Low",
        "monthly_cost": 0,
    },
    "income": {
        "social_security_person_a": 0,
        "pension_person_a": 0,
        "other_income_monthly_person_a": 0,
        "social_security_person_b": 0,
        "pension_person_b": 0,
        "other_income_monthly_person_b": 0,
        "income_total": 0,
    },
    "expenses": {
        "optional_utilities": 0,
        "optional_phone_internet": 0,
        "optional_life_insurance": 0,
        "optional_transportation": 0,
        "optional_auto": 0,
        "optional_auto_insurance": 0,
        "monthly_debt_payments": 0,
        "optional_other": 0,
        "facility_move_adjustment": True,
        "other_monthly_total": 0,
    },
    "caregiver": {
        "caregiver_type": "None",
        "include_caregiver_cost": True,
        "caregiver_cost": 0,
    },
    "benefits": {
        "va_estimate_person_a": 0,
        "va_estimate_person_b": 0,
        "ltc_daily_benefit_person_a": 0,
        "ltc_daily_benefit_person_b": 0,
        "medicaid_status": "Unsure",
        "benefits_total": 0,
    },
    "home": {
        "sale_price": 0,
        "home_monthly_total": 0,
        "reverse_mortgage_active": False,
        "reverse_mortgage_income": 0,
    },
    "liquidity": {
        "planning_to_sell": False,
        "car_sale_value": 0,
        "furniture_sale_value": 0,
        "other_sale_value": 0,
        "keeping_car": True,
        "liquidity_total": 0,
    },
    "home_mods": {
        "home_mods_needed": "None",
        "home_mods_budget": 0,
        "amortize_mods": False,
        "mods_monthly_total": 0,
    },
    "assets": {
        "cash_savings": 0,
        "brokerage_taxable": 0,
        "ira_total": 0,
        "home_equity": 0,
        "other_assets": 0,
        "assets_total_effective": 0,
    },
    "timeline": {
        "monthly_all_in": 0,
        "gap": 0,
        "runway_months": None,
    },
    "progress": {
        "landing_complete": False,
        "income_complete": False,
        "expenses_complete": False,
        "caregiver_complete": False,
        "benefits_complete": False,
        "home_complete": False,
        "liquidity_complete": False,
        "home_mods_complete": False,
        "assets_complete": False,
        "timeline_ready": False,
    },
}

def ensure_cp() -> Dict[str, Any]:
    cp = st.session_state.setdefault(CP_KEY, {})
    def deepseed(dst, src):
        for k, v in src.items():
            if isinstance(v, dict):
                deepseed(dst.setdefault(k, {}), v)
            else:
                dst.setdefault(k, v)
        return dst
    return deepseed(cp, DEFAULTS)

def cp_get(*path, default=None):
    cp = ensure_cp()
    cur = cp
    for p in path:
        cur = cur.get(p, {})
    return cur if cur != {} else default

def cp_set(path, value):
    cp = ensure_cp()
    cur = cp
    for p in path[:-1]:
        cur = cur.setdefault(p, {})
    cur[path[-1]] = value
