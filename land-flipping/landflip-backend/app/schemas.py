from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any

# Users
class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    role: str
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Owners
class OwnerBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    country: Optional[str] = None

class OwnerCreate(OwnerBase):
    pass

class OwnerOut(OwnerBase):
    id: int
    class Config:
        from_attributes = True

# Campaigns
class CampaignBase(BaseModel):
    name: str
    channel: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "active"

class CampaignCreate(CampaignBase):
    pass

class CampaignOut(CampaignBase):
    id: int
    class Config:
        from_attributes = True

# Parcels
class ParcelBase(BaseModel):
    parcel_id: Optional[str] = None
    apn: Optional[str] = None
    owner_name: Optional[str] = None
    owner_id: Optional[int] = None
    county: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    acreage: Optional[float] = None
    address: Optional[str] = None
    status: Optional[str] = None
    score: Optional[int] = None
    valuation: Optional[float] = None
    offer_min: Optional[float] = None
    offer_max: Optional[float] = None
    campaign_id: Optional[int] = None

class ParcelCreate(ParcelBase):
    geom_wkt: Optional[str] = None

class ParcelUpdate(ParcelBase):
    pass

class ParcelOut(ParcelBase):
    id: int
    class Config:
        from_attributes = True

# Interactions
class InteractionBase(BaseModel):
    parcel_id: int
    campaign_id: Optional[int] = None
    channel: Optional[str] = None
    direction: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class InteractionCreate(InteractionBase):
    pass

class InteractionOut(InteractionBase):
    id: int
    class Config:
        from_attributes = True

# GeoJSON
class GeoJSONFeature(BaseModel):
    type: str
    geometry: Any
    properties: dict

class GeoJSONFeatureCollection(BaseModel):
    type: str
    features: List[GeoJSONFeature]
