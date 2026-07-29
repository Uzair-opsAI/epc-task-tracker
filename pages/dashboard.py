import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta

from database import (
    get_tasks,
    get_projects,
    get_employees
)


def show():

    st.title("🏗 Kent EPC Executive Dashboard")

    tasks = get_tasks()
    projects = get_projects()
    employees = get_employees()

    if tasks.empty:
        st.warning("No activity data found.")
        return

    # --------------------------------------------------
    # Data Preparation
    # --------------------------------------------------

    tasks["Planned Finish"] = pd.to_datetime(
        tasks["Planned Finish"],
        errors="coerce"
    )

    tasks["Planned Start"] = pd.to_datetime(
        tasks["Planned Start"],
        errors="coerce"
    )

    today = datetime.today()

    total = len(tasks)

    completed = len(
        tasks[
            tasks["Status"] == "Completed"
        ]
    )

    in_progress = len(
        tasks[
            tasks["Status"] == "In Progress"
        ]
    )

    not_started = len(
        tasks[
            tasks["Status"] == "Not Started"
        ]
    )

    overdue = len(
        tasks[
            (tasks["Planned Finish"] < today)
            &
            (tasks["Status"] != "Completed")
        ]
    )

    due_week = len(
        tasks[
            (tasks["Planned Finish"] >= today)
            &
            (
                tasks["Planned Finish"]
                <= today + timedelta(days=7)
            )
        ]
    )

    avg_progress = tasks["Progress"].mean()

    # --------------------------------------------------
    # Sidebar Filters
    # --------------------------------------------------

    st.sidebar.header("Dashboard Filters")

    project_filter = st.sidebar.selectbox(
        "Project",
        ["All"] +
        sorted(
            tasks["Project"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    discipline_filter = st.sidebar.selectbox(
        "Discipline",
        ["All"] +
        sorted(
            tasks["Discipline"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    status_filter = st.sidebar.selectbox(
        "Status",
        ["All"] +
        sorted(
            tasks["Status"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    filtered = tasks.copy()

    if project_filter != "All":
        filtered = filtered[
            filtered["Project"] == project_filter
        ]

    if discipline_filter != "All":
        filtered = filtered[
            filtered["Discipline"] == discipline_filter
        ]

    if status_filter != "All":
        filtered = filtered[
            filtered["Status"] == status_filter
        ]

    # Recalculate KPIs after filtering

    total = len(filtered)

    completed = len(
        filtered[
            filtered["Status"] == "Completed"
        ]
    )

    in_progress = len(
        filtered[
            filtered["Status"] == "In Progress"
        ]
    )

    not_started = len(
        filtered[
            filtered["Status"] == "Not Started"
        ]
    )

    overdue = len(
        filtered[
            (filtered["Planned Finish"] < today)
            &
            (filtered["Status"] != "Completed")
        ]
    )

    due_week = len(
        filtered[
            (filtered["Planned Finish"] >= today)
            &
            (
                filtered["Planned Finish"]
                <= today + timedelta(days=7)
            )
        ]
    )

    avg_progress = filtered["Progress"].mean()

    # --------------------------------------------------
    # KPI Cards
    # --------------------------------------------------

    st.subheader("📈 Project KPIs")

    row1 = st.columns(3)

    row1[0].metric(
        "📋 Total Activities",
        total
    )

    row1[1].metric(
        "🟢 Completed",
        completed
    )

    row1[2].metric(
        "🟡 In Progress",
        in_progress
    )

    row2 = st.columns(3)

    row2[0].metric(
        "⚪ Not Started",
        not_started
    )

    row2[1].metric(
        "🔴 Overdue",
        overdue
    )

    row2[2].metric(
        "🟠 Due This Week",
        due_week
    )

    st.metric(
        "📊 Average Progress",
        f"{avg_progress:.0f}%"
    )

    st.divider()

    # --------------------------------------------------
    # Project Progress Gauge
    # --------------------------------------------------

    left, right = st.columns([1,1])

    with left:

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=avg_progress,
                title={
                    "text":"Overall Progress"
                },
                gauge={
                    "axis":{
                        "range":[0,100]
                    }
                }
            )
        )

        fig.update_layout(
            height=360
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

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
            hole=0.50,
            title="Activity Status Distribution"
        )

        fig.update_layout(
            height=360
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------
    # Discipline vs Priority
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        discipline = (
            filtered["Discipline"]
            .value_counts()
            .reset_index()
        )

        discipline.columns = [
            "Discipline",
            "Activities"
        ]

        fig = px.bar(
            discipline,
            x="Discipline",
            y="Activities",
            color="Activities",
            text="Activities",
            title="Activities by Discipline"
        )

        fig.update_layout(
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        priority = (
            filtered["Priority"]
            .value_counts()
            .reset_index()
        )

        priority.columns = [
            "Priority",
            "Activities"
        ]

        fig = px.bar(
            priority,
            x="Priority",
            y="Activities",
            color="Activities",
            text="Activities",
            title="Priority Distribution"
        )

        fig.update_layout(
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()
      # --------------------------------------------------
    # Employee Workload & Project Health
    # --------------------------------------------------

    st.subheader("👷 Employee Workload & 🏗 Project Health")

    left, right = st.columns(2)

    with left:

        employee_summary = (
            filtered["Assigned To"]
            .fillna("Unassigned")
            .value_counts()
            .reset_index()
        )

        employee_summary.columns = [
            "Employee",
            "Activities"
        ]

        fig = px.bar(
            employee_summary,
            x="Employee",
            y="Activities",
            color="Activities",
            text="Activities",
            title="Activities per Employee"
        )

        fig.update_layout(
            height=420,
            xaxis_title="Employee",
            yaxis_title="Activities"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        project_summary = (
            filtered
            .groupby("Project")
            .agg(
                Total=("Activity ID", "count"),
                Progress=("Progress", "mean")
            )
            .reset_index()
        )

        project_summary["Progress"] = (
            project_summary["Progress"]
            .fillna(0)
            .round(0)
        )

        fig = px.bar(
            project_summary,
            x="Project",
            y="Progress",
            color="Progress",
            text="Progress",
            title="Average Project Progress (%)"
        )

        fig.update_layout(height=420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------
    # Project Health Table
    # --------------------------------------------------

    st.subheader("📊 Project Health")

    health = project_summary.copy()

    def health_status(progress):

        if progress >= 80:
            return "🟢 Healthy"

        elif progress >= 50:
            return "🟡 Monitor"

        else:
            return "🔴 Critical"

    health["Health"] = health["Progress"].apply(
        health_status
    )

    health.rename(
        columns={
            "Total": "Activities",
            "Progress": "Average Progress (%)"
        },
        inplace=True
    )

    st.dataframe(
        health,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------
    # Activities Due This Week
    # --------------------------------------------------

    st.subheader("📅 Activities Due in the Next 7 Days")

    upcoming = filtered[
        (filtered["Planned Finish"] >= today)
        &
        (
            filtered["Planned Finish"]
            <= today + timedelta(days=7)
        )
    ].sort_values("Planned Finish")

    if upcoming.empty:

        st.success("No activities due this week.")

    else:

        st.dataframe(
            upcoming[
                [
                    "Activity ID",
                    "Activity Name",
                    "Project",
                    "Assigned To",
                    "Priority",
                    "Planned Finish",
                    "Status",
                    "Progress"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # --------------------------------------------------
    # Overdue Activities
    # --------------------------------------------------

    st.subheader("🚨 Overdue Activities")

    overdue_table = filtered[
        (filtered["Planned Finish"] < today)
        &
        (filtered["Status"] != "Completed")
    ].sort_values("Planned Finish")

    if overdue_table.empty:

        st.success("🎉 No overdue activities.")

    else:

        st.error(
            f"{len(overdue_table)} overdue activities require attention."
        )

        st.dataframe(
            overdue_table[
                [
                    "Activity ID",
                    "Activity Name",
                    "Project",
                    "Assigned To",
                    "Priority",
                    "Planned Finish",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # --------------------------------------------------
    # Recent Activities
    # --------------------------------------------------

    st.subheader("🕒 Recently Added Activities")

    if "Created On" in filtered.columns:

        recent = filtered.copy()

        recent["Created On"] = pd.to_datetime(
            recent["Created On"],
            errors="coerce"
        )

        recent = recent.sort_values(
            "Created On",
            ascending=False
        ).head(10)

        st.dataframe(
            recent[
                [
                    "Activity ID",
                    "Activity Name",
                    "Project",
                    "Assigned To",
                    "Created On",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "'Created On' column not available."
        )

    st.divider()

    # --------------------------------------------------
    # Executive Summary
    # --------------------------------------------------

    st.subheader("📋 Executive Summary")

    summary = (
        filtered
        .groupby("Project")
        .agg(
            Total_Activities=("Activity ID", "count"),
            Avg_Progress=("Progress", "mean")
        )
        .reset_index()
    )

    completed_summary = (
        filtered[
            filtered["Status"] == "Completed"
        ]
        .groupby("Project")
        .size()
        .reset_index(name="Completed")
    )

    progress_summary = (
        filtered[
            filtered["Status"] == "In Progress"
        ]
        .groupby("Project")
        .size()
        .reset_index(name="In Progress")
    )

    summary = summary.merge(
        completed_summary,
        on="Project",
        how="left"
    )

    summary = summary.merge(
        progress_summary,
        on="Project",
        how="left"
    )

    summary.fillna(0, inplace=True)

    summary["Avg_Progress"] = (
        summary["Avg_Progress"]
        .round(0)
        .astype(int)
    )

    summary.rename(
        columns={
            "Avg_Progress": "Average Progress (%)"
        },
        inplace=True
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------
    # Dashboard Footer
    # --------------------------------------------------

    st.caption(
        "Kent EPC Project Tracker • Executive Dashboard • Version 1.0"
    )
