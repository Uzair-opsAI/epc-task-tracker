import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta

from database import get_tasks
from components.styles import load_css


# ===========================================================
# OPERATIONS DASHBOARD
# ===========================================================

def show():

    # =======================================================
    # LOAD CSS
    # =======================================================

    load_css()

    # =======================================================
    # HEADER
    # =======================================================

    st.title("⚡ Operations Dashboard")

    st.caption(
        "Daily Engineering Project Monitoring"
    )

    info1, info2, info3 = st.columns([2,2,1])

    with info1:

        st.info("Engineering Project Controls")

    with info2:

        st.success("Google Sheets Connected")

    with info3:

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

        st.warning(
            "No activities available."
        )

        st.stop()

    # =======================================================
    # DATA CLEANING
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

    today = pd.Timestamp.today().normalize()

    # =======================================================
    # SIDEBAR FILTERS
    # =======================================================

    st.sidebar.header("Dashboard Filters")

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

    # =======================================================
    # APPLY FILTERS
    # =======================================================

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

    overdue = len(

        filtered[
            (
                filtered["Planned Finish"]
                < today
            )
            &
            (
                filtered["Status"]
                != "Completed"
            )
        ]

    )

    due_this_week = len(

        filtered[
            (
                filtered["Planned Finish"]
                >= today
            )
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
    # OPERATIONS SUMMARY
    # =======================================================

    st.subheader("Operations Summary")

    # =======================================================
    # KPI ROW 1
    # =======================================================

    row1 = st.columns(3)

    with row1[0]:

        st.metric(
            label="📋 Total Activities",
            value=f"{total}"
        )

    with row1[1]:

        st.metric(
            label="✅ Completed",
            value=f"{completed}"
        )

    with row1[2]:

        st.metric(
            label="📈 Average Progress",
            value=f"{avg_progress:.1f}%"
        )

    # =======================================================
    # KPI ROW 2
    # =======================================================

    row2 = st.columns(3)

    with row2[0]:

        st.metric(
            label="🚨 Overdue",
            value=f"{overdue}"
        )

    with row2[1]:

        st.metric(
            label="📅 Due This Week",
            value=f"{due_this_week}"
        )

    with row2[2]:

        st.metric(
            label="⚙ In Progress",
            value=f"{in_progress}"
        )

    st.divider()
        # =======================================================
    # PROJECT STATUS OVERVIEW
    # =======================================================

    st.subheader("Project Status Overview")

    left, right = st.columns(2)

    # =======================================================
    # OVERALL PROGRESS
    # =======================================================

    with left:

        fig = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=avg_progress,

                number={
                    "suffix":"%"
                },

                title={
                    "text":"Overall Progress"
                },

                gauge={

                    "axis":{
                        "range":[0,100]
                    },

                    "bar":{
                        "color":"#1565C0"
                    },

                    "steps":[

                        {
                            "range":[0,40],
                            "color":"#FDECEC"
                        },

                        {
                            "range":[40,70],
                            "color":"#FFF4CC"
                        },

                        {
                            "range":[70,100],
                            "color":"#E8F5E9"
                        }

                    ]

                }

            )
        )

        fig.update_layout(

            height=360,

            margin=dict(
                l=20,
                r=20,
                t=50,
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

            title="Activity Status",

            height=360,

            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            )

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()
        # =======================================================
    # OPERATIONAL ACTION CENTER
    # =======================================================

    action_left, action_right = st.columns(2)

    # =======================================================
    # ACTIVITIES DUE THIS WEEK
    # =======================================================

    with action_left:

        st.subheader("📅 Activities Due This Week")

        due_df = filtered[

            (filtered["Planned Finish"] >= today)

            &

            (
                filtered["Planned Finish"]
                <= today + timedelta(days=7)
            )

            &

            (
                filtered["Status"] != "Completed"
            )

        ].copy()

        due_df = due_df.sort_values(
            "Planned Finish"
        )

        if due_df.empty:

            st.success(
                "No activities due this week."
            )

        else:

            st.dataframe(

                due_df[
                    [
                        "Activity ID",
                        "Activity Name",
                        "Project",
                        "Assigned To",
                        "Planned Finish",
                        "Status"
                    ]
                ],

                use_container_width=True,

                hide_index=True

            )

    # =======================================================
    # OVERDUE ACTIVITIES
    # =======================================================

    with action_right:

        st.subheader("🚨 Overdue Activities")

        overdue_df = filtered[

            (
                filtered["Planned Finish"]
                < today
            )

            &

            (
                filtered["Status"]
                != "Completed"
            )

        ].copy()

        overdue_df = overdue_df.sort_values(
            "Planned Finish"
        )

        if overdue_df.empty:

            st.success(
                "No overdue activities."
            )

        else:

            st.error(
                f"{len(overdue_df)} activity(s) require immediate attention."
            )

            st.dataframe(

                overdue_df[
                    [
                        "Activity ID",
                        "Activity Name",
                        "Project",
                        "Assigned To",
                        "Priority",
                        "Planned Finish"
                    ]
                ],

                use_container_width=True,

                hide_index=True

            )

    st.divider()
        # =======================================================
    # RECENT ACTIVITY FEED
    # =======================================================

    st.subheader("🕒 Recent Activity Feed")

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
            .head(8)
        )

        st.dataframe(

            recent_df[
                [
                    "Activity ID",
                    "Activity Name",
                    "Project",
                    "Assigned To",
                    "Status",
                    "Created On"
                ]
            ],

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info(
            "Recent activity information is unavailable."
        )

    st.divider()

    # =======================================================
    # TODAY'S OPERATIONS SUMMARY
    # =======================================================

    st.subheader("Today's Operations Summary")

    summary = []

    summary.append(
        f"📋 Total monitored activities: **{total}**"
    )

    summary.append(
        f"✅ Completed activities: **{completed}**"
    )

    summary.append(
        f"⚙ Activities currently in progress: **{in_progress}**"
    )

    if overdue == 0:

        summary.append(
            "🟢 No overdue activities requiring attention."
        )

    else:

        summary.append(
            f"🔴 **{overdue}** overdue activities require immediate follow-up."
        )

    if due_this_week == 0:

        summary.append(
            "📅 No activities are due during the next 7 days."
        )

    else:

        summary.append(
            f"📅 **{due_this_week}** activities are due within the next 7 days."
        )

    for item in summary:

        st.success(item)

    st.divider()

    # =======================================================
    # FOOTER
    # =======================================================

    footer_left, footer_right = st.columns([3,1])

    with footer_left:

        st.caption(
            "Kent EPC Project Tracker • Operations Dashboard • Version 3.0"
        )

    with footer_right:

        st.caption(
            datetime.now().strftime("%d-%b-%Y")
        )
