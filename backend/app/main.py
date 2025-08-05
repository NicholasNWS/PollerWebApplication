from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .db import SessionLocal, engine, Base

# Create tables (for dev only; use migrations in production)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(title="PLC Poller Config API")

# Configure CORS (origins from env var or default)
origins = [os.getenv("CORS_ORIGIN", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the PLC Poller Config API"}

# PLC endpoints
@app.post("/plcs/", response_model=schemas.PLC, status_code=201, tags=["PLC"])
def create_plc(plc: schemas.PLCCreate, db: Session = Depends(get_db)):
    if crud.get_plc_by_name(db, name=plc.name):
        raise HTTPException(status_code=409, detail="PLC already registered")
    new = crud.create_plc(db, plc)
    return new

@app.get("/plcs/", response_model=list[schemas.PLC], tags=["PLC"])
def read_plcs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_plcs(db, skip=skip, limit=limit)

@app.get("/plcs/{plc_id}", response_model=schemas.PLC, tags=["PLC"])
def read_plc(plc_id: int, db: Session = Depends(get_db)):
    plc = crud.get_plc(db, plc_id)
    if not plc:
        raise HTTPException(status_code=404, detail="PLC not found")
    return plc

@app.patch("/plcs/{plc_id}", response_model=schemas.PLC, tags=["PLC"])
def update_plc(plc_id: int, updates: schemas.PLCUpdate, db: Session = Depends(get_db)):
    plc = crud.get_plc(db, plc_id)
    if not plc:
        raise HTTPException(status_code=404, detail="PLC not found")
    updated = crud.update_plc(db, plc, updates)
    return updated

@app.delete("/plcs/{plc_id}", status_code=204, tags=["PLC"])
def delete_plc(plc_id: int, db: Session = Depends(get_db)):
    plc = crud.get_plc(db, plc_id)
    if not plc:
        raise HTTPException(status_code=404, detail="PLC not found")
    crud.delete_plc(db, plc)

# Influx Config
@app.get("/influx", response_model=schemas.InfluxConfig, tags=["Influx"])
def get_influx(db: Session = Depends(get_db)):
    cfg = crud.get_influx_config(db)
    if not cfg:
        raise HTTPException(status_code=404, detail="Influx config not set")
    return cfg

@app.post("/influx", response_model=schemas.InfluxConfig, tags=["Influx"])
def set_influx(cfg_in: schemas.InfluxConfigBase, db: Session = Depends(get_db)):
    existing = crud.get_influx_config(db)
    if existing:
        return crud.update_influx_config(db, existing, cfg_in)
    return crud.create_influx_config(db, cfg_in)