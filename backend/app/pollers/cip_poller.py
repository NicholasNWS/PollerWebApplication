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
    def __init__(self, host: str, poll_interval: float = 5.0):
        self.host = host
        self.poll_interval = poll_interval
        self.driver = LogixDriver(self.host)

    def connect(self):
        self.driver.open()
        logger.info("Connected to CIP PLC: %s", self.host)

    def poll_once(self, tags: list[str], influx_bucket: str):
        results = self.driver.read(*tags)
        for r in results:
            if r.value is None:
                logger.warning("None value for %s", r.tag)
                continue
            point = Point(r.tag).field(r.tag, float(r.value)).time(time.time_ns())
            InfluxClient._client.write_api().write(bucket=influx_bucket, record=point)
            logger.info("Wrote %s=%s", r.tag, r.value)

    def run(self, tags: list[str], influx_bucket: str):
        self.connect()
        while True:
            self.poll_once(tags, influx_bucket)
            time.sleep(self.poll_interval)