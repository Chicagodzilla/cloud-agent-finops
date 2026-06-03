# CloudCare Agent

Open-source multi-agent cloud support and FinOps assistant built with FastAPI, Vue, LangGraph, MCP tools, and RAG.

CloudCare Agent helps users ask cloud product questions, query mock billing and resources, analyze utilization, and generate cost optimization suggestions. It is designed as a practical foundation for agentic customer support, cloud operations assistance, and AI-powered service workflow demos.

## Highlights

- Multi-agent orchestration with LangGraph.
- FastAPI backend with SSE streaming responses.
- Vue 3 + Element Plus chat workspace.
- MCP tools for cloud orders, resources, monitoring, promotion, and FinOps analysis.
- Local mock cloud data for open-source demos.
- RAG and knowledge-graph oriented product support modules.
- Research, roadmap, and technical planning documents included.

## Project Structure

```text
agent/                 Multi-agent system, MCP tools, memory, RAG helpers
app/                   FastAPI application and chat streaming API
front/cloud_agent/     Vue 3 frontend workspace
mock_data/             Cloud product and support knowledge mock documents
docs/research/         Market research, direction analysis, technical roadmap
scripts/               Local development startup scripts
```

## Quick Start

### 1. Backend environment

```bash
cp agent/.env.example agent/.env
```

For local demos, keep:

```bash
MOCK_DATA_MODE=true
```

Set `DASHSCOPE_API_KEY` when you want to run real LLM calls.

### 2. Python dependencies

```bash
uv venv .venv --python 3.12
uv pip install -r agent/requirements.txt fastapi uvicorn langchain-openai langchain-milvus langchain-neo4j python-multipart
```

### 3. Frontend dependencies

```bash
cd front/cloud_agent
npm install
cd ../..
```

### 4. Run services

```bash
./scripts/dev_backend.sh
./scripts/dev_frontend.sh
```

Or run both:

```bash
./scripts/dev_all.sh
```

Default URLs:

- Frontend: http://127.0.0.1:5174
- Backend docs: http://127.0.0.1:5001/docs

## FinOps Mock Demo Tools

The MCP cloud platform server supports local mock mode by default:

- `query_user_orders`
- `query_user_instances`
- `query_monthly_bill_summary`
- `query_resource_cost_breakdown`
- `query_instance_metrics`
- `analyze_instance_usage`
- `estimate_savings`
- `generate_finops_report`

Example:

```bash
cd agent
MOCK_DATA_MODE=true ../.venv/bin/python - <<'PY'
from mcp_servers.cloud_platform_server import generate_finops_report
print(generate_finops_report("user_1001", "2026-05")[:500])
PY
```

## Tests

```bash
MOCK_DATA_MODE=true ./.venv/bin/python -m pytest \
  agent/test/test_finops_mock_provider.py \
  agent/test/test_finops_mcp_tools.py \
  -v
```

## Documentation

- [Master document](docs/research/2026-06-03-cloudcare-agent-master-doc.md)
- [Market research report](docs/research/2026-06-02-intelligent-customer-service-agent-market-research.md)
- [Project opportunity directions](docs/research/2026-06-02-project-opportunity-directions.md)
- [Evaluation and roadmap](docs/research/2026-06-02-direction-evaluation-and-roadmap.md)
- [Technical plan and backlog](docs/research/2026-06-03-finops-technical-plan-and-backlog.md)

## Roadmap

- Structured FinOps report rendering in the frontend.
- Trace and AgentOps replay for routing and tool calls.
- Golden set evaluation for support and FinOps scenarios.
- Real cloud provider billing/resource API integrations.
- Knowledge-base gap discovery and support operations copilot.

## Security Notes

- Do not commit `agent/.env`.
- Use `agent/.env.example` for configuration templates.
- Mock mode is enabled by default for open-source demos.
- Any real cloud resource changes should require explicit human approval.

