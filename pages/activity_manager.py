import streamlit as st
import pandas as pd
from datetime import datetime

from components.styles import load_css

from database import (
    get_tasks,
    add_activity,
    get_project_names,
    get_employee_names
)

# ===========================================================
# CONSTANTS
# ===========================================================

DISCIPLINES = [
    "Electrical",
    "Mechanical",
    "Civil",
    "Instrumentation",
    "Process"
]

PRIORITIES = [
    "Critical",
    "High",
    "Medium",
    "Low"
]

STATUS = [
    "Not Started",
    "In Progress",
    "Waiting for Review",
    "Completed",
    "On Hold"
]

# ===========================================================
# PAGE
# ===========================================================

def show():

    load_css()

    # =======================================================
    # HEADER
    # =======================================================

    st.title("📋 Activity Manager")

    st.caption(
        "Manage EPC engineering activities, assignments and progress."
    )

    tasks = get_tasks()

    if tasks.empty:

        st.warning("No activities available.")

        st.stop()

    # =======================================================
    # DATA PREPARATION
    # =======================================================

    tasks["Progress"] = pd.to_numeric(
        tasks["Progress"],
        errors="coerce"
    ).fillna(0)

    tasks["Planned Finish"] = pd.to_datetime(
        tasks["Planned Finish"],
        errors="coerce"
    )

    today = pd.Timestamp.today()

    total = len(tasks)

    completed = (
        tasks["Status"] == "Completed"
    ).sum()

    in_progress = (
        tasks["Status"] == "In Progress"
    ).sum()

    not_started = (
        tasks["Status"] == "Not Started"
    ).sum()

    overdue = (

        (

            tasks["Planned Finish"] < today

        )

        &

        (

            tasks["Status"] != "Completed"

        )

    ).sum()

    # =======================================================
    # KPI DASHBOARD
    # =======================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "📋 Total Activities",
            total
        )

    with c2:

        st.metric(
            "🟢 Completed",
            completed
        )

    with c3:

        st.metric(
            "🟡 In Progress",
            in_progress
        )

    with c4:

        st.metric(
            "🔴 Overdue",
            overdue
        )

    st.divider()

    # =======================================================
    # TABS
    # =======================================================

    tab1, tab2 = st.tabs(

        [

            "📄 Activity Register",

            "➕ Add Activity"

        ]

    )
    with tab1:

        st.subheader("📄 Activity Register")

        # =======================================================
        # SEARCH
        # =======================================================

        search = st.text_input(
            "🔍 Search Activities",
            placeholder="Search by Activity ID, Activity Name, Project, Lead or Assigned To..."
        )

        # =======================================================
        # FILTERS
        # =======================================================

        filter1, filter2, filter3, filter4 = st.columns(4)

        with filter1:

            project_filter = st.selectbox(
                "Project",
                ["All"] + sorted(tasks["Project"].dropna().unique().tolist())
            )

        with filter2:

            discipline_filter = st.selectbox(
                "Discipline",
                ["All"] + sorted(tasks["Discipline"].dropna().unique().tolist())
            )

        with filter3:

            status_filter = st.selectbox(
                "Status",
                ["All"] + sorted(tasks["Status"].dropna().unique().tolist())
            )

        with filter4:

            priority_filter = st.selectbox(
                "Priority",
                ["All"] + sorted(tasks["Priority"].dropna().unique().tolist())
            )

        filtered = tasks.copy()

        # =======================================================
        # APPLY SEARCH
        # =======================================================

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
        # APPLY FILTERS
        # =======================================================

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

        # =======================================================
        # SUMMARY
        # =======================================================

        left, right = st.columns([2, 1])

        with left:

            st.info(
                f"Displaying **{len(filtered)}** of **{len(tasks)}** activities."
            )

        with right:

            csv = filtered.to_csv(index=False).encode("utf-8")

            st.download_button(
                "📥 Export CSV",
                csv,
                file_name=f"Activity_Register_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # =======================================================
        # TABLE
        # =======================================================

        display_columns = [
            "Activity ID",
            "Activity Name",
            "Project",
            "Discipline",
            "Lead",
            "Assigned To",
            "Priority",
            "Planned Start",
            "Planned Finish",
            "Progress",
            "Status"
        ]

        available_columns = [
            col for col in display_columns
            if col in filtered.columns
        ]

        st.dataframe(
            filtered[available_columns],
            use_container_width=True,
            hide_index=True,
            height=550
        )

        # =======================================================
        # QUICK SUMMARY
        # =======================================================

        st.divider()

        s1, s2, s3 = st.columns(3)

        with s1:

            st.metric(
                "Displayed Activities",
                len(filtered)
            )

        with s2:

            st.metric(
                "Projects",
                filtered["Project"].nunique()
            )

        with s3:

            st.metric(
                "Employees",
                filtered["Assigned To"].nunique()
            )
    with tab2:

        st.subheader("➕ Add New Activity")

        st.info(
            "Complete the activity details below. Fields marked with * are mandatory."
        )

        st.divider()

        # ======================================================
        # ROW 1
        # ======================================================

        col1, col2 = st.columns(2)

        with col1:

            activity_id = st.text_input(
                "Activity ID *",
                placeholder="e.g. ELEC-001"
            )

            activity_name = st.text_input(
                "Activity Name *",
                placeholder="Cable Routing Review"
            )

            project = st.selectbox(
                "Project *",
                get_project_names()
            )

            category = st.text_input(
                "Category",
                placeholder="Engineering / Procurement / Construction"
            )

        with col2:

            discipline = st.selectbox(
                "Discipline *",
                DISCIPLINES
            )

            priority = st.selectbox(
                "Priority",
                PRIORITIES
            )

            status = st.selectbox(
                "Status",
                STATUS
            )

            progress = st.slider(
                "Progress (%)",
                min_value=0,
                max_value=100,
                value=0
            )

        st.divider()

        # ======================================================
        # ROW 2
        # ======================================================

        col3, col4 = st.columns(2)

        with col3:

            lead = st.selectbox(
                "Lead Engineer *",
                get_employee_names()
            )

            assigned = st.selectbox(
                "Assigned To *",
                get_employee_names()
            )

        with col4:

            start = st.date_input(
                "Planned Start"
            )

            finish = st.date_input(
                "Planned Finish"
            )

        st.divider()

        remarks = st.text_area(
            "Remarks",
            height=120,
            placeholder="Enter activity notes, dependencies, risks or comments..."
        )

        st.divider()

        # ======================================================
        # VALIDATION
        # ======================================================

        error = False

        if finish < start:

            st.error(
                "Planned Finish cannot be earlier than Planned Start."
            )

            error = True

        if activity_id.strip() == "":

            st.warning(
                "Activity ID is mandatory."
            )

            error = True

        if activity_name.strip() == "":

            st.warning(
                "Activity Name is mandatory."
            )

            error = True

        existing_ids = (
            tasks["Activity ID"]
            .astype(str)
            .str.upper()
            .tolist()
        )

        duplicate = (
            activity_id.upper()
            in existing_ids
        )

        if duplicate:

            st.error(
                "Activity ID already exists."
            )

            error = True

        st.divider()

        # ======================================================
        # PREVIEW
        # ======================================================

        with st.expander(
            "👁 Preview Activity",
            expanded=False
        ):

            preview = pd.DataFrame({

                "Field":[
                    "Activity ID",
                    "Activity Name",
                    "Project",
                    "Category",
                    "Discipline",
                    "Lead",
                    "Assigned To",
                    "Priority",
                    "Status",
                    "Progress",
                    "Planned Start",
                    "Planned Finish"
                ],

                "Value":[
                    activity_id,
                    activity_name,
                    project,
                    category,
                    discipline,
                    lead,
                    assigned,
                    priority,
                    status,
                    f"{progress} %",
                    start,
                    finish
                ]

            })

            st.dataframe(
                preview,
                use_container_width=True,
                hide_index=True
            )

        st.divider()
        # ======================================================
        # ACTIVITY INSIGHTS
        # ======================================================

        st.subheader("📊 Activity Insights")

        insight1, insight2, insight3 = st.columns(3)

        with insight1:

            st.metric(
                "Current Progress",
                f"{progress}%"
            )

        with insight2:

            duration = (finish - start).days

            st.metric(
                "Planned Duration",
                f"{duration} Days"
            )

        with insight3:

            st.metric(
                "Selected Priority",
                priority
            )

        if progress == 100:

            st.success("🟢 Activity will be created as Completed.")

        elif progress >= 75:

            st.info("🔵 Activity is nearing completion.")

        elif progress >= 40:

            st.warning("🟡 Activity is currently in progress.")

        else:

            st.error("🔴 Activity has just started or is pending.")

        st.divider()

        # ======================================================
        # SAVE BUTTON
        # ======================================================

        if st.button(
            "💾 Save Activity",
            use_container_width=True,
            type="primary"
        ):

            if error:

                st.stop()

            add_activity({

                "Activity_ID": activity_id,

                "Activity_Name": activity_name,

                "Project": project,

                "Category": category,

                "Discipline": discipline,

                "Lead": lead,

                "Assigned_To": assigned,

                "Priority": priority,

                "Planned_Start": str(start),

                "Planned_Finish": str(finish),

                "Progress": progress,

                "Status": status,

                "Remarks": remarks

            })

            st.success(
                f"""
✅ Activity **{activity_id}** has been successfully added.

Project : {project}

Assigned To : {assigned}
"""
            )

            st.toast(
                "Activity added successfully.",
                icon="✅"
            )

            st.balloons()

            st.cache_data.clear()

            st.rerun()
