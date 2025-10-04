from __future__ import annotations
"""Contextual Welcome - clean layout (no tall canvas), left text / right image, solid gating."""

import base64, mimetypes
from pathlib import Path
import streamlit as st

# --- theme fallback (keeps app running even if theme import fails) ---
try:
    from ui.theme import inject_theme  # type: ignore
except Exception:  # pragma: no cover
    def inject_theme() -> None:
        st.markdown(
            """
            <style>
/* Force Streamlit body to center content */
main > div {
    display: flex;
    justify-content: center;  /* horizontal centering */
    align-items: center;      /* vertical centering */
    min-height: 100vh;        /* full viewport height */
}

/* Optional: center the block-container specifically */
.block-container {
    margin: auto;
}

              .block-container{max-width:1160px;padding-top:8px;}
              header[data-testid="stHeader"]{background:transparent;}
              footer{visibility:hidden;}
            </style>
            """,
            unsafe_allow_html=True,
        )

IMAGE_MAP = {
    "self": "static/images/contextual_welcome_self.png",
    "proxy": "static/images/contextual_welcome_someone_else.png",
}
COPY = {
    "self": {
        "headline": "We are here to help you find the support you are looking for.",
        "name_placeholder": "What is your name?",
        "pill_left": "For someone",
        "pill_right": "For me",
    },
    "proxy": {
        "headline": "We are here to help you find the support your loved ones need.",
        "name_placeholder": "What is their name?",
        "pill_left": "For someone",
        "pill_right": "For me",
    },
}
RELATIONSHIP_CHOICES = [
    ("parent", "Parent"),
    ("spouse", "Spouse/Partner"),
    ("child", "Adult Child"),
    ("sibling", "Sibling"),
    ("relative", "Other Relative"),
    ("friend", "Friend/Neighbor"),
    ("caregiver", "Professional Caregiver"),
    ("poa_cm", "POA / Case Manager"),
    ("other", "Other"),
    ("unknown", "Prefer not to say"),
]

def _data_uri(path_str: str) -> str | None:
    try:
        p = Path(path_str)
        if not p.exists():
            return None
        b = p.read_bytes()
        ext = p.suffix.lower()
        mime = mimetypes.types_map.get(ext, "image/png")
        return f"data:{mime};base64,{base64.b64encode(b).decode('ascii')}"
    except Exception:
        return None

def _safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()

def _inject_page_css() -> None:
    st.markdown(
        """
        <style>
/* Force Streamlit body to center content */
main > div {
    display: flex;
    justify-content: center;  /* horizontal centering */
    align-items: center;      /* vertical centering */
    min-height: 100vh;        /* full viewport height */
}

/* Optional: center the block-container specifically */
.block-container {
    margin: auto;
}

          /* Ensure full viewport height for all parent containers */
          body, html, .stApp, section.main {
            height: 100vh;
            margin: 0;
            padding: 0;
            overflow: hidden;
          }
          /* Center the main content area absolutely */
          section.main:has(.cw-wrap-marker) > div.block-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            min-height: auto !important;
            background-color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            max-width: 1160px;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
          }
          /* Remove extra vertical spacing wrappers on this page */
          section.main:has(.cw-wrap-marker) [data-testid="stVerticalBlock"] {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
          }

          /* Ghost bar removal + tidy input look (safe globally) */
          .stTextInput > div > div {
            background: transparent !important;
            box-shadow: none !important;
          }
          .stTextInput input {
            background: #ffffff !important;
            border: 1px solid rgba(15,23,42,.12) !important;
            border-radius: 10px !important;
            height: 44px !important;
          }

          /* Headline spacing */
          .cw-headline { margin: 0 0 12px 0; font-size: 1.6rem; line-height: 1.25; }

          /* Pills row */
          .pill-row { display: flex; gap: 10px; margin: 10px 0 14px; }
          .pill-row .stButton>button {
            height: 36px; border-radius: 999px; padding: 6px 16px; font-weight: 700;
            width: auto !important;
          }

          /* Inline row for name + continue */
          .name-row { display: flex; gap: 12px; align-items: center; margin: 8px 0 4px; }
          .name-row .stButton>button {
            height: 44px; border-radius: 10px; font-weight: 700; min-width: 160px;
          }

          /* Keep image to the right, text wraps naturally on the left */
          .cw-image img {
            display: block; width: 100%; height: auto; border-radius: 12px;
            transform: rotate(-3deg);
            filter: drop-shadow(0 22px 40px rgba(0,0,0,.18));
          }

          @media (max-width: 980px) {
            .name-row { flex-direction: column; align-items: stretch; }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render(which: str = "you") -> None:
    inject_theme()
    st.set_page_config(page_title="Contextual Welcome", layout="wide")

    # Which flow?
    entry = "self" if str(which).lower() in ("you", "self", "me") else "proxy"
    copy = COPY[entry]
    img_src = IMAGE_MAP.get(entry, "")

    # Session state
    if "aud" not in st.session_state:
        st.session_state.aud = {
            "entry": entry,
            "recipient_name": None,
            "proxy_name": None,
            "relationship_code": None,
            "relationship_label": None,
            "relationship_other": None,
            "qualifiers": {},
        }
    aud = st.session_state.aud
    aud["entry"] = entry

    _inject_page_css()

    # Marker so CSS is scoped to THIS page only
    st.markdown('<div class="cw-wrap-marker"></div>', unsafe_allow_html=True)

    # Two-column layout: text left, image right (no overlap)
    left, right = st.columns([1, 1])

    with left:
        # Headline
        st.markdown(f'<div class="cw-headline">{copy["headline"]}</div>', unsafe_allow_html=True)

        # Name input (single widget)
        name_key = "cw_name_self" if entry == "self" else "cw_name_proxy"
        name_ph = copy["name_placeholder"]
        name_val = aud.get("recipient_name") or ""
        name = st.text_input(name_ph, value=name_val, key=name_key, label_visibility="collapsed").strip()
        aud["recipient_name"] = name or aud.get("recipient_name")

        # Relationship (proxy flow), progressive after name
        if entry == "proxy" and (aud.get("recipient_name") or "").strip():
            labels = [label for _, label in RELATIONSHIP_CHOICES]
            default_idx = labels.index(aud["relationship_label"]) if aud.get("relationship_label") in labels else 0
            rel_label = st.selectbox(
                f"What's your relationship to {aud['recipient_name'] or 'them'}?",
                labels,
                index=default_idx,
                key="cw_relationship",
            )
            code_lookup = {label: code for code, label in RELATIONSHIP_CHOICES}
            aud["relationship_label"] = rel_label
            aud["relationship_code"] = code_lookup.get(rel_label)
            if aud["relationship_code"] == "other":
                aud["relationship_other"] = st.text_input(
                    "Briefly describe the relationship",
                    value=aud.get("relationship_other") or "",
                    key="cw_relationship_other",
                    label_visibility="collapsed",
                )
            else:
                aud["relationship_other"] = None
        elif entry == "proxy":
            aud["relationship_label"] = None
            aud["relationship_code"] = None
            aud["relationship_other"] = None

        # Gating
        name_ok = bool((aud.get("recipient_name") or "").strip())
        rel_ok = True if entry == "self" else bool(aud.get("relationship_code"))
        can_continue = name_ok and rel_ok

        # Continue
        st.markdown('<div class="name-row">', unsafe_allow_html=True)
        if st.button("Continue", key="cw_continue", use_container_width=False, disabled=not can_continue):
            if not aud.get("recipient_name"):
                aud["recipient_name"] = "You" if entry == "self" else "Your Loved One"
            _safe_switch_page("ui/pages/hub.py")
        st.markdown('</div>', unsafe_allow_html=True)

        # Helper captions
        if not name_ok:
            st.caption("Please enter a name to continue.")
        elif entry == "proxy" and not rel_ok:
            st.caption("Select your relationship to continue.")

    with right:
        # Image on the right, no overlap
        if img_src and not img_src.startswith(("http://", "https://", "data:")):
            img_src = _data_uri(img_src) or ""
        if img_src:
            st.markdown('<div class="cw-image">', unsafe_allow_html=True)
            st.markdown(f'<img src="{img_src}" alt="collage">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)