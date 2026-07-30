import os
import asyncio
import warnings
import pandas as pd
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
# MCP 客户端及适配器
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient

# LangChain 核心与 Agent 相关组件
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_deepseek import ChatDeepSeek

# 忽略弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

# API配置
api_key = ""
URL = "https://chat.cloudapi.vip/v1"
model = ChatOpenAI(
    model_name="qwen3",
    openai_api_key=api_key,
    openai_api_base=URL,
)


# 定义 Planner 结构化输出的数据格式
class Plan(BaseModel):
    steps: List[str] = Field(description="Resolving steps sorted sequentially to solve the given task.")


def pretty_print_response(response):
    print("\n\n===== Response from Agent =====\n")
    if isinstance(response, str):
        output = response
    else:
        output = str(response).replace("\\n", "\n")

    keyword = "tool_calls=[{"
    if keyword in output:
        output = output.replace(keyword, "\n" + keyword)

    print(output)


async def plan_then_execute(task: str, tools, model) -> str:
    """
    Plan-then-Execute 框架的具体实现
    """
    # ---------------- 1. Plan 阶段 ----------------
    print("\n[Phase 1/3] Generating Plan...")
    tools_description = "\n".join([f"- {t.name}: {t.description}" for t in tools])

    planner_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert planner for infrastructure network problems. 
Your task is to break down the user's request into a detailed, sequential plan of steps. 
Do not solve the problem directly, just output the steps needed."""),
        ("human", "Task: {input}\n\nAvailable Tools:\n{tools_description}")
    ])

    # 结合 Pydantic 结构化输出获取步骤列表
    planner = planner_prompt | model.with_structured_output(Plan)
    plan_output = await planner.ainvoke({
        "input": task,
        "tools_description": tools_description
    })

    steps = plan_output.steps
    print(f"Generated Plan ({len(steps)} steps):")
    for idx, s in enumerate(steps, 1):
        print(f"  {idx}. {s}")

    # ---------------- 2. Execute 阶段 ----------------
    print("\n[Phase 2/3] Executing Plan...")

    # 创建执行步骤时的 Executor Agent
    executor_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert executor tasked with completing a single step of a larger plan.
Use your tools to complete the task assigned to you.
Context from previously completed steps:
{context}"""),
        ("human", "Current step to execute: {input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    executor_agent = create_tool_calling_agent(model, tools, executor_prompt)
    executor_agent_executor = AgentExecutor(agent=executor_agent, tools=tools, verbose=True)

    execution_context = ""

    for idx, step in enumerate(steps, 1):
        print(f"\n>> Executing Step {idx}/{len(steps)}: {step}")
        try:
            res = await executor_agent_executor.ainvoke({
                "input": step,
                "context": execution_context
            })
            step_result = res.get("output", "No response content.")
        except Exception as e:
            step_result = f"Execution failed: {str(e)}"
            print(f"Error during step {idx}: {e}")

        execution_context += f"Step {idx}: {step}\nResult: {step_result}\n\n"

    # ---------------- 3. Synthesis (总结) 阶段 ----------------
    print("\n[Phase 3/3] Synthesizing Final Answer...")
    synthesis_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert coordinator. Based on the original task, the plan, and the execution results, write a comprehensive final answer.
Ensure that the final answer is logically coherent and directly answers the user's original query."""),
        ("human",
         "Original Task: {task}\n\nPlan and Execution History:\n{context}\n\nPlease generate the final response.")
    ])

    synthesizer = synthesis_prompt | model
    synthesis_res = await synthesizer.ainvoke({
        "task": task,
        "context": execution_context
    })

    return synthesis_res.content


async def main():
    # 初始化多服务器 MCP 客户端
    client = MultiServerMCPClient(
        {
            "ULSR_master": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_all.py"]
            }
        }
    )

    # 获取可用工具
    tools = await client.get_tools()
    print("\nAvailable tools:")
    for tool in tools:
        print(f"- {tool.name}")

    # 读取任务 Excel 文件
    task_df = pd.read_excel("Task_for_client.xlsx")
    tasks = task_df["Task"].tolist()

    results = []

    for idx, task in enumerate(tasks, start=1):
        print(f"\n\n===== Task {idx} =====\n{task}")

        try:
            # 运行自定义的 Plan-then-Execute 流程，超时设为 180 秒
            resp_str = await asyncio.wait_for(
                plan_then_execute(task, tools, model),
                timeout=180
            )
            pretty_print_response(resp_str)

        except asyncio.TimeoutError:
            print(f"Task {idx} 超时（180秒），已跳过。")
            resp_str = "Timeout: No response within 180 seconds."
        except Exception as e:
            print(f"Task {idx} 运行异常: {e}")
            resp_str = f"Error occurred: {str(e)}"

        results.append({
            "Task_ID": idx,
            "Tasks": task,
            "Agent_Response": resp_str
        })

        # 实时保存结果
        output_df = pd.DataFrame(results)
        output_df.to_excel(
            "MCP_agent_response_one_client_qwen.xlsx",
            index=False
        )
        print(f"Task {idx} saved to MCP_agent_response_one_client_qwen3_chat.xlsx")


if __name__ == "__main__":
    asyncio.run(main())