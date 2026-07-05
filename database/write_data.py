
from influxdb_client import Point

from database.influx_client import write_api
from config import Config


def write_sensor_data(
    device_id,
    temperature,
    humidity,
    mq7,
    nh3,
    co2
):

    point = (
        Point("sensor_data")
        .tag("device_id", device_id)

        .field("temperature", float(temperature))
        .field("humidity", float(humidity))

        .field("mq7", float(mq7))
        .field("nh3", float(nh3))
        .field("co2", float(co2))
    )

    write_api.write(
        bucket=Config.INFLUX_BUCKET,
        org=Config.INFLUX_ORG,
        record=point
    )

    return True
