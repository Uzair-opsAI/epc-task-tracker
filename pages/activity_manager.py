import streamlit as st
from components.styles import load_css
from database import (
    get_tasks,
    add_activity,
    get_project_names,
    get_employee_names
)

DISCIPLINES = ["Electrical","Mechanical","Civil","Instrumentation","Process"]
PRIORITIES = ["Critical","High","Medium","Low"]
STATUS = ["Not Started","In Progress","Waiting for Review","Completed","On Hold"]

def show():
    load_css()
    st.title("📋 Activity Manager")

    tab1, tab2 = st.tabs(["📄 Activities","➕ Add Activity"])

    with tab1:

        tasks = get_tasks()

        st.subheader("📄 Activity Register")

        search = st.text_input(
            "🔍 Search Activity",
            placeholder="Search by Activity ID, Activity Name or Project"
        )

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            project_filter = st.selectbox(
                "Project",
                ["All"] + sorted(tasks["Project"].dropna().unique().tolist())
            )

        with col2:
            discipline_filter = st.selectbox(
                "Discipline",
                ["All"] + sorted(tasks["Discipline"].dropna().unique().tolist())
            )

        with col3:
            status_filter = st.selectbox(
                "Status",
                ["All"] + sorted(tasks["Status"].dropna().unique().tolist())
            )

        with col4:
            priority_filter = st.selectbox(
                "Priority",
                ["All"] + sorted(tasks["Priority"].dropna().unique().tolist())
            )

        filtered = tasks.copy()

        if search:
            filtered = filtered[
                filtered.astype(str).apply(
                    lambda row: row.str.contains(search, case=False, na=False).any(),
                    axis=1
                )
            ]

        if project_filter != "All":
            filtered = filtered[filtered["Project"] == project_filter]

        if discipline_filter != "All":
            filtered = filtered[filtered["Discipline"] == discipline_filter]

        if status_filter != "All":
            filtered = filtered[filtered["Status"] == status_filter]

        if priority_filter != "All":
            filtered = filtered[filtered["Priority"] == priority_filter]

        st.data_editor(
            filtered,
            use_container_width=True,
            hide_index=True,
            disabled=True
        )

    with tab2:

        st.subheader("➕ Add New Activity")

        activity_id = st.text_input("Activity ID")
        activity_name = st.text_input("Activity Name")

        project = st.selectbox("Project", get_project_names())
        category = st.text_input("Category")
        discipline = st.selectbox("Discipline", DISCIPLINES)
        lead = st.selectbox("Lead", get_employee_names())
        assigned = st.selectbox("Assigned To", get_employee_names())
        priority = st.selectbox("Priority", PRIORITIES)

        start = st.date_input("Planned Start")
        finish = st.date_input("Planned Finish")

        progress = st.slider("Progress (%)",0,100,0)
        status = st.selectbox("Status", STATUS)
        remarks = st.text_area("Remarks")

        if st.button("💾 Save Activity", use_container_width=True):

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

            st.success("✅ Activity Added Successfully!")
            st.rerun()
