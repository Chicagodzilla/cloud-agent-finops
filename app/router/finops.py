from fastapi import APIRouter

from schemas.finops import FinOpsReportRequest
from service.finops_report_service import build_finops_report


router = APIRouter()


@router.post("/finops/report")
async def finops_report_endpoint(request: FinOpsReportRequest):
    return build_finops_report(
        user_id=request.user_id,
        billing_month=request.billing_month,
        target_instance_type=request.target_instance_type,
    )

