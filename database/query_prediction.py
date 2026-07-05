from database.influx_client import query_api
from config import Config


# ==========================================
# Latest Prediction
# ==========================================

def get_latest_prediction():

    query = f'''
    from(bucket: "{Config.INFLUX_BUCKET}")
      |> range(start: -30d)
      |> filter(fn: (r) => r["_measurement"] == "prediction_data")
      |> pivot(
            rowKey:["_time"],
            columnKey:["_field"],
            valueColumn:"_value"
      )
      |> sort(columns:["_time"], desc:true)
      |> limit(n:1)
    '''

    try:

        tables = query_api.query(
            query=query,
            org=Config.INFLUX_ORG
        )

        for table in tables:

            for record in table.records:

                return {

                    "probability": record.values.get("probability", 0),

                    "risk": record.values.get("risk", record.values.get("risk_level", "Unknown")),

                    "time": record.get_time().isoformat()

                }

    except Exception as e:

        print("Latest Prediction Error :", e)

    return {

        "probability": 0,

        "risk": "Unknown",

        "time": "--"

    }


# ==========================================
# Prediction History
# ==========================================

def get_prediction_history(limit=20):

    query = f'''
    from(bucket: "{Config.INFLUX_BUCKET}")
      |> range(start: -30d)
      |> filter(fn: (r) => r["_measurement"] == "prediction_data")
      |> pivot(
            rowKey:["_time"],
            columnKey:["_field"],
            valueColumn:"_value"
      )
      |> sort(columns:["_time"], desc:true)
      |> limit(n:{limit})
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

                    "probability": record.values.get("probability", 0),

                    "risk": record.values.get(
                        "risk",
                        record.values.get("risk_level", "Unknown")
                    ),

                    "time": record.get_time().isoformat()

                })

    except Exception as e:

        print("Prediction History Error :", e)

    return history