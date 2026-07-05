from database.influx_client import client

health = client.health()

print("Status:", health.status)
print("Message:", health.message)