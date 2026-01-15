# app/main.py
"""
WHY THIS FILE EXISTS (short version):
- This is the "front door" of the service.
- It wires together:
  1) API routes (JSON endpoints)
  2) Static dashboard serving (HTML/CSS/JS)
  3) Health endpoint (for AWS + monitoring + deploy validation)

WHAT THIS MAPS TO IN THE PROJECT:
- "Backend API" piece
- "Dashboard hosting" piece
- Later: ECS health checks + smoke tests will call /health
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router


def create_app() -> FastAPI:
    """
    WHY we use an app factory:
    - Makes testing easier (tests can create an app instance)
    - Makes deployment cleaner (prod/dev configs later)
    """
    app = FastAPI(title="Cloud-Native ML/Data Pipeline Demo", version="0.1.0")

    # ---- Dashboard (Static Files) ----
    # WHY: We want recruiters to click a URL and SEE something immediately.
    # Serving a one-page dashboard from the same service keeps deployment simple:
    # one container, one URL, one place to debug.
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

    # ---- API Routes ----
    # WHY: The dashboard will call these endpoints for live data.
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
