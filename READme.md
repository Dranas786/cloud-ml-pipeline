Pipeline practise project

Tech-Stack (ECS Fargate + FastAPI + a 1-page HTML dashboard + GitHub Actions CI/CD):
Fast API

LinksL
/ → one-page dashboard
/docs → interactive API docs (Swagger UI)
/health → health/version check
/api/... → endpoints that power the dashboard

The service runs as a Docker container, deployed to AWS ECS Fargate, and updates automatically via GitHub Actions.
