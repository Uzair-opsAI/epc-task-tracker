import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta

from components.styles import load_css

from database import get_tasks


# ============================================================
# PORTFOLIO ANALYTICS
# ============================================================

def show():

    # ========================================================
    # LOAD CSS
    # ========================================================

    load_css()

    # ========================================================
    # HEADER
    # ========================================================

    st.title("📈 Portfolio Analytics")

    st.caption(
        "Engineering Portfolio Performance & Business Intelligence"
    )

    info1, info2, info3 = st.columns([2, 2, 1])

    with info1:

        st.info("Engineering Project Controls")

    with info2:

        st.success("Google Sheets Connected")

    with info3:

        st.metric(
            "Last Refresh",
            datetime.now().strftime("%H:%M")
        )

    st.divider()

    # ========================================================
    # LOAD DATA
    # ========================================================

    tasks = get_tasks()

    if tasks.empty:

        st.warning(
            "No activity data available."
        )

        st.stop()

    # ========================================================
    # DATA CLEANING
    # ========================================================

    tasks["Planned Start"] = pd.to_datetime(
        tasks["Planned Start"],
        errors="coerce"
    )

    tasks["Planned Finish"] = pd.to_datetime(
        tasks["Planned Finish"],
        errors="coerce"
    )

    tasks["Progress"] = pd.to_numeric(
        tasks["Progress"],
        errors="coerce"
    ).fillna(0)

    today = pd.Timestamp.today().normalize()

    # ========================================================
    # SIDEBAR FILTERS
    # ========================================================

    st.sidebar.header("Analytics Filters")

    project = st.sidebar.selectbox(
        "Project",
        ["All"] +
        sorted(
            tasks["Project"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    discipline = st.sidebar.selectbox(
        "Discipline",
        ["All"] +
        sorted(
            tasks["Discipline"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    status = st.sidebar.selectbox(
        "Status",
        ["All"] +
        sorted(
            tasks["Status"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    priority = st.sidebar.selectbox(
        "Priority",
        ["All"] +
        sorted(
            tasks["Priority"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    search = st.sidebar.text_input(
        "Search Activity"
    )

    # ========================================================
    # APPLY FILTERS
    # ========================================================

    filtered = tasks.copy()

    if project != "All":

        filtered = filtered[
            filtered["Project"] == project
        ]

    if discipline != "All":

        filtered = filtered[
            filtered["Discipline"] == discipline
        ]

    if status != "All":

        filtered = filtered[
            filtered["Status"] == status
        ]

    if priority != "All":

        filtered = filtered[
            filtered["Priority"] == priority
        ]

    if search:

        filtered = filtered[
            filtered.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]

    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total = len(filtered)

    completed = (
        filtered["Status"] == "Completed"
    ).sum()

    overdue = len(
        filtered[
            (filtered["Planned Finish"] < today)
            &
            (filtered["Status"] != "Completed")
        ]
    )

    avg_progress = round(
        filtered["Progress"].mean(),
        1
    )

    completion_rate = (
        round(
            (completed / total) * 100,
            1
        )
        if total
        else 0
    )

    overdue_rate = (
        round(
            (overdue / total) * 100,
            1
        )
        if total
        else 0
    )
