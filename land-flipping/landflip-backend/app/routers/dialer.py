from fastapi import APIRouter, Request

router = APIRouter(prefix="/dialer", tags=["dialer"])

@router.post("/webhook")
async def webhook(req: Request):
    # Receive call events (e.g., from Asterisk AMI/AR) and map to interactions
    data = await req.json()
    return {"ok": True}
