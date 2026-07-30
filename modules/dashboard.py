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

from components.styles import load_css


# ===========================================================
# DASHBOARD
# ===========================================================

def show():

    # =======================================================
    # Load CSS
    # =======================================================

    load_css()

    # =======================================================
    # HEADER
    # =======================================================

    st.title("⚡ Kent EPC Project Tracker")

    st.caption(
        "Executive Project Controls Dashboard"
    )

    c1, c2, c3 = st.columns([2,2,1])

    with c1:

        st.info("🏗 Engineering Projects")

    with c2:

        st.success("🟢 Google Sheets Connected")

    with c3:

        st.metric(
            "Refresh",
            datetime.now().strftime("%H:%M")
        )

    st.divider()

    # =======================================================
    # LOAD DATA
    # =======================================================

    tasks = get_tasks()

    if tasks.empty:

        st.warning("No activities available.")

        st.stop()

    # =======================================================
    # CLEAN DATA
    # =======================================================

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

    today = pd.Timestamp.today()

    # =======================================================
    # SIDEBAR FILTERS
    # =======================================================

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

    priority_filter = st.sidebar.selectbox(
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

    # =======================================================
    # APPLY FILTERS
    # =======================================================

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

    if priority_filter != "All":

        filtered = filtered[
            filtered["Priority"] == priority_filter
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

    # =======================================================
    # KPI CALCULATIONS
    # =======================================================

    total = len(filtered)

    completed = (
        filtered["Status"] == "Completed"
    ).sum()

    in_progress = (
        filtered["Status"] == "In Progress"
    ).sum()

    not_started = (
        filtered["Status"] == "Not Started"
    ).sum()

    overdue = len(

        filtered[

            (filtered["Planned Finish"] < today)

            &

            (filtered["Status"] != "Completed")

        ]

    )

    due_this_week = len(

        filtered[

            (filtered["Planned Finish"] >= today)

            &

            (

                filtered["Planned Finish"]

                <= today + timedelta(days=7)

            )

        ]

    )

    avg_progress = round(

        filtered["Progress"].mean(),

        1

    )

    # =======================================================
    # EXECUTIVE KPI SECTION
    # =======================================================

    # =======================================================
    # KPI ROW 1
    # =======================================================

    row1 = st.columns(3)

    with row1[0]:
        st.metric(
            label="📋 Total Activities",
            value=total,
            delta=None
        )

    with row1[1]:
        st.metric(
            label="🟢 Completed",
            value=completed,
            delta=f"{(completed/total*100):.1f}%"
            if total else "0%"
        )

    with row1[2]:
        st.metric(
            label="🟡 In Progress",
            value=in_progress
        )

    # =======================================================
    # KPI ROW 2
    # =======================================================

    row2 = st.columns(3)

    with row2[0]:
        st.metric(
            label="⚪ Not Started",
            value=not_started
        )

    with row2[1]:
        st.metric(
            label="🔴 Overdue",
            value=overdue
        )

    with row2[2]:
        st.metric(
            label="📅 Due This Week",
            value=due_this_week
        )

    # =======================================================
    # OVERALL PROGRESS
    # =======================================================

    st.metric(
        label="📈 Average Progress",
        value=f"{avg_progress:.1f}%"
    )

    st.divider()

    # =======================================================
    # EXECUTIVE SNAPSHOT
    # =======================================================

    snapshot1, snapshot2, snapshot3, snapshot4 = st.columns(4)

    snapshot1.info(
        f"**Projects**\n\n{filtered['Project'].nunique()}"
    )

    snapshot2.info(
        f"**Employees**\n\n{filtered['Assigned To'].nunique()}"
    )

    snapshot3.info(
        f"**Disciplines**\n\n{filtered['Discipline'].nunique()}"
    )

    completion_rate = (
        completed / total * 100
        if total else 0
    )

    snapshot4.info(
        f"**Completion Rate**\n\n{completion_rate:.1f}%"
    )

    st.divider()

    # =======================================================
    # CHART SECTION STARTS HERE
    # =======================================================

    left, right = st.columns(2)
        # =======================================================
    # OVERALL PROGRESS & STATUS DISTRIBUTION
    # =======================================================

    with left:

        st.subheader("🎯 Overall Progress")

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=avg_progress,
                number={
                    "suffix": "%"
                },
                title={
                    "text": "Average Project Progress"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": "#1565C0"
                    },
                    "steps": [
                        {
                            "range": [0, 40],
                            "color": "#FDECEC"
                        },
                        {
                            "range": [40, 70],
                            "color": "#FFF7E6"
                        },
                        {
                            "range": [70, 100],
                            "color": "#E8F5E9"
                        }
                    ]
                }
            )
        )

        fig.update_layout(
            height=380,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =======================================================
    # STATUS DISTRIBUTION
    # =======================================================

    with right:

        st.subheader("📊 Activity Status Distribution")

        status_df = (
            filtered["Status"]
            .value_counts()
            .reset_index()
        )

        status_df.columns = [
            "Status",
            "Activities"
        ]

        fig = px.pie(
            status_df,
            values="Activities",
            names="Status",
            hole=0.55
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            height=380,
            legend_title="Status",
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

        # =======================================================
    # DISCIPLINE & PRIORITY ANALYSIS
    # =======================================================

    left, right = st.columns(2)

    with left:

        st.subheader("⚡ Activities by Discipline")

        discipline_df = (
            filtered.groupby("Discipline")
            .size()
            .reset_index(name="Activities")
            .sort_values("Activities", ascending=False)
        )

        fig = px.bar(
            discipline_df,
            x="Discipline",
            y="Activities",
            color="Activities",
            text="Activities",
            color_continuous_scale="Blues"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            height=420,
            showlegend=False,
            xaxis_title=None,
            yaxis_title="No. of Activities"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("🚨 Priority Distribution")

        priority_df = (
            filtered.groupby("Priority")
            .size()
            .reset_index(name="Activities")
        )

        priority_order = [
            "Critical",
            "High",
            "Medium",
            "Low"
        ]

        priority_df["Priority"] = pd.Categorical(
            priority_df["Priority"],
            categories=priority_order,
            ordered=True
        )

        priority_df = priority_df.sort_values("Priority")

        fig = px.bar(
            priority_df,
            x="Priority",
            y="Activities",
            color="Priority",
            text="Activities"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            height=420,
            showlegend=False,
            xaxis_title=None,
            yaxis_title="No. of Activities"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # =======================================================
    # EMPLOYEE & PROJECT ANALYSIS
    # =======================================================

    left, right = st.columns(2)

    with left:

        st.subheader("👷 Employee Workload")

        employee_df = (
            filtered.groupby("Assigned To")
            .size()
            .reset_index(name="Activities")
            .sort_values("Activities", ascending=False)
        )

        fig = px.bar(
            employee_df,
            x="Assigned To",
            y="Activities",
            color="Activities",
            text="Activities",
            color_continuous_scale="Viridis"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            height=420,
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Assigned Activities"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("📂 Project Progress")

        project_df = (
            filtered.groupby("Project")
            .agg(
                Average_Progress=("Progress", "mean"),
                Total_Activities=("Activity ID", "count")
            )
            .reset_index()
        )

        project_df["Average_Progress"] = (
            project_df["Average_Progress"]
            .round(1)
        )

        fig = px.bar(
            project_df,
            x="Project",
            y="Average_Progress",
            color="Average_Progress",
            text="Average_Progress",
            color_continuous_scale="Greens"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig.update_layout(
            height=420,
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Average Progress (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()
        # =======================================================
    # ACTIVITIES DUE THIS WEEK
    # =======================================================

    st.subheader("📅 Activities Due This Week")

    due_df = filtered[
        (filtered["Planned Finish"] >= today)
        &
        (
            filtered["Planned Finish"]
            <= today + timedelta(days=7)
        )
    ].copy()

    due_df = due_df.sort_values("Planned Finish")

    if due_df.empty:

        st.success("✅ No activities are due during the next 7 days.")

    else:

        st.dataframe(
            due_df[
                [
                    "Activity ID",
                    "Activity Name",
                    "Project",
                    "Assigned To",
                    "Priority",
                    "Planned Finish",
                    "Progress",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # =======================================================
    # OVERDUE ACTIVITIES
    # =======================================================

    st.subheader("🚨 Overdue Activities")

    overdue_df = filtered[
        (filtered["Planned Finish"] < today)
        &
        (filtered["Status"] != "Completed")
    ].copy()

    overdue_df = overdue_df.sort_values("Planned Finish")

    if overdue_df.empty:

        st.success("🎉 No overdue activities.")

    else:

        st.warning(
            f"{len(overdue_df)} overdue activity(s) require attention."
        )

        st.dataframe(
            overdue_df[
                [
                    "Activity ID",
                    "Activity Name",
                    "Project",
                    "Assigned To",
                    "Priority",
                    "Planned Finish",
                    "Progress",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # =======================================================
    # RECENT ACTIVITIES
    # =======================================================

    st.subheader("🕒 Recently Added Activities")

    if "Created On" in filtered.columns:

        recent_df = filtered.copy()

        recent_df["Created On"] = pd.to_datetime(
            recent_df["Created On"],
            errors="coerce"
        )

        recent_df = (
            recent_df
            .sort_values(
                "Created On",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            recent_df[
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
            "The Google Sheet currently does not contain a 'Created On' column."
        )

    st.divider()

    # =======================================================
    # PROJECT HEALTH SUMMARY
    # =======================================================

    st.subheader("📊 Project Health Summary")

    project_health = (
        filtered
        .groupby("Project")
        .agg(
            Total_Activities=("Activity ID", "count"),
            Average_Progress=("Progress", "mean"),
            Completed=("Status",
                lambda x: (x == "Completed").sum()),
            In_Progress=("Status",
                lambda x: (x == "In Progress").sum()),
            Overdue=("Status",
                lambda x: (
                    (
                        filtered.loc[x.index, "Planned Finish"] < today
                    )
                    &
                    (x != "Completed")
                ).sum())
        )
        .reset_index()
    )

    project_health["Average_Progress"] = (
        project_health["Average_Progress"]
        .round(1)
    )

    def get_health(progress):

        if progress >= 80:
            return "🟢 Healthy"

        elif progress >= 50:
            return "🟡 Monitor"

        return "🔴 Critical"

    project_health["Health"] = (
        project_health["Average_Progress"]
        .apply(get_health)
    )

    st.dataframe(
        project_health,
        use_container_width=True,
        hide_index=True
    )

    st.divider()
        # =======================================================
    # EXECUTIVE DASHBOARD STATISTICS
    # =======================================================

    st.subheader("📈 Executive Dashboard Statistics")

    stat1, stat2, stat3, stat4 = st.columns(4)

    completion_rate = (
        round((completed / total) * 100, 1)
        if total > 0 else 0
    )

    overdue_rate = (
        round((overdue / total) * 100, 1)
        if total > 0 else 0
    )

    avg_activities = (
        round(total / filtered["Project"].nunique(), 1)
        if filtered["Project"].nunique() > 0 else 0
    )

    avg_employee_load = (
        round(total / filtered["Assigned To"].nunique(), 1)
        if filtered["Assigned To"].nunique() > 0 else 0
    )

    with stat1:

        st.metric(
            "Completion Rate",
            f"{completion_rate}%"
        )

    with stat2:

        st.metric(
            "Overdue Rate",
            f"{overdue_rate}%"
        )

    with stat3:

        st.metric(
            "Avg Activities / Project",
            avg_activities
        )

    with stat4:

        st.metric(
            "Avg Employee Load",
            avg_employee_load
        )

    st.divider()

    # =======================================================
    # DATA QUALITY CHECK
    # =======================================================

    st.subheader("📋 Data Quality Overview")

    dq1, dq2, dq3 = st.columns(3)

    with dq1:

        missing_progress = (
            filtered["Progress"]
            .isna()
            .sum()
        )

        st.metric(
            "Missing Progress",
            missing_progress
        )

    with dq2:

        missing_assignee = (
            filtered["Assigned To"]
            .isna()
            .sum()
        )

        st.metric(
            "Unassigned Activities",
            missing_assignee
        )

    with dq3:

        duplicate_ids = (
            filtered["Activity ID"]
            .duplicated()
            .sum()
        )

        st.metric(
            "Duplicate Activity IDs",
            duplicate_ids
        )

    st.divider()

    # =======================================================
    # DASHBOARD INFORMATION
    # =======================================================

    with st.expander("ℹ Dashboard Information", expanded=False):

        st.markdown(
            """
### Dashboard Features

This dashboard provides:

- Executive KPI Monitoring
- Activity Status Overview
- Discipline Workload Analysis
- Priority Distribution
- Employee Workload
- Project Progress Monitoring
- Due Activities Tracking
- Overdue Activity Monitoring
- Project Health Assessment
- Executive Statistics

---

### Data Source

Google Sheets

---

### Refresh Frequency

Live (Every Page Refresh)

---

### Developed For

Kent PLC - Electrical Department

Graduate Engineer Digitalisation Project
"""
        )

    st.divider()

    # =======================================================
    # FOOTER
    # =======================================================

    footer_left, footer_right = st.columns([3,1])

    with footer_left:

        st.caption(
            "Kent EPC Project Tracker • Executive Dashboard • Version 2.0"
        )

    with footer_right:

        st.caption(
            datetime.now().strftime("%d %b %Y")
        )
