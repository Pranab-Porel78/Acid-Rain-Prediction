import joblib
import numpy as np

model = joblib.load("ml/model.pkl")
scaler = joblib.load("ml/scaler.pkl")
encoder = joblib.load("ml/encoder.pkl")


def predict(sensor, pollution):

    # Sensor values
    temperature = float(sensor.get("temperature", 0))
    humidity = float(sensor.get("humidity", 0))

    # Pollution values
    pressure = float(pollution.get("pressure", 1013.25))
    pm25 = float(pollution.get("pm25", 0))
    pm10 = float(pollution.get("pm10", 0))
    so2 = float(pollution.get("so2", 0))
    no2 = float(pollution.get("no2", 0))
    nh3 = float(pollution.get("nh3", 0))
    co = float(pollution.get("co", 0))
    o3 = float(pollution.get("o3", 0))

    features = np.array([[
        temperature,
        humidity,
        pressure,
        pm25,
        pm10,
        so2,
        no2,
        nh3,
        co,
        o3
    ]])

    features = scaler.transform(features)

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0]

    risk = encoder.inverse_transform([prediction])[0]

    probability = round(float(np.max(probability) * 100), 2)

    return probability, risk