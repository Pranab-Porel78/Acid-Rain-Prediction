from influxdb_client import Point

from database.influx_client import write_api
from config import Config


def write_pollution_data(city, latitude, longitude, pollution):

    point = (
        Point("pollution_data")
        .tag("city", city)
        .tag("latitude", str(latitude))
        .tag("longitude", str(longitude))

        .field("aqi", int(pollution["aqi"]))

        .field("co", float(pollution["co"]))
        .field("no2", float(pollution["no2"]))
        .field("so2", float(pollution["so2"]))
        .field("o3", float(pollution["o3"]))
        .field("nh3", float(pollution["nh3"]))

        .field("pm25", float(pollution["pm25"]))
        .field("pm10", float(pollution["pm10"]))

        # New field required by your ML model
        .field("pressure", float(pollution["pressure"]))
    )

    write_api.write(
        bucket=Config.INFLUX_BUCKET,
        org=Config.INFLUX_ORG,
        record=point
    )

    return True