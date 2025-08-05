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
    def __init__(self, host: str, protocol: str, unit: int = 1, poll_interval: float = 5.0):
        self.host = host
        self.protocol = protocol
        self.unit = unit
        self.poll_interval = poll_interval
        self.client = ModbusTcpClient(self.host)

    def connect(self) -> None:
        if not self.client.connect():
            logger.error("Failed to connect to Modbus at %s", self.host)
            raise ConnectionError(f"Cannot connect to Modbus PLC at {self.host}")
        logger.info("Connected to Modbus PLC: %s", self.host)

    def poll_once(self, tags: list[dict], influx_bucket: str) -> None:
        for tag in tags:
            try:
                rr = self.client.read_holding_registers(tag['address'], count=1, unit=self.unit)
                if rr.isError():
                    logger.error("Error reading tag %s: %s", tag['name'], rr)
                    continue
                raw = rr.registers[0]
                value = raw * tag.get('mult', 1) / (10 ** tag.get('dec', 0))
                InfluxClient.write_point(
                    bucket=influx_bucket,
                    measurement="modbus_data",
                    field=tag['name'],
                    value=float(value),
                    timestamp_ns=time.time_ns(),
                    tags={"plc": self.host, "protocol": self.protocol},
                )
                logger.info("Wrote %s=%s", tag['name'], value)
            except Exception:
                logger.exception("Failed to poll or write tag %s", tag['name'])

    def close(self) -> None:
        try:
            self.client.close()
        except Exception:
            logger.warning("Error closing Modbus client for %s", self.host)

    def run(self, tags: list[dict], influx_bucket: str) -> None:
        try:
            self.connect()
            while True:
                self.poll_once(tags, influx_bucket)
                time.sleep(self.poll_interval)
        except Exception:
            logger.exception("Unrecoverable polling error for %s", self.host)
        finally:
            self.close()