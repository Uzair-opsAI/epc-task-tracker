import streamlit as st

def metric_card(title, value, **kwargs):
    st.success(f"{title}: {value}")

def success_card(title, value):
    metric_card(title, value)

def warning_card(title, value):
    metric_card(title, value)

def danger_card(title, value):
    metric_card(title, value)

def info_card(title, value):
    metric_card(title, value)
