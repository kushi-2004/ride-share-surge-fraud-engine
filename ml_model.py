import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

MODEL_PATH = "demand_model.pkl"

def train_and_save_model():
    X_train = np.array([
        [8, 0, 0], [8, 0, 1], [9, 0, 0], [12, 0, 0], 
        [17, 0, 1], [18, 0, 2], [19, 0, 0], [22, 0, 0],
        [8, 1, 0], [13, 1, 0], [18, 1, 1], [20, 1, 2]
    ])
    y_train = np.array([20, 35, 25, 15, 45, 60, 40, 18, 10, 22, 30, 38])
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, MODEL_PATH)
    return model

def predict_demand(hour: int, is_weekend: int, weather: int) -> float:
   
    if not os.path.exists(MODEL_PATH):
        model = train_and_save_model()
    else:
        model = joblib.load(MODEL_PATH)
        
    features = np.array([[hour, is_weekend, weather]])
    predicted = model.predict(features)
    return float(round(predicted[0], 2))