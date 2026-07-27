
import streamlit as st
import pandas as pd

st.set_page_config(page_title="EPC Task Tracker", layout="wide")

st.title("📋 EPC Task Tracker (Starter)")
st.info("Next step: connect Google Sheets. This starter verifies your Streamlit deployment.")

@st.cache_data
def load_demo():
    return pd.DataFrame([
        {"Task_ID":1,"Task_Name":"Cable Schedule Review","Assigned_To":"Zulfiqar","Office":"Vadodara","Status":"In Progress"},
        {"Task_ID":2,"Task_Name":"Lighting Calculation","Assigned_To":"Rahul","Office":"Mumbai","Status":"Not Started"},
        {"Task_ID":3,"Task_Name":"Panel Datasheet","Assigned_To":"Amit","Office":"Mumbai","Status":"Completed"},
    ])

df=load_demo()

c1,c2,c3=st.columns(3)
c1.metric("Total Tasks",len(df))
c2.metric("Completed",(df["Status"]=="Completed").sum())
c3.metric("In Progress",(df["Status"]=="In Progress").sum())

office=st.selectbox("Office",["All"]+sorted(df["Office"].unique().tolist()))
if office!="All":
    df=df[df["Office"]==office]
st.dataframe(df,use_container_width=True)

st.success("Deployment successful. In the next step you'll replace this demo data with live Google Sheets.")
