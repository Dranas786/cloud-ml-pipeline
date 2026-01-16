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
    # Attach API routes to the app under the /api prefix.
    # Routers group related endpoints; the prefix defines where they live in the URL space.
    # This keeps API paths separate from the dashboard (/), docs (/docs), and static assets.

    return app


app = create_app()

"""
SUB-APPLICATION SUMMARY:

FastAPI supports composing multiple ASGI applications together.
A sub-application is mounted at a path prefix and fully owns that URL space.

Why we mount StaticFiles instead of using routes:
- Static files are not API business logic.
- StaticFiles is an optimized ASGI app (correct headers, MIME types, security).
- Avoids dangerous catch-all routes like "/{path:path}".
- Keeps app wiring (composition) in main.py and endpoint logic in routes.py.

Common real-world sub-app uses (not just static HTML):
- /ui        → frontend app (React/Vite build)
- /admin     → internal admin dashboard
- /metrics   → Prometheus / monitoring ASGI app
- /auth      → authentication providers
- /v1, /v2   → versioned APIs

Design rule:
Routes answer questions.
Sub-apps own territory.
"""
