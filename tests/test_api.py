import requests

url = "http://127.0.0.1:5000/api/sensor"

data = {
    "device_id": "ESP32_001",
    "temperature": 31.5,
    "humidity": 80,
    "mq7": 170,
    "mq135": 320
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())