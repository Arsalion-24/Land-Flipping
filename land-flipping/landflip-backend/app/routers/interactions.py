from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/interactions", tags=["interactions"])

@router.get("/parcel/{parcel_id}", response_model=List[schemas.InteractionOut])
def list_for_parcel(parcel_id: int, db: Session = Depends(get_db)):
    return db.query(models.Interaction).filter(models.Interaction.parcel_id == parcel_id).order_by(models.Interaction.id.desc()).all()

@router.post("/", response_model=schemas.InteractionOut)
def create_interaction(payload: schemas.InteractionCreate, db: Session = Depends(get_db)):
    inter = models.Interaction(**payload.model_dump())
    db.add(inter)
    db.commit()
    db.refresh(inter)
    return inter

@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    inter = db.get(models.Interaction, interaction_id)
    if not inter:
        raise HTTPException(status_code=404, detail="Interaction not found")
    db.delete(inter)
    db.commit()
    return {"deleted": interaction_id}
