from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models
from ..ml import heuristic_score, train_model, estimate_value

router = APIRouter(prefix="/ml", tags=["ml"])

@router.post("/score")
def score_all(db: Session = Depends(get_db)):
    updated = 0
    for p in db.query(models.Parcel).all():
        p.score = heuristic_score(float(p.acreage) if p.acreage is not None else None, p.county)
        updated += 1
    db.commit()
    return {"scored": updated}

@router.post("/train")
def train(db: Session = Depends(get_db)):
    parcels = db.query(models.Parcel).all()
    try:
        path = train_model(parcels)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"model": path}

@router.post("/value")
def value_all(db: Session = Depends(get_db)):
    updated = 0
    for p in db.query(models.Parcel).all():
        p.valuation = estimate_value(p)
        updated += 1
    db.commit()
    return {"valued": updated}
