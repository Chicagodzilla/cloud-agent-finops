from mcp_servers import mock_data_provider as provider


def test_query_user_orders_returns_only_current_user_orders():
    result = provider.query_user_orders("user_1001", limit=10)

    assert result["status"] == "success"
    assert len(result["data"]) >= 3
    assert {row["user_id"] for row in result["data"]} == {"user_1001"}


def test_query_user_instances_returns_only_current_user_resources():
    result = provider.query_user_instances("user_1001", limit=10)

    assert result["status"] == "success"
    assert len(result["data"]) >= 2
    assert {row["user_id"] for row in result["data"]} == {"user_1001"}


def test_analyze_instance_usage_identifies_idle_resources():
    result = provider.analyze_instance_usage("i-bp1_user1001_ecs", "user_1001")

    assert result["status"] == "success"
    assert result["data"]["diagnosis"] == "RESOURCES_IDLE"
    assert result["data"]["metrics_7d_avg"]["cpu_usage_percent"] < 10
    assert result["data"]["metrics_7d_avg"]["memory_usage_percent"] < 30


def test_estimate_savings_returns_positive_savings_for_downsize():
    result = provider.estimate_savings(
        instance_id="i-bp1_user1001_ecs",
        target_instance_type="ecs.g8a.xlarge",
        user_id="user_1001",
    )

    assert result["status"] == "success"
    assert result["data"]["current_instance_type"] == "ecs.g8a.4xlarge"
    assert result["data"]["target_instance_type"] == "ecs.g8a.xlarge"
    assert result["data"]["estimated_monthly_savings"] > 0
    assert result["data"]["requires_approval"] is True

