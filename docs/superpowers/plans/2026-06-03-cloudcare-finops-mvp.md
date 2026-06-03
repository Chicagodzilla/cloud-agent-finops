# CloudCare FinOps MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first open-source friendly CloudCare FinOps MVP foundation with local mock data, stronger FinOps MCP tools, and a consolidated project document.

**Architecture:** Keep the existing FastAPI + LangGraph + MCP + Vue structure. Add a focused mock data provider under `agent/mcp_servers/`, route MCP tools through provider functions, and document the end-to-end strategy in `docs/research/`.

**Tech Stack:** Python 3.12, pytest, FastMCP, LangGraph, FastAPI, Vue 3, Element Plus.

---

### Task 1: Consolidated Project Document

**Files:**
- Create: `docs/research/2026-06-03-cloudcare-agent-master-doc.md`

- [x] **Step 1: Create master document**

Write a document that links the market research report, project direction report, evaluation roadmap, technical plan, and phased To do list.

- [x] **Step 2: Review for missing placeholders**

Scan the master document for placeholder markers and incomplete sections. Expected: no placeholder markers remain.

### Task 2: FinOps Mock Data Provider

**Files:**
- Create: `agent/mcp_servers/mock_data_provider.py`
- Test: `agent/test/test_finops_mock_provider.py`

- [ ] **Step 1: Write failing provider tests**

Test these behaviors:

- `query_user_orders("user_1001")` returns only `user_1001` orders.
- `query_user_instances("user_1001")` returns only `user_1001` resources.
- `analyze_instance_usage("i-bp1_user1001_ecs", "user_1001")` returns `RESOURCES_IDLE`.
- `estimate_savings("i-bp1_user1001_ecs", "ecs.g8a.xlarge", "user_1001")` returns a positive estimated monthly saving.

- [ ] **Step 2: Implement provider**

Add in-memory mock orders, instances, metrics, product prices, and helper functions.

- [ ] **Step 3: Verify tests pass**

Run:

```bash
./.venv/bin/python -m pytest agent/test/test_finops_mock_provider.py -v
```

Expected: all tests pass.

### Task 3: MCP Tool Enhancement

**Files:**
- Modify: `agent/mcp_servers/cloud_platform_server.py`
- Test: `agent/test/test_finops_mcp_tools.py`

- [ ] **Step 1: Write failing MCP tool tests**

Test JSON output for:

- `query_user_orders`
- `query_user_instances`
- `analyze_instance_usage`
- `query_monthly_bill_summary`
- `query_resource_cost_breakdown`
- `query_instance_metrics`
- `estimate_savings`

- [ ] **Step 2: Route tools through provider**

Use mock provider when `MOCK_DATA_MODE` is not set to `false`. Keep MySQL path available for later.

- [ ] **Step 3: Remove duplicate promotion tool registration**

Keep the product-id based `get_promotion_materials(product_id, user_id="")` and rename the older product-name helper.

- [ ] **Step 4: Verify tests pass**

Run:

```bash
MOCK_DATA_MODE=true ./.venv/bin/python -m pytest agent/test/test_finops_mcp_tools.py -v
```

Expected: all tests pass.

### Task 4: Agent Prompt and Config Update

**Files:**
- Modify: `agent/agents/finops_agent.py`
- Modify: `agent/.env.example`
- Modify: `agent/requirements.txt`

- [ ] **Step 1: Update FinOpsAgent tools**

Include `query_monthly_bill_summary`, `query_resource_cost_breakdown`, `query_instance_metrics`, and `estimate_savings`.

- [ ] **Step 2: Update prompt**

Require the agent to base savings estimates on `estimate_savings` and avoid invented numbers.

- [ ] **Step 3: Update config docs**

Add `MOCK_DATA_MODE=true` to `.env.example` and `pymysql` to requirements.

### Task 5: Verification

**Files:**
- Existing tests and import checks.

- [ ] **Step 1: Run unit tests**

```bash
MOCK_DATA_MODE=true ./.venv/bin/python -m pytest agent/test/test_finops_mock_provider.py agent/test/test_finops_mcp_tools.py -v
```

- [ ] **Step 2: Run import checks**

```bash
MOCK_DATA_MODE=true ./.venv/bin/python - <<'PY'
from mcp_servers.cloud_platform_server import query_monthly_bill_summary, estimate_savings
print(query_monthly_bill_summary("user_1001", "2026-05")[:80])
print(estimate_savings("i-bp1_user1001_ecs", "ecs.g8a.xlarge", "user_1001")[:80])
PY
```

Expected: both print JSON strings with `"status": "success"`.
