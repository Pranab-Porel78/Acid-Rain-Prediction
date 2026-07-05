from services.air_api import fetch_air_pollution
from database.write_pollution import write_pollution_data

# Kolkata Coordinates
LAT = 22.5726
LON = 88.3639

pollution = fetch_air_pollution(LAT, LON)

write_pollution_data(
    city="Kolkata",
    latitude=LAT,
    longitude=LON,
    pollution=pollution
)

print("Pollution data stored successfully.")