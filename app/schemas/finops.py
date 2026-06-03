from pydantic import BaseModel


class FinOpsReportRequest(BaseModel):
    user_id: str = "芝加哥斯拉"
    billing_month: str = "2026-05"
    target_instance_type: str = "ecs.g8a.xlarge"
