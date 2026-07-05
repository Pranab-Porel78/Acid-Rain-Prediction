import requests
from config import Config

# OpenWeather API URLs
AIR_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_air_pollution(lat, lon):

    # Air Pollution API
    air_response = requests.get(
        AIR_URL,
        params={
            "lat": lat,
            "lon": lon,
            "appid": Config.OPENWEATHER_API_KEY
        }
    )

    air_response.raise_for_status()

    air_data = air_response.json()

    # Current Weather API
    weather_response = requests.get(
        WEATHER_URL,
        params={
            "lat": lat,
            "lon": lon,
            "appid": Config.OPENWEATHER_API_KEY,
            "units": "metric"
        }
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    pollution = air_data["list"][0]

    return {

        "aqi": pollution["main"]["aqi"],

        "co": pollution["components"]["co"],
        "no2": pollution["components"]["no2"],
        "so2": pollution["components"]["so2"],
        "o3": pollution["components"]["o3"],
        "nh3": pollution["components"]["nh3"],
        "pm25": pollution["components"]["pm2_5"],
        "pm10": pollution["components"]["pm10"],

        # New field
        "pressure": weather_data["main"]["pressure"]
    }