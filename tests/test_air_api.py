from services.air_api import fetch_air_pollution

# Example: Kolkata
data = fetch_air_pollution(
    22.5726,
    88.3639
)

print(data)