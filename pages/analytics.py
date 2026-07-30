import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta

from components.styles import load_css

from database import (
    get_tasks
)

# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

def show():

    load_css()

    # ========================================================
    # HEADER
    # ========================================================

    st.title("📊 Executive Analytics Dashboard")

    st.caption(
        "Portfolio-wide EPC project performance, engineering productivity and schedule analytics."
    )

    info1, info2, info3 = st.columns([2, 2, 1])

    with info1:

        st.info("🏗 Engineering Project Controls")

    with info2:

        st.success("🟢 Live Google Sheets Data")

    with info3:

        st.metric(
            "Updated",
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

    # ========================================================
    # EXECUTIVE KPI DASHBOARD
    # ========================================================
        st.subheader("📈 Executive Performance Dashboard")

    # ========================================================
    # KPI ROW 1
    # ========================================================

    row1 = st.columns(4)

    with row1[0]:

        st.metric(
            "📋 Total Activities",
            total
        )

    with row1[1]:

        st.metric(
            "🟢 Completed",
            completed,
            delta=f"{(completed/total*100):.1f}%"
            if total else "0%"
        )

    with row1[2]:

        st.metric(
            "🟡 In Progress",
            in_progress
        )

    with row1[3]:

        st.metric(
            "⚪ Not Started",
            not_started
        )

    # ========================================================
    # KPI ROW 2
    # ========================================================

    row2 = st.columns(3)

    with row2[0]:

        st.metric(
            "🔴 Overdue",
            overdue
        )

    with row2[1]:

        st.metric(
            "📅 Due This Week",
            due_this_week
        )

    with row2[2]:

        st.metric(
            "📈 Average Progress",
            f"{avg_progress:.1f}%"
        )

    st.divider()

    # ========================================================
    # EXECUTIVE SNAPSHOT
    # ========================================================

    st.subheader("📊 Portfolio Snapshot")

    s1, s2, s3, s4 = st.columns(4)

    completion_rate = (
        round((completed / total) * 100, 1)
        if total else 0
    )

    portfolio_health = (
        "🟢 Healthy"
        if avg_progress >= 80
        else "🟡 Monitor"
        if avg_progress >= 50
        else "🔴 Critical"
    )

    with s1:

        st.info(
            f"""
**Projects**

{filtered['Project'].nunique()}
"""
        )

    with s2:

        st.info(
            f"""
**Employees**

{filtered['Assigned To'].nunique()}
"""
        )

    with s3:

        st.info(
            f"""
**Completion Rate**

{completion_rate:.1f}%
"""
        )

    with s4:

        st.info(
            f"""
**Portfolio Health**

{portfolio_health}
"""
        )

    st.divider()

    # ========================================================
    # PROGRESS OVERVIEW
    # ========================================================

    left, right = st.columns(2)
    # ========================================================
    # OVERALL PROGRESS GAUGE
    # ========================================================

    with left:

        st.subheader("🎯 Overall Portfolio Progress")

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=avg_progress,
                number={"suffix": "%"},
                title={
                    "text": "Average Completion"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": "#1976D2"
                    },
                    "steps": [
                        {
                            "range": [0, 40],
                            "color": "#FDECEC"
                        },
                        {
                            "range": [40, 70],
                            "color": "#FFF4E5"
                        },
                        {
                            "range": [70, 100],
                            "color": "#E8F5E9"
                        }
                    ],
                    "threshold": {
                        "line": {
                            "color": "red",
                            "width": 4
                        },
                        "value": 80
                    }
                }
            )
        )

        gauge.update_layout(
            height=430,
            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            )
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    # ========================================================
    # STATUS DISTRIBUTION
    # ========================================================

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

        pie = px.pie(
            status_df,
            values="Activities",
            names="Status",
            hole=0.55
        )

        pie.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        pie.update_layout(
            height=430,
            legend_title="Status",
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=20
            )
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    st.divider()

    # ========================================================
    # DISCIPLINE & PRIORITY ANALYSIS
    # ========================================================

    left, right = st.columns(2)
    # ========================================================
    # ACTIVITIES BY DISCIPLINE
    # ========================================================

    with left:

        st.subheader("⚡ Activities by Discipline")

        discipline_df = (
            filtered.groupby("Discipline")
            .size()
            .reset_index(name="Activities")
            .sort_values(
                "Activities",
                ascending=False
            )
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
            xaxis_title="",
            yaxis_title="Activities"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ========================================================
    # PRIORITY DISTRIBUTION
    # ========================================================

    with right:

        st.subheader("🚨 Priority Distribution")

        priority_order = [
            "Critical",
            "High",
            "Medium",
            "Low"
        ]

        priority_df = (
            filtered.groupby("Priority")
            .size()
            .reset_index(name="Activities")
        )

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
            xaxis_title="",
            yaxis_title="Activities"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ========================================================
    # EMPLOYEE & PROJECT PERFORMANCE
    # ========================================================

    left, right = st.columns(2)

    # ========================================================
    # EMPLOYEE WORKLOAD
    # ========================================================

    with left:

        st.subheader("👷 Employee Workload")

        employee_df = (
            filtered.groupby("Assigned To")
            .size()
            .reset_index(name="Activities")
            .sort_values(
                "Activities",
                ascending=False
            )
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
            xaxis_title="",
            yaxis_title="Assigned Activities"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ========================================================
    # PROJECT PERFORMANCE
    # ========================================================

    with right:

        st.subheader("🏗 Project Performance")

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
            xaxis_title="",
            yaxis_title="Average Progress (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ========================================================
    # OPERATIONAL ANALYTICS
    # ========================================================
        # ========================================================
    # ACTIVITIES DUE THIS WEEK
    # ========================================================

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

        st.success(
            "✅ No activities are due within the next 7 days."
        )

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

    # ========================================================
    # OVERDUE ACTIVITIES
    # ========================================================

    st.subheader("🚨 Overdue Activities")

    overdue_df = filtered[
        (filtered["Planned Finish"] < today)
        &
        (filtered["Status"] != "Completed")
    ].copy()

    overdue_df = overdue_df.sort_values("Planned Finish")

    if overdue_df.empty:

        st.success(
            "🎉 Great! No overdue activities."
        )

    else:

        st.warning(
            f"{len(overdue_df)} overdue activities require immediate attention."
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

    # ========================================================
    # PROJECT HEALTH SUMMARY
    # ========================================================

    st.subheader("🏗 Project Health Summary")

    project_health = (
        filtered
        .groupby("Project")
        .agg(
            Total_Activities=("Activity ID", "count"),
            Average_Progress=("Progress", "mean"),
            Completed=("Status", lambda x: (x == "Completed").sum()),
            In_Progress=("Status", lambda x: (x == "In Progress").sum())
        )
        .reset_index()
    )

    project_health["Average_Progress"] = (
        project_health["Average_Progress"]
        .round(1)
    )

    def project_health_status(progress):

        if progress >= 80:
            return "🟢 Healthy"

        elif progress >= 50:
            return "🟡 Monitor"

        return "🔴 Critical"

    project_health["Health"] = (
        project_health["Average_Progress"]
        .apply(project_health_status)
    )

    st.dataframe(
        project_health,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # EXECUTIVE STATISTICS
    # ========================================================

    st.subheader("📈 Executive Statistics")

    stat1, stat2, stat3, stat4 = st.columns(4)

    completion_rate = (
        round((completed / total) * 100, 1)
        if total else 0
    )

    overdue_rate = (
        round((overdue / total) * 100, 1)
        if total else 0
    )

    avg_activities = (
        round(
            total / filtered["Project"].nunique(),
            1
        )
        if filtered["Project"].nunique() > 0
        else 0
    )

    avg_employee_load = (
        round(
            total / filtered["Assigned To"].nunique(),
            1
        )
        if filtered["Assigned To"].nunique() > 0
        else 0
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
            "Activities / Project",
            avg_activities
        )

    with stat4:

        st.metric(
            "Activities / Employee",
            avg_employee_load
        )

    st.divider()

    # ========================================================
    # EXECUTIVE INSIGHTS
    # ========================================================

    st.subheader("📝 Executive Insights")

    insights = []

    if overdue > 0:
        insights.append(
            f"🔴 {overdue} overdue activities require immediate management attention."
        )

    if due_this_week > 0:
        insights.append(
            f"📅 {due_this_week} activities are due within the next 7 days."
        )

    if completion_rate >= 80:
        insights.append(
            "🟢 Overall portfolio completion is healthy."
        )

    elif completion_rate >= 50:
        insights.append(
            "🟡 Portfolio progress should be monitored closely."
        )

    else:
        insights.append(
            "🔴 Portfolio completion is below target."
        )

    if avg_progress >= 80:
        insights.append(
            "🏆 Average activity progress indicates strong execution."
        )

    elif avg_progress >= 50:
        insights.append(
            "⚠ Project execution is moderate and should be monitored."
        )

    else:
        insights.append(
            "🚨 Low average activity progress detected."
        )

    for item in insights:

        st.info(item)

    st.divider()

    # ========================================================
    # DASHBOARD INFORMATION
    # ========================================================

    with st.expander(
        "ℹ Dashboard Information",
        expanded=False
    ):

        st.markdown(
            """
### Executive Analytics Dashboard

This dashboard provides:

- Executive KPI Monitoring
- Portfolio Health Overview
- Project Performance Analysis
- Discipline Workload Analysis
- Employee Workload Analysis
- Priority Distribution
- Due & Overdue Activity Tracking
- Project Health Summary
- Executive Statistics
- Management Insights

---

**Data Source:** Google Sheets

**Refresh:** Live on page refresh

**Developed For:** Kent PLC – EPC Project Controls
"""
        )

    st.divider()

    # ========================================================
    # FOOTER
    # ========================================================

    footer_left, footer_right = st.columns([3, 1])

    with footer_left:

        st.caption(
            "Kent EPC Project Tracker • Executive Analytics Dashboard • Version 2.0"
        )

    with footer_right:

        st.caption(
            datetime.now().strftime("%d %b %Y")
        )
