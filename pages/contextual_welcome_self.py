try:
    from pages.contextual_welcome_base import render
except Exception:
    from contextual_welcome_base import render
render("you")
