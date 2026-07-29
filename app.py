import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import get_tasks
from database import get_projects
from database import get_employees
from pages.activity_manager import show as activity_page
from pages.analytics import show as analytics_page
from pages.dashboard import show as dashboard_page
# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Kent EPC Tracker",
    page_icon="📋",
    layout="wide"
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("📋 Kent EPC Tracker")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📋 Tasks",
        "📊 Analytics",
        "⚙ Settings",
        "ℹ About"
    ]
)

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
if page == "🏠 Dashboard":

    dashboard_page()
# -------------------------------------------------
# TASKS
# -------------------------------------------------
elif page == "📋 Tasks":

    activity_page()
# -------------------------------------------------
# ANALYTICS
# -------------------------------------------------
elif page == "📊 Analytics":
    analytics_page()

# -------------------------------------------------
# SETTINGS
# -------------------------------------------------
elif page == "⚙ Settings":

    st.title("Settings")

    st.info("Coming in Module 5")

# -------------------------------------------------
# ABOUT
# -------------------------------------------------
elif page == "ℹ About":

    st.title("About")

    st.write("""
    **Kent EPC Project Tracker**

    Version 1.0

    Developed using

    - Streamlit

    - Google Sheets

    - GitHub

    Designed for collaborative EPC project tracking.
    """)
