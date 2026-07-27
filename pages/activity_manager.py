import streamlit as st
from database import get_tasks

def show():

    st.title("📋 Activity Manager")

    st.markdown("---")

    tasks = get_tasks()

    st.dataframe(
        tasks,
        use_container_width=True,
        hide_index=True
    )
