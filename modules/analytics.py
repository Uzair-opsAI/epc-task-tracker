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
        # ========================================================
    # EXECUTIVE KPI SUMMARY
    # ========================================================

    st.subheader("Executive Summary")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    # --------------------------------------------------------
    # TOTAL ACTIVITIES
    # --------------------------------------------------------

    with kpi1:

        st.metric(
            label="📋 Total Activities",
            value=f"{total}"
        )

    # --------------------------------------------------------
    # COMPLETION RATE
    # --------------------------------------------------------

    with kpi2:

        st.metric(
            label="✅ Completion Rate",
            value=f"{completion_rate:.1f}%"
        )

    # --------------------------------------------------------
    # AVERAGE PROGRESS
    # --------------------------------------------------------

    with kpi3:

        st.metric(
            label="📈 Average Progress",
            value=f"{avg_progress:.1f}%"
        )

    # --------------------------------------------------------
    # OVERDUE RATE
    # --------------------------------------------------------

    with kpi4:

        st.metric(
            label="🚨 Overdue",
            value=f"{overdue_rate:.1f}%"
        )

    st.divider()
        if total
        else 0
    )
    # ========================================================
    # WORKLOAD ANALYTICS
    # ========================================================

    st.subheader("Workload Analytics")

    left, right = st.columns(2)

    # ========================================================
    # ACTIVITIES BY DISCIPLINE
    # ========================================================

    with left:

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

            x="Activities",

            y="Discipline",

            orientation="h",

            text="Activities",

            color="Activities",

            color_continuous_scale="Blues"

        )

        fig.update_traces(

            textposition="outside"

        )

        fig.update_layout(

            title="Activities by Discipline",

            height=430,

            showlegend=False,

            xaxis_title="Activities",

            yaxis_title="",

            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10
            )

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ========================================================
    # EMPLOYEE WORKLOAD
    # ========================================================

    with right:

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

            text="Activities",

            color="Activities",

            color_continuous_scale="Viridis"

        )

        fig.update_traces(

            textposition="outside"

        )

        fig.update_layout(

            title="Employee Workload",

            height=430,

            showlegend=False,

            xaxis_title="",

            yaxis_title="Assigned Activities",

            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10
            )

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()
    # ========================================================
    # PROJECT PERFORMANCE
    # ========================================================

    st.subheader("Project Performance")

    project_df = (
        filtered.groupby("Project")
        .agg(
            Average_Progress=("Progress", "mean"),
            Total_Activities=("Activity ID", "count"),
            Completed=(
                "Status",
                lambda x: (x == "Completed").sum()
            ),
            Overdue=(
                "Status",
                lambda x: (
                    (
                        filtered.loc[
                            x.index,
                            "Planned Finish"
                        ] < today
                    )
                    &
                    (x != "Completed")
                ).sum()
            )
        )
        .reset_index()
    )

    project_df["Average_Progress"] = (
        project_df["Average_Progress"]
        .round(1)
    )

    # --------------------------------------------------------
    # PROJECT PERFORMANCE CHART
    # --------------------------------------------------------

    fig = px.bar(

        project_df,

        x="Average_Progress",

        y="Project",

        orientation="h",

        text="Average_Progress",

        color="Average_Progress",

        color_continuous_scale="Greens"

    )

    fig.update_traces(

        texttemplate="%{text:.1f}%",

        textposition="outside"

    )

    fig.update_layout(

        height=450,

        showlegend=False,

        title="Average Progress by Project",

        xaxis_title="Average Progress (%)",

        yaxis_title="",

        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ========================================================
    # PROJECT SUMMARY
    # ========================================================

    st.subheader("Project Summary")

    summary = project_df.copy()

    def health(progress):

        if progress >= 80:
            return "🟢 Healthy"

        elif progress >= 50:
            return "🟡 Monitor"

        return "🔴 Critical"

    summary["Health"] = (
        summary["Average_Progress"]
        .apply(health)
    )

    summary = summary[
        [
            "Project",
            "Total_Activities",
            "Completed",
            "Overdue",
            "Average_Progress",
            "Health"
        ]
    ]

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    st.divider()
    # ========================================================
    # EXECUTIVE INSIGHTS
    # ========================================================

    st.subheader("Executive Insights")

    insights = []

    # --------------------------------------------------------
    # Overall Portfolio Progress
    # --------------------------------------------------------

    insights.append(
        f"📈 Average portfolio progress is **{avg_progress:.1f}%**."
    )

    # --------------------------------------------------------
    # Completion Rate
    # --------------------------------------------------------

    insights.append(
        f"✅ Overall completion rate stands at **{completion_rate:.1f}%**."
    )

    # --------------------------------------------------------
    # Overdue Activities
    # --------------------------------------------------------

    if overdue > 0:

        insights.append(
            f"🔴 There are **{overdue} overdue activities** requiring immediate attention."
        )

    else:

        insights.append(
            "🟢 No overdue activities detected."
        )

    # --------------------------------------------------------
    # Highest Workload Discipline
    # --------------------------------------------------------

    if not discipline_df.empty:

        top_discipline = discipline_df.iloc[0]

        insights.append(

            f"⚡ **{top_discipline['Discipline']}** discipline currently has the highest workload with **{top_discipline['Activities']} activities**."

        )

    # --------------------------------------------------------
    # Highest Workload Employee
    # --------------------------------------------------------

    if not employee_df.empty:

        top_employee = employee_df.iloc[0]

        insights.append(

            f"👤 **{top_employee['Assigned To']}** has the highest assigned workload (**{top_employee['Activities']} activities**)."

        )

    # --------------------------------------------------------
    # Best Performing Project
    # --------------------------------------------------------

    if not project_df.empty:

        best_project = project_df.loc[
            project_df["Average_Progress"].idxmax()
        ]

        insights.append(

            f"🏆 **{best_project['Project']}** is the best performing project with an average progress of **{best_project['Average_Progress']:.1f}%**."

        )

    # --------------------------------------------------------
    # Lowest Performing Project
    # --------------------------------------------------------

    if not project_df.empty:

        weakest_project = project_df.loc[
            project_df["Average_Progress"].idxmin()
        ]

        insights.append(

            f"⚠️ **{weakest_project['Project']}** has the lowest average progress (**{weakest_project['Average_Progress']:.1f}%**)."

        )

    # --------------------------------------------------------
    # Display Insights
    # --------------------------------------------------------

    for insight in insights:

        st.info(insight)

    st.divider()
    # ========================================================
    # EXPORT ANALYTICS REPORT
    # ========================================================

    st.subheader("Analytics Report")

    report_df = summary.copy()

    csv = report_df.to_csv(
        index=False
    ).encode("utf-8")

    left, right = st.columns([3, 1])

    with left:

        st.markdown(
            """
This report contains a consolidated portfolio summary including:

- Project-wise activity count
- Average project progress
- Completed activities
- Overdue activities
- Overall project health

The exported report reflects the currently applied filters.
"""
        )

    with right:

        st.download_button(
            label="📥 Download Report",
            data=csv,
            file_name="Portfolio_Analytics_Report.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.divider()

    # ========================================================
    # ANALYTICS SUMMARY
    # ========================================================

    st.subheader("Analytics Overview")

    overview1, overview2 = st.columns(2)

    with overview1:

        st.success(
            f"""
Portfolio contains **{total}** activities across
**{filtered['Project'].nunique()}** active projects.
"""
        )

    with overview2:

        st.info(
            f"""
Average portfolio progress is **{avg_progress:.1f}%**
with a completion rate of **{completion_rate:.1f}%**.
"""
        )

    st.divider()

    # ========================================================
    # FOOTER
    # ========================================================

    footer_left, footer_right = st.columns([3, 1])

    with footer_left:

        st.caption(
            "Kent EPC Project Tracker • Portfolio Analytics • Version 2.0"
        )

    with footer_right:

        st.caption(
            datetime.now().strftime("%d-%b-%Y")
        )
