import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import get_tasks
from database import get_projects
from database import get_employees
from pages.activity_manager import show as activity_page
from pages.analytics import show as analytics_page
from pages.dashboard import show as dashboard_page
# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Kent EPC Tracker",
    page_icon="📋",
    layout="wide"
)
