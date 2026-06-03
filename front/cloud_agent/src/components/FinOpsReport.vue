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
  border: 1px solid rgba(125, 211, 252, 0.48);
  border-radius: 8px;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.92), rgba(239, 249, 255, 0.78));
  box-shadow: 0 18px 42px rgba(37, 99, 235, 0.1);
  backdrop-filter: blur(16px);
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
  color: #0284c7;
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
  border-radius: 8px;
  background:
    linear-gradient(135deg, rgba(240, 253, 250, 0.96), rgba(224, 242, 254, 0.86));
  border: 1px solid rgba(45, 212, 191, 0.46);
  color: #0f766e;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.78);
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
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(191, 219, 254, 0.52);
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
  overflow-x: auto;
  border: 1px solid rgba(191, 219, 254, 0.56);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.62);
}
.resource-row {
  display: grid;
  grid-template-columns: 1.6fr 1.3fr 0.7fr 0.7fr 0.9fr;
  gap: 10px;
  min-width: 640px;
  padding: 10px 12px;
  color: #334155;
  font-size: 13px;
  border-top: 1px solid rgba(191, 219, 254, 0.42);
}
.resource-row:first-child {
  border-top: 0;
}
.resource-head {
  background: rgba(239, 246, 255, 0.76);
  color: #475569;
  font-weight: 700;
}
.recommendation-list {
  display: grid;
  gap: 10px;
}
.recommendation {
  padding: 14px;
  border-radius: 8px;
  border: 1px solid rgba(125, 211, 252, 0.54);
  background:
    linear-gradient(135deg, rgba(239, 246, 255, 0.9), rgba(236, 254, 255, 0.74));
}
.recommendation-topline {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  color: #075985;
}
.recommendation p {
  margin: 8px 0;
  color: #334155;
}
.risk {
  font-size: 13px;
  color: #b45309;
}
.risk-list {
  display: grid;
  gap: 6px;
  margin-top: 16px;
  color: #64748b;
  font-size: 13px;
}
</style>
