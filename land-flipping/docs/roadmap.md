# Phase Plan

Phase 1
- XLSX ingestion and scheduler
- Shapefile ETL via GDAL/GeoPandas to PostGIS
- Nominatim geocoding + address normalization
- Map filters and parcel detail panel
- Auth baseline (JWT, RBAC skeleton)

Phase 2
- Scrapy project + Playwright integration
- Celery pipelines, retries, monitoring
- CRM entities and campaign UI
- Asterisk dialer integration and call logging
- WhatsApp/SMS/Email channels

Phase 3
- Contract generation (Markdown→PDF)
- DocuSeal/LibreSign integration
- Auction scrapers + alerts
- ML lead scoring + valuation prototype

Phase 4
- Country adapters (2 examples)
- Security hardening: TLS, audit logs, PII encryption
- k3s manifests and CI/CD
