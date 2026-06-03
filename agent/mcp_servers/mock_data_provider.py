"""Local mock cloud-platform data for FinOps demos.

The MCP server uses this provider when external MySQL is not configured. Keep
the shape close to the SQL-backed tools so agents can switch data sources
without changing prompts.
"""

from __future__ import annotations

from datetime import date, timedelta
from statistics import mean
from typing import Any


ORDERS: list[dict[str, Any]] = [
    {
        "order_id": "ORD-1001-001",
        "user_id": "user_1001",
        "resource_id": "i-bp1_user1001_ecs",
        "product_type": "ECS",
        "product_name": "ecs.g8a.4xlarge",
        "billing_mode": "包年包月",
        "amount": 12500.0,
        "billing_month": "2026-05",
        "status": "Paid",
        "created_at": "2026-05-01 10:00:00",
    },
    {
        "order_id": "ORD-1001-002",
        "user_id": "user_1001",
        "resource_id": "rm-bp1_user1001_rds",
        "product_type": "RDS",
        "product_name": "rds.mysql.c1.large",
        "billing_mode": "包年包月",
        "amount": 3600.0,
        "billing_month": "2026-05",
        "status": "Paid",
        "created_at": "2026-05-05 14:30:00",
    },
    {
        "order_id": "ORD-1001-003",
        "user_id": "user_1001",
        "resource_id": "bandwidth-1001-shared",
        "product_type": "Bandwidth",
        "product_name": "共享带宽 100Mbps",
        "billing_mode": "按量付费",
        "amount": 850.5,
        "billing_month": "2026-05",
        "status": "Paid",
        "created_at": "2026-05-18 08:15:00",
    },
    {
        "order_id": "ORD-1002-001",
        "user_id": "user_1002",
        "resource_id": "i-bp1_user1002_ecs",
        "product_type": "ECS",
        "product_name": "ecs.c7.large",
        "billing_mode": "按量付费",
        "amount": 245.2,
        "billing_month": "2026-05",
        "status": "Paid",
        "created_at": "2026-05-15 09:00:00",
    },
]

INSTANCES: list[dict[str, Any]] = [
    {
        "instance_id": "i-bp1_user1001_ecs",
        "user_id": "user_1001",
        "order_id": "ORD-1001-001",
        "instance_type": "ecs.g8a.4xlarge",
        "region_id": "cn-beijing",
        "zone_id": "cn-beijing-k",
        "status": "Running",
        "public_ip": "47.100.1.1",
    },
    {
        "instance_id": "rm-bp1_user1001_rds",
        "user_id": "user_1001",
        "order_id": "ORD-1001-002",
        "instance_type": "rds.mysql.c1.large",
        "region_id": "cn-beijing",
        "zone_id": "cn-beijing-l",
        "status": "Running",
        "public_ip": None,
    },
    {
        "instance_id": "i-bp1_user1002_ecs",
        "user_id": "user_1002",
        "order_id": "ORD-1002-001",
        "instance_type": "ecs.c7.large",
        "region_id": "cn-hangzhou",
        "zone_id": "cn-hangzhou-h",
        "status": "Stopped",
        "public_ip": "114.55.2.2",
    },
]

INSTANCE_MONTHLY_PRICE: dict[str, float] = {
    "ecs.g8a.4xlarge": 1250.0,
    "ecs.g8a.xlarge": 430.0,
    "ecs.c7.large": 245.2,
    "rds.mysql.c1.large": 360.0,
}


def _metric_rows() -> list[dict[str, Any]]:
    today = date.today()
    idle = [
        (2.1, 18.5, 1.2),
        (2.5, 19.1, 1.6),
        (3.2, 20.4, 2.0),
        (1.9, 17.9, 1.0),
        (2.8, 18.2, 1.4),
        (2.4, 19.0, 1.3),
        (2.0, 18.7, 1.1),
    ]
    normal = [
        (36.5, 62.1, 42.0),
        (41.2, 65.0, 51.0),
        (38.4, 63.5, 48.0),
        (44.0, 67.3, 55.0),
        (39.1, 60.8, 47.0),
        (42.8, 64.2, 53.0),
        (40.3, 61.9, 49.0),
    ]
    rows: list[dict[str, Any]] = []
    for index, values in enumerate(idle):
        rows.append(_metric_row("i-bp1_user1001_ecs", "user_1001", today, index, values))
    for index, values in enumerate(normal):
        rows.append(_metric_row("i-bp1_user1002_ecs", "user_1002", today, index, values))
    return rows


def _metric_row(
    instance_id: str,
    user_id: str,
    today: date,
    index: int,
    values: tuple[float, float, float],
) -> dict[str, Any]:
    cpu, memory, bandwidth = values
    return {
        "instance_id": instance_id,
        "user_id": user_id,
        "metric_date": (today - timedelta(days=6 - index)).isoformat(),
        "avg_cpu_usage_percent": cpu,
        "avg_memory_usage_percent": memory,
        "max_network_out_mbps": bandwidth,
    }


METRICS: list[dict[str, Any]] = _metric_rows()


def query_user_orders(user_id: str, limit: int = 5) -> dict[str, Any]:
    rows = [row for row in ORDERS if row["user_id"] == user_id]
    rows = sorted(rows, key=lambda row: row["created_at"], reverse=True)[:limit]
    if not rows:
        return {"status": "success", "message": "该用户目前没有任何订单记录。", "data": []}
    return {"status": "success", "data": rows, "source": "mock_data_provider.orders"}


def query_user_instances(user_id: str, limit: int = 5) -> dict[str, Any]:
    rows = [row for row in INSTANCES if row["user_id"] == user_id]
    rows = sorted(rows, key=lambda row: row["instance_id"], reverse=True)[:limit]
    if not rows:
        return {"status": "success", "message": "未查询到您的服务器实例数据。", "data": []}
    return {"status": "success", "data": rows, "source": "mock_data_provider.instances"}


def query_monthly_bill_summary(user_id: str, billing_month: str = "2026-05") -> dict[str, Any]:
    rows = [
        row
        for row in ORDERS
        if row["user_id"] == user_id and row["billing_month"] == billing_month
    ]
    product_totals: dict[str, float] = {}
    for row in rows:
        product_totals[row["product_type"]] = product_totals.get(row["product_type"], 0.0) + row["amount"]
    breakdown = [
        {"product_type": product_type, "amount": round(amount, 2)}
        for product_type, amount in sorted(product_totals.items())
    ]
    return {
        "status": "success",
        "data": {
            "billing_month": billing_month,
            "total_amount": round(sum(row["amount"] for row in rows), 2),
            "currency": "CNY",
            "breakdown": breakdown,
            "order_count": len(rows),
        },
        "source": "mock_data_provider.orders",
    }


def query_resource_cost_breakdown(
    resource_id: str,
    user_id: str,
    billing_month: str = "2026-05",
) -> dict[str, Any]:
    rows = [
        row
        for row in ORDERS
        if row["user_id"] == user_id
        and row["resource_id"] == resource_id
        and row["billing_month"] == billing_month
    ]
    if not rows:
        return {
            "status": "not_found",
            "message": "未查询到该资源在指定月份的费用数据。",
            "data": None,
        }
    total = round(sum(row["amount"] for row in rows), 2)
    return {
        "status": "success",
        "data": {
            "resource_id": resource_id,
            "billing_month": billing_month,
            "total_amount": total,
            "currency": "CNY",
            "items": rows,
        },
        "source": "mock_data_provider.orders",
    }


def query_instance_metrics(instance_id: str, user_id: str, days: int = 7) -> dict[str, Any]:
    if not _owns_instance(instance_id, user_id):
        return {
            "status": "error",
            "message": "未找到该实例，或您无权查看该实例监控数据。",
            "data": [],
        }
    rows = [
        row
        for row in METRICS
        if row["instance_id"] == instance_id and row["user_id"] == user_id
    ][-days:]
    if not rows:
        return {"status": "not_found", "message": "未查询到该实例监控数据。", "data": []}
    return {"status": "success", "data": rows, "source": "mock_data_provider.metrics"}


def analyze_instance_usage(instance_id: str, user_id: str) -> dict[str, Any]:
    metrics = query_instance_metrics(instance_id, user_id)
    if metrics["status"] != "success":
        return metrics
    rows = metrics["data"]
    cpu = round(mean(row["avg_cpu_usage_percent"] for row in rows), 2)
    memory = round(mean(row["avg_memory_usage_percent"] for row in rows), 2)
    bandwidth = round(max(row["max_network_out_mbps"] for row in rows), 2)
    if cpu < 10 and memory < 30:
        diagnosis = "RESOURCES_IDLE"
    elif cpu > 70 or memory > 80:
        diagnosis = "RESOURCES_TIGHT"
    else:
        diagnosis = "RESOURCES_NORMAL"
    return {
        "status": "success",
        "data": {
            "instance_id": instance_id,
            "owner_id": user_id,
            "metrics_7d_avg": {
                "cpu_usage_percent": cpu,
                "memory_usage_percent": memory,
                "network_out_bandwidth_mbps": bandwidth,
            },
            "diagnosis": diagnosis,
        },
        "source": "mock_data_provider.metrics",
    }


def estimate_savings(
    instance_id: str,
    target_instance_type: str,
    user_id: str,
) -> dict[str, Any]:
    instance = _find_owned_instance(instance_id, user_id)
    if not instance:
        return {
            "status": "error",
            "message": "未找到该实例，或您无权查看该实例费用数据。",
            "data": None,
        }
    current_type = instance["instance_type"]
    current_price = INSTANCE_MONTHLY_PRICE.get(current_type)
    target_price = INSTANCE_MONTHLY_PRICE.get(target_instance_type)
    if current_price is None or target_price is None:
        return {
            "status": "not_found",
            "message": "缺少当前规格或目标规格的价格数据，暂无法估算节省金额。",
            "data": None,
        }
    monthly_savings = max(current_price - target_price, 0.0)
    return {
        "status": "success",
        "data": {
            "instance_id": instance_id,
            "current_instance_type": current_type,
            "target_instance_type": target_instance_type,
            "current_monthly_price": current_price,
            "target_monthly_price": target_price,
            "estimated_monthly_savings": round(monthly_savings, 2),
            "currency": "CNY",
            "requires_approval": True,
            "assumption": "基于 mock 月度规格价格估算，真实费用需以云厂商账单为准。",
        },
        "source": "mock_data_provider.price_catalog",
    }


def _owns_instance(instance_id: str, user_id: str) -> bool:
    return _find_owned_instance(instance_id, user_id) is not None


def _find_owned_instance(instance_id: str, user_id: str) -> dict[str, Any] | None:
    for instance in INSTANCES:
        if instance["instance_id"] == instance_id and instance["user_id"] == user_id:
            return instance
    return None

