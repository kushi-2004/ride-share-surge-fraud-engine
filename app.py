import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import plotly.express as px
import datetime
import streamlit as st
import pydeck as pdk

st.set_page_config(
    page_title="Ride-Share Surge & Fraud Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 75, 75, 0.4);
        box-shadow: 0 12px 30px rgba(255, 75, 75, 0.15);
    }
    .metric-title {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 1.6rem;
        color: #ffffff;
        font-weight: 700;
    }
    .metric-delta {
        font-size: 0.8rem;
        color: #10b981;
        margin-top: 6px;
        font-weight: 600;
    }

    .main-title {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff8c42 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }

    [data-testid="stSidebar"] {
        background-color: #0b1120;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 75, 75, 0.2);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .sidebar-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 8px;
        margin-bottom: 0px;
    }
    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Ride-Share Surge & Fraud Dashboard", layout="wide")

st.markdown('<h1 class="main-title">Real-Time Ride-Share Engine</h1>', unsafe_allow_html=True)
st.caption("Live Surge Pricing, Fraud Detection & Geospatial Driver Matching Platform")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Active System</div>
            <div class="metric-value">FastAPI + Redis</div>
            <div class="metric-delta">Live & Connected</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Fraud Monitoring</div>
            <div class="metric-value">Active</div>
            <div class="metric-delta">Protection On</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Surge Engine</div>
            <div class="metric-value">ML Dynamic</div>
            <div class="metric-delta">Ready</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Matching Radius</div>
            <div class="metric-value">1 - 50 KM</div>
            <div class="metric-delta">Geospatial</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")


if "driver_pings" not in st.session_state:
    st.session_state.driver_pings = []

if "surge_history" not in st.session_state:
    
    st.session_state.surge_history = [
        {"time": "08:00", "h3_cell": "888eca3727a6d4", "demand": 12, "supply": 8, "surge_multiplier": 1.1},
        {"time": "09:00", "h3_cell": "888eca3727a6d4", "demand": 25, "supply": 5, "surge_multiplier": 2.2},
        {"time": "10:00", "h3_cell": "888eca3727a6d4", "demand": 30, "supply": 6, "surge_multiplier": 2.5},
        {"time": "11:00", "h3_cell": "888eca3727a6d4", "demand": 15, "supply": 10, "surge_multiplier": 1.2},
    ]


with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <span style="font-size: 2.2rem;">🚗</span>
            <div class="sidebar-title">Ride-Share Engine</div>
            <div class="sidebar-subtitle">Surge & Fraud Control Hub</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### System Configuration")
   
    api_url = st.text_input("FastAPI Base URL", value="http://127.0.0.1:8000")
    
    st.markdown("---")
    st.markdown("### Navigation Info")
    st.info("Select tabs on the main screen to explore live maps, surge calculation, and fraud detection.")
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>SLTC Cloud Computing Project</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Driver Ping & Map", 
    "Surge Calculator", 
    "Historical Analytics", 
    "ML Predictive Surge", 
    "Nearby Driver Matching"
])

with tab1:
    st.markdown("### Driver GPS Location & Teleportation Fraud Detection")
    
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        driver_id = st.text_input("Driver ID", value="DRV_1001", key="tab1_driver_id")
        lat = st.number_input("Latitude", value=6.9271, format="%.4f", key="tab1_lat")
    with col1_2:
        lon = st.number_input("Longitude", value=79.8612, format="%.4f", key="tab1_lon")
        timestamp = st.number_input("Timestamp (Epoch)", value=1729080000, step=1, key="tab1_time")
        
    if st.button("Send Driver Ping", key="tab1_ping_btn"):
        try:
            payload = {
                "driver_id": driver_id,
                "latitude": lat,
                "longitude": lon,
                "timestamp": int(timestamp)
            }
            response = requests.post(f"{api_url}/driver/ping", json=payload)
            if response.status_code == 200:
                st.success("Driver ping sent successfully to FastAPI backend!")
                res_data = response.json()
                import pandas as pd
                df_response = pd.DataFrame([res_data])
                st.markdown("#### Response Details")
                st.dataframe(df_response, use_container_width=True)
            else:
                st.error(f"Error from server: {response.text}")
        except Exception as e:
            st.warning(f"Could not connect to FastAPI server: {e}")

    st.markdown("---")
    st.markdown("#### Live Driver Map View")
    
    import pydeck as pdk
    import pandas as pd
    chart_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=chart_data,
        get_position=['lon', 'lat'],
        get_color='[255, 75, 75, 200]',
        get_radius=500,
        pickable=True
    )
    
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=11,
        pitch=0
    )
    
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=None
    )
    st.pydeck_chart(r)
with tab2:
    st.subheader("Surge Pricing Multiplier Calculator")
    
    h3_cell_input = st.text_input("H3 Cell ID", "888eca3727a6d4")
    
    col1, col2 = st.columns(2)
    with col1:
        demand = st.slider("Demand (Ride Requests)", min_value=1, max_value=100, value=15)
    with col2:
        supply = st.slider("Supply (Active Drivers)", min_value=1, max_value=100, value=5)

    if st.button("Calculate Surge Multiplier", type="primary"):
        try:
            url = f"{api_url}/surge/calculate/{h3_cell_input}?demand={demand}&supply={supply}"
            response = requests.post(url)
            res_data = response.json()
            
            surge_val = res_data.get('surge_multiplier')
            st.metric(label="Calculated Surge Multiplier", value=f"{surge_val}x")
           
            current_time = datetime.datetime.now().strftime("%H:%M")
            st.session_state.surge_history.append({
                "time": current_time,
                "h3_cell": h3_cell_input,
                "demand": demand,
                "supply": supply,
                "surge_multiplier": surge_val
            })
            
            st.json(res_data)
        except Exception as e:
            st.error(f"Connection Error: {e}")

with tab3:
    st.subheader("Historical Analytics & Peak Hours Trends")
    
    if st.session_state.surge_history:
        hist_df = pd.DataFrame(st.session_state.surge_history)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Surge Multiplier Trend Over Time")
            fig_surge = px.line(hist_df, x="time", y="surge_multiplier", markers=True, 
                                title="Surge Multiplier Variations",
                                labels={"time": "Time", "surge_multiplier": "Surge Multiplier (x)"})
            st.plotly_chart(fig_surge, use_container_width=True)
            
        with col2:
            st.markdown("##### Demand vs Supply Trend")
            fig_ds = px.bar(hist_df, x="time", y=["demand", "supply"], barmode="group",
                            title="Demand & Supply Levels by Time",
                            labels={"time": "Time", "value": "Count", "variable": "Metric"})
            st.plotly_chart(fig_ds, use_container_width=True)
            
        st.markdown("##### Complete Surge Calculation Logs")
        st.dataframe(hist_df, use_container_width=True)
    else:
        st.info("Previous data is not yet available..")

with tab4:
    st.subheader("Machine Learning Predictive Surge Pricing")
    st.markdown("Predicting future demand and calculating 'surge' using an ML model, based on the time, day of the week, and weather..")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        ml_hour = st.slider("Hour of Day (0 - 23)", 0, 23, 18)
    with col2:
        ml_weekend = st.selectbox("Day Type", [0, 1], format_func=lambda x: "Weekday" if x==0 else "Weekend")
    with col3:
        ml_weather = st.selectbox("Weather Condition", [0, 1, 2], format_func=lambda x: ["Clear", "Rain", "Heavy Rain"][x])
        
    ml_supply = st.slider("Active Drivers (Supply)", 1, 50, 10)

    if st.button("Predict Demand & Calculate Surge", type="primary"):
        try:
            url = f"{api_url}/surge/predict-ml?hour={ml_hour}&is_weekend={ml_weekend}&weather={ml_weather}&supply={ml_supply}"
            response = requests.get(url)
            res_data = response.json()
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric(label="Predicted Demand (Requests)", value=res_data.get('predicted_demand'))
            with col_m2:
                st.metric(label="ML-Driven Surge Multiplier", value=f"{res_data.get('surge_multiplier')}x")
                
            st.json(res_data)
        except Exception as e:
            st.error(f"Connection Error: {e}")

with tab5:
    st.subheader("Passenger & Nearby Driver Matching (Redis Geospatial)")
    st.markdown("Finding active drivers located near the passenger's current position (within a certain radius).")

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        p_lat = st.number_input("Passenger Latitude", value=6.9271, format="%.4f", key="p_lat")
    with col_p2:
        p_lon = st.number_input("Passenger Longitude", value=79.8612, format="%.4f", key="p_lon")
    with col_p3:
        p_radius = st.slider("Search Radius (KM)", min_value=1, max_value=50, value=10)

    if st.button("Find Nearby Drivers", type="primary"):
        try:
            url = f"{api_url}/drivers/nearby?lat={p_lat}&lon={p_lon}&radius_km={p_radius}"
            response = requests.get(url)
            res_data = response.json()

            drivers_list = res_data.get("nearby_drivers", [])
            st.success(f"Search successful! Number of drivers found: **{len(drivers_list)}**")

            if drivers_list:
                df_nearby = pd.DataFrame(drivers_list)

                col_table, col_map = st.columns([1, 1])

                with col_table:
                    st.subheader("Matched Drivers")
                    st.dataframe(
                        df_nearby[['driver_id', 'distance_km', 'latitude', 'longitude']],
                        use_container_width=True
                    )

                with col_map:
                    st.subheader("Live Map View")

                    layer = pdk.Layer(
                        "ScatterplotLayer",
                        data=df_nearby,
                        get_position='[longitude, latitude]',
                        get_color='[255, 75, 75, 220]',
                        get_radius=250,
                        pickable=True,
                        auto_highlight=True,
                    )

                    view_state = pdk.ViewState(
                        latitude=p_lat,
                        longitude=p_lon,
                        zoom=12,
                        pitch=0
                    )

                    r = pdk.Deck(
                        layers=[layer],
                        initial_view_state=view_state,
                        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
                    )
                    st.pydeck_chart(r)
            else:
                st.warning("No drivers were found in this area. Please first register some drivers using 'Driver Ping'..")

        except Exception as e:
            st.error(f"Connection Error: {e}")