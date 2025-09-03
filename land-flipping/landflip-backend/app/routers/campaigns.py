from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.get("/", response_model=List[schemas.CampaignOut])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).order_by(models.Campaign.id.desc()).all()

@router.post("/", response_model=schemas.CampaignOut)
def create_campaign(payload: schemas.CampaignCreate, db: Session = Depends(get_db)):
    c = models.Campaign(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("/{campaign_id}", response_model=schemas.CampaignOut)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    c = db.get(models.Campaign, campaign_id)
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return c

@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    c = db.get(models.Campaign, campaign_id)
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(c)
    db.commit()
    return {"deleted": campaign_id}

@router.get("/{campaign_id}/metrics")
def campaign_metrics(campaign_id: int, db: Session = Depends(get_db)):
    total = db.query(models.Parcel).filter(models.Parcel.campaign_id == campaign_id).count()
    by_status = (
        db.query(models.Parcel.status, func.count(models.Parcel.id))
        .filter(models.Parcel.campaign_id == campaign_id)
        .group_by(models.Parcel.status)
        .all()
    )
    inter_stats = (
        db.query(models.Interaction.status, func.count(models.Interaction.id))
        .filter(models.Interaction.campaign_id == campaign_id)
        .group_by(models.Interaction.status)
        .all()
    )
    return {
        "parcels_total": total,
        "parcels_by_status": dict(by_status),
        "interactions_by_status": dict(inter_stats),
    }
