from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .db import SessionLocal, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PLC Poller Config API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PLC Routes
@app.post("/plcs/", response_model=schemas.PLC)
def create_plc(plc: schemas.PLCCreate, db: Session = Depends(get_db)):
    db_plc = crud.get_plc_by_name(db, name=plc.name)
    if db_plc:
        raise HTTPException(status_code=400, detail="PLC already registered")
    return crud.create_plc(db, plc)

@app.get("/plcs/", response_model=list[schemas.PLC])
def read_plcs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_plcs(db, skip=skip, limit=limit)

@app.get("/plcs/{plc_id}", response_model=schemas.PLC)
def read_plc(plc_id: int, db: Session = Depends(get_db)):
    db_plc = crud.get_plc(db, plc_id)
    if not db_plc:
        raise HTTPException(status_code=404, detail="PLC not found")
    return db_plc

@app.patch("/plcs/{plc_id}", response_model=schemas.PLC)
def update_plc(plc_id: int, updates: schemas.PLCUpdate, db: Session = Depends(get_db)):
    db_plc = crud.get_plc(db, plc_id)
    if not db_plc:
        raise HTTPException(status_code=404, detail="PLC not found")
    return crud.update_plc(db, db_plc, updates)

@app.delete("/plcs/{plc_id}")
def delete_plc(plc_id: int, db: Session = Depends(get_db)):
    db_plc = crud.get_plc(db, plc_id)
    if not db_plc:
        raise HTTPException(status_code=404, detail="PLC not found")
    crud.delete_plc(db, db_plc)
    return {"detail": "Deleted"}

# Influx Config
@app.get("/influx", response_model=schemas.InfluxConfig)
def get_influx(db: Session = Depends(get_db)):
    cfg = crud.get_influx_config(db)
    if not cfg:
        raise HTTPException(status_code=404, detail="Influx config not set")
    return cfg

@app.post("/influx", response_model=schemas.InfluxConfig)
def set_influx(cfg: schemas.InfluxConfigBase, db: Session = Depends(get_db)):
    existing = crud.get_influx_config(db)
    if existing:
        return crud.update_influx_config(db, existing, cfg)
    return crud.create_influx_config(db, cfg)