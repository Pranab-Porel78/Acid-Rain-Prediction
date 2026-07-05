from database.influx_client import query_api
from config import Config


# ==========================================
# Get Latest Pollution Data
# ==========================================

def get_latest_pollution_data():

    query = f'''
    from(bucket: "{Config.INFLUX_BUCKET}")
      |> range(start: -7d)
      |> filter(fn: (r) => r["_measurement"] == "pollution_data")
      |> pivot(
            rowKey:["_time"],
            columnKey:["_field"],
            valueColumn:"_value"
      )
      |> sort(columns: ["_time"], desc: true)
      |> limit(n: 1)
    '''

    try:

        tables = query_api.query(
            query=query,
            org=Config.INFLUX_ORG
        )

        for table in tables:

            for record in table.records:

                return {

                    "city": record.values.get("city", "--"),

                    "latitude": record.values.get("latitude", "--"),

                    "longitude": record.values.get("longitude", "--"),

                    "aqi": record.values.get("aqi", 0),

                    "pressure": record.values.get("pressure", 0),

                    "pm25": record.values.get("pm25", 0),

                    "pm10": record.values.get("pm10", 0),

                    "co": record.values.get("co", 0),

                    "no2": record.values.get("no2", 0),

                    "so2": record.values.get("so2", 0),

                    "o3": record.values.get("o3", 0),

                    "nh3": record.values.get("nh3", 0),

                    "time": record.get_time().isoformat()

                }

    except Exception as e:

        print("Latest Pollution Error :", e)

    return {

        "city": "--",
        "latitude": "--",
        "longitude": "--",
        "aqi": 0,
        "pressure": 0,
        "pm25": 0,
        "pm10": 0,
        "co": 0,
        "no2": 0,
        "so2": 0,
        "o3": 0,
        "nh3": 0,
        "time": "--"

    }


# ==========================================
# Get Pollution History
# ==========================================

def get_pollution_history(limit=20):

    query = f'''
    from(bucket: "{Config.INFLUX_BUCKET}")
      |> range(start: -30d)
      |> filter(fn: (r) => r["_measurement"] == "pollution_data")
      |> pivot(
            rowKey:["_time"],
            columnKey:["_field"],
            valueColumn:"_value"
      )
      |> sort(columns: ["_time"], desc: true)
      |> limit(n: {limit})
    '''

    history = []

    try:

        tables = query_api.query(
            query=query,
            org=Config.INFLUX_ORG
        )

        for table in tables:

            for record in table.records:

                history.append({

                    "city": record.values.get("city", "--"),

                    "aqi": record.values.get("aqi", 0),

                    "pressure": record.values.get("pressure", 0),

                    "pm25": record.values.get("pm25", 0),

                    "pm10": record.values.get("pm10", 0),

                    "co": record.values.get("co", 0),

                    "no2": record.values.get("no2", 0),

                    "so2": record.values.get("so2", 0),

                    "o3": record.values.get("o3", 0),

                    "nh3": record.values.get("nh3", 0),

                    "latitude": record.values.get("latitude", "--"),

                    "longitude": record.values.get("longitude", "--"),

                    "time": record.get_time().isoformat()

                })

    except Exception as e:

        print("Pollution History Error :", e)

    return history