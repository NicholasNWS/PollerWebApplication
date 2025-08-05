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
        port=plc.port
    )
    db.add(db_plc)
    db.commit()
    db.refresh(db_plc)

    # Add tags
    for tag in plc.tags:
        db_tag = models.Tag(
            name=tag.name,
            address=tag.address,
            function_code=tag.function_code,
            unit_id=tag.unit_id,
            plc_id=db_plc.id
        )
        db.add(db_tag)
    db.commit()
    db.refresh(db_plc)  # Refresh to include tags if needed

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
