"""
 * 小滴课堂,愿景：让技术不再难学
 * @Remark 有问题联系我【xdclass68】
 * 源码-笔记-技术交流群,官网 https://xdclass.net
"""
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import Dict, Any

from core.workflow.state import AgentState
from agents.billing_agent import UserIdInjector

class FinOpsAgentNode:
    """
    FinOps Agent：成本优化与架构诊断专家。
    负责分析用户的资源监控数据，判断是否存在资源浪费，并给出降本增效的建议。
    """
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
        load_dotenv(dotenv_path)

        self.llm = ChatOpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            model=os.getenv("MODEL", "qwen-plus"),
            base_url=os.getenv("BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
            temperature=0.1, 
        )
        
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'mcp_servers.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.servers_config = json.load(f)

    async def _ensure_tools(self):
        pass

    async def __call__(self, state: AgentState) -> Dict[str, Any]:
        config = {"configurable": {"user_id": state.get("user_id", "unknown")}}

        client = MultiServerMCPClient(
            connections=self.servers_config.get("mcpServers", {}),
            tool_interceptors=[UserIdInjector()]
        )
        all_tools = await client.get_tools()
        target_tools = [
            "query_user_instances",
            "query_monthly_bill_summary",
            "query_resource_cost_breakdown",
            "query_instance_metrics",
            "analyze_instance_usage",
            "estimate_savings",
        ]
        tools = [t for t in all_tools if t.name in target_tools]
        
        system_prompt = f"""你是一个专业的云上【FinOps成本优化专家】。
你刚刚接手了上一个 Agent (BillingAgent) 传递过来的上下文。

你的任务：
1. 先调用 `query_monthly_bill_summary` 查询用户最近月份账单摘要，了解费用构成。
2. 仔细阅读上下文中的对话历史，优先提取用户想要优化的**实例 ID (instance_id)**。
3. 如果上下文中没有 instance_id，调用 `query_user_instances` 获取该用户实例列表，并优先选择 Running 状态的 ECS 实例继续分析；如果有多台实例，可先给出清单并建议用户指定目标。
4. 对目标实例调用 `query_resource_cost_breakdown` 查询资源级费用，再调用 `query_instance_metrics` 和 `analyze_instance_usage` 获取近 7 天监控数据与诊断结论。
5. 如果诊断为 `RESOURCES_IDLE`，可以建议降配；但涉及“每月可节省多少钱”时必须调用 `estimate_savings`，严禁自己估算或编造金额。
6. 以云架构师的口吻给用户提出**降本增效建议**：
   - 明确说明依据：账单摘要、资源费用、CPU/内存/带宽监控、工具返回的诊断。
   - 给出建议动作：降配、保留观察、停止闲置资源、购买更合适计费方式等。
   - 标明风险：任何降配/关停都需要人工确认，先确认业务峰值、定时任务和依赖服务。
   - 语气要专业、诚恳，完全站在为用户省钱的角度。

注意：系统会自动注入 user_id，调用工具时传占位符 "auto" 即可。
- 严禁编造实例 ID、监控指标和费用节省金额；必须基于工具返回结果回答。
- 最终回答中如出现节省金额，必须说明来自 `estimate_savings`，且标注为估算值。
- 严禁出现“工具不可用/接口坏了/系统异常”等内部表述，对用户只给业务友好表达。
"""
        inner_agent = create_react_agent(
            model=self.llm,
            tools=tools,
            prompt=system_prompt
        )
        
        print("💡 [FinOpsAgent] 正在接手并分析实例监控指标，生成降本优化报告...")
        
        result = await inner_agent.ainvoke(
            {"messages": state["messages"]}, 
            config=config
        )
        
        final_message = result["messages"][-1]
        
        # 执行完毕后，把 next_agent 清空，代表流程彻底结束
        return {"messages": [final_message], "next_agent": ""}
