import streamlit as st
from datetime import datetime

# ==========================================================
# IMPORT PAGES
# ==========================================================

from pages.dashboard import show as dashboard_page
from pages.activity_manager import show as activity_page
from pages.analytics import show as analytics_page

# ==========================================================
# GLOBAL STYLES
# ==========================================================

from components.styles import load_css

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
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        # 📋 Kent EPC Tracker
        """
    )

    st.caption(
        "Engineering Project Controls"
    )

    st.divider()

    st.subheader("Navigation")

    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):
        st.session_state.page = "Dashboard"

    if st.button(
        "📋 Activity Manager",
        use_container_width=True
    ):
        st.session_state.page = "Activity Manager"

    if st.button(
        "📊 Analytics",
        use_container_width=True
    ):
        st.session_state.page = "Analytics"

    st.divider()

    st.subheader("Application")

    st.caption("Kent PLC")

    st.caption("Version 2.0")

    st.caption(
        datetime.now().strftime("%d %b %Y")
    )

# ==========================================================
# PAGE ROUTER
# ==========================================================

page = st.session_state.page
# ==========================================================
# GLOBAL HEADER
# ==========================================================

header_left, header_right = st.columns([5, 1])

with header_left:

    st.title("🏗 Kent EPC Project Tracker")

    st.caption(
        "Executive Project Controls Dashboard"
    )

with header_right:

    st.metric(
        "Refresh",
        datetime.now().strftime("%H:%M")
    )

st.divider()

# ==========================================================
# PAGE ROUTER
# ==========================================================

if page == "Dashboard":

    dashboard_page()

elif page == "Activity Manager":

    activity_page()

elif page == "Analytics":

    analytics_page()

# ==========================================================
# FUTURE MODULES
# ==========================================================

elif page == "Settings":

    st.title("⚙ Settings")

    st.info(
        "Settings module will be available in the next version."
    )

elif page == "About":

    st.title("ℹ About")

    st.markdown(
        """
### Kent EPC Project Tracker

Version **2.0**

Developed for:

- Engineering Project Controls
- EPC Activity Tracking
- Portfolio Analytics
- Engineering Resource Management

Backend

- Google Sheets

Framework

- Streamlit

Visualization

- Plotly

Developer

Electrical Engineering Digitalisation Initiative
"""
    )

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

footer1, footer2 = st.columns([3, 1])

with footer1:

    st.caption(
        "Kent PLC • EPC Project Controls Platform • Version 2.0"
    )

with footer2:

    st.caption(
        datetime.now().strftime("%d %b %Y")
    )
