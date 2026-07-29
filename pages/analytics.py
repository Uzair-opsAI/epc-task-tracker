import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from database import get_tasks


def show():

    st.title("📊 Analytics Dashboard")

    tasks = get_tasks()

    if tasks.empty:
        st.warning("No activity data available.")
        return

    # ---------------------------------------
    # Data Preparation
    # ---------------------------------------

    tasks["Planned Finish"] = pd.to_datetime(
        tasks["Planned Finish"],
        errors="coerce"
    )

    tasks["Planned Start"] = pd.to_datetime(
        tasks["Planned Start"],
        errors="coerce"
    )

    today = datetime.today()

    completed = tasks[tasks["Status"] == "Completed"]

    progress = tasks[tasks["Status"] == "In Progress"]

    overdue = tasks[
        (tasks["Planned Finish"] < today)
        &
        (tasks["Status"] != "Completed")
    ]

    due_week = tasks[
        (tasks["Planned Finish"] >= today)
        &
        (
            tasks["Planned Finish"]
            <= today + timedelta(days=7)
        )
    ]

    # ---------------------------------------
    # Sidebar Filters
    # ---------------------------------------

    st.sidebar.header("Analytics Filters")

    project = st.sidebar.selectbox(
        "Project",
        ["All"] + sorted(
            tasks["Project"].dropna().unique().tolist()
        )
    )

    discipline = st.sidebar.selectbox(
        "Discipline",
        ["All"] + sorted(
            tasks["Discipline"].dropna().unique().tolist()
        )
    )

    status = st.sidebar.selectbox(
        "Status",
        ["All"] + sorted(
            tasks["Status"].dropna().unique().tolist()
        )
    )

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

    # ---------------------------------------
    # KPI Cards
    # ---------------------------------------

    st.subheader("📈 Key Performance Indicators")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Activities",
        len(filtered)
    )

    c2.metric(
        "Completed",
        len(
            filtered[
                filtered["Status"] == "Completed"
            ]
        )
    )

    c3.metric(
        "In Progress",
        len(
            filtered[
                filtered["Status"] == "In Progress"
            ]
        )
    )

    c4.metric(
        "Average Progress",
        f"{filtered['Progress'].mean():.0f}%"
    )

    c5, c6 = st.columns(2)

    c5.metric(
        "Overdue",
        len(
            filtered[
                (filtered["Planned Finish"] < today)
                &
                (filtered["Status"] != "Completed")
            ]
        )
    )

    c6.metric(
        "Due This Week",
        len(
            filtered[
                (filtered["Planned Finish"] >= today)
                &
                (
                    filtered["Planned Finish"]
                    <= today + timedelta(days=7)
                )
            ]
        )
    )

    st.divider()

    # ---------------------------------------
    # Status Distribution
    # ---------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        status_count = (
            filtered["Status"]
            .value_counts()
            .reset_index()
        )

        status_count.columns = [
            "Status",
            "Activities"
        ]

        fig = px.pie(
            status_count,
            values="Activities",
            names="Status",
            hole=0.45,
            title="Activity Status Distribution"
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        priority_count = (
            filtered["Priority"]
            .value_counts()
            .reset_index()
        )

        priority_count.columns = [
            "Priority",
            "Activities"
        ]

        fig = px.bar(
            priority_count,
            x="Priority",
            y="Activities",
            title="Priority Distribution",
            text="Activities"
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ---------------------------------------
    # Discipline & Project Analysis
    # ---------------------------------------

    left, right = st.columns(2)

    with left:

        discipline_count = (
            filtered["Discipline"]
            .value_counts()
            .reset_index()
        )

        discipline_count.columns = [
            "Discipline",
            "Activities"
        ]

        fig = px.bar(
            discipline_count,
            x="Discipline",
            y="Activities",
            color="Activities",
            title="Activities by Discipline"
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        project_count = (
            filtered["Project"]
            .value_counts()
            .reset_index()
        )

        project_count.columns = [
            "Project",
            "Activities"
        ]

        fig = px.bar(
            project_count,
            x="Project",
            y="Activities",
            color="Activities",
            title="Activities by Project"
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )
