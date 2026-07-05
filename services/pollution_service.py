from services.air_api import fetch_air_pollution
from database.write_pollution import write_pollution_data
from database.query_pollution import (
    get_latest_pollution_data,
    get_pollution_history
)


def fetch_and_store_pollution(city, latitude, longitude):

    pollution = fetch_air_pollution(latitude, longitude)

    write_pollution_data(
        city,
        latitude,
        longitude,
        pollution
    )

    return {
        "status": "success",
        "message": "Pollution data stored successfully."
    }


def latest_pollution():
    return get_latest_pollution_data()


def pollution_history(limit):
    return get_pollution_history(limit)