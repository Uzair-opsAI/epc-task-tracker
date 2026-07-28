import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ----------------------------------------------------
# Google Sheets Connection
# ----------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_resource
def connect_google_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    return client


# ----------------------------------------------------
# Open Spreadsheet
# ----------------------------------------------------

def open_sheet(sheet_name="EPC Task Tracker"):

    client = connect_google_sheet()

    return client.open(sheet_name)


# ----------------------------------------------------
# Read Tasks
# ----------------------------------------------------

def get_tasks():

    sheet = open_sheet()

    worksheet = sheet.worksheet("Tasks")

    data = worksheet.get_all_records()

    return pd.DataFrame(data)


# ----------------------------------------------------
# Read Projects
# ----------------------------------------------------

def get_projects():

    sheet = open_sheet()

    worksheet = sheet.worksheet("Projects")

    data = worksheet.get_all_records()

    return pd.DataFrame(data)


# ----------------------------------------------------
# Read Employees
# ----------------------------------------------------

def get_employees():

    sheet = open_sheet()

    worksheet = sheet.worksheet("Employees")

    data = worksheet.get_all_records()

    return pd.DataFrame(data)
from datetime import datetime

# ----------------------------------------------------
# Add New Activity
# ----------------------------------------------------

def add_activity(activity):

    sheet = open_sheet()

    worksheet = sheet.worksheet("Tasks")

    worksheet.append_row([
        activity["Activity_ID"],
        activity["Activity_Name"],
        activity["Project"],
        activity["Category"],
        activity["Discipline"],
        activity["Lead"],
        activity["Assigned_To"],
        activity["Priority"],
        activity["Planned_Start"],
        activity["Planned_Finish"],
        activity["Progress"],
        activity["Status"],
        activity["Remarks"],
        datetime.now().strftime("%d-%b-%Y %H:%M")
    ])

# ----------------------------------------------------
# Get Project Names
# ----------------------------------------------------

def get_project_names():

    projects = get_projects()

    return projects["Project"].tolist()


# ----------------------------------------------------
# Get Employee Names
# ----------------------------------------------------

def get_employee_names():

    employees = get_employees()

    return employees["Employee"].tolist()
