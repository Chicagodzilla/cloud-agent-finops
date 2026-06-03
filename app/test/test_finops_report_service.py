import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_DIR = ROOT / "app"
AGENT_DIR = ROOT / "agent"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
if str(AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(AGENT_DIR))

from service.finops_report_service import build_finops_report


def test_build_finops_report_returns_structured_payload(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")

    payload = build_finops_report(
        user_id="user_1001",
        billing_month="2026-05",
        target_instance_type="ecs.g8a.xlarge",
    )

    assert payload["status"] == "success"
    assert payload["data"]["type"] == "finops_report"
    assert payload["data"]["summary"]["estimated_monthly_savings"] == 820.0
    assert payload["data"]["recommendations"][0]["requires_approval"] is True
