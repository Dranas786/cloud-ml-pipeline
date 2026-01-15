# app/api/routes.py
"""
WHY THIS FILE EXISTS (short version):
- Keeps endpoints organized and separate from app startup.
- Makes it easy to scale: add /api/train, /api/ingest, etc. later.

PROJECT MAPPING:
- "API layer" (backend)
- Later we’ll connect this to ingestion/transform/model pipeline code.
"""

from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    """
    WHY:
    - AWS ECS needs a simple endpoint to check if the container is healthy.
    - Our CI/CD can smoke-test this after deploy.
    """
    return {"status": "ok", "time_utc": datetime.now(timezone.utc).isoformat()}


@router.get("/summary")
def summary():
    """
    WHY:
    - The dashboard needs a simple endpoint to show "pipeline status".
    - For now we return placeholder values.
    - Later this will come from the DB / last pipeline run record.
    """
    return {
        "pipeline_status": "OK",
        "last_run_utc": datetime.now(timezone.utc).isoformat(),
        "rows_ingested": 1200,
        "rows_validated": 1189,
        "rows_failed": 11,
        "model_version": "v0.1.0",
    }


@router.get("/metrics")
def metrics():
    """
    WHY:
    - Dashboard needs something concrete to visualize.
    - Later we’ll compute real metrics (accuracy/RMSE) from training.
    """
    return {
        "metric_name": "rmse",
        "metric_value": 0.84,
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/predictions")
def predictions(limit: int = 20):
    """
    WHY:
    - Dashboard table/chart needs sample rows.
    - Later this will come from real inference output stored in DB.
    """
    limit = max(1, min(limit, 100))
    data = []
    for i in range(limit):
        data.append(
            {
                "id": i + 1,
                "feature_x": i * 0.5,
                "prediction": 10 + i * 0.3,
                "actual": 10 + i * 0.28,
            }
        )
    return {"items": data}
