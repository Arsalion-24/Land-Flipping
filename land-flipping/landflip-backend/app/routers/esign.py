from fastapi import APIRouter, HTTPException, Request
import os
import httpx

router = APIRouter(prefix="/esign", tags=["esign"])

DOCUSEAL_URL = os.getenv("DOCUSEAL_URL", "http://docuseal:3000")
DOCUSEAL_API_KEY = os.getenv("DOCUSEAL_API_KEY", "")

@router.post("/envelope")
async def create_envelope(template_id: str, recipient_email: str, recipient_name: str):
    # This assumes DocuSeal API compatibility; adjust per actual API
    if not DOCUSEAL_API_KEY:
        raise HTTPException(status_code=500, detail="DocuSeal not configured")
    payload = {
        "template_id": template_id,
        "recipients": [{"email": recipient_email, "name": recipient_name}],
    }
    headers = {"Authorization": f"Bearer {DOCUSEAL_API_KEY}"}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{DOCUSEAL_URL}/api/envelopes", json=payload, headers=headers)
        if r.status_code >= 300:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()

@router.post("/webhook")
async def webhook(req: Request):
    # Accept status updates from the e-sign service
    data = await req.json()
    return {"ok": True}
