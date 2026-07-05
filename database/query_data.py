
from database.influx_client import query_api
from config import Config


def get_latest_sensor_data():

    query = f'''
    from(bucket: "{Config.INFLUX_BUCKET}")
      |> range(start: -1d)
      |> filter(fn: (r) => r["_measurement"] == "sensor_data")
      |> last()
    '''

    tables = query_api.query(
        query=query,
        org=Config.INFLUX_ORG
    )

    data = {}

    for table in tables:
        for record in table.records:
            data[record.get_field()] = record.get_value()
            data["time"] = record.get_time()

    return data


def get_sensor_history(limit=50):

    query = f'''
    from(bucket: "{Config.INFLUX_BUCKET}")
      |> range(start: -30d)
      |> filter(fn: (r) => r["_measurement"] == "sensor_data")
      |> pivot(
            rowKey: ["_time"],
            columnKey: ["_field"],
            valueColumn: "_value"
        )
      |> sort(columns: ["_time"], desc: true)
      |> limit(n: {limit})
    '''

    tables = query_api.query(
        query=query,
        org=Config.INFLUX_ORG
    )

    history = []

    for table in tables:
        for record in table.records:

            history.append({

                "device_id": record.values.get("device_id"),

                "temperature": record.values.get("temperature"),
                "humidity": record.values.get("humidity"),

                "mq7": record.values.get("mq7"),
                "nh3": record.values.get("nh3"),
                "co2": record.values.get("co2"),

                "time": record.get_time().isoformat()

            })

    return history

