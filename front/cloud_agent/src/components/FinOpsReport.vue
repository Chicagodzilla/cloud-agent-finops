<template>
  <section class="finops-report">
    <div class="report-header">
      <div>
        <div class="eyebrow">FinOps Report</div>
        <h3>{{ report.summary.title }}</h3>
      </div>
      <div class="savings-card">
        <span>预计月节省</span>
        <strong>{{ money(report.summary.estimated_monthly_savings) }}</strong>
      </div>
    </div>

    <div class="summary-grid">
      <div class="metric">
        <span>账单月份</span>
        <strong>{{ report.summary.billing_month }}</strong>
      </div>
      <div class="metric">
        <span>本月账单</span>
        <strong>{{ money(report.summary.total_bill_amount) }}</strong>
      </div>
      <div class="metric">
        <span>优化状态</span>
        <strong>{{ statusText }}</strong>
      </div>
    </div>

    <div class="section-title">资源诊断</div>
    <div class="resource-table">
      <div class="resource-row resource-head">
        <span>资源</span>
        <span>规格</span>
        <span>CPU</span>
        <span>内存</span>
        <span>诊断</span>
      </div>
      <div v-for="resource in report.resources" :key="resource.instance_id" class="resource-row">
        <span>{{ resource.instance_id }}</span>
        <span>{{ resource.instance_type }}</span>
        <span>{{ resource.cpu_avg_7d }}%</span>
        <span>{{ resource.memory_avg_7d }}%</span>
        <span>{{ diagnosisText(resource.diagnosis) }}</span>
      </div>
    </div>

    <div class="section-title">优化建议</div>
    <div class="recommendation-list">
      <article v-for="item in report.recommendations" :key="item.resource_id" class="recommendation">
        <div class="recommendation-topline">
          <strong>{{ item.title }}</strong>
          <span>{{ money(item.estimated_monthly_savings) }}/月</span>
        </div>
        <p>{{ item.reason }}</p>
        <div class="risk">{{ item.risk }}</div>
      </article>
    </div>

    <div class="risk-list">
      <div v-for="risk in report.risks" :key="risk">{{ risk }}</div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { FinOpsReport } from '../types/finops'

const props = defineProps<{
  report: FinOpsReport
}>()

const statusText = computed(() => {
  return props.report.summary.overall_status === 'has_savings_opportunity' ? '发现优化空间' : '暂无明显优化空间'
})

const money = (value: number) => `¥${value.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`

const diagnosisText = (diagnosis: string) => {
  if (diagnosis === 'RESOURCES_IDLE') return '资源闲置'
  if (diagnosis === 'RESOURCES_TIGHT') return '资源紧张'
  return '资源正常'
}
</script>

<style scoped>
.finops-report {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #dbe7f5;
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 14px 32px rgba(15, 35, 95, 0.07);
}
.report-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
  margin-bottom: 18px;
}
.eyebrow {
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
  text-transform: uppercase;
}
.report-header h3 {
  margin: 4px 0 0;
  color: #0f172a;
  font-size: 20px;
}
.savings-card {
  min-width: 150px;
  padding: 12px 14px;
  border-radius: 10px;
  background: #ecfdf5;
  border: 1px solid #bbf7d0;
  color: #166534;
}
.savings-card span,
.metric span {
  display: block;
  font-size: 12px;
  color: #64748b;
}
.savings-card strong {
  display: block;
  margin-top: 4px;
  font-size: 22px;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}
.metric {
  padding: 12px;
  border-radius: 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}
.metric strong {
  display: block;
  margin-top: 6px;
  color: #1e293b;
}
.section-title {
  margin: 18px 0 10px;
  color: #334155;
  font-weight: 700;
}
.resource-table {
  overflow: hidden;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
}
.resource-row {
  display: grid;
  grid-template-columns: 1.6fr 1.3fr 0.7fr 0.7fr 0.9fr;
  gap: 10px;
  padding: 10px 12px;
  color: #334155;
  font-size: 13px;
  border-top: 1px solid #e2e8f0;
}
.resource-row:first-child {
  border-top: 0;
}
.resource-head {
  background: #f8fafc;
  color: #64748b;
  font-weight: 700;
}
.recommendation-list {
  display: grid;
  gap: 10px;
}
.recommendation {
  padding: 14px;
  border-radius: 10px;
  border: 1px solid #bfdbfe;
  background: #eff6ff;
}
.recommendation-topline {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: #1e3a8a;
}
.recommendation p {
  margin: 8px 0;
  color: #334155;
}
.risk {
  font-size: 13px;
  color: #92400e;
}
.risk-list {
  display: grid;
  gap: 6px;
  margin-top: 16px;
  color: #64748b;
  font-size: 13px;
}
</style>

