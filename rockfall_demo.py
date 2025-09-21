import streamlit as st
import random

st.set_page_config(page_title="Rockfall Prediction Demo", layout="wide")
st.title("AI-based Rockfall Prediction Dashboard")

# Simulated Zones & Risk Levels
zones = ["Zone 1", "Zone 2", "Zone 3", "Zone 4"]
risk_levels = ["Low", "Medium", "High"]

st.sidebar.header("Simulated Sensor Inputs")
rainfall = st.sidebar.slider("Rainfall (mm)", 0, 200, 50)
displacement = st.sidebar.slider("Displacement (mm)", 0, 50, 10)

st.subheader("Risk Alerts")
for zone in zones:
    risk = random.choices(risk_levels, weights=[0.5, 0.3, 0.2])[0]
    if risk == "High":
        st.error(f"⚠️ {zone} — HIGH RISK! Evacuate immediately!")
    elif risk == "Medium":
        st.warning(f"⚠️ {zone} — Medium Risk, monitor closely.")
    else:
        st.success(f"✅ {zone} — Low Risk")

st.subheader("Risk Map (Simulated)")
st.text("🔹 Here you can show a heatmap overlay of risk zones using Folium or Plotly")
