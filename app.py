import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
def get_connection():
    conn = sqlite3.connect("iot_monitoring.db")
    return conn
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            device_id TEXT PRIMARY KEY,
            device_name TEXT,
            location TEXT,
            status TEXT,
            signal_strength INTEGER,
            data_usage_mb REAL,
            last_active TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()
def fetch_devices():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM devices", conn)
    conn.close()
    return df

def insert_device(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO devices
        (device_id, device_name, location, status, signal_strength, data_usage_mb, last_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()
st.set_page_config(page_title="IoT Monitoring Platform", layout="wide")

st.title("🚀 IoT Device Monitoring & KPI Analytics Platform")

menu = st.sidebar.selectbox("Menu", ["Dashboard", "Add Device", "AI Anomaly Detection"])
if menu == "Dashboard":
    df = fetch_devices()

    if not df.empty:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Devices", len(df))
        col2.metric("Active Devices", len(df[df["status"]=="ACTIVE"]))
        col3.metric("Faulty Devices", len(df[df["status"]=="FAULTY"]))

        st.subheader("📊 Data Usage Trend")
        fig = px.bar(df, x="device_id", y="data_usage_mb")
        st.plotly_chart(fig, width="stretch")

        st.subheader("📈 Device Status Distribution")
        fig2 = px.pie(df, names="status")
        st.plotly_chart(fig2, width="stretch")

        st.subheader("📋 Device Table")
        st.dataframe(df)

    else:
        st.warning("No devices found. Add some devices.")
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
            str(last_active)
        ))
        st.success("Device Added Successfully!")
elif menu == "AI Anomaly Detection":
    st.subheader("🤖 AI-Based Device Anomaly Detection")

    df = fetch_devices()

    if len(df) > 2:
        features = df[["signal_strength", "data_usage_mb"]]

        model = IsolationForest(contamination=0.2, random_state=42)
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

        st.plotly_chart(fig, width="stretch")

    else:
        st.warning("Need at least 3 devices for AI detection.")
