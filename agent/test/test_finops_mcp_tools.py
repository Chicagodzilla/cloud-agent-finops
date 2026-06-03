import json

from mcp_servers.cloud_platform_server import (
    analyze_instance_usage,
    estimate_savings,
    generate_finops_report,
    query_instance_metrics,
    query_monthly_bill_summary,
    query_resource_cost_breakdown,
    query_user_instances,
    query_user_orders,
)


def parse(payload: str) -> dict:
    return json.loads(payload)


def test_mcp_query_user_orders_uses_mock_data(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")

    result = parse(query_user_orders(user_id="user_1001", limit=10))

    assert result["status"] == "success"
    assert result["source"] == "mock_data_provider.orders"
    assert {row["user_id"] for row in result["data"]} == {"user_1001"}


def test_mcp_query_user_instances_uses_mock_data(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")

    result = parse(query_user_instances(user_id="user_1001", limit=10))

    assert result["status"] == "success"
    assert result["source"] == "mock_data_provider.instances"
    assert "i-bp1_user1001_ecs" in {row["instance_id"] for row in result["data"]}


def test_mcp_analyze_instance_usage_returns_idle_diagnosis(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")

    result = parse(analyze_instance_usage("i-bp1_user1001_ecs", user_id="user_1001"))

    assert result["status"] == "success"
    assert result["data"]["diagnosis"] == "RESOURCES_IDLE"


def test_mcp_query_monthly_bill_summary_returns_breakdown(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")

    result = parse(query_monthly_bill_summary(user_id="user_1001", billing_month="2026-05"))

    assert result["status"] == "success"
    assert result["data"]["total_amount"] == 16950.5
    assert {"product_type": "ECS", "amount": 12500.0} in result["data"]["breakdown"]


def test_mcp_query_resource_cost_breakdown_returns_resource_items(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")

    result = parse(
        query_resource_cost_breakdown(
            resource_id="i-bp1_user1001_ecs",
            user_id="user_1001",
            billing_month="2026-05",
        )
    )

    assert result["status"] == "success"
    assert result["data"]["resource_id"] == "i-bp1_user1001_ecs"
    assert result["data"]["total_amount"] == 12500.0


def test_mcp_query_instance_metrics_returns_daily_rows(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")

    result = parse(query_instance_metrics("i-bp1_user1001_ecs", user_id="user_1001", days=7))

    assert result["status"] == "success"
    assert len(result["data"]) == 7
    assert result["data"][0]["instance_id"] == "i-bp1_user1001_ecs"


def test_mcp_estimate_savings_returns_approval_required(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")

    result = parse(
        estimate_savings(
            instance_id="i-bp1_user1001_ecs",
            target_instance_type="ecs.g8a.xlarge",
            user_id="user_1001",
        )
    )

    assert result["status"] == "success"
    assert result["data"]["estimated_monthly_savings"] == 820.0
    assert result["data"]["requires_approval"] is True


def test_mcp_generate_finops_report_returns_structured_payload(monkeypatch):
    monkeypatch.setenv("MOCK_DATA_MODE", "true")

    result = parse(
        generate_finops_report(
            user_id="user_1001",
            billing_month="2026-05",
            target_instance_type="ecs.g8a.xlarge",
        )
    )

    assert result["status"] == "success"
    assert result["data"]["type"] == "finops_report"
    assert result["data"]["summary"]["estimated_monthly_savings"] == 820.0
    assert result["data"]["recommendations"][0]["action"] == "downsize"
