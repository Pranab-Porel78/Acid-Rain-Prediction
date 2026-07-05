from influxdb_client import Point

from database.influx_client import write_api
from config import Config


def write_prediction(probability, risk_level):

    point = (
        Point("prediction_data")
        .field("probability", float(probability))
        .field("risk_level", risk_level)
    )

    write_api.write(
        bucket=Config.INFLUX_BUCKET,
        org=Config.INFLUX_ORG,
        record=point
    )

    return True