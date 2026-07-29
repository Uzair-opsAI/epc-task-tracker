import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.styles import load_css
from components.cards import dashboard_card
from components.metrics import (
    metric_card,
    success_card,
    warning_card,
    danger_card,
    info_card
)
from datetime import datetime, timedelta

from database import (
    get_tasks,
    get_projects,
    get_employees
)


def show():
    load_css()
    st.markdown(
        """
        <div class="main-title">
            Kent EPC Project Tracker
        </div>
    
        <div class="sub-title">
            Executive Project Controls Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.info("🏗 Engineering Projects")
    
    with col2:
        st.success("🟢 Google Sheets Connected")
    
    with col3:
        st.caption(
            f"Last Refresh\n\n{datetime.now().strftime('%H:%M:%S')}"
        )
    
    st.divider()

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

    st.subheader("📈 Executive KPI Dashboard")

    row1 = st.columns(3)
    
    with row1[0]:
    
        info_card(
            "Total Activities",
            total
        )
    
    with row1[1]:
    
        success_card(
            "Completed",
            completed
        )
    
    with row1[2]:
    
        warning_card(
            "In Progress",
            in_progress
        )
    
    row2 = st.columns(3)
    
    with row2[0]:
    
        metric_card(
            "Not Started",
            not_started,
            icon="⚪",
            color="#9CA3AF",
            subtitle="Pending activities"
        )
    
    with row2[1]:
    
        danger_card(
            "Overdue",
            overdue
        )
    
    with row2[2]:
    
        metric_card(
            "Due This Week",
            due_week,
            icon="📅",
            color="#F97316",
            subtitle="Upcoming deadlines"
        )
    
    metric_card(
        "Average Progress",
        f"{avg_progress:.0f}%",
        icon="📈",
        color="#2563EB",
        subtitle="Across all filtered activities"
    )
    
    st.divider()

    # --------------------------------------------------
    # Executive Dashboard Widgets
    # --------------------------------------------------
    
    left, right = st.columns(2)
    
    # ==================================================
    # Overall Progress
    # ==================================================
    
    with left:
    
        with dashboard_card(
            title="Overall Progress",
            icon="🎯",
            subtitle="Average completion across all activities"
        ):
    
            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=avg_progress,
                    title={
                        "text": "Overall Progress"
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100]
                        }
                    }
                )
            )
    
            fig.update_layout(
                height=340,
                margin=dict(l=20, r=20, t=40, b=20)
            )
    
            st.plotly_chart(
                fig,
                use_container_width=True
            )
    
    # ==================================================
    # Activity Status
    # ==================================================
    
    with right:
    
        with dashboard_card(
            title="Activity Status",
            icon="📊",
            subtitle="Current status distribution"
        ):
    
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
                hole=0.45
            )
    
            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )
    
            fig.update_layout(
                height=340,
                showlegend=True,
                margin=dict(l=20, r=20, t=20, b=20)
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
