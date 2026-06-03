import sys
from pathlib import Path
from typing import Any


AGENT_DIR = Path(__file__).resolve().parents[2] / "agent"
if str(AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(AGENT_DIR))

from mcp_servers import mock_data_provider


def build_finops_report(
    user_id: str,
    billing_month: str = "2026-05",
    target_instance_type: str = "ecs.g8a.xlarge",
) -> dict[str, Any]:
    return mock_data_provider.generate_finops_report(
        user_id=user_id,
        billing_month=billing_month,
        target_instance_type=target_instance_type,
    )

