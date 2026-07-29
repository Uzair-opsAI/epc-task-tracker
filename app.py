import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import get_tasks
from database import get_projects
from database import get_employees
from pages.activity_manager import show as activity_page
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

    st.title("🏗 Kent EPC Project Tracker")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        project = st.selectbox(
            "Project",
            [
                "BP - Duqm Refinery",
                "Shell",
                "Reliance",
                "ONGC"
            ]
        )

    with col2:
        office = st.selectbox(
            "Office",
            [
                "All",
                "Vadodara",
                "Mumbai"
            ]
        )

    with col3:
        discipline = st.selectbox(
            "Discipline",
            [
                "All",
                "Electrical",
                "Mechanical",
                "Civil",
                "Instrumentation",
                "Process"
            ]
        )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)
    tasks = get_tasks()

    completed = len(tasks[tasks["Status"] == "Completed"])

    progress = len(tasks[tasks["Status"] == "In Progress"])
    
    # Convert Planned Finish column into dates
    tasks["Planned Finish"] = pd.to_datetime(
        tasks["Planned Finish"]
    ).dt.date
    
    today = datetime.today().date()
    
    # Automatically calculate overdue activities
    overdue = len(
        tasks[
            (tasks["Planned Finish"] < today)
            &
            (tasks["Status"] != "Completed")
        ]
    )
    
    # Activities due within the next 7 days
    next_week = today + timedelta(days=7)
    
    due_this_week = len(
        tasks[
            (tasks["Planned Finish"] >= today)
            &
            (tasks["Planned Finish"] <= next_week)
        ]
    )

    c1.metric("📋 Total Activities", len(tasks))

    c2.metric("🟢 Completed", completed)
    
    c3.metric("🟡 In Progress", progress)
    
    c4.metric("🔴 Overdue", overdue)
    
    c5.metric("🟠 Due This Week", due_this_week)
    
    c6.metric(
        "📈 Average Progress",
        f"{tasks['Progress'].mean():.0f}%"
    )
    st.markdown("---")

# -------------------------------------------------
# TASKS
# -------------------------------------------------
elif page == "📋 Tasks":

    activity_page()
# -------------------------------------------------
# ANALYTICS
# -------------------------------------------------
elif page == "📊 Analytics":

    st.title("📊 Analytics")

    st.info("Coming in Module 4")

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
