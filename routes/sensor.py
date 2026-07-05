
from flask import Blueprint, request, jsonify

from services.sensor_service import (
    save_sensor_data,
    latest_sensor_data,
    sensor_history
)

sensor_bp = Blueprint("sensor", __name__)


@sensor_bp.route("/sensor", methods=["POST"])
def receive_sensor_data():

    print("=" * 60)
    print("ESP32 Request Received")

    data = request.get_json()

    print("Incoming JSON:")
    print(data)

    result = save_sensor_data(data)

    print("Sensor Data Saved Successfully")
    print("=" * 60)

    return jsonify(result)


@sensor_bp.route("/sensor/latest", methods=["GET"])
def get_latest():

    return jsonify(latest_sensor_data())


@sensor_bp.route("/sensor/history", methods=["GET"])
def history():

    limit = request.args.get("limit", default=50, type=int)

    return jsonify(sensor_history(limit))
