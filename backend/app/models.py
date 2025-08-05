from sqlalchemy import Column, Integer, String, JSON, Boolean
from .db import Base

class PLC(Base):
    __tablename__ = 'plcs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String, nullable=False)
    protocol = Column(String, nullable=False)  # 'modbus' or 'cip'
    tags = Column(JSON, default=[])
    active = Column(Boolean, default=True)

class InfluxConfig(Base):
    __tablename__ = 'influx_config'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    token = Column(String, nullable=False)
    org = Column(String, nullable=False)
    bucket = Column(String, nullable=False)