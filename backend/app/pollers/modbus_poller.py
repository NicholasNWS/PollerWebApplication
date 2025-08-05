import time
import logging
from pymodbus.client import ModbusTcpClient
from influxdb_client import Point
from ..influx import InfluxClient

logger = logging.getLogger(__name__)

class ModbusPoller:
    """
    Poller for Modbus TCP PLCs. Reads registers using per-PLC settings and writes to InfluxDB.
    """
    def __init__(self, host: str, unit: int = 1, poll_interval: float = 5.0):
        self.host = host
        self.unit = unit
        self.poll_interval = poll_interval
        self.client = ModbusTcpClient(self.host)

    def connect(self):
        if not self.client.connect():
            logger.error("Failed to connect to Modbus at %s", self.host)
            raise ConnectionError
        logger.info("Connected to Modbus PLC: %s", self.host)

    def poll_once(self, tags: list[dict], influx_bucket: str):
        for tag in tags:
            rr = self.client.read_holding_registers(tag['addr'], count=1, unit=self.unit)
            if rr.isError():
                logger.error("Error reading %s", tag)
                continue
            raw = rr.registers[0]
            value = raw * tag.get('mult',1) / (10 ** tag.get('dec',0))
            point = Point(tag['field']).field(tag['field'], float(value)).time(time.time_ns())
            InfluxClient._client.write_api().write(bucket=influx_bucket, record=point)
            logger.info("Wrote %s=%s", tag['field'], value)

    def run(self, tags: list[dict], influx_bucket: str):
        self.connect()
        while True:
            self.poll_once(tags, influx_bucket)
            time.sleep(self.poll_interval)