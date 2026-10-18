import math

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Coordinates දෙකක් අතර දුර Kilometers වලින් ගණනය කිරීම."""
    R = 6371.0  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def check_teleportation(lat1: float, lon1: float, time1: int,
                        lat2: float, lon2: float, time2: int,
                        max_speed_kmh: float = 180.0):
    """
    Speed එක Threshold (180 km/h) එකට වඩා වැඩි නම් GPS Spoofing / Teleportation ලෙස හඳුනා ගැනීම.
    """
    distance_km = haversine_distance(lat1, lon1, lat2, lon2)
    time_diff_hours = (time2 - time1) / 3600.0

    if time_diff_hours <= 0:
        return True, 9999.0  # Invalid time gap -> Flag as fraud

    speed_kmh = distance_km / time_diff_hours

    if speed_kmh > max_speed_kmh:
        return True, speed_kmh  # Fraud detected
    
    return False, speed_kmh  # Normal behavior