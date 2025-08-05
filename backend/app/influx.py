import os
import logging
from influxdb_client import InfluxDBClient, Point

logger = logging.getLogger(__name__)


class InfluxClient:
    _client: InfluxDBClient | None = None

    @classmethod
    def init(cls, url: str, token: str, org: str) -> None:
        """
        Initialize the singleton InfluxDB client.
        """
        if cls._client is not None:
            logger.warning("InfluxClient already initialized, reinitializing.")
        cls._client = InfluxDBClient(url=url, token=token, org=org)
        logger.info("InfluxClient initialized for org=%s at %s", org, url)

    @classmethod
    def write_point(
        cls,
        bucket: str,
        measurement: str,
        field: str,
        value: float,
        timestamp_ns: int,
        tags: dict[str, str] | None = None,
    ) -> None:
        """
        Write a single point to InfluxDB, with optional tags.
        Raises RuntimeError if client is not initialized.
        """
        if cls._client is None:
            raise RuntimeError("InfluxClient is not initialized. Call init() first.")

        write_api = cls._client.write_api()
        point = Point(measurement).field(field, float(value)).time(timestamp_ns)

        if tags:
            for tag_key, tag_val in tags.items():
                point.tag(tag_key, tag_val)

        logger.debug(
            "Writing to InfluxDB bucket=%s: measurement=%s, field=%s=%s, tags=%s",
            bucket,
            measurement,
            field,
            value,
            tags,
        )
        write_api.write(bucket=bucket, record=point)
        logger.info("InfluxDB write successful: %s.%s", measurement, field)

    @classmethod
    def query(cls, query_str: str) -> list:
        """
        Execute a Flux query against the database.
        Returns the raw query result.
        """
        if cls._client is None:
            raise RuntimeError("InfluxClient is not initialized. Call init() first.")

        query_api = cls._client.query_api()
        result = query_api.query(query_str)
        logger.debug("InfluxDB query executed: %s", query_str)
        return result

    @classmethod
    def close(cls) -> None:
        """
        Close and dispose of the InfluxDB client.
        """
        if cls._client:
            try:
                cls._client.close()
                logger.info("InfluxClient connection closed.")
            except Exception as e:
                logger.warning("Error closing InfluxClient: %s", e)
            finally:
                cls._client = None
