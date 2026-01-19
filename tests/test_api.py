"""
WHY THIS FILE EXISTS:
- Verifies that our API endpoints respond correctly.
- Acts as a regression safety net in CI.
- If an endpoint breaks, the PR is blocked.

PROJECT MAPPING:
- CI → Testing layer
- This is NOT transformation, NOT deployment, NOT AWS.
"""
from fastapi.testclient import TestClient
# import a test HTTP client to call endpoints (no docker, no ports)

from app.main import create_app
# import the app factory to test (fresh app instance for tests)

client = TestClient(create_app())

"""
WHAT THIS TEST CHECKS:
- /api/health returns HTTP 200
- response contains expected keys

WHY:
- Used by ECS health checks and CI smoke tests later
"""
# pytest automatically finds functions that start with test_. This is how pytest knows to run it
def test_health_endpoint():
    response = client.get("/api/health") # call the route and returns an HTTP response object
    assert response.status_code == 200 # checks if route is reachable or fails

    # checks if response json is valid
    data = response.json()
    assert data["status"] == "ok"
    assert "time_utc" in data

# testing the structure, not the numbers
def test_summary_endpoint_shape():
    response = client.get("/api/summary")
    assert response.status_code == 200

    # contract testing (check if the required fields are present)
    data = response.json()
    assert "pipeline_status" in data
    assert "last_run_utc" in data
    assert "rows_ingested" in data
    assert "rows_validated" in data
    assert "rows_failed" in data
    assert "model_version" in data


def test_predictions_limit_param():
    # checks if endpoint is valid
    response = client.get("/api/predictions?limit=5")

    # checks if the result is as expected
    # check 1 -> get as many items as we ask
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 5

    # check 2 -> checks for required fields
    first_item = data["items"][0]
    assert "id" in first_item
    assert "feature_x" in first_item
    assert "prediction" in first_item
    assert "actual" in first_item

# These tests validate API contracts and act as a CI safety net, preventing breaking changes from reaching production.





 
