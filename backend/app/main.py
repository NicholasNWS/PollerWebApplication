from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .db import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PLC Poller Config API")

origins = [os.getenv("CORS_ORIGIN", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get("/plcs/", response_model=List[schemas.PLC], tags=["PLC"])
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

# --- Add Tag endpoints here ---

@app.post("/plcs/{plc_id}/tags/", response_model=schemas.Tag, status_code=201, tags=["Tag"])
def create_tag_for_plc(plc_id: int, tag: schemas.TagCreate, db: Session = Depends(get_db)):
    plc = crud.get_plc(db, plc_id)
    if not plc:
        raise HTTPException(status_code=404, detail="PLC not found")
    new_tag = crud.create_tag(db, tag, plc_id)
    return new_tag

@app.get("/plcs/{plc_id}/tags/", response_model=List[schemas.Tag], tags=["Tag"])
def read_tags_for_plc(plc_id: int, db: Session = Depends(get_db)):
    plc = crud.get_plc(db, plc_id)
    if not plc:
        raise HTTPException(status_code=404, detail="PLC not found")
    return crud.get_tags_by_plc(db, plc_id)

# Influx Config endpoints
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
