from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas

# PLC operations
def get_plc(db: Session, plc_id: int):
    return db.query(models.PLC).filter(models.PLC.id == plc_id).first()

def get_plc_by_name(db: Session, name: str):
    return db.query(models.PLC).filter(models.PLC.name == name).first()

def get_plcs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PLC).offset(skip).limit(limit).all()

def create_plc(db: Session, plc: schemas.PLCCreate):
    # Check for duplicate name or IP address
    if db.query(models.PLC).filter(models.PLC.name == plc.name).first():
        raise HTTPException(status_code=400, detail="PLC name already exists.")
    if db.query(models.PLC).filter(models.PLC.ip_address == plc.ip_address).first():
        raise HTTPException(status_code=400, detail="PLC IP address already exists.")

    db_plc = models.PLC(
        name=plc.name,
        ip_address=plc.ip_address,
        port=plc.port,
        protocol=plc.protocol,
        active=plc.active,
    )
    db.add(db_plc)
    db.flush()  # Assign ID for use in tags

    # Add tags
    for tag in plc.tags:
        if db.query(models.Tag).filter(
            models.Tag.plc_id == db_plc.id,
            models.Tag.name == tag.name
        ).first():
            raise HTTPException(status_code=400, detail=f"Duplicate tag '{tag.name}' for PLC.")

        db_tag = models.Tag(
            name=tag.name,
            address=tag.address,
            function_code=tag.function_code,
            unit_id=tag.unit_id,
            plc_id=db_plc.id,
        )
        db.add(db_tag)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create PLC or tags due to uniqueness violation.")

    db.refresh(db_plc)
    return db_plc

def update_plc(db: Session, db_plc: models.PLC, updates: schemas.PLCUpdate):
    data = updates.dict(exclude_unset=True)

    # If name or IP is updated, check for duplicates
    if "name" in data and data["name"] != db_plc.name:
        if db.query(models.PLC).filter(models.PLC.name == data["name"]).first():
            raise HTTPException(status_code=400, detail="PLC name already exists.")
    if "ip_address" in data and data["ip_address"] != db_plc.ip_address:
        if db.query(models.PLC).filter(models.PLC.ip_address == data["ip_address"]).first():
            raise HTTPException(status_code=400, detail="PLC IP address already exists.")

    # Handle tags
    if "tags" in data:
        db_plc.tags.clear()  # Clear existing tags
        for tag in data.pop("tags"):
            # Prevent duplicate tag names
            if any(t.name == tag.name for t in db_plc.tags):
                raise HTTPException(status_code=400, detail=f"Duplicate tag '{tag.name}' in update.")

            db_plc.tags.append(models.Tag(**tag.dict(), plc_id=db_plc.id))

    # Update other fields
    for field, value in data.items():
        setattr(db_plc, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to update PLC due to uniqueness violation.")

    db.refresh(db_plc)
    return db_plc

def delete_plc(db: Session, db_plc: models.PLC):
    db.delete(db_plc)
    db.commit()

# Tag operations
def get_tags_by_plc(db: Session, plc_id: int):
    return db.query(models.Tag).filter(models.Tag.plc_id == plc_id).all()

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def create_tag(db: Session, plc_id: int, tag: schemas.TagCreate):
    # Prevent duplicate tag name for this PLC
    if db.query(models.Tag).filter(
        models.Tag.plc_id == plc_id,
        models.Tag.name == tag.name
    ).first():
        raise HTTPException(status_code=400, detail="Tag with this name already exists for this PLC.")

    db_tag = models.Tag(
        name=tag.name,
        address=tag.address,
        function_code=tag.function_code,
        unit_id=tag.unit_id,
        plc_id=plc_id,
    )
    db.add(db_tag)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create tag due to uniqueness violation.")

    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, db_tag: models.Tag):
    db.delete(db_tag)
    db.commit()

# InfluxConfig operations
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
