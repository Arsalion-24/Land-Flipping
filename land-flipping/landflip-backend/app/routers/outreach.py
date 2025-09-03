from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
import os
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models

router = APIRouter(prefix="/outreach", tags=["outreach"])

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM")

class EmailPayload(BaseModel):
    to: EmailStr
    subject: str
    body: str
    parcel_id: int | None = None
    campaign_id: int | None = None

@router.post("/email")
def send_email(payload: EmailPayload, db: Session = Depends(get_db)):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS, SMTP_FROM]):
        raise HTTPException(status_code=500, detail="SMTP not configured")
    msg = MIMEText(payload.body)
    msg["Subject"] = payload.subject
    msg["From"] = SMTP_FROM
    msg["To"] = payload.to
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_FROM, [payload.to], msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Email send failed: {e}")
    if payload.parcel_id:
        db.add(models.Interaction(parcel_id=payload.parcel_id, campaign_id=payload.campaign_id, channel="email", direction="out", status="sent", notes=f"Subject: {payload.subject}"))
        db.commit()
    return {"sent": True}
