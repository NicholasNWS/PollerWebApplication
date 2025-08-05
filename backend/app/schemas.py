from pydantic import BaseModel, Field, constr
from typing import List, Optional

# Tag schemas
tag_name_t = constr(min_length=1)

class TagBase(BaseModel):
    name: tag_name_t
    address: int
    function_code: int
    unit_id: int

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    plc_id: int
    class Config:
        orm_mode = True

# PLC schemas
class PLCBase(BaseModel):
    name: str = Field(..., description="The unique name of the PLC")
    ip_address: str = Field(..., description="IP address of the PLC")
    port: int = Field(..., description="TCP port of the PLC")
    protocol: constr(regex="^(modbus|cip)$") = Field(..., description="Communication protocol: 'modbus' or 'cip'")
    active: bool = Field(True, description="Whether the PLC is active")

class PLCCreate(PLCBase):
    tags: List[TagCreate] = []

class PLCUpdate(BaseModel):
    name: Optional[str]
    ip_address: Optional[str]
    port: Optional[int]
    protocol: Optional[constr(regex="^(modbus|cip)$")]
    tags: Optional[List[TagCreate]]
    active: Optional[bool]

class PLC(PLCBase):
    id: int
    tags: List[Tag] = []
    class Config:
        orm_mode = True

# Influx config schemas
class InfluxConfigBase(BaseModel):
    url: str
    token: str
    org: str
    bucket: str

class InfluxConfig(InfluxConfigBase):
    id: int
    class Config:
        orm_mode = True