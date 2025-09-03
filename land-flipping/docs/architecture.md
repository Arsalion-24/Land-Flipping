# Architecture Overview

Services
- api: FastAPI monolith exposing modules for ingestion, CRM, campaigns, contracts, auctions, ML.
- worker: Celery worker for ETL, scraping orchestration, enrichment, ML jobs. Broker: Redis. Results: DB.
- scraper: Scrapy project executed via Celery tasks; Playwright/Selenium container for dynamic sites.
- db: PostgreSQL + PostGIS.
- web: React + MapLibre frontend (static) served by Nginx.
- optional: asterisk, docuseal, minio (object storage), vector-tile service.

Data model (Phase 1)
- parcels(id, parcel_id, apn, owner_name, county, acreage, address, geom POLYGON 4326, created_at)
- owners(id, name)
- campaigns(id, name, channel, created_at)
- interactions(id, parcel_id, channel, direction, status, notes, created_at)

APIs (Phase 1)
- GET /health
- POST /parcels/ingest-csv multipart file
- GET /parcels
- GET /parcels/geojson

Pipelines
- CSV ingestion: parse, normalize columns, optional WKT geometry, insert into PostGIS.
- Future: XLSX ingestion, geocoding via Nominatim, shapefile ETL via GDAL/GeoPandas.

Security
- CORS configured; future: JWT auth, RBAC, TLS termination at reverse proxy.

DevOps
- docker-compose with db, redis, api, web.
- future: separate images for worker and scraper; k3s manifests; GitHub Actions CI.
