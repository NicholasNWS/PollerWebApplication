from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class PLC(Base):
    __tablename__ = "plcs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    ip_address = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    protocol = Column(String, nullable=False)
    active = Column(Boolean, default=True)

    tags = relationship("Tag", back_populates="plc", cascade="all, delete-orphan")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(Integer, nullable=False)
    function_code = Column(Integer, nullable=False)
    unit_id = Column(Integer, nullable=False)
    plc_id = Column(Integer, ForeignKey("plcs.id", ondelete="CASCADE"), index=True, nullable=False)

    plc = relationship("PLC", back_populates="tags")

class InfluxConfig(Base):
    __tablename__ = "influx_config"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    token = Column(String, nullable=False)
    org = Column(String, nullable=False)
    bucket = Column(String, nullable=False)