from database.query_data import get_latest_sensor_data
from database.query_pollution import get_latest_pollution_data
from database.query_prediction import (
    get_latest_prediction,
    get_prediction_history
)

from database.write_prediction import write_prediction

from services.predictor import predict


# ==========================================
# Run Prediction
# ==========================================

def predict_acid_rain():

    sensor = get_latest_sensor_data()

    pollution = get_latest_pollution_data()

    probability, risk = predict(

        sensor,
        pollution

    )

    write_prediction(

        probability,
        risk

    )

    return {

        "sensor": sensor,

        "pollution": pollution,

        "probability": probability,

        "risk": risk

    }


# ==========================================
# Latest Prediction
# ==========================================

def latest_prediction():

    return get_latest_prediction()


# ==========================================
# Prediction History
# ==========================================

def prediction_history(limit=20):

    return get_prediction_history(limit)