from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/utils", tags=["utils"])

@router.get("/geocode")
async def geocode(address: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "landflip/1.0"}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params, headers=headers)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Geocoding failed")
        data = r.json()
        if not data:
            return {"found": False}
        item = data[0]
        return {"found": True, "lat": float(item["lat"]), "lon": float(item["lon"]) }
