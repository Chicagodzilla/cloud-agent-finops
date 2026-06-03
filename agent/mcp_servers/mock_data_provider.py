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


def generate_finops_report(
    user_id: str,
    billing_month: str = "2026-05",
    target_instance_type: str = "ecs.g8a.xlarge",
) -> dict[str, Any]:
    bill_summary = query_monthly_bill_summary(user_id, billing_month)
    instances = query_user_instances(user_id, limit=20)["data"]
    resources: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []
    total_savings = 0.0

    for instance in instances:
        if not _is_finops_candidate(instance):
            continue
        usage = analyze_instance_usage(instance["instance_id"], user_id)
        if usage["status"] != "success":
            continue
        usage_data = usage["data"]
        metrics = usage_data["metrics_7d_avg"]
        cost = query_resource_cost_breakdown(instance["instance_id"], user_id, billing_month)
        cost_amount = 0.0
        if cost["status"] == "success":
            cost_amount = cost["data"]["total_amount"]
        resources.append(
            {
                "instance_id": instance["instance_id"],
                "instance_type": instance["instance_type"],
                "status": instance["status"],
                "region_id": instance["region_id"],
                "cpu_avg_7d": metrics["cpu_usage_percent"],
                "memory_avg_7d": metrics["memory_usage_percent"],
                "network_peak_mbps": metrics["network_out_bandwidth_mbps"],
                "current_month_cost": cost_amount,
                "diagnosis": usage_data["diagnosis"],
            }
        )
        if usage_data["diagnosis"] == "RESOURCES_IDLE":
            savings = estimate_savings(instance["instance_id"], target_instance_type, user_id)
            savings_amount = 0.0
            if savings["status"] == "success":
                savings_amount = savings["data"]["estimated_monthly_savings"]
            total_savings += savings_amount
            recommendations.append(
                {
                    "resource_id": instance["instance_id"],
                    "action": "downsize",
                    "priority": "high",
                    "title": f"建议将 {instance['instance_type']} 降配到 {target_instance_type}",
                    "reason": "近 7 天 CPU 与内存长期低利用率，存在明显资源闲置。",
                    "risk": "降配前需确认业务峰值、定时任务、依赖服务和容量冗余。",
                    "estimated_monthly_savings": round(savings_amount, 2),
                    "currency": "CNY",
                    "requires_approval": True,
                }
            )

    overall_status = "has_savings_opportunity" if recommendations else "no_obvious_savings"
    report = {
        "type": "finops_report",
        "summary": {
            "title": f"{billing_month} 云资源成本优化建议",
            "overall_status": overall_status,
            "billing_month": billing_month,
            "total_bill_amount": bill_summary["data"]["total_amount"],
            "estimated_monthly_savings": round(total_savings, 2),
            "currency": "CNY",
        },
        "resources": resources,
        "recommendations": recommendations,
        "risks": [
            "报告中的节省金额为基于 mock 规格价格的估算值。",
            "任何降配、关停或计费方式变更都需要人工确认后执行。",
        ],
        "sources": [
            {"type": "tool", "name": "query_monthly_bill_summary"},
            {"type": "tool", "name": "query_user_instances"},
            {"type": "tool", "name": "analyze_instance_usage"},
            {"type": "tool", "name": "estimate_savings"},
        ],
    }
    return {"status": "success", "data": report, "source": "mock_data_provider.finops_report"}


def _owns_instance(instance_id: str, user_id: str) -> bool:
    return _find_owned_instance(instance_id, user_id) is not None


def _find_owned_instance(instance_id: str, user_id: str) -> dict[str, Any] | None:
    for instance in INSTANCES:
        if instance["instance_id"] == instance_id and instance["user_id"] == user_id:
            return instance
    return None


def _is_finops_candidate(instance: dict[str, Any]) -> bool:
    return instance["status"] == "Running" and instance["instance_type"].startswith("ecs.")
