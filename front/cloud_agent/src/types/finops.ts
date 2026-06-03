export interface FinOpsReportSummary {
  title: string
  overall_status: string
  billing_month: string
  total_bill_amount: number
  estimated_monthly_savings: number
  currency: string
}

export interface FinOpsResource {
  instance_id: string
  instance_type: string
  status: string
  region_id: string
  cpu_avg_7d: number
  memory_avg_7d: number
  network_peak_mbps: number
  current_month_cost: number
  diagnosis: string
}

export interface FinOpsRecommendation {
  resource_id: string
  action: string
  priority: string
  title: string
  reason: string
  risk: string
  estimated_monthly_savings: number
  currency: string
  requires_approval: boolean
}

export interface FinOpsReport {
  type: 'finops_report'
  summary: FinOpsReportSummary
  resources: FinOpsResource[]
  recommendations: FinOpsRecommendation[]
  risks: string[]
  sources: Array<{ type: string; name: string }>
}

export interface FinOpsReportResponse {
  status: string
  data: FinOpsReport
  source?: string
}

