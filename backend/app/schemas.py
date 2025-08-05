from pydantic import BaseModel, Field
from typing import List, Optional

class PLCBase(BaseModel):
    name: str
    ip_address: str
    protocol: str = Field(..., pattern="^(modbus|cip)$")
    active: bool = True

class PLCCreate(PLCBase):
    pass

class PLCUpdate(BaseModel):
    name: Optional[str]
    ip_address: Optional[str]
    protocol: Optional[str]
    tags: Optional[List[str]]
    active: Optional[bool]

class PLC(PLCBase):
    id: int
    class Config:
        orm_mode = True

class InfluxConfigBase(BaseModel):
    url: str
    token: str
    org: str
    bucket: str

class InfluxConfig(InfluxConfigBase):
    id: int
    class Config:
        orm_mode = True