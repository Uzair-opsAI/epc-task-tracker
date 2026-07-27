import streamlit as st
from database import get_tasks
from database import get_projects
from database import get_employees
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

    c1, c2, c3, c4 = st.columns(4)
    tasks = get_tasks()

    completed = len(tasks[tasks["Status"] == "Completed"])
    progress = len(tasks[tasks["Status"] == "In Progress"])
    overdue = len(tasks[tasks["Status"] == "Overdue"])

    c1.metric("📋 Total Tasks", len(tasks))
    c2.metric("🟢 Completed", completed)
    c3.metric("🟡 In Progress", progress)
    c4.metric("🔴 Overdue", overdue)
    st.markdown("---")

    st.subheader("Task List")

    st.dataframe(
        tasks,
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------
# TASKS
# -------------------------------------------------
elif page == "📋 Tasks":

    st.title("📋 Task Management")

    st.info("Coming in Module 3")

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
