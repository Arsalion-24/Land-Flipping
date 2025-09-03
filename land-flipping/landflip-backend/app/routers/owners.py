from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import models, schemas
from ..security_encryption import encrypt_value, decrypt_value

router = APIRouter(prefix="/owners", tags=["owners"])

@router.get("/", response_model=List[schemas.OwnerOut])
def list_owners(db: Session = Depends(get_db)):
    owners = db.query(models.Owner).order_by(models.Owner.id.desc()).limit(1000).all()
    for o in owners:
        o.email = decrypt_value(o.email)
        o.phone = decrypt_value(o.phone)
    return owners

@router.post("/", response_model=schemas.OwnerOut)
def create_owner(payload: schemas.OwnerCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data["email"] = encrypt_value(data.get("email"))
    data["phone"] = encrypt_value(data.get("phone"))
    owner = models.Owner(**data)
    db.add(owner)
    db.commit()
    db.refresh(owner)
    owner.email = decrypt_value(owner.email)
    owner.phone = decrypt_value(owner.phone)
    return owner

@router.get("/{owner_id}", response_model=schemas.OwnerOut)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    owner.email = decrypt_value(owner.email)
    owner.phone = decrypt_value(owner.phone)
    return owner

@router.delete("/{owner_id}")
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    db.delete(owner)
    db.commit()
    return {"deleted": owner_id}
