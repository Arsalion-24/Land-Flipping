from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    name = Column(String(256))
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(32), default="admin")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), index=True)
    email = Column(String(256))
    phone = Column(String(64))
    country = Column(String(2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    parcels = relationship("Parcel", back_populates="owner")

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), index=True)
    channel = Column(String(64))
    description = Column(Text)
    status = Column(String(32), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interactions = relationship("Interaction", back_populates="campaign")
    parcels = relationship("Parcel", back_populates="campaign")

class Parcel(Base):
    __tablename__ = "parcels"
    id = Column(Integer, primary_key=True, index=True)
    parcel_id = Column(String(128), index=True)
    apn = Column(String(128), index=True)
    owner_name = Column(String(256), index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=True)
    county = Column(String(128), index=True)
    state = Column(String(64), index=True)
    country = Column(String(2), index=True)
    acreage = Column(Numeric)
    address = Column(Text)
    status = Column(String(64), index=True, default="lead")
    score = Column(Integer)
    valuation = Column(Numeric)
    offer_min = Column(Numeric)
    offer_max = Column(Numeric)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    geom = Column(Geometry("POLYGON", srid=4326))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("Owner", back_populates="parcels")
    campaign = relationship("Campaign", back_populates="parcels")
    interactions = relationship("Interaction", back_populates="parcel")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True)
    parcel_id = Column(Integer, ForeignKey("parcels.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    channel = Column(String(64))
    direction = Column(String(16))
    status = Column(String(64))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    parcel = relationship("Parcel", back_populates="interactions")
    campaign = relationship("Campaign", back_populates="interactions")

class AuctionSource(Base):
    __tablename__ = "auction_sources"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), index=True)
    url = Column(Text)
    county = Column(String(128))
    state = Column(String(64))
    country = Column(String(2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuctionEvent(Base):
    __tablename__ = "auction_events"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("auction_sources.id"))
    parcel_id_text = Column(String(256))
    status = Column(String(64))
    raw = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    method = Column(String(8))
    path = Column(Text)
    status_code = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
