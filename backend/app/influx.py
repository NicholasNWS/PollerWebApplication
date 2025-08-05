from influxdb_client import InfluxDBClient
import os

# Singleton Influx client, configured from DB values
class InfluxClient:
    _client = None

    @classmethod
    def init(cls, url, token, org):
        cls._client = InfluxDBClient(url=url, token=token, org=org)

    @classmethod
    def write_point(cls, bucket, measurement, field, value, timestamp_ns):
        write_api = cls._client.write_api()
        point = {
            "measurement": measurement,
            "fields": {field: float(value)},
            "time": timestamp_ns
        }
        write_api.write(bucket=bucket, record=point)