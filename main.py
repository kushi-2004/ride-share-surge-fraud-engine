from fastapi import FastAPI
from pydantic import BaseModel
import redis
from surge_engine import get_h3_index, calculate_surge_multiplier
from fraud_engine import check_teleportation
from ml_model import predict_demand
import math

app = FastAPI(title="Ride-Share Surge & Fraud Engine")

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class DriverPing(BaseModel):
    driver_id: str
    latitude: float
    longitude: float
    timestamp: int

@app.post("/driver/ping")
def receive_driver_ping(ping: DriverPing):
    try:
        h3_cell = get_h3_index(ping.latitude, ping.longitude)

        redis_key = f"driver:{ping.driver_id}:location"
        prev_data = r.hgetall(redis_key)
    
        r.sadd("all_drivers", ping.driver_id)

        if prev_data:
            prev_lat = float(prev_data["lat"])
            prev_lng = float(prev_data["lng"])
            prev_time = int(prev_data["time"])

            is_fraud, speed = check_teleportation(
                prev_lat, prev_lng, prev_time,
                ping.latitude, ping.longitude, ping.timestamp
            )
            
            if is_fraud:
                r.hset(redis_key, mapping={
                    "lat": ping.latitude,
                    "lng": ping.longitude,
                    "time": ping.timestamp,
                    "status": "FRAUD"
                })
                return {"status": "FLAGGED", "reason": "GPS Spoofing / Teleportation Detected", "calculated_speed_kmh": speed}

        r.hset(redis_key, mapping={
            "lat": ping.latitude,
            "lng": ping.longitude,
            "time": ping.timestamp,
            "status": "VALID"
        })
        
        return {"status": "OK", "h3_cell": h3_cell}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.post("/surge/calculate/{h3_cell}")
def get_surge(h3_cell: str, demand: int = 10, supply: int = 5):
    surge = calculate_surge_multiplier(demand, supply)
    return {
        "h3_cell": h3_cell,
        "demand": demand,
        "supply": supply,
        "surge_multiplier": surge
    }

@app.get("/surge/predict-ml")
def get_ml_predicted_surge(hour: int, is_weekend: int, weather: int, supply: int = 5):
    predicted_demand = predict_demand(hour, is_weekend, weather)
    
    surge = calculate_surge_multiplier(demand=int(predicted_demand), supply=supply)
    
    return {
        "predicted_demand": predicted_demand,
        "supply": supply,
        "hour": hour,
        "is_weekend": bool(is_weekend),
        "weather_code": weather,
        "surge_multiplier": surge
    }

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

@app.get("/drivers/nearby")
def get_nearby_drivers(lat: float, lon: float, radius_km: float = 10.0):
    try:
        driver_ids = r.smembers("all_drivers")
        drivers = []
        
        for d_id in driver_ids:
            driver_id = d_id.decode('utf-8') if isinstance(d_id, bytes) else d_id
            redis_key = f"driver:{driver_id}:location"
            d_data = r.hgetall(redis_key)
            
            if d_data:
                d_lat = float(d_data.get(b"lat", d_data.get("lat", 0)))
                d_lon = float(d_data.get(b"lng", d_data.get("lng", 0)))
                status = d_data.get(b"status", d_data.get("status", b"VALID"))
                if isinstance(status, bytes):
                    status = status.decode('utf-8')
               
                if status == "VALID":
                    dist = calculate_distance(lat, lon, d_lat, d_lon)
                    if dist <= radius_km:
                        drivers.append({
                            "driver_id": driver_id,
                            "distance_km": round(dist, 2),
                            "longitude": d_lon,
                            "latitude": d_lat
                        })
                        
        return {"status": "OK", "count": len(drivers), "nearby_drivers": drivers}
    except Exception as e:
        return {"status": "ERROR", "message": str(e), "nearby_drivers": []}