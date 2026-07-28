import streamlit as st
from database import (
    get_tasks,
    add_activity,
    get_project_names,
    get_employee_names
)

def show():

    st.title("📋 Activity Manager")

    tab1, tab2 = st.tabs(["📄 Activities", "➕ Add Activity"])

    with tab1:

        tasks = get_tasks()

        st.dataframe(
            tasks,
            use_container_width=True,
            hide_index=True
        )

    with tab2:

        st.subheader("Add New Activity")

        activity_id = st.text_input("Activity ID")

        activity_name = st.text_input("Activity Name")

        project = st.selectbox(
            "Project",
            get_project_names()
        )

        category = st.text_input("Category")

        discipline = st.selectbox(
            "Discipline",
            [
                "Electrical",
                "Mechanical",
                "Civil",
                "Instrumentation",
                "Process"
            ]
        )

        lead = st.selectbox(
            "Lead",
            get_employee_names()
        )

        assigned = st.selectbox(
            "Assigned To",
            get_employee_names()
        )

        priority = st.selectbox(
            "Priority",
            [
                "Critical",
                "High",
                "Medium",
                "Low"
            ]
        )

        start = st.date_input("Planned Start")

        finish = st.date_input("Planned Finish")

        progress = st.slider(
            "Progress",
            0,
            100,
            0
        )

        status = st.selectbox(
            "Status",
            [
                "Not Started",
                "In Progress",
                "Waiting for Review",
                "Completed",
                "On Hold"
            ]
        )

        remarks = st.text_area("Remarks")

        if st.button("💾 Save Activity"):

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

            st.success("Activity Added Successfully!")

            st.rerun()
