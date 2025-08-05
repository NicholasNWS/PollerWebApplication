import time
import logging
from pycomm3 import LogixDriver
from influxdb_client import Point
from ..influx import InfluxClient

logger = logging.getLogger(__name__)

class CipPoller:
    """
    Poller for EtherNet/IP PLCs via pycomm3. Reads tag list and writes to InfluxDB.
    """
    def __init__(self, host: str, protocol: str, poll_interval: float = 5.0):
        self.host = host
        self.protocol = protocol
        self.poll_interval = poll_interval
        self.driver = LogixDriver(self.host)

    def connect(self) -> None:
        try:
            self.driver.open()
            logger.info("Connected to CIP PLC: %s", self.host)
        except Exception:
            logger.exception("Failed to connect to CIP PLC: %s", self.host)
            raise

    def poll_once(self, tags: list[str], influx_bucket: str) -> None:
        results = self.driver.read(*tags)
        for r in results:
            if r.value is None:
                logger.warning("None value for %s", r.tag)
                continue
            try:
                InfluxClient.write_point(
                    bucket=influx_bucket,
                    measurement="cip_data",
                    field=r.tag,
                    value=float(r.value),
                    timestamp_ns=time.time_ns(),
                    tags={"plc": self.host, "protocol": self.protocol},
                )
                logger.info("Wrote %s=%s", r.tag, r.value)
            except Exception:
                logger.exception("Failed to write point for %s", r.tag)

    def close(self) -> None:
        try:
            self.driver.close()
        except Exception:
            logger.warning("Error closing CIP driver for %s", self.host)

    def run(self, tags: list[str], influx_bucket: str) -> None:
        try:
            self.connect()
            while True:
                self.poll_once(tags, influx_bucket)
                time.sleep(self.poll_interval)
        except Exception:
            logger.exception("Unrecoverable polling error for %s", self.host)
        finally:
            self.close()