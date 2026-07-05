
from device_config import DEVICE_CONFIG

from database.write_data import write_sensor_data
from database.query_data import (
    get_latest_sensor_data,
    get_sensor_history
)

from services.pollution_service import fetch_and_store_pollution
from services.prediction_service import predict_acid_rain


def save_sensor_data(data):

    # Store sensor data
    write_sensor_data(
        device_id=data["device_id"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        mq7=data["mq7"],
        nh3=data["nh3"],
        co2=data["co2"]
    )

    # Get device location
    device = DEVICE_CONFIG.get(data["device_id"])

    if device is None:
        return {
            "status": "error",
            "message": "Unknown device"
        }

    # Fetch pollution data
    pollution = fetch_and_store_pollution(
        city=device["city"],
        latitude=device["latitude"],
        longitude=device["longitude"]
    )

    print("Pollution fetched")

    # Run prediction
    prediction = predict_acid_rain()

    return {
        "status": "success",
        "sensor": get_latest_sensor_data(),
        "pollution": pollution,
        "prediction": prediction
    }


def latest_sensor_data():
    return get_latest_sensor_data()


def sensor_history(limit):
    return get_sensor_history(limit)