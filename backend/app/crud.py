from sqlalchemy.orm import Session
from . import models, schemas

def get_plc(db: Session, plc_id: int):
    return db.query(models.PLC).filter(models.PLC.id == plc_id).first()

def get_plc_by_name(db: Session, name: str):
    return db.query(models.PLC).filter(models.PLC.name == name).first()

def get_plcs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PLC).offset(skip).limit(limit).all()

def create_plc(db: Session, plc: schemas.PLCCreate):
    db_plc = models.PLC(
        name=plc.name,
        ip_address=plc.ip_address,
        protocol=plc.protocol,
        tags=plc.tags,
        active=plc.active
    )
    db.add(db_plc)
    db.commit()
    db.refresh(db_plc)
    return db_plc

def update_plc(db: Session, db_plc: models.PLC, updates: schemas.PLCUpdate):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_plc, field, value)
    db.commit()
    db.refresh(db_plc)
    return db_plc

def delete_plc(db: Session, db_plc: models.PLC):
    db.delete(db_plc)
    db.commit()
    return None

# InfluxConfig CRUD

def get_influx_config(db: Session):
    return db.query(models.InfluxConfig).first()

def create_influx_config(db: Session, cfg: schemas.InfluxConfigBase):
    db_cfg = models.InfluxConfig(**cfg.dict())
    db.add(db_cfg)
    db.commit()
    db.refresh(db_cfg)
    return db_cfg

def update_influx_config(db: Session, db_cfg: models.InfluxConfig, updates: schemas.InfluxConfigBase):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_cfg, field, value)
    db.commit()
    db.refresh(db_cfg)
    return db_cfg