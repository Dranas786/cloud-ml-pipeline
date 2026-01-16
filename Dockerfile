# Dockerfile

# Packages the FastAPI backend and static dashboard into a Docker image.
# This image is what gets built in CI and deployed to AWS ECS Fargate.
# Keeping everything in one container simplifies deployment and rollback.

# WHY:
# - ECS Fargate runs Docker containers
# - This file defines how our FastAPI app is packaged and run

# ---- Base image ----
# Use official lightweight Python image
FROM python:3.11-slim

# ---- Environment settings ----
# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure logs are flushed immediately (important for AWS logs)
ENV PYTHONUNBUFFERED=1

# ---- Working directory ----
# All commands will run inside /app
WORKDIR /app
# NOTE:
# /app is the container working directory.
# app/ inside it is the Python application package.
# Same name, different layers.

# ---- Install dependencies ----
# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy application code ----
COPY app ./app
COPY static ./static

# ---- Expose port ----
# ECS and local Docker will use this
EXPOSE 8000

# ---- Start the application ----
# Use uvicorn as the ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Equivalent to: uvicorn app.main:app --host 0.0.0.0 --port 8000
#  0.0.0.0 instead of local host as local host breaks inside docker
