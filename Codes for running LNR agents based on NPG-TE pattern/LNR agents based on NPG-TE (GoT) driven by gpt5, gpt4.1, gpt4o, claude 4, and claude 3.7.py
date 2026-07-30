import os
import asyncio
import warnings
import pandas as pd
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, Field

# MCP 客户端及适配器
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient

# LangChain 核心与 Agent 相关组件
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_deepseek import ChatDeepSeek

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
# ==================== Graph-of-Thought (Tool-Chain) 数据结构 ====================

class ToolStep(BaseModel):
    tool_name: str = Field(description="The exact name of the tool to be executed in this step.")
    input_source: str = Field(
        description="Explanation of where this tool gets its input (e.g., outputs/files from a previous tool).")
    output_destination: str = Field(
        description="Explanation of the output (e.g., file generated) passed to the subsequent tool.")
    step_description: str = Field(description="Brief description of what this step accomplishes.")


class CandidatePath(BaseModel):
    path_id: str = Field(description="Unique identifier for the candidate path, e.g., 'path_1', 'path_2'")
    steps: List[ToolStep] = Field(description="The sequential list of tool steps forming this execution chain.")
    meets_requirements: bool = Field(
        description="True if this sequence of tools successfully produces the final output requested by the task.")
    correctness_penalty: int = Field(
        description="0 if the path meets requirements; 10 if it is incomplete or incorrect.")
    length_score: int = Field(
        description="The number of steps (tools) in this path. Fewer steps result in a lower score.")
    total_cost_score: float = Field(
        description="Sum of correctness_penalty and length_score. Lower total cost is preferred.")


class ToolGraphPlanning(BaseModel):
    candidate_paths: List[CandidatePath] = Field(
        description="List of one or more candidate tool chains analyzed based on tool inputs/outputs.")
    selected_path_id: str = Field(
        description="The path_id of the selected optimal chain (the one with the lowest total_cost_score).")


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


# ==================== GoT 执行阶段组件 ====================

async def execute_single_tool_step(step: ToolStep, context: str, tool, model) -> str:
    """
    单步执行阶段：仅将当前步骤所需的单一工具赋给 Agent，确保一步一个 toolcall
    """
    executor_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert executor. Your task is to execute the designated tool to complete the current step.
You must use the provided tool and only this tool. Do not attempt to use any other tools.
Analyze the context from previous steps to extract necessary parameters (such as filenames or query parameters).

Context from previous steps:
{context}"""),
        ("human", "Goal: {step_description}\nTool to execute: {tool_name}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 仅将当前步骤对应的单一工具打包传入
    single_tool_list = [tool]
    executor_agent = create_tool_calling_agent(model, single_tool_list, executor_prompt)
    executor_agent_executor = AgentExecutor(agent=executor_agent, tools=single_tool_list, verbose=True)

    try:
        res = await executor_agent_executor.ainvoke({
            "step_description": step.step_description,
            "tool_name": step.tool_name,
            "context": context
        })
        return res.get("output", "No response content.")
    except Exception as e:
        return f"Execution of tool {step.tool_name} failed: {str(e)}"


async def graph_of_thought_execute(task: str, tools, model) -> str:
    """
    基于工具关系构图并进行评分选择的 GoT 执行框架
    """
    # 将可用工具组织为字典，便于执行时检索
    tools_map = {t.name: t for t in tools}

    # ---------------- 1. Planning Phase (分析依赖并构图打分) ----------------
    print("\n[Phase 1/3] Planning and Selecting Optimal Tool Chain...")
    tools_description = "\n".join([f"- {t.name}: {t.description}" for t in tools])

    planner_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert network infrastructure planner. 
Your task is to analyze the user's request and the available tools to formulate one or more candidate tool execution chains.
Identify the dependency relationships between tools based on their inputs and outputs (e.g., if Tool A creates a file that Tool B requires, Tool B depends on Tool A).

For each candidate path:
1. List the sequential steps, detailing how files/data flow from one tool to another.
2. Check if the path satisfies the task requirements (meets_requirements).
3. Compute the correctness_penalty (0 if it satisfies the task, 10 if it does not).
4. Compute the length_score (equal to the number of tools in the chain).
5. Compute the total_cost_score (correctness_penalty + length_score). Lower score is better.

Select the candidate path with the lowest total_cost_score. If only one path is viable, select it."""),
        ("human", "Task: {input}\n\nAvailable Tools:\n{tools_description}")
    ])

    planner = planner_prompt | model.with_structured_output(ToolGraphPlanning)
    planning_result = await planner.ainvoke({
        "input": task,
        "tools_description": tools_description
    })

    # 获取选中的工具链
    selected_path = None
    print("\nAnalyzed Candidate Tool Chains:")
    for path in planning_result.candidate_paths:
        is_selected = "[SELECTED]" if path.path_id == planning_result.selected_path_id else ""
        print(f"  - Path ID: {path.path_id} {is_selected}")
        print(f"    Sequence: {' -> '.join([s.tool_name for s in path.steps])}")
        print(f"    Meets Requirements: {path.meets_requirements}")
        print(f"    Correctness Penalty: {path.correctness_penalty}, Length Score (Steps): {path.length_score}")
        print(f"    Total Cost Score: {path.total_cost_score}")
        if path.path_id == planning_result.selected_path_id:
            selected_path = path

    if not selected_path:
        # 如果未找到匹配的路径，默认选择第一个
        if planning_result.candidate_paths:
            selected_path = planning_result.candidate_paths[0]
            print(f"\nFallback: Selected path '{selected_path.path_id}' as no direct match was identified.")
        else:
            return "Error: No viable tool chain could be planned."

    print(f"\nExecuting Selected Path: {selected_path.path_id}")

    # ---------------- 2. Execution Phase (严格单步工具调用) ----------------
    print("\n[Phase 2/3] Executing Selected Tool Chain...")
    execution_context = ""
    executed_history = []

    for idx, step in enumerate(selected_path.steps, 1):
        print(f"\n>> Step {idx}/{len(selected_path.steps)}: Invoking tool '{step.tool_name}'")

        # 确认规划的工具是否存在于当前环境中
        if step.tool_name not in tools_map:
            err_msg = f"Tool '{step.tool_name}' is not available in the current environment."
            print(f"Error: {err_msg}")
            executed_history.append((step, f"Failed: {err_msg}"))
            execution_context += f"Step {idx} ({step.tool_name}): Failed. {err_msg}\n"
            continue

        target_tool = tools_map[step.tool_name]

        # 传入当前步骤、上下文及对应的单一工具进行调用
        step_result = await execute_single_tool_step(step, execution_context, target_tool, model)

        executed_history.append((step, step_result))
        execution_context += f"Step {idx} ({step.tool_name}) Output:\n{step_result}\n\n"

    # ---------------- 3. Synthesis Phase (整合输出) ----------------
    print("\n[Phase 3/3] Synthesizing Final Answer...")

    synthesis_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert coordinator. Based on the original task and the detailed tool execution history, synthesize a clear and structured final answer.
Do not invent any information; rely strictly on the results returned by the tools."""),
        ("human", "Original Task: {task}\n\nExecution History:\n{history}\n\nPlease generate the final response.")
    ])

    synthesizer = synthesis_prompt | model
    synthesis_res = await synthesizer.ainvoke({
        "task": task,
        "history": execution_context
    })

    return synthesis_res.content


# ==================== 主入口函数保持不变 ====================

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
            # 运行更新后的 GoT 流程，超时设为 180 秒
            resp_str = await asyncio.wait_for(
                graph_of_thought_execute(task, tools, model),
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

        # 保存结果
        output_df = pd.DataFrame(results)
        output_df.to_excel(
            "MCP_agent_response_one_client_GOT_gpt5.xlsx",
            index=False
        )
        print(f"Task {idx} saved to MCP_agent_response_one_client_GOT_deepseek_chat.xlsx")


if __name__ == "__main__":
    asyncio.run(main())