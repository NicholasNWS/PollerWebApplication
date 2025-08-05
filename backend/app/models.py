from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class PLC(Base):
    __tablename__ = "plcs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    ip_address = Column(String, nullable=False)
    port = Column(Integer, nullable=False)

    tags = relationship("Tag", back_populates="plc", cascade="all, delete-orphan")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(Integer, nullable=False)
    function_code = Column(Integer, nullable=False)
    unit_id = Column(Integer, nullable=False)
    plc_id = Column(Integer, ForeignKey("plcs.id"), nullable=False)

    plc = relationship("PLC", back_populates="tags")
