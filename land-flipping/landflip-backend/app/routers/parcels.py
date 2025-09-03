from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from shapely import wkt, wkb
from shapely.geometry import mapping
from geoalchemy2.shape import from_shape
import csv
import io
from typing import List, Optional
import pandas as pd
import zipfile
import tempfile
import geopandas as gpd
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/parcels", tags=["parcels"])

@router.get("/", response_model=List[schemas.ParcelOut])
def list_parcels(
    db: Session = Depends(get_db),
    owner_name: Optional[str] = None,
    county: Optional[str] = None,
    state: Optional[str] = None,
    status: Optional[str] = None,
    campaign_id: Optional[int] = None,
    limit: int = Query(500, ge=1, le=5000),
):
    q = db.query(models.Parcel)
    if owner_name:
        q = q.filter(models.Parcel.owner_name.ilike(f"%{owner_name}%"))
    if county:
        q = q.filter(models.Parcel.county.ilike(f"%{county}%"))
    if state:
        q = q.filter(models.Parcel.state.ilike(f"%{state}%"))
    if status:
        q = q.filter(models.Parcel.status == status)
    if campaign_id is not None:
        q = q.filter(models.Parcel.campaign_id == campaign_id)
    return q.order_by(models.Parcel.id.desc()).limit(limit).all()

@router.get("/geojson", response_model=schemas.GeoJSONFeatureCollection)
def parcels_geojson(db: Session = Depends(get_db), limit: int = Query(1000, ge=1, le=10000)):
    features = []
    for p in db.query(models.Parcel).order_by(models.Parcel.id.desc()).limit(limit).all():
        geom_geojson = None
        if p.geom is not None:
            try:
                shape = wkb.loads(bytes(p.geom.data))
                geom_geojson = mapping(shape)
            except Exception:
                geom_geojson = None
        props = {
            "id": p.id,
            "parcel_id": p.parcel_id,
            "apn": p.apn,
            "owner_name": p.owner_name,
            "county": p.county,
            "state": p.state,
            "country": p.country,
            "acreage": float(p.acreage) if p.acreage is not None else None,
            "address": p.address,
            "status": p.status,
            "score": p.score,
            "valuation": float(p.valuation) if p.valuation is not None else None,
        }
        features.append({"type": "Feature", "geometry": geom_geojson, "properties": props})
    return {"type": "FeatureCollection", "features": features}

@router.post("/", response_model=schemas.ParcelOut)
def create_parcel(payload: schemas.ParcelCreate, db: Session = Depends(get_db)):
    geom = None
    if payload.geom_wkt:
        try:
            shape = wkt.loads(payload.geom_wkt)
            geom = from_shape(shape, srid=4326)
        except Exception:
            geom = None
    data = payload.model_dump(exclude={"geom_wkt"})
    parcel = models.Parcel(**data, geom=geom)
    db.add(parcel)
    db.commit()
    db.refresh(parcel)
    return parcel

@router.patch("/{parcel_id}", response_model=schemas.ParcelOut)
def update_parcel(parcel_id: int, payload: schemas.ParcelUpdate, db: Session = Depends(get_db)):
    parcel = db.get(models.Parcel, parcel_id)
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(parcel, k, v)
    db.commit()
    db.refresh(parcel)
    return parcel

@router.post("/ingest-csv")
def ingest_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith((".csv", ".txt")):
        raise HTTPException(status_code=400, detail="Only CSV supported for this endpoint")
    data = file.file.read().decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(data))
    count = 0
    for row in reader:
        geom = None
        geom_wkt = row.get("geom_wkt") or row.get("WKT") or row.get("geometry")
        if geom_wkt:
            try:
                shape = wkt.loads(geom_wkt)
                geom = from_shape(shape, srid=4326)
            except Exception:
                geom = None
        parcel = models.Parcel(
            parcel_id=row.get("parcel_id") or row.get("ParcelID") or row.get("parcel") or None,
            apn=row.get("apn") or row.get("APN") or None,
            owner_name=row.get("owner") or row.get("owner_name") or None,
            county=row.get("county") or row.get("County") or None,
            state=row.get("state") or row.get("State") or None,
            country=row.get("country") or row.get("Country") or None,
            acreage=(float(row.get("acreage")) if row.get("acreage") else None),
            address=row.get("address") or None,
            status=row.get("status") or "lead",
            geom=geom,
        )
        db.add(parcel)
        count += 1
        if count % 500 == 0:
            db.commit()
    db.commit()
    return {"ingested": count}

@router.post("/ingest-xlsx")
def ingest_xlsx(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only XLSX/XLS supported")
    content = file.file.read()
    try:
        df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read Excel: {e}")
    # Normalize columns
    cols = {c.lower().strip(): c for c in df.columns}
    def get_val(row, keys):
        for k in keys:
            if k in cols:
                v = row[cols[k]]
                return None if pd.isna(v) else v
        return None
    count = 0
    for _, row in df.iterrows():
        geom = None
        geom_wkt = get_val(row, ["geom_wkt", "wkt", "geometry"])
        if geom_wkt:
            try:
                shape = wkt.loads(str(geom_wkt))
                geom = from_shape(shape, srid=4326)
            except Exception:
                geom = None
        acreage_val = get_val(row, ["acreage", "acres", "size_acres"]) 
        acreage = float(acreage_val) if acreage_val is not None else None
        parcel = models.Parcel(
            parcel_id=str(get_val(row, ["parcel_id", "parcel", "parcelid"]) or "" ) or None,
            apn=str(get_val(row, ["apn"]) or "") or None,
            owner_name=str(get_val(row, ["owner", "owner_name"]) or "") or None,
            county=str(get_val(row, ["county"]) or "") or None,
            state=str(get_val(row, ["state"]) or "") or None,
            country=str(get_val(row, ["country"]) or "") or None,
            acreage=acreage,
            address=str(get_val(row, ["address"]) or "") or None,
            status=str(get_val(row, ["status"]) or "lead"),
            geom=geom,
        )
        db.add(parcel)
        count += 1
        if count % 500 == 0:
            db.commit()
    db.commit()
    return {"ingested": count}

@router.post("/ingest-shapefile")
def ingest_shapefile(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith((".zip",)):
        raise HTTPException(status_code=400, detail="Upload a zipped Shapefile (.zip)")
    content = file.file.read()
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = f"{tmp}/input.zip"
        with open(zip_path, "wb") as f:
            f.write(content)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(tmp)
        # load all .shp files
        count = 0
        for shp in gpd.io.file.fiona.listlayers(tmp):
            pass
        # attempt to read any shapefile in folder
        gdfs = []
        for path in gpd.io.file.fiona.listdir(tmp):
            if path.lower().endswith(".shp"):
                gdfs.append(gpd.read_file(f"{tmp}/{path}").to_crs(4326))
        if not gdfs:
            # try generic read
            try:
                gdf = gpd.read_file(tmp).to_crs(4326)
                gdfs = [gdf]
            except Exception:
                raise HTTPException(status_code=400, detail="No shapefile found in ZIP")
        for gdf in gdfs:
            for _, row in gdf.iterrows():
                geom = None
                if row.geometry is not None and not row.geometry.is_empty:
                    try:
                        geom = from_shape(row.geometry, srid=4326)
                    except Exception:
                        geom = None
                parcel = models.Parcel(
                    parcel_id=str(row.get("parcel_id") or row.get("PARCEL_ID") or row.get("APN") or "" ) or None,
                    apn=str(row.get("apn") or row.get("APN") or "") or None,
                    county=str(row.get("county") or row.get("COUNTY") or "") or None,
                    state=str(row.get("state") or row.get("STATE") or "") or None,
                    country=str(row.get("country") or row.get("COUNTRY") or "US") or None,
                    acreage=float(row.get("acreage") or row.get("ACRES") or 0) or None,
                    address=None,
                    status="lead",
                    geom=geom,
                )
                db.add(parcel)
                count += 1
                if count % 500 == 0:
                    db.commit()
        db.commit()
        return {"ingested": count}
