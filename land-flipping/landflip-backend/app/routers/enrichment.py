from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models
from ..enrichment import simple_web_lookup, normalize_phone

router = APIRouter(prefix="/enrichment", tags=["enrichment"])

@router.post("/owner/{owner_id}")
def enrich_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    res = simple_web_lookup(owner.name or "", None, None)
    updated = False
    if res.get("phone") and not owner.phone:
        owner.phone = normalize_phone(res["phone"]) or owner.phone
        updated = True
    if res.get("email") and not owner.email:
        owner.email = res["email"]
        updated = True
    if updated:
        db.commit()
    return {"updated": updated, "phone": owner.phone, "email": owner.email}

@router.post("/parcel/{parcel_id}")
def enrich_parcel(parcel_id: int, db: Session = Depends(get_db)):
    parcel = db.get(models.Parcel, parcel_id)
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    if parcel.owner_id:
        return enrich_owner(parcel.owner_id, db)
    # fallback on owner_name
    if parcel.owner_name:
        tmp_owner = models.Owner(name=parcel.owner_name)
        db.add(tmp_owner)
        db.flush()
        parcel.owner_id = tmp_owner.id
        db.commit()
        return enrich_owner(tmp_owner.id, db)
    return {"updated": False}
