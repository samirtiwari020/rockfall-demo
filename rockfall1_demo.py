import streamlit as st
import random
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Rockfall Prediction Dashboard", layout="wide")
st.title("AI-based Rockfall Prediction Dashboard")

# --- Sidebar: Simulated Inputs ---
st.sidebar.header("Simulated Sensor Inputs")
rainfall = st.sidebar.slider("Rainfall (mm)", 0, 200, 50)
displacement = st.sidebar.slider("Displacement (mm)", 0, 50, 10)
strain = st.sidebar.slider("Strain (mm/m)", 0, 5, 1)

# --- Main Layout ---
col1, col2 = st.columns([2,1])

# --- Column 1: Risk Map ---
with col1:
    st.subheader("Risk Map (Simulated)")

    # Simulate 4 zones with coordinates
    zone_coords = {"Zone 1": [28.5,77.0],
                   "Zone 2": [28.51,77.01],
                   "Zone 3": [28.52,77.02],
                   "Zone 4": [28.53,77.03]}
    
    # Initialize Map
    m = folium.Map(location=[28.515,77.015], zoom_start=14)
    
    # Risk DataFrame for Graph
    df_risk = pd.DataFrame(columns=["Zone", "Risk Level", "Probability"])
    
    for zone, coord in zone_coords.items():
        # Random risk probabilities
        prob = random.randint(0,100)
        if prob>70:
            risk = "High"
            color = "red"
        elif prob>40:
            risk = "Medium"
            color = "orange"
        else:
            risk = "Low"
            color = "green"
        
        folium.CircleMarker(location=coord, radius=15, color=color, fill=True, fill_color=color,
                            popup=f"{zone}: {risk} Risk ({prob}%)").add_to(m)
        
        df_risk = pd.concat([df_risk, pd.DataFrame([[zone, risk, prob]], columns=df_risk.columns)], ignore_index=True)
    
    # Add Legend
    legend_html = """
     <div style="position: fixed; bottom: 50px; left: 50px; width:120px; height:90px;
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding:10px;">
     <b>Risk Legend</b><br>
     <i style="color:green">● Low</i><br>
     <i style="color:orange">● Medium</i><br>
     <i style="color:red">● High</i>
     </div>
     """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    st_folium(m, width=700, height=500)

# --- Column 2: Alerts & Stats ---
with col2:
    st.subheader("Dynamic Alerts")
    for idx, row in df_risk.iterrows():
        if row["Risk Level"]=="High":
            st.markdown(f"<h4 style='color:red'>⚠️ {row['Zone']} — HIGH RISK ({row['Probability']}%)!</h4>", unsafe_allow_html=True)
        elif row["Risk Level"]=="Medium":
            st.markdown(f"<h4 style='color:orange'>⚠️ {row['Zone']} — Medium Risk ({row['Probability']}%)</h4>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h4 style='color:green'>✅ {row['Zone']} — Low Risk ({row['Probability']}%)</h4>", unsafe_allow_html=True)
    
    st.subheader("Current Sensor Stats")
    st.metric("Rainfall (mm)", rainfall)
    st.metric("Displacement (mm)", displacement)
    st.metric("Strain (mm/m)", strain)

    st.subheader("Risk Probability Graph")
    fig = px.bar(df_risk, x="Zone", y="Probability", color="Risk Level",
                 color_discrete_map={"Low":"green", "Medium":"orange", "High":"red"},
                 text="Probability", range_y=[0,100])
    st.plotly_chart(fig, use_container_width=True)
