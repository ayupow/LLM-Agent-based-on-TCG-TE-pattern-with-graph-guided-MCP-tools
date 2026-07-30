import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.ticker import MaxNLocator
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import ChatOpenAI
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
import pandas as pd
from langchain_deepseek import ChatDeepSeek
import warnings


plt.rcParams["font.family"] = "Times New Roman"

warnings.filterwarnings("ignore", category=DeprecationWarning)


api_key = "" #please fill in your API key
URL = "https://chat.cloudapi.vip/v1"

model = ChatOpenAI(
    model_name="claude-sonnet-4-20250514-s",
    openai_api_key=api_key,
    openai_api_base=URL,
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

async def main():
    client = MultiServerMCPClient(
        {
            "ULSR_master": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_all.py"]
            }
        }
    )

    tools = await client.get_tools()
    print("\nAvailable tools:")
    for tool in tools:
        print(f"- {tool.name}")

    agent = create_react_agent(
        model,
        tools=tools,
        prompt="""
You are an expert in interdependent infrastructure networks, and your task is to solve the problem step by step using the provided tools.
__________________________________________________________________
To solve a task, please use the following format:
Complete format:
Thought: (reflect on your progress and decide what to do next (based on observation if exist), do not skip)
Action: (the action name, should be one of [{tool_names}]. Decide the action based on previous Thought and Observation)
Action Input: (name of a .json file, decide the input based on previous Thought and Observation)
Observation: (the result of the action)
(this process can repeat, and you can only process one task at a time)

OR
Thought: (review original question and check my total process) 
Final Answer: (output the final answer to the original input question based on observation)
__________________________________________________________________
Answer the question below using the following tools: {tools} 
Use the tools provided, and use the most specific tool available for each action. Your final answer should contain all information necessary to answer the question and subquestions.
Question: {input}
__________________________________________________________________
REMEMBER:
1. You can only respond with a single complete "Thought, Action, Action Input, Observation" format OR a single "Final Answer" format.
2. Don't create files that don't exist yourself.
3. Before all actions begin, you need to first plan the overall execution steps to complete the task.
Begin!"""
    )

    task_df = pd.read_excel("Task_for_client_25-50.xlsx")
    tasks = task_df["Task"].tolist()

    results = []

    for idx, task in enumerate(tasks, start=1):
        print(f"\n\n===== Task {idx} =====\n{task}")

        try:
            response = await asyncio.wait_for(
                agent.ainvoke({"messages": [("user", task)]}),
                timeout=180
            )

            pretty_print_response(response)

            if isinstance(response, str):
                resp_str = response
            else:
                resp_str = str(response).replace("\\n", "\n")

        except asyncio.TimeoutError:
            resp_str = "Timeout (exceeded 180 seconds)"

        results.append({
            "Task_ID": idx,
            "Tasks": task,
            "Agent_Response": resp_str
        })

        output_df = pd.DataFrame(results)
        output_df.to_excel(
            "MCP_agent_response_one_client_claude-sonnet-4-20250514.xlsx",
            index=False
        )
        print(f"Task {idx} saved to MCP_agent_response_one_client_claude-sonnet-4-20250514.xlsx")


if __name__ == "__main__":
    asyncio.run(main())

