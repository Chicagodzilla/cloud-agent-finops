import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[2]
APP_DIR = ROOT / "app"
AGENT_DIR = ROOT / "agent"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
if str(AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(AGENT_DIR))

from router import finops


def test_finops_report_endpoint_returns_report(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")
    app = FastAPI()
    app.include_router(finops.router, prefix="/api")
    client = TestClient(app)

    response = client.post(
        "/api/finops/report",
        json={
            "user_id": "user_1001",
            "billing_month": "2026-05",
            "target_instance_type": "ecs.g8a.xlarge",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["data"]["type"] == "finops_report"
    assert payload["data"]["summary"]["estimated_monthly_savings"] == 820.0

