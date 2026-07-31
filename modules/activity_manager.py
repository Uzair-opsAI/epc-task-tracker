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
# MASTER DATA
# ===========================================================

DISCIPLINES = [
    "Electrical",
    "Mechanical",
    "Civil",
    "Instrumentation",
    "Process"
]

PACKAGES = [

    "P&ID",

    "Line List",

    "Equipment Layout",

    "Equipment Datasheet",

    "Cable Schedule",

    "Single Line Diagram",

    "Cause & Effect",

    "Fire Proofing",

    "Hazardous Area",

    "Load List",

    "Instrument Index",

    "MTO",

    "Others"

]

PHASES = [

    "Development",

    "IDC",

    "LSO",

    "IFR",

    "IFR Review",

    "Comments Incorporation",

    "IFC",

    "Issued",

    "Completed"

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
# AUTO STATUS
# ===========================================================

def get_status(progress):

    if progress == 0:

        return "Not Started"

    elif progress == 100:

        return "Completed"

    else:

        return "In Progress"


# ===========================================================
# PAGE
# ===========================================================

def show():

    load_css()

    # =======================================================
    # HEADER
    # =======================================================

    st.title("📘 Engineering Activity Register")

    st.caption(
        "Engineering Deliverables & Activity Tracking"
    )

    info1, info2, info3 = st.columns([2,2,1])

    with info1:

        st.info(
            "Engineering Project Controls"
        )

    with info2:

        st.success(
            "Google Sheets Connected"
        )

    with info3:

        st.metric(
            "Updated",
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

    today = pd.Timestamp.today().normalize()

    total = len(tasks)

    completed = (
        tasks["Status"] == "Completed"
    ).sum()

    running = (
        tasks["Status"] == "In Progress"
    ).sum()

    not_started = (
        tasks["Status"] == "Not Started"
    ).sum()

    overdue = len(

        tasks[

            (
                tasks["Planned Finish"]
                < today
            )

            &

            (
                tasks["Status"]
                != "Completed"
            )

        ]

    )

    # =======================================================
    # KPI STRIP
    # =======================================================

    st.subheader("Engineering Portfolio")

    row1 = st.columns(4)

    with row1[0]:

        st.metric(
            "Activities",
            total
        )

    with row1[1]:

        st.metric(
            "Completed",
            completed
        )

    with row1[2]:

        st.metric(
            "Running",
            running
        )

    with row1[3]:

        st.metric(
            "Overdue",
            overdue
        )

    st.divider()

    # =======================================================
    # MAIN TABS
    # =======================================================

    register_tab, add_tab = st.tabs(

        [

            "📑 Engineering Register",

            "➕ Add Engineering Activity"

        ]

    )
        # =======================================================
    # ENGINEERING REGISTER
    # =======================================================

    with register_tab:

        st.subheader("Engineering Deliverables Register")

        # ===================================================
        # SEARCH
        # ===================================================

        search = st.text_input(
            "🔍 Search",
            placeholder="Search Activity ID, Activity Name, Project, Package or Engineer..."
        )

        # ===================================================
        # FILTERS
        # ===================================================

        f1, f2, f3 = st.columns(3)

        with f1:

            project_filter = st.selectbox(
                "Project",
                ["All"] +
                sorted(
                    tasks["Project"]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )

        with f2:

            discipline_filter = st.selectbox(
                "Discipline",
                ["All"] + DISCIPLINES
            )

        with f3:

            status_filter = st.selectbox(
                "Status",
                ["All"] + STATUS
            )

        f4, f5, f6 = st.columns(3)

        with f4:

            package_filter = st.selectbox(
                "Package",
                ["All"] + PACKAGES
            )

        with f5:

            phase_filter = st.selectbox(
                "Phase",
                ["All"] + PHASES
            )

        with f6:

            engineer_filter = st.selectbox(
                "Engineer",
                ["All"] +
                sorted(
                    tasks["Assigned To"]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )

        filtered = tasks.copy()

        # ===================================================
        # SEARCH
        # ===================================================

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

        # ===================================================
        # FILTERS
        # ===================================================

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

        # ---------------------------------------------------
        # Optional filters
        # ---------------------------------------------------

        if (
            package_filter != "All"
            and
            "Package" in filtered.columns
        ):

            filtered = filtered[
                filtered["Package"] == package_filter
            ]

        if (
            phase_filter != "All"
            and
            "Phase" in filtered.columns
        ):

            filtered = filtered[
                filtered["Phase"] == phase_filter
            ]

        if engineer_filter != "All":

            filtered = filtered[
                filtered["Assigned To"] == engineer_filter
            ]

        st.divider()

        # ===================================================
        # REGISTER SUMMARY
        # ===================================================

        left, right = st.columns([3,1])

        with left:

            st.info(
                f"Displaying **{len(filtered)}** of **{len(tasks)}** engineering activities."
            )

        with right:

            csv = filtered.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(

                "📥 Export Register",

                csv,

                file_name=f"Engineering_Register_{datetime.now().strftime('%Y%m%d')}.csv",

                mime="text/csv",

                use_container_width=True

            )

        st.divider()

        # ===================================================
        # ENGINEERING REGISTER TABLE
        # ===================================================

        preferred_columns = [

            "Activity ID",

            "Activity Name",

            "Project",

            "Discipline",

            "Package",

            "Phase",

            "Assigned To",

            "Planned Finish",

            "Progress",

            "Status"

        ]

        available_columns = [

            column

            for column in preferred_columns

            if column in filtered.columns

        ]

        st.dataframe(

            filtered[available_columns],

            use_container_width=True,

            hide_index=True,

            height=550

        )

        st.divider()

        # ===================================================
        # REGISTER STATISTICS
        # ===================================================

        s1, s2, s3, s4 = st.columns(4)

        with s1:

            st.metric(
                "Activities",
                len(filtered)
            )

        with s2:

            st.metric(
                "Projects",
                filtered["Project"].nunique()
            )

        with s3:

            st.metric(
                "Disciplines",
                filtered["Discipline"].nunique()
            )

        with s4:

            st.metric(
                "Engineers",
                filtered["Assigned To"].nunique()
            )

        st.divider()
            # =======================================================
    # ADD ENGINEERING ACTIVITY
    # =======================================================

    with add_tab:

        st.subheader("Add Engineering Activity")

        st.info(
            "Create a new engineering deliverable or schedule activity."
        )

        st.divider()

        # ===================================================
        # PROJECT INFORMATION
        # ===================================================

        st.markdown("### 📁 Project Information")

        p1, p2 = st.columns(2)

        with p1:

            project = st.selectbox(
                "Project *",
                get_project_names()
            )

            discipline = st.selectbox(
                "Discipline *",
                DISCIPLINES
            )

        with p2:

            package = st.selectbox(
                "Package *",
                PACKAGES
            )

            phase = st.selectbox(
                "Phase *",
                PHASES
            )

        st.divider()

        # ===================================================
        # ACTIVITY INFORMATION
        # ===================================================

        st.markdown("### 📋 Activity Information")

        a1, a2 = st.columns(2)

        with a1:

            activity_id = st.text_input(
                "Activity ID *",
                placeholder="OMCC-DE-PS-1000"
            )

            activity_name = st.text_input(
                "Activity Name *",
                placeholder="P&ID Construction - Development"
            )

        with a2:

            duration = st.number_input(
                "Duration (Days)",
                min_value=1,
                value=10
            )

            priority = st.selectbox(
                "Priority",
                PRIORITIES
            )

        st.divider()

        # ===================================================
        # PLANNING INFORMATION
        # ===================================================

        st.markdown("### 📅 Planning Information")

        d1, d2 = st.columns(2)

        with d1:

            planned_start = st.date_input(
                "Planned Start"
            )

            predecessor = st.text_input(
                "Predecessor",
                placeholder="OMCC-DE-PS-0990"
            )

        with d2:

            planned_finish = st.date_input(
                "Planned Finish"
            )

            successor = st.text_input(
                "Successor (Optional)"
            )

        st.divider()

        # ===================================================
        # ENGINEERING ASSIGNMENT
        # ===================================================

        st.markdown("### 👨‍💼 Engineering Assignment")

        e1, e2 = st.columns(2)

        with e1:

            lead = st.selectbox(
                "Lead Engineer",
                get_employee_names()
            )

        with e2:

            assigned = st.selectbox(
                "Assigned Engineer",
                get_employee_names()
            )

        st.divider()

        # ===================================================
        # PROGRESS
        # ===================================================

        st.markdown("### 📊 Progress")

        progress = st.slider(
            "Progress (%)",
            0,
            100,
            0
        )

        status = get_status(progress)

        st.success(
            f"Current Status : **{status}**"
        )

        remarks = st.text_area(
            "Engineering Remarks",
            height=120,
            placeholder="Design comments, assumptions, client remarks, IFC notes..."
        )

        st.divider()

        # ===================================================
        # VALIDATION
        # ===================================================

        error = False

        if planned_finish < planned_start:

            st.error(
                "Finish date cannot be before start date."
            )

            error = True

        if activity_id.strip() == "":

            st.error(
                "Activity ID is mandatory."
            )

            error = True

        if activity_name.strip() == "":

            st.error(
                "Activity Name is mandatory."
            )

            error = True

        existing_ids = (
            tasks["Activity ID"]
            .astype(str)
            .str.upper()
            .tolist()
        )

        if activity_id.upper() in existing_ids:

            st.error(
                "Activity ID already exists."
            )

            error = True

        st.divider()

        # ===================================================
        # ENGINEERING PREVIEW
        # ===================================================

        with st.expander(
            "📄 Activity Preview",
            expanded=False
        ):

            preview = pd.DataFrame({

                "Field":[

                    "Project",

                    "Discipline",

                    "Package",

                    "Phase",

                    "Activity ID",

                    "Activity",

                    "Duration",

                    "Lead",

                    "Assigned",

                    "Priority",

                    "Progress",

                    "Status"

                ],

                "Value":[

                    project,

                    discipline,

                    package,

                    phase,

                    activity_id,

                    activity_name,

                    duration,

                    lead,

                    assigned,

                    priority,

                    f"{progress}%",

                    status

                ]

            })

            st.dataframe(

                preview,

                use_container_width=True,

                hide_index=True

            )

        st.divider()
