from .celery_app import celery_app
import time
import requests
from bs4 import BeautifulSoup

@celery_app.task
def scheduled_ingest(source: str):
    time.sleep(1)
    return {"status": "ok", "source": source}

@celery_app.task
def run_scraper(url: str):
    r = requests.get(url, timeout=20, headers={"User-Agent": "landflip/1.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    return {"length": len(soup.get_text())}

@celery_app.task
def geocode_address(address: str):
    # placeholder; use utils endpoint on demand
    return {"address": address}
