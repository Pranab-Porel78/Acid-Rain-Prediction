from database.write_data import write_sensor_data

write_sensor_data(
    device_id="ESP32_001",
    temperature=30.2,
    humidity=76,
    mq7=150,
    mq135=280
)

print("Data inserted successfully.")