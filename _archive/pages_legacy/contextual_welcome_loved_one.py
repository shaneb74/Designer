# pages/contextual_welcome_loved_one.py
try:
    from pages.contextual_welcome_base import render  # Streamlit package import
except Exception:
    from contextual_welcome_base import render        # fallback when executed directly
render("loved")
