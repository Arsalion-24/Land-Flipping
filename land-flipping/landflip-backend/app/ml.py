from __future__ import annotations
import os
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

MODEL_PATH = os.getenv("MODEL_PATH", "/app/model.pkl")


def heuristic_score(acreage: float | None, county: str | None, delinquency_years: float | None = None) -> int:
    score = 50
    if acreage:
        if acreage >= 40:
            score += 20
        elif acreage >= 10:
            score += 10
        else:
            score += 5
    if county:
        score += 5
    if delinquency_years:
        score += min(int(delinquency_years * 3), 15)
    return max(0, min(100, score))


def features_from_parcel(parcel) -> np.ndarray:
    acreage = float(parcel.acreage) if parcel.acreage is not None else 0.0
    county_hash = (hash(parcel.county or "") % 1000) / 1000.0
    state_hash = (hash(parcel.state or "") % 1000) / 1000.0
    return np.array([acreage, county_hash, state_hash], dtype=float)


def train_model(parcels) -> str:
    X = []
    y = []
    for p in parcels:
        X.append(features_from_parcel(p))
        # pseudo-label valuation as acreage * constant if no valuation
        target = float(p.valuation) if p.valuation is not None else (float(p.acreage or 0) * 2500.0)
        y.append(target)
    if not X:
        raise ValueError("No data to train")
    X = np.vstack(X)
    y = np.array(y)
    model = GradientBoostingRegressor(random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return MODEL_PATH


def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def estimate_value(parcel) -> float:
    model = load_model()
    if not model:
        return float(parcel.acreage or 0) * 2500.0
    x = features_from_parcel(parcel).reshape(1, -1)
    pred = float(model.predict(x)[0])
    return pred
