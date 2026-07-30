import os
import asyncio
import warnings
import re
import pandas as pd
from typing import List

# MCP 客户端及适配器
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient

# LangChain 核心与 Agent 相关组件
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI

# 忽略弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

# API配置
api_key = ""
URL = "https://chat.cloudapi.vip/v1"

model = ChatOpenAI(
    model_name="gpt-5",
    openai_api_key=api_key,
    openai_api_base=URL,
    temperature=0
)


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
Please list each step on a new line, starting with a number (e.g., "1. [Step description]").
Do not write any introductory or concluding text. Just output the raw numbered steps."""),
        ("human", "Task: {input}\n\nAvailable Tools:\n{tools_description}")
    ])

    planner = planner_prompt | model
    planner_response = await planner.ainvoke({
        "input": task,
        "tools_description": tools_description
    })

    plan_text = planner_response.content

    # 解析步骤
    steps = []
    for line in plan_text.split("\n"):
        line = line.strip()
        match = re.match(r'^(?:\d+[\.\-\u3001]|\-|\*)\s*(.*)', line)
        if match:
            step_text = match.group(1).strip()
            if step_text:
                steps.append(step_text)

    if not steps:
        steps = [line.strip() for line in plan_text.split("\n") if line.strip()]

    print(f"Generated Plan ({len(steps)} steps):")
    for idx, s in enumerate(steps, 1):
        print(f"  {idx}. {s}")

    # ---------------- 2. Execute 阶段 ----------------
    print("\n[Phase 2/3] Executing Plan...")

    # 强化 Prompt：强制要求进行真实的 Tool Call，并限制输入参数为 Global_Data.json
    executor_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert executor tasked with completing a single step of a larger plan.

CRITICAL INSTRUCTIONS FOR REAL EXECUTION:
1. You MUST call the appropriate tool from your toolset to perform the required action. Do NOT just output text describing or simulating what you would do.
2. For ANY tool you choose to execute, you MUST use "Global_Data.json" as the value for the input file, data source, or database parameter. 
3. Look closely at the schema of the tool you are calling, and set the parameter representing the dataset or file path strictly to "Global_Data.json".

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
    # 初始化多服务器 MCP 客户端 (根据 langchain-mcp-adapters 0.1.0+ 标准，不使用 async with 块)
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
    if not os.path.exists("Task_for_client.xlsx"):
        print("Error: Task_for_client.xlsx not found.")
        return

    task_df = pd.read_excel("Task_for_client.xlsx")
    tasks = task_df["Task"].tolist()

    results = []

    for idx, task in enumerate(tasks, start=1):
        print(f"\n\n===== Task {idx} =====\n{task}")

        try:
            # 设置 180 秒超时
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
        output_xlsx_name = "MCP_agent_response_one_client_gpt5.xlsx"
        output_df.to_excel(
            output_xlsx_name,
            index=False
        )
        print(f"Task {idx} saved to {output_xlsx_name}")


if __name__ == "__main__":
    asyncio.run(main())