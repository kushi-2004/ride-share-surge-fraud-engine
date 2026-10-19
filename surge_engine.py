import math

def get_h3_index(lat: float, lng: float, resolution: int = 8) -> str:
    lat_grid = int((lat + 90) * 10000)
    lng_grid = int((lng + 180) * 10000)
    return f"88{resolution:x}{lat_grid:05x}{lng_grid:05x}"

def calculate_surge_multiplier(demand: int, supply: int, alpha: float = 0.5, 
                               base_ratio: float = 1.2, max_surge: float = 3.5) -> float:
    ratio = (demand + 1e-5) / (supply + 1e-5)
    if ratio <= base_ratio:
        return 1.0
    
    surge = 1.0 + alpha * (ratio - base_ratio)
    return round(min(max_surge, surge), 2)