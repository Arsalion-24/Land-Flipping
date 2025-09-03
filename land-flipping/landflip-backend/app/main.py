from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import API_CORS_ORIGINS
from .db import Base, engine
from .routers import health, parcels
from .routers import owners, campaigns, interactions, auth
from .routers import ml as ml_router
from .routers import utils as utils_router
from .routers import outreach as outreach_router
from .routers import auctions as auctions_router
from .routers import esign as esign_router
from .routers import dialer as dialer_router
from .routers import enrichment as enrichment_router
from .middleware import AuditMiddleware

app = FastAPI(title="Land Flipping Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in API_CORS_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuditMiddleware)

Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(parcels.router)
app.include_router(owners.router)
app.include_router(campaigns.router)
app.include_router(interactions.router)
app.include_router(ml_router.router)
app.include_router(utils_router.router)
app.include_router(outreach_router.router)
app.include_router(auctions_router.router)
app.include_router(esign_router.router)
app.include_router(dialer_router.router)
app.include_router(enrichment_router.router)
