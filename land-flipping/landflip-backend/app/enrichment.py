import re
import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

PHONE_RE = re.compile(r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def normalize_phone(p: str | None) -> str | None:
    if not p:
        return None
    digits = re.sub(r"\D", "", p)
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    return p


def simple_web_lookup(name: str, county: str | None = None, state: str | None = None) -> dict:
    query = f"{name} {county or ''} {state or ''} phone email"
    try:
        r = requests.get("https://html.duckduckgo.com/html/", params={"q": query}, timeout=20, headers={"User-Agent": "landflip/1.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True)
        phones = PHONE_RE.findall(text)
        emails = EMAIL_RE.findall(text)
        phone = normalize_phone(phones[0]) if phones else None
        email = emails[0] if emails else None
        return {"phone": phone, "email": email, "raw_hits": len(phones) + len(emails)}
    except Exception:
        return {"phone": None, "email": None, "raw_hits": 0}


def fuzzy_match(target: str, candidate: str) -> int:
    return int(fuzz.token_set_ratio(target, candidate))
