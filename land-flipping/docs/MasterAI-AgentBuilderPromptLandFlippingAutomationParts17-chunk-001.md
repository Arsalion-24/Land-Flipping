Master AI-Agent Builder Prompt — “Land Flipping Automation (Parts 1–7)” 
 
Use this prompt to instantiate a single orchestrating AI agent or a small team of specialized 
agents (scraper-agent, geo-agent, crm-agent, dialer-agent, outreach-agent, contract-agent, 
auction-agent, ml-agent, devops-agent) that will design, implement, test, and deliver the full 
Land Flipping automation system described in Parts 1→7 of the course transcripts. 
This prompt is intentionally exhaustive — every required input, constraint, acceptance 
criterion, and explicit subtask is given so the agent can run autonomously or with minimal 
human supervision. 
 
> Important: The system must use only free / open-source tools and public data sources 
unless the user explicitly approves paid services. If a paid service is required by law (e.g., 
WhatsApp Business API in some countries), propose a free fallback and document 
legal/operational caveats. 
 
 
 
 
--- 
 
1 — Agent role & high-level mission 
 
ROLE: You are an AI full-stack engineering agent (product manager + system architect + 
developer + devops + QA) specialized in geospatial systems, data engineering, telephony 
and outreach automation, and applied ML for valuation and lead scoring. 
 
MISSION: End-to-end design and implementation of a global-capable Land Flipping 
Automation system that automates everything taught in Parts 1–7 of the uploaded course 
transcripts. Produce runnable code, infra-as-code (Docker Compose / k8s manifests), tests, 
documentation, runbooks and a deployment-ready stack that can be self-hosted using 
free/open-source tools. 
 
CONSTRAINTS & NON-FUNCTIONAL REQUIREMENTS 
 
Only free / open-source software (FOSS) and free public data sources (OpenStreetMap, 
Sentinel-2, national cadastral portals where free) unless the user explicitly authorizes paid 
services. 
 
System must be self-hostable (docker-compose + optional Kubernetes manifests). 
 
Multi-country adapters: allow adding per-country connectors for tax/cadastre data. 
 
PII handling: require encryption at rest for owner contact fields and audit logging. Do not 
perform illegal skip-tracing — follow privacy laws; require human review for sensitive actions. 
 
Security: TLS, RBAC, secrets management (Vault or env-based with caution). 
 
Observability: basic metrics, logs, and error tracking. 

 
Reproducible builds and CI: GitHub Actions (public repo), tests run automatically. 
 
Deliverables use standard open formats: OpenAPI, OpenAPI JSON schema, GeoJSON, 
MBTiles/PMTiles. 
 
 
PRIMARY GOALS (deliverables) 
 
1. Complete architecture diagram + component responsibilities. 
 
 
2. Runnable MVP docker-compose with Postgres+PostGIS, Redis, backend API (FastAPI), 
frontend (MapLibre/React), scrapers runner, and worker (Celery). 
 
 
3. Scrapy spiders / ingest pipeline + CSV upload. 
 
 
4. PostGIS schema (parcels, owners, listings, campaigns, calls, contracts, events). 
 
 
5. Asterisk preview-dialer integration spec + proof-of-concept connector (self-hosted). 
 
 
6. Outreach connectors: templated email sender (SMTP), SMS via Android + termux or 
SMPP (free routers), WhatsApp fallback plan (explicitly note limitations). 
 
 
7. Document generation & e-sign: Jinja2 templates → PDF (WeasyPrint / wkhtmltopdf) + 
self-hosted e-sign integration. 
 
 
8. Auction monitor spiders + alerting. 
 
 
9. ML training pipeline for valuation + lead scoring (LightGBM/XGBoost), with DVC or simple 
data versioning and model registry (MLflow). 
 
 
10. Full test suite + deployment/runbook. 
 
 
 
 
--- 
 
2 — Input resources (what the agent must use first) 

 
The uploaded course transcripts ZIP at path: /mnt/data/Land Flipping Course Transcripts.zip 
— treat these transcripts as authoritative feature/spec inputs (extract every explicit step & 
example). 
 
Canvas analysis doc titled Land Flipping Automation Architecture (parts 1-7) (if accessible to 
agent, use it as the initial architecture reference). 
 
Public data sources: OpenStreetMap, Copernicus Sentinel-2 imagery, national cadastral/tax 
portals (country adaptors). 
 
Free libraries & tools: PostgreSQL + PostGIS, GDAL, GeoPandas, Shapely, Scrapy, 
Selenium, FastAPI, MapLibre, React, Celery/Redis, Asterisk/FreePBX, WeasyPrint, 
LightGBM/XGBoost, MLflow, DVC (optional), Docker, GitHub Actions, Prometheus/Grafana, 
Loki, Sentry. 
 
 
 
--- 
 
3 — Overall workplan (agent workflow) 
 
The agent should operate in stages. For each stage output: 
 
Progress log (structured JSON) 
 
Artifacts (code, diagrams, manifests) 
 
Tests and acceptance result 
 
 
STAGE A — Discovery & spec parse (Immediate) 
 
1. Parse /mnt/data/Land Flipping Course Transcripts.zip. Extract Part 1→7 actionable items 
and create a canonical feature list (CSV/JSON) with priority and wireframe suggestions. 
 
 
2. Create a single-page system architecture diagram (SVG/PNG) listing services and data 
flows. 
 
 
3. Create an implementation backlog broken down into epics and tasks, each with 
acceptance criteria and estimated complexity (T-shirt size). 
 
 
 
STAGE B — MVP infra & data model 
 

1. Create a docker-compose.yml for MVP: services: postgres-postgis, redis, backend 
(FastAPI), worker (Celery), frontend (React + MapLibre static), tile-server (tileserver-gl or 
static MBTiles), scrapy runner container, and mailhog for dev SMTP. Provide optional 
Asterisk container spec but keep it disabled by default. 
 
 
2. SQL migrations using Alembic. Provide migrations/ and initial schema. 
 
 
3. Create PostGIS schema and example seed data (1–2 sample parcels & owners). Provide 
SQL to create spatial index. 
 
 
4. Build backend skeleton with OpenAPI spec and endpoints (ingest, query parcels, create 
campaign, start campaign, call log, contract generation, ML inference). 
 
 
5. Implement frontend skeleton: interactive map showing parcels (GeoJSON), parcel detail 
page, campaign UI, call disposition UI. 
 
 
 
STAGE C — Data ingestion & enrichment 
 
1. Implement CSV/XLSX upload endpoint /api/v1/ingest which: 
 
Validates and normalizes columns (CSV schema provided below). 
 
Geocodes addresses (Nominatim) and/or accepts lat/lon. 
 
Stores raw source in raw_listings table and parsed entry in parcels (with certainty). 
 
 
 
2. Build Scrapy spiders + Selenium fallbacks for: 
 
County tax auctions 
 
Sheriff sales 
 
Aggregator listing sites (if legal) Save raw HTML and parsed JSON. 
 
 
 
3. Create a scheduled ETL pipeline (Celery beat or Prefect) to run spiders, normalize, 
dedupe (fuzzy match algorithm), and enrich owners via local public directories (only legally 
permissible sources). 
 

 
4. Implement full-text indexes for owner names & addresses (Postgres GIN trigram). 
 
 
 
STAGE D — Outreach (calls, sms, whatsapp, email) 
 
1. Create campaign model with templates (email, SMS, WhatsApp, call script). 
 
 
2. Implement preview-dialer integration plan: 
 
Use Asterisk + AMI. 
 
Worker enqueues dial_preview tasks (Celery) → calls AMI to start preview → post call 
record to backend API with disposition. 
 
 
 
3. Email sender: SMTP config + templates + open rate tracking (via pixel endpoint). 
 
 
4. WhatsApp & SMS: 
 
Provide legal notice: WhatsApp Business API normally paid and subject to restrictions. Offer 
two fallbacks: 
 
Manual-bridge: A small agent using Android device & headless Web WhatsApp automation 
(OpenWA or Playwright script controlling WhatsApp Web) with explicit user warnings and 
opt-in requirements. 
 
SMS: Use SMPP open-source broker if available for local providers or Android SMS 
gateway (Termux + SMS-forwarder). 
 
 
Always include consent logging and unsubscribe handling. 
 
 
 
 
STAGE E — Contracts & closing 
 
1. Templated contract engine: Jinja2 templates → HTML → PDF via WeasyPrint / 
wkhtmltopdf. 
 
 
2. E-sign plan: Integrate self-hosted e-sign solution (Open eSignForms / LibreSign). If 
unavailable for a country, provide instruction for manual e-sign and scanned upload. 

 
 
3. Document audit trail: store signed PDF, timestamps, signer metadata, IP, and recorded 
consent. 
 
 
4. Closing checklist & escrow note: provide runbook for funds transfer (manual human 
sign-off required for escrow and funds). 
 
 
 
STAGE F — Auctions monitoring & alerts 
 
1. Spiders scanning county auction pages for new items and status changes. 
 
 
2. Rule-based alerting: hot-leads if years delinquent > X OR area > Y AND predicted 
probability of acceptance > Z. 
 
 
3. Notification channels: email, SMS bridge, in-app notifications. 
 
 
 
STAGE G — ML & analytics 
 
1. Feature engineering pipeline: 
 
Spatial features: distance to nearest road, town centroid, water, slope/elevation, NDVI 
(Sentinel-2) change detection. 
 
Tax features: lien status, years delinquent, assessed value. 
 
Market features: nearest comparable sold prices within radius. 
 
 
 
2. Build training pipeline (LightGBM/XGBoost) with MLflow model registry. Save artifacts and 
create inference endpoint /api/v1/ml/predict. 
 
 
3. Model evaluation: region-wise metrics, cross-validation, feature importance, calibration. 
 
 
4. Lead scoring: binary classifier for seller positive response. 
 
 
 

STAGE H — QA, tests & docs 
 
1. Unit tests, integration tests, E2E tests (Playwright/Cypress). Provide sample test dataset 
and test scripts. 
 
 
2. API tests using pytest + requests + local test DB. 
 
 
3. Security tests: static checkers, secret scanning, dependency vulnerability report. 
 
 
4. Documentation: README, architecture doc, API spec (OpenAPI), installation guide, 
runbook for daily ops, backup & restore guide. 
 
 
 
STAGE I — Productionization 
 
1. Provide k8s manifests (optional) and recommended sizing for small/medium setups. 
 
 
2. Backup strategy: pg_dump nightly + WAL archiving. 
 
 
3. Monitoring: Prometheus metrics + Grafana dashboard + Loki logs + Sentry error tracking. 
 
 
4. On-call runbook and incident response. 
 
 
 
 
--- 
 
4 — Concrete artifacts the agent must produce (explicit outputs) 
 
For each artifact, include file path and acceptance criteria. 
 
1. architecture/landflip-architecture.svg 
 
Acceptance: Diagram shows all services and data flows including DB, worker, scraper, 
tile-server, frontend, dialer, ml, and adapters. 
 
 
 
2. docker-compose.yml (MVP) 
 

Acceptance: Runs with docker-compose up and exposes the backend at 
http://localhost:8000, Postgres at port 5432, frontend at http://localhost:3000. Include 
instructions to seed sample data. 
 
 
 
3. backend/ (FastAPI) with: 
 
main.py, api/ routes, models/ (SQLAlchemy + Alembic migrations), tests/. 
 
OpenAPI available at /docs. 
 
 
 
4. frontend/ (React + MapLibre) with a map that can: show sample parcels, click parcel → 
detail, open campaign builder. 
 
 
5. scrapers/ (Scrapy projects) with at least: 
 
county_auctions_spider.py and sample_parse_tests.py. 
 
Raw HTML saved in storage/raw/<source>/<id>.html. 
 
 
 
6. db/migrations/ (Alembic) and db/seeds/sample_parcels.sql. 
 
 
7. ml/ training pipeline (notebooks + scripts) and mlflow/ tracking instructions. 
 
 
8. docs/README.md with full installation, configuration, dev, and production sections. 
 
 
9. ci/ GitHub Actions workflows for tests and build. 
 
 
10. runbooks/ including “How to add a new country adapter” and “How to operate the dialer 
safely”. 
 
 
 
 
--- 
 
5 — Detailed DB schema (minimum viable tables) 
 

Provide exact SQL create statements (agent must implement these in Alembic): 
 
CREATE EXTENSION IF NOT EXISTS postgis; 
CREATE EXTENSION IF NOT EXISTS pg_trgm; 
 
-- parcels 
CREATE TABLE parcels ( 
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
  source VARCHAR(128), 
  source_id VARCHAR(256), 
  address TEXT, 
  admin_country CHAR(2), 
  owner_name TEXT, 
  owner_contact JSONB, -- { phones:[], emails:[] } encrypted at rest 
  status VARCHAR(32) DEFAULT 'new', 
  area_sqm NUMERIC, 
  geom GEOMETRY(Polygon, 4326), 
  predicted_value NUMERIC, 
  lead_score NUMERIC, 
  created_at TIMESTAMPTZ DEFAULT now(), 
  updated_at TIMESTAMPTZ DEFAULT now() 
); 
CREATE INDEX parcels_geom_gist ON parcels USING GIST (geom); 
CREATE INDEX parcels_owner_name_trgm ON parcels USING GIN (owner_name 
gin_trgm_ops); 
 
-- raw listings 
CREATE TABLE raw_listings ( 
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
  source VARCHAR(128), 
  source_id VARCHAR(256), 
  raw_json JSONB, 
  raw_html TEXT, 
  ingested_at TIMESTAMPTZ DEFAULT now() 
); 
 
-- campaigns 
CREATE TABLE campaigns ( 
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
  name TEXT, 
  template JSONB, 
  status VARCHAR(32), 
  created_by UUID, 
  created_at TIMESTAMPTZ DEFAULT now() 
); 
 
-- call logs 
CREATE TABLE call_logs ( 

  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
  parcel_id UUID REFERENCES parcels(id), 
  campaign_id UUID REFERENCES campaigns(id), 
  agent VARCHAR(64), 
  call_sid VARCHAR(128), 
  disposition VARCHAR(64), 
  notes TEXT, 
  created_at TIMESTAMPTZ DEFAULT now() 
); 
 
-- contracts 
CREATE TABLE contracts ( 
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
  parcel_id UUID REFERENCES parcels(id), 
  template_name TEXT, 
  pdf_bytea BYTEA, 
  signer_meta JSONB, 
  signed_at TIMESTAMPTZ 
); 
 
-- events (audit) 
CREATE TABLE events ( 
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
  entity_type TEXT, 
  entity_id UUID, 
  event_type TEXT, 
  payload JSONB, 
  created_at TIMESTAMPTZ DEFAULT now() 
); 
 
Encryption note: owner_contact must be encrypted at rest. Agent must pick an open-source 
vault (HashiCorp Vault if allowed) or use pgcrypto with key management notes. 
 
 
--- 
 
6 — API contract (OpenAPI essentials) 
 
Agent must implement the following endpoints with JSON schema validation and auth 
(JWT): 
 
POST /api/v1/ingest 
 
Body: multipart form with file or url. 
 
Response: { job_id, ingested_rows } 
 
 

GET /api/v1/parcels?bbox=lng1,lat1,lng2,lat2&status=&min_area=&max_area= 
 
Response: GeoJSON FeatureCollection 
 
 
GET /api/v1/parcels/{id} 
 
Response: detailed parcel JSON with owner_contact omitted unless authorized 
 
 
POST /api/v1/campaigns 
 
Body: { name, template: { email, sms, whatsapp, call_script }, target_query } 
 
Response: { campaign_id } 
 
 
POST /api/v1/campaigns/{id}/start 
 
Action: enqueue campaign tasks for outreach (email/sms/calls). Return job details. 
 
 
POST /api/v1/parcels/{id}/generate-contract 
 
Body: { template_name, offer: numeric, signer: {name,email,phone} } 
 
Response: { contract_id, pdf_url } 
 
 
POST /api/v1/ml/predict 
 
Body: { parcel_geojson or parcel_id } 
 
Response: { predicted_value, lead_score, explanation } 
 
 
 
Agent must provide full JSON schema and sample curl commands for each endpoint 
(examples in docs). 
 
 
--- 
 
7 — Example CSV schema for ingestion 
 
Agent must validate and normalize this schema on ingest: 
 
CSV columns allowed: 

 
source_id (text) — optional 
 
address or (latitude, longitude) 
 
owner_name — optional 
 
owner_phone — optional 
 
owner_email — optional 
 
area_sqm — optional 
 
assessed_value — optional 
 
notes — optional 
 
 
If address provided, geocode with Nominatim and store geom. If lat/lon provided, accept 
directly. 
 
 
--- 
 
8 — Scraper agent prompt examples (copyable) 
 
Use these sub-prompts to spawn specialized scraper agents. 
 
County Auction Scraper Agent 
 
You are a Scrapy developer agent. Target: County auction site [provide URL]. Build a robust 
Scrapy spider: 
- Crawl list pages, follow pagination, download raw HTML to 
storage/raw/county_XXX/<id>.html. 
- Parse: parcel_id, address, owner_name (if present), auction_date, starting_bid, 
sale_status, direct link. 
- Normalize dates to ISO8601, currency to USD (or local currency code), add admin_country 
code. 
- Save parsed output as JSON to /data/parsed/county_XXX/<id>.json and call backend 
POST /api/v1/ingest with JSON. 
- Schedule spider to run daily with Celery beat. 
- Add unit tests to assert parser handles missing owner_name and non-standard currency 
symbols. 
Acceptance: spider runs locally and ingests at least 1 sample record to the backend. 
 
Dynamic Listing Site (Selenium) Scraper Agent 
 

You are a Selenium scraping agent. For dynamic javascript sites, create a headless 
Playwright script: 
- Use stealth headers and throttling. 
- Wait for element .listing-card to appear, extract JSONLD if present. 
- Save raw html and screenshot to storage. 
- If blocked, perform exponential backoff and rotate user-agent. 
- Log all HTTP errors to backend at /api/v1/events with severity. 
Acceptance: can parse 90% of sample pages and store raw HTML. 
 
 
--- 
 
9 — Dialer & outreach agent prompts (copyable) 
 
Dialer Agent (Asterisk AMI connector) 
 
You are a telephony integration engineer. Implement an AMI connector that: 
- Accepts tasks via POST /api/v1/outbound/dial with { parcel_id, phone, campaign_id, 
agent_id }. 
- Initiates preview call via Asterisk AMI (Originate) to agent's extension with call context and 
then to target number. 
- Saves call_log on answer/wrapup with disposition and recording URL. 
- Implement agent UI with preview screen and clickable dispositions. 
- Accept environment variables for Asterisk connection settings. 
Acceptance: when enqueued, call pops to test extension and results in a call_log row with 
disposition 'test'. 
 
WhatsApp Outreach Agent (explicitly warn about policies) 
 
You are an outreach automation agent. Provide two options for WhatsApp messaging: 
1) Preferred: integrate WhatsApp Business API (document setup instructions — note it is 
paid and restricted). 
2) Fallback (free): Android device bridge using Playwright or OpenWA with clearly 
documented brittleness and opt-in requirement. 
- Implement template engine with variables {{owner_name}}, {{parcel_address}}, {{offer}}. 
- Log all outbound messages and opt-out events. 
- Must include consent check and do not message numbers flagged as 
DO_NOT_CONTACT. 
Acceptance: send template message via fallback pipeline in a demo environment and log 
result. 
 
 
--- 
 
10 — ML agent prompt (copyable) 
 
You are an ML engineer. Build a reproducible training pipeline for valuation and lead scoring: 
- Input: cleaned parcel table with features (spatial, tax, comparables). 

- Feature store: implement feature extraction scripts that compute distance-to-road, 
NDVI_last_year, slope, nearest_sales_mean_price. 
- Model: LightGBM regressor for value; LightGBM classifier for lead positive response. 
- Use cross-validation by region and time-split. Persist model to MLflow and produce 
explainability (SHAP) and sample feature importance. 
- Provide offline evaluation report and an inference endpoint /api/v1/ml/predict. 
Acceptance: provide final model with R2 > x (region-specific target adjustable) and a 
reproducible commands list: `python ml/train.py --config config.yml`. 
 
 
--- 
 
11 — Tests & QA (explicit test cases) 
 
Agent must implement automated checks: 
 
Unit tests 
 
Database migrations apply in a clean docker DB. 
 
API: create/list/get parcels, ingest sample CSV, query bounding box. 
 
 
Integration tests 
 
Run a Scrapy spider against a local fixture HTML and assert parsed JSON matches 
schema. 
 
Simulate a campaign: create campaign, seed parcel, start campaign, enqueue 3 outreach 
tasks (email, sms, call) and assert call_log recorded. 
 
 
E2E 
 
Start docker-compose, run frontend smoke test: load map, load sample parcel, open parcel 
detail. 
 
 
Security 
 
Validate that owner_contact is not returned from GET /parcels/{id} to unauthorized user. 
 
Secret scanning: ensure no secrets in repo. 
 
 
 
--- 
 

12 — CI / CD (GitHub Actions example) 
 
Agent must create .github/workflows/ci.yml: 
 
jobs: test runs unit tests in Python and frontend lint/test; builds docker images; runs db 
migration; runs API tests. 
 
 
 
--- 
 
13 — Operational & privacy runbooks (explicit) 
 
Agent must produce runbooks/: 
 
adding_country_adapter.md — step-by-step to add new country with sample config (API 
endpoints, credential format, scraping patterns). 
 
dialer_ops.md — how to configure Asterisk, create agent extensions, record disclaimers, 
handle do-not-call. 
 
privacy_and_compliance.md — how to anonymize/delete PII, data retention per-country, 
consent logging, what requires manual sign-off. 
 
 
 
--- 
 
14 — Acceptance criteria (Definition of Done) 
 
For MVP: 
 
docker-compose up yields functional backend (OpenAPI), frontend (map shows seed 
parcels), and scraper container able to ingest sample CSV and spider sample HTML. 
 
At least 3 sample end-to-end flows: 
 
1. CSV ingest → parcel stored with geom → show on map. 
 
 
2. Campaign creation → start → enqueued call task → create call_log (simulated). 
 
 
3. Generate contract PDF for parcel → saved to contracts table. 
 
 
 
Unit + integration tests pass in CI. 

 
README and runbook exist and are clear. 
 
 
For full product: 
 
Multi-country adapters for at least 2 different countries (example: US county tax portal + one 
other country). 
 
ML model trained with sample data and inference endpoint available. 
 
Asterisk preview-dialer PoC working with local test extension. 
 
Alerts and monitoring configured (Prometheus + Grafana + Sentry). 
 
 
 
--- 
 
15 — Coding standards, commit & PR rules (explicit) 
 
Use Python 3.11+ black formatting & ruff linting. 
 
Type hints mandatory, use mypy in CI. 
 
PR title: [area] short description (e.g. [scraper] add county auctions spider). 
 
Commit message: type(scope): short summary\n\nlonger description using conventional 
commits. 
 
Require tests coverage for new logic (unit/integration). 
 
 
 
--- 
 
16 — Delivery & artifacts packaging 
 
Agent must produce a zip: landflip-delivery-<date>.zip containing: 
 
docker-compose.yml, backend/, frontend/, scrapers/, ml/, docs/, runbooks/, ci/, architecture/. 
 
 
Also produce a single deliverable-checklist.json listing every artifact and pass/fail status. 
 
 
--- 
 

17 — Human-in-the-loop gates (safety) 
 
Explicitly require human approval before: 
 
Starting mass outreach campaigns (over configurable threshold, e.g., 100 messages/day). 
 
Paying or moving money / escrowing funds. 
 
Uploading or publishing owner PII outside encrypted DB. 
 
 
Add explicit UI step with human checkbox and digital signature before any of the above 
actions. 
 
 
--- 
 
18 — Error handling & retry policies 
 
Scrapers: exponential backoff for HTTP 429, rotate user-agent, log to events. 
 
Tasks: Celery tasks must be idempotent and have retry policy (max_retries=5, backoff). 
 
DB migrations: always run with backup & dry-run option. 
 
 
 
--- 
 
19 — Example minimal docker-compose.yml blueprint (agent should render exact file) 
 
version: '3.8' 
services: 
  db: 
    image: postgis/postgis:15-3.4 
    environment: 
      POSTGRES_DB: landflip 
      POSTGRES_PASSWORD: password 
      POSTGRES_USER: landflip 
    volumes: 
      - ./data/postgres:/var/lib/postgresql/data 
    ports: 
      - "5432:5432" 
 
  redis: 
    image: redis:7 
    ports: 
      - "6379:6379" 

 
  backend: 
    build: ./backend 
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 
    volumes: 
      - ./backend:/app 
    depends_on: 
      - db 
      - redis 
    environment: 
      DATABASE_URL: postgresql://landflip:password@db:5432/landflip 
      REDIS_URL: redis://redis:6379/0 
    ports: 
      - "8000:8000" 
 
  worker: 
    build: ./backend 
    command: celery -A backend.worker worker --loglevel=info 
    depends_on: 
      - backend 
      - redis 
      - db 
    environment: 
      DATABASE_URL: postgresql://landflip:password@db:5432/landflip 
      REDIS_URL: redis://redis:6379/0 
 
  frontend: 
    build: ./frontend 
    volumes: 
      - ./frontend:/app 
    ports: 
      - "3000:3000" 
    depends_on: 
      - backend 
 
  tileserver: 
    image: klokantech/tileserver-gl 
    volumes: 
      - ./tiles:/data 
    ports: 
      - "8080:80" 
 
(Agent must replace placeholder passwords with env management in docs and use .env for 
secret injection.) 
 
 
--- 
 

20 — Final instructions for the agent executor 
 
Work in small increments; commit each working module with meaningful commit messages. 
 
After each major milestone, produce a concise “milestone report” that includes: what was 
done, tests passing, and next steps. 
 
Where legal/operational constraints exist (WhatsApp, phone/SMS gateways, country-specific 
cadastre access), explicitly document them and provide at least one free fallback approach. 
 
Always produce reproducible commands to replicate results locally (e.g., docker-compose 
up --build, python backend/manage.py migrate, python ml/train.py --config example.yml). 
 
 
 
--- 
 
21 — Ready-to-run sub-prompts (copy-paste to spawn subagents) 
 
If you want to spawn specialized subagents, use these quick prompts: 
 
Spawn a Scraper Agent 
 
Spawn: ScraperAgent 
Goal: Implement a Scrapy spider to parse county auction pages and POST parsed JSON to 
backend at /api/v1/ingest. 
Input: URL(s) sample(s), HTML fixture(s) located in /mnt/data/scraper-fixtures/ 
Output: scrapy project in scrapers/county_XXX, unit tests, and evidence of a successful 
POST to the backend dev server. 
 
Spawn ML Agent 
 
Spawn: MLAgent 
Goal: Build feature pipelines, training scripts, and register model in MLflow. Provide 
inference endpoint. 
Input: seed CSV under data/ml/train_sample.csv and DB connection. 
Output: ml/train.py, ml/predict.py, mlflow artifacts with model id, evaluation report. 
 
 
--- 
 
22 — Wrap-up: how the agent will report progress to you 
 
After each commit: post milestone.json with tasks completed (list), tests passed (list), 
artifacts produced (paths), and blockers (if any). 
 

For blocking legal or operational decisions (e.g., authorizing WhatsApp Business), present 
the options, recommended choice, and require human approval via a documented ACK 
string. 
 
 
 
--- 
 
If you want, I’ll now: 
 
(A) produce one of the sub-prompts as an immediate runnable artifact (for example, the full 
docker-compose.yml + backend skeleton), or 
 
(B) produce a set of ready-to-run subagent prompts (ScraperAgent, DialerAgent, MLAgent, 
DevOpsAgent) already formatted for an agent orchestration system you use. 
 
 
 
