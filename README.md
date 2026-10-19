# 🚀 Real-Time Ride-Share Surge & Fraud Engine

A comprehensive real-time microservices-inspired analytical platform built with **FastAPI**, **Streamlit**, **Redis**, and **Machine Learning** for dynamic surge pricing, geospatial driver matching, and GPS spoofing (teleportation) fraud detection.

---

## ✨ Key Features

1. **🚨 GPS Spoofing & Teleportation Fraud Detection (`/driver/ping`)**
   - Real-time monitoring of driver coordinates and timestamps.
   - Calculates movement velocity and flags impossible travel speeds (teleportation) instantly[cite: 11].
2. **📈 Dynamic ML Surge Pricing Calculator (`/surge/calculate/{h3_cell}`)**
   - Integrates Uber's H3 geospatial indexing to calculate demand-supply ratios dynamically.
   - Automatically computes price multipliers based on real-time traffic and request volume.
3. **🗺️ Live Driver Mapping & Geospatial Matching**
   - Interactive Pydeck map visualization supporting dark mode UI.
   - Geospatial proximity calculations to match riders with nearby available drivers.
4. **📊 Analytical Streamlit Dashboard**
   - Modern deep slate UI theme featuring dynamic KPI metrics, input controls, and organized tabular data representations (`st.dataframe`).

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python, Uvicorn, Redis (In-Memory Database)
- **Frontend & UI:** Streamlit, Pydeck, Pandas, Requests
- **Machine Learning & Spatial Indexing:** Uber H3, Custom Surge & Anomaly Detection Algorithms
- **Version Control:** Git & GitHub
