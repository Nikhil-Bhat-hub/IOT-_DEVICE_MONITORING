import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
# -------------------------------
# DATABASE CONNECTION
# -------------------------------

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nikhil@2005",
        database="iot_monitoring"
    )

# -------------------------------
# FETCH DATA
# -------------------------------

def fetch_devices():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM devices", conn)
    conn.close()
    return df

def insert_device(data):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO devices 
    (device_id, device_name, location, status, signal_strength, data_usage_mb, last_active)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query, data)
    conn.commit()
    conn.close()

# -------------------------------
# STREAMLIT UI
# -------------------------------

st.set_page_config(page_title="IoT Monitoring Platform", layout="wide")

st.title("IoT Device Monitoring & KPI Analytics Platform")

menu = st.sidebar.selectbox("Menu", ["Dashboard", "Add Device", "AI Anomaly Detection"])

# -------------------------------
# DASHBOARD
# -------------------------------

if menu == "Dashboard":
    df = fetch_devices()

    if not df.empty:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Devices", len(df))
        col2.metric("Active Devices", len(df[df["status"]=="ACTIVE"]))
        col3.metric("Faulty Devices", len(df[df["status"]=="FAULTY"]))

        st.subheader("Data Usage Trend")
        fig = px.bar(df, x="device_id", y="data_usage_mb")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Device Status Distribution")
        fig2 = px.pie(df, names="status")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Device Table")
        st.dataframe(df)

    else:
        st.warning("No devices found.")

# -------------------------------
# ADD DEVICE
# -------------------------------

elif menu == "Add Device":
    st.subheader("Add New Device")

    device_id = st.text_input("Device ID")
    device_name = st.text_input("Device Name")
    location = st.text_input("Location")
    status = st.selectbox("Status", ["ACTIVE", "INACTIVE", "FAULTY"])
    signal_strength = st.slider("Signal Strength", 0, 100)
    data_usage = st.number_input("Data Usage (MB)", 0.0)
    last_active = st.date_input("Last Active")

    if st.button("Add Device"):
        insert_device((
            device_id,
            device_name,
            location,
            status,
            signal_strength,
            data_usage,
            datetime.combine(last_active, datetime.min.time())
        ))
        st.success("Device Added Successfully!")

# -------------------------------
# AI ANOMALY DETECTION
# -------------------------------

elif menu == "AI Anomaly Detection":
    st.subheader("AI-Based Device Anomaly Detection")

    df = fetch_devices()

    if len(df) > 2:
        features = df[["signal_strength", "data_usage_mb"]]

        model = IsolationForest(contamination=0.2)
        df["anomaly"] = model.fit_predict(features)

        df["anomaly"] = df["anomaly"].map({1: "Normal", -1: "Anomaly"})

        st.dataframe(df[["device_id", "signal_strength", "data_usage_mb", "anomaly"]])

        fig = px.scatter(
            df,
            x="signal_strength",
            y="data_usage_mb",
            color="anomaly",
            hover_data=["device_id"]
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Need at least 3 devices for AI detection.")

       
