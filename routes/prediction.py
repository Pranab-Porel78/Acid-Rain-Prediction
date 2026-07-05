from flask import Blueprint, jsonify, request

from services.prediction_service import (
    predict_acid_rain,
    latest_prediction,
    prediction_history
)

prediction_bp = Blueprint(
    "prediction",
    __name__
)


# ==========================================
# Run Prediction
# ==========================================

@prediction_bp.route("/predict", methods=["GET", "POST"])
def predict():

    return jsonify(
        predict_acid_rain()
    )


# ==========================================
# Latest Prediction
# ==========================================

@prediction_bp.route("/prediction/latest", methods=["GET"])
def latest():

    return jsonify(
        latest_prediction()
    )


# ==========================================
# Prediction History
# ==========================================

@prediction_bp.route("/prediction/history", methods=["GET"])
def history():

    limit = request.args.get(
        "limit",
        default=20,
        type=int
    )

    return jsonify(
        prediction_history(limit)
    )