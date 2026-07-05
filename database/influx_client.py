from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from config import Config

# Create InfluxDB Client
client = InfluxDBClient(
    url=Config.INFLUX_URL,
    token=Config.INFLUX_TOKEN,
    org=Config.INFLUX_ORG
)

# APIs
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
delete_api = client.delete_api()