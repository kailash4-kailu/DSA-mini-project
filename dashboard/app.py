"""
Real-Time IoT Sensor Streaming Analytics Dashboard
====================================================
Professional Streamlit dashboard that reads from MySQL and auto-refreshes.
"""

import os
import sys
import time
import logging

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

load_dotenv()

from database.db import (
    fetch_recent_readings,
    fetch_metrics,
    fetch_top_anomalies,
    fetch_device_ids,
    fetch_total_counts,
)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Real-Time IoT Sensor Streaming Analytics",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS for professional look
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Main background */
    .main .block-container {padding-top: 1rem; padding-bottom: 1rem;}

    /* KPI card styling */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px 16px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        margin-bottom: 8px;
    }
    .kpi-card.green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .kpi-card.orange {
        background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
    }
    .kpi-card.red {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    }
    .kpi-card.blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .kpi-card.purple {
        background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
    }
    .kpi-card h3 {
        font-size: 14px;
        margin: 0 0 4px 0;
        opacity: 0.9;
        font-weight: 400;
    }
    .kpi-card h1 {
        font-size: 28px;
        margin: 0;
        font-weight: 700;
    }

    /* Status badges */
    .status-normal {
        background-color: #38ef7d; color: #1a1a2e; padding: 6px 16px;
        border-radius: 20px; font-weight: 700; display: inline-block;
    }
    .status-warning {
        background-color: #f2c94c; color: #1a1a2e; padding: 6px 16px;
        border-radius: 20px; font-weight: 700; display: inline-block;
    }
    .status-critical {
        background-color: #eb3349; color: white; padding: 6px 16px;
        border-radius: 20px; font-weight: 700; display: inline-block;
    }

    /* Sidebar */
    .css-1d391kg {padding-top: 1rem;}

    /* Hide hamburger and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


def kpi_card(title: str, value, css_class: str = ""):
    """Render a styled KPI card."""
    st.markdown(
        f'<div class="kpi-card {css_class}"><h3>{title}</h3><h1>{value}</h1></div>',
        unsafe_allow_html=True,
    )


def status_badge(anomaly_ratio: float) -> str:
    """Determine system status based on recent anomaly ratio."""
    if anomaly_ratio > 0.3:
        return '<span class="status-critical">🔴 CRITICAL</span>'
    elif anomaly_ratio > 0.1:
        return '<span class="status-warning">🟡 WARNING</span>'
    else:
        return '<span class="status-normal">🟢 NORMAL</span>'


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/sensor.png", width=64)
    st.title("🔧 Controls")

    refresh_rate = st.slider(
        "Refresh interval (sec)",
        min_value=1,
        max_value=30,
        value=int(os.getenv("DASHBOARD_REFRESH_SECONDS", "3")),
    )

    # Device filter
    device_ids = fetch_device_ids()
    device_options = ["All"] + device_ids
    selected_device = st.selectbox("📟 Device Filter", device_options, index=0)

    limit = st.slider("Recent readings", 50, 500, 200, 50)

    st.markdown("---")
    st.markdown("### 🏗️ Architecture")
    st.markdown(
        """
        ```
        CSV → Kafka Producer
              ↓
        Kafka Topic
              ↓
        Stream Processor
          ├─ Isolation Forest
          ├─ Sliding Windows
          ├─ Running Stats
          └─ Heap Tracker
              ↓
           MySQL
              ↓
        This Dashboard
        ```
        """
    )
    st.markdown("---")
    st.caption(f"Auto-refresh every {refresh_rate}s")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("# 📡 Real-Time IoT Sensor Streaming Analytics")
st.markdown("*Live monitoring of IoT sensor data processed through Kafka → ML → MySQL pipeline*")
st.markdown("---")

# ---------------------------------------------------------------------------
# Fetch data
# ---------------------------------------------------------------------------
counts = fetch_total_counts()
total_readings = counts.get("total", 0) or 0
total_anomalies = int(counts.get("anomalies", 0) or 0)

readings_raw = fetch_recent_readings(device_id=selected_device, limit=limit)
df = pd.DataFrame(readings_raw) if readings_raw else pd.DataFrame()

metrics_raw = fetch_metrics()
metrics_df = pd.DataFrame(metrics_raw) if metrics_raw else pd.DataFrame()

top_anomalies_raw = fetch_top_anomalies(limit=10)
top_anom_df = pd.DataFrame(top_anomalies_raw) if top_anomalies_raw else pd.DataFrame()

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
if not df.empty:
    latest = df.iloc[0]  # newest record (ORDER BY id DESC)
    recent_anomaly_ratio = df["is_anomaly"].mean() if "is_anomaly" in df.columns else 0

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        kpi_card("🌡️ Temperature", f"{latest.get('temperature', '—')} °C", "orange")
    with k2:
        kpi_card("💧 Humidity", f"{latest.get('humidity', '—')} %", "blue")
    with k3:
        kpi_card("🔵 Pressure", f"{latest.get('pressure', '—')} hPa", "purple")
    with k4:
        kpi_card("📳 Vibration", f"{latest.get('vibration', '—')} mm/s", "green")
    with k5:
        kpi_card("📊 Total Readings", f"{total_readings:,}", "")
    with k6:
        kpi_card("⚠️ Anomalies", f"{total_anomalies:,}", "red")

    # Status badge
    st.markdown(f"### Sensor Status: {status_badge(recent_anomaly_ratio)}", unsafe_allow_html=True)
else:
    st.info("⏳ Waiting for data… Start the producer and processor to see live data.")

# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
if not df.empty and "timestamp" in df.columns:
    # Sort ascending for time-series plots
    plot_df = df.sort_values("id", ascending=True).copy()
    plot_df["row_num"] = range(len(plot_df))

    st.markdown("---")
    col_left, col_right = st.columns(2)

    # ── Live sensor chart ──
    with col_left:
        st.markdown("### 📈 Live Temperature Readings")
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=plot_df["timestamp"], y=plot_df["temperature"],
            mode="lines+markers", name="Temperature",
            line=dict(color="#f2994a", width=2),
            marker=dict(size=3),
        ))
        fig_temp.update_layout(
            xaxis_title="Time", yaxis_title="Temperature (°C)",
            template="plotly_dark", height=350,
            margin=dict(l=40, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    # ── Rolling average vs actual ──
    with col_right:
        st.markdown("### 📉 Temperature: Actual vs Rolling Average")
        fig_roll = go.Figure()
        fig_roll.add_trace(go.Scatter(
            x=plot_df["timestamp"], y=plot_df["temperature"],
            mode="lines", name="Actual",
            line=dict(color="#4facfe", width=1.5),
        ))
        if "rolling_temperature" in plot_df.columns:
            fig_roll.add_trace(go.Scatter(
                x=plot_df["timestamp"], y=plot_df["rolling_temperature"],
                mode="lines", name="Rolling Avg (30)",
                line=dict(color="#f45c43", width=2.5, dash="dash"),
            ))
        fig_roll.update_layout(
            xaxis_title="Time", yaxis_title="Temperature (°C)",
            template="plotly_dark", height=350,
            margin=dict(l=40, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_roll, use_container_width=True)

    # ── Anomaly visualization ──
    st.markdown("### 🚨 Anomaly Detection Visualization")
    normal_df = plot_df[plot_df["is_anomaly"] == 0]
    anomaly_df = plot_df[plot_df["is_anomaly"] == 1]

    fig_anom = go.Figure()
    fig_anom.add_trace(go.Scatter(
        x=normal_df["timestamp"], y=normal_df["temperature"],
        mode="markers", name="Normal",
        marker=dict(color="#38ef7d", size=5, opacity=0.6),
    ))
    fig_anom.add_trace(go.Scatter(
        x=anomaly_df["timestamp"], y=anomaly_df["temperature"],
        mode="markers", name="Anomaly",
        marker=dict(color="#eb3349", size=10, symbol="x", line=dict(width=2, color="white")),
    ))
    fig_anom.update_layout(
        xaxis_title="Time", yaxis_title="Temperature (°C)",
        template="plotly_dark", height=350,
        margin=dict(l=40, r=20, t=10, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_anom, use_container_width=True)

    # ── Multi-metric chart ──
    st.markdown("---")
    mc1, mc2 = st.columns(2)

    with mc1:
        st.markdown("### 💧 Humidity")
        fig_h = go.Figure()
        fig_h.add_trace(go.Scatter(
            x=plot_df["timestamp"], y=plot_df["humidity"],
            mode="lines", name="Humidity", line=dict(color="#4facfe", width=1.5),
        ))
        if "rolling_humidity" in plot_df.columns:
            fig_h.add_trace(go.Scatter(
                x=plot_df["timestamp"], y=plot_df["rolling_humidity"],
                mode="lines", name="Rolling Avg", line=dict(color="#f2c94c", width=2, dash="dash"),
            ))
        fig_h.update_layout(template="plotly_dark", height=300, margin=dict(l=40, r=20, t=10, b=40))
        st.plotly_chart(fig_h, use_container_width=True)

    with mc2:
        st.markdown("### 📳 Vibration")
        fig_v = go.Figure()
        fig_v.add_trace(go.Scatter(
            x=plot_df["timestamp"], y=plot_df["vibration"],
            mode="lines", name="Vibration", line=dict(color="#a18cd1", width=1.5),
        ))
        if "rolling_vibration" in plot_df.columns:
            fig_v.add_trace(go.Scatter(
                x=plot_df["timestamp"], y=plot_df["rolling_vibration"],
                mode="lines", name="Rolling Avg", line=dict(color="#38ef7d", width=2, dash="dash"),
            ))
        fig_v.update_layout(template="plotly_dark", height=300, margin=dict(l=40, r=20, t=10, b=40))
        st.plotly_chart(fig_v, use_container_width=True)

# ---------------------------------------------------------------------------
# Per-device metrics table
# ---------------------------------------------------------------------------
if not metrics_df.empty:
    st.markdown("---")
    st.markdown("### 📊 Device Metrics Summary")
    display_cols = [
        "device_id", "total_readings", "anomaly_count",
        "avg_temperature", "avg_humidity", "avg_pressure", "avg_vibration",
        "min_temperature", "max_temperature",
    ]
    available = [c for c in display_cols if c in metrics_df.columns]
    st.dataframe(metrics_df[available], use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Top anomalies
# ---------------------------------------------------------------------------
if not top_anom_df.empty:
    st.markdown("### 🏆 Top Anomaly-Score Events")
    display_cols = [
        "timestamp", "device_id", "temperature", "humidity",
        "pressure", "vibration", "anomaly_score",
    ]
    available = [c for c in display_cols if c in top_anom_df.columns]
    st.dataframe(top_anom_df[available], use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Recent events table
# ---------------------------------------------------------------------------
if not df.empty:
    st.markdown("---")
    st.markdown("### 🕐 Recent Sensor Events")
    show_cols = [
        "timestamp", "device_id", "temperature", "humidity",
        "pressure", "vibration", "anomaly_score", "is_anomaly",
    ]
    available = [c for c in show_cols if c in df.columns]
    recent_table = df.head(20)[available]
    st.dataframe(recent_table, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Auto-refresh
# ---------------------------------------------------------------------------
time.sleep(refresh_rate)
st.rerun()
