from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup
from ..db import get_db
from .. import models

router = APIRouter(prefix="/auctions", tags=["auctions"])

@router.get("/sources")
def list_sources(db: Session = Depends(get_db)):
    return db.query(models.AuctionSource).order_by(models.AuctionSource.id.desc()).all()

@router.post("/sources")
def add_source(name: str, url: str, county: str = "", state: str = "", country: str = "US", db: Session = Depends(get_db)):
    s = models.AuctionSource(name=name, url=url, county=county, state=state, country=country)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.delete("/sources/{source_id}")
def delete_source(source_id: int, db: Session = Depends(get_db)):
    s = db.get(models.AuctionSource, source_id)
    if not s:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(s)
    db.commit()
    return {"deleted": source_id}

@router.post("/run/{source_id}")
def run_source(source_id: int, db: Session = Depends(get_db)):
    s = db.get(models.AuctionSource, source_id)
    if not s:
        raise HTTPException(status_code=404, detail="Not found")
    try:
        r = requests.get(s.url, timeout=20, headers={"User-Agent": "landflip/1.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True)
        # naive extract: look for "APN" or parcel-like tokens
        events = 0
        for token in set(text.split()):
            if any(k in token.upper() for k in ["APN", "PARCEL", "PIN"]):
                db.add(models.AuctionEvent(source_id=s.id, parcel_id_text=token[:256], status="found", raw=token))
                events += 1
        db.commit()
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Fetch failed: {e}")
