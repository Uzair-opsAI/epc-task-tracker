import streamlit as st
from components.styles import load_css
from datetime import datetime

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Kent EPC Project Tracker",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# ==========================================================
# HEADER
# ==========================================================

st.title("🏗 Kent EPC Project Tracker")

st.caption(
    "AI-Powered EPC Engineering Project Controls & Activity Management System"
)

st.divider()

# ==========================================================
# WELCOME SECTION
# ==========================================================

left, right = st.columns([2, 1])

with left:

    st.markdown(
        """
### Welcome

This application is designed to help engineering teams manage:

- 📋 Engineering Activities
- 📊 Project Analytics
- 🏗 Project Monitoring
- 👷 Resource Allocation
- 📈 Executive Reporting
- 📅 Schedule Tracking

Use the navigation panel on the left to access each module.
"""
    )

with right:

    st.success("🟢 Google Sheets Connected")

    st.info(
        f"Last Opened\n\n{datetime.now().strftime('%d %b %Y %H:%M')}"
    )

st.divider()

# ==========================================================
# MODULES
# ==========================================================

st.subheader("📦 Available Modules")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
### 📊 Dashboard

Executive project overview

- KPI Dashboard
- Project Health
- Schedule Monitoring
- Progress Overview
"""
    )

    st.markdown(
        """
### 📋 Activity Manager

Manage engineering activities

- Activity Register
- Add Activities
- Search & Filter
- Export Data
"""
    )

    st.markdown(
        """
### 📈 Analytics

Interactive project analytics

- Charts
- Trends
- Workload Analysis
- Executive Insights
"""
    )

with col2:

    st.markdown(
        """
### 🚧 Coming Soon

- 🏗 Project Register
- 👷 Employee Management
- 📄 Reports
- 📅 Gantt Chart
- ⚠ Risk Register
- 📁 Document Register
"""
    )

st.divider()

# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

st.subheader("ℹ System Information")

info1, info2, info3 = st.columns(3)

with info1:

    st.metric(
        "Application",
        "Kent EPC Tracker"
    )

with info2:

    st.metric(
        "Version",
        "2.0"
    )

with info3:

    st.metric(
        "Backend",
        "Google Sheets"
    )

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

left, right = st.columns([3, 1])

with left:

    st.caption(
        "Developed for Kent PLC • Electrical Engineering Digitalisation Initiative"
    )

with right:

    st.caption(
        datetime.now().strftime("%d %b %Y")
    )
