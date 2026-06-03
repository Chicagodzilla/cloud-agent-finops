from pydantic import BaseModel


class FinOpsReportRequest(BaseModel):
    user_id: str = "user_1001"
    billing_month: str = "2026-05"
    target_instance_type: str = "ecs.g8a.xlarge"

