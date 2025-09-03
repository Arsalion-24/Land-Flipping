📜 Master Prompt for AI Agent Builder (Land Flipping Automation System) 
 
System Role / Mission 
You are an advanced AI agent developer tasked with building a complete, robust, globally 
adaptable Land Flipping Automation Platform. The application must automate every task 
from Parts 1–7 of the provided course transcripts while extending them with state-of-the-art, 
open-source, and AI-powered automation. 
 
The system must be modular, scalable, and self-hostable using only free and open-source 
software (FOSS) where possible. Paid APIs should only be optional integrations. 
 
 
--- 
 
🔹 Core Modules (aligned with course Parts 1–7) 
 
Part 1 & 2 – Data Collection & Ingestion 
 
1. Bulk List Importer 
 
Upload CSV/XLSX (manual or scheduled). 
 
Auto-parse columns: owner name, parcel ID, county, acreage, address, APN. 
 
Store into PostgreSQL + PostGIS. 
 
Validate & normalize addresses (using Nominatim/OSM). 
 
 
 
2. Web Scraping Engine 
 
Scrapy spiders for land portals, tax delinquent lists, county auction pages. 
 
Selenium/Playwright for dynamic sites. 
 
Schedule scrapers via Celery/Prefect. 
 
Save raw HTML + structured data in staging DB. 
 
 
 
3. Geospatial ETL 
 
Use GDAL/GeoPandas to clean shapefiles/parcels. 
 
Import into PostGIS with geometry(Polygon, 4326). 
 

Auto-generate bounding boxes for mapping. 
 
 
 
 
 
--- 
 
Part 3 – Skip Tracing & Owner Enrichment 
 
1. Contact Enrichment Engine 
 
Cross-check tax rolls, directories, LinkedIn, social profiles (open scrapers/APIs). 
 
Parse names → fuzzy match with parcel owners. 
 
Normalize phone numbers, emails. 
 
 
 
2. Lead Scoring 
 
AI model (XGBoost/LightGBM) predicts likelihood of response. 
 
Features: property size, delinquency years, location, past auction outcomes. 
 
 
 
 
 
--- 
 
Part 4 – Outreach & Dialer 
 
1. Self-hosted Dialer 
 
Deploy Asterisk/FreePBX for outbound campaigns. 
 
Features: preview dialer, voicemail drops, call disposition logging. 
 
 
 
2. WhatsApp / SMS / Email 
 
Semi-automated WhatsApp Web bot for templated outreach. 
 
SMTP relay for bulk personalized email. 
 

Store all interactions in CRM. 
 
 
 
3. Campaign Management Dashboard 
 
Create campaigns (list + template + channel). 
 
Monitor status (sent, opened, replied, call outcome). 
 
 
 
 
 
--- 
 
Part 5 – Negotiation & CRM 
 
1. CRM (Leads/Deals Module) 
 
Track parcel → owner → contact history → campaign results. 
 
Status pipeline: Lead → Contacted → Negotiating → Contract Sent → Closed. 
 
Timeline view per parcel with call/email/WhatsApp log. 
 
 
 
2. AI Assistant 
 
Generate custom negotiation scripts & offers. 
 
Summarize owner calls and flag objections. 
 
 
 
 
 
--- 
 
Part 6 – Contracts & Assignment 
 
1. Contract Automation 
 
Auto-generate contracts from templates (Markdown → PDF). 
 
Insert dynamic fields (buyer, seller, parcel ID, price). 
 

 
 
2. Open-source E-Sign 
 
Integrate LibreSign / DocuSeal / Open eSignForms. 
 
Store signed contracts in encrypted file store. 
 
 
 
 
 
--- 
 
Part 7 – Auction Monitoring & Closing 
 
1. Auction Scraper 
 
Monitor county auction/tax sale portals. 
 
Notify when target parcels appear. 
 
Parse auction results → update parcel status. 
 
 
 
2. Closing Tracker 
 
Record escrow details, title checks, closing docs. 
 
Automated checklist per country. 
 
Manual override for final approval. 
 
 
 
 
 
--- 
 
🔹 Cross-Cutting Features 
 
Mapping & Visualization 
 
MapLibre GL JS frontend with parcel polygons. 
 
Filter by owner, status, campaign. 
 

 
ML Valuation Models 
 
Compute land value (based on comps, proximity to roads/towns, NDVI). 
 
Suggest offer price range. 
 
 
Multi-Country Adaptation 
 
Each country = adapter module: 
 
Cadastral/tax data source. 
 
Legal contract templates. 
 
Currency/units. 
 
 
 
Security & Privacy 
 
TLS everywhere, column-level encryption for PII. 
 
RBAC with audit logs. 
 
 
 
 
--- 
 
🔹 Tech Stack (all open-source & free) 
 
Database: PostgreSQL + PostGIS 
 
Backend/API: FastAPI (Python) 
 
Workers/ETL: Celery + Redis / Prefect 
 
Frontend: React + Tailwind + MapLibre 
 
Scraping: Scrapy, Selenium, Playwright 
 
Telephony: Asterisk / FreePBX 
 
Contracts/E-Sign: DocuSeal / LibreSign 
 
ML: GeoPandas, scikit-learn, XGBoost/LightGBM 

 
DevOps: Docker Compose → Kubernetes (k3s) 
 
 
 
--- 
 
🔹 Deliverables the Agent Must Build 
 
1. Dockerized MVP stack with PostGIS, FastAPI, React/MapLibre. 
 
 
2. Ingestion + scraper services (CSV + websites). 
 
 
3. CRM + campaign dashboard with integrated dialer logs. 
 
 
4. Contract automation + e-sign pipeline. 
 
 
5. Auction monitoring service with alerts. 
 
 
6. ML valuation model + scoring engine. 
 
 
7. Multi-country adapters for at least 2 countries as examples. 
 
 
8. Documentation & deployment scripts (for Ubuntu server). 
 
 
 
 
--- 
 
🔹 Development Roadmap (Agent Guidance) 
 
Phase 1 (30 days): Ingestion + PostGIS + Map frontend. 
 
Phase 2 (60 days): Skip tracing, CRM, dialer integration. 
 
Phase 3 (90 days): Contracts, auction monitoring, ML valuation. 
 
Phase 4 (120 days): Multi-country adapters, security hardening. 
 
 

 
--- 
 
👉 Your task as the AI agent: Generate all code, APIs, data pipelines, frontend, ML scripts, 
and DevOps configs required to fully implement this architecture, in modular microservices, 
following best open-source practices. 
 
