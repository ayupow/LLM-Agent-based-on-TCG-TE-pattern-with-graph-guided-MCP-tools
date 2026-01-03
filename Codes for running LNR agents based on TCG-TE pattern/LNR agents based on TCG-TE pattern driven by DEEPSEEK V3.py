# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.schema import HumanMessage
from langgraph.errors import GraphRecursionError
from langchain_fireworks import ChatFireworks
import asyncio
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")


# 设置OpenAI API密钥
# os.environ["http_proxy"] = "http://localhost:7890"
# os.environ["https_proxy"] = "http://localhost:7890"

import warnings

# 忽略弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

os.environ["OPENAI_API_KEY"] = ""  #please fill in your API key
os.environ["DEEPSEEK_API_KEY"] = " " #please fill in your API key
deepseek_api_key=os.environ["DEEPSEEK_API_KEY"],

# model = ChatOpenAI(
#     openai_api_key=os.environ["OPENAI_API_KEY"],
#     temperature=0,
#     model_name='gpt-4o'
# )

model = ChatDeepSeek(
    temperature=0,
    model_name='deepseek-chat'
)



# gpt-3.5-turbo-0125

async def main():
    client = MultiServerMCPClient(
        {

            "data processing": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_01.py"]
            },
            "critical infrastructure facility identifying": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_02.py"]
            },
            "cascading failure_scenario simulating": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_03.py"]
            },
            "failed facility restoration scheduling": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_04.py"]
            },
            "emergency portable equipment deploying": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_05.py"]
            },
            "failed facility restoration resource allocating": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_06.py"]
            },
            "failed and recovered ULS performance comparing": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_07.py"]
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
    prompt="""You are an expert in interdependent infrastructure networks, and your task is to solve the problem step by step using the provided tools.
__________________________________________________________________
To solve a task, please use the following format:
Complete format:
Thought: (reflect on your progress and decide what to do next (based on observation if exist), do not skip)
Action: (the action name, should be one of [{tool.names}]. Decide the action based on previous Thought and Observation)
Action Input: (name of a .json file, decide the input based on previous Thought and Observation)
Observation: (the result of the action)
(this process can repeat, and you can only process one task at a time)

OR
Thought: (review original question and check my total process) 
Final Answer: (output the final answer to the original input question based on observation)
__________________________________________________________________

Answer the question below using the following tools: {relevant_tools} 
Use the tools provided, and use the most specific tool available for each action. Your final answer should contain all information necessary to answer the question and subquestions.
Question: {input}
__________________________________________________________________
REMEMBER:
1. You can only respond with a single complete "Thought, Action, Action Input, Observation" format OR a single "Final Answer" format.
2. Don't create files that don't exist yourself.
3. Before all actions begin, you need to first plan the overall execution steps to complete the task.
Begin!""")
    # response = await agent.ainvoke({
    #     "messages": [
    #         ("user",
    #          "Please use the infrastructure information in Global_Data.json and finally design the recovery order of different nodes based on the node importance determined by closeness centrality. Before execution, you have to plan the task by visiting mcp_server_global_planning")
    #     ]
    # })

    # def pretty_print_response(response):
    #     print("\n\n===== Response from Agent =====\n")
    #
    #     if isinstance(response, str):
    #         output = response
    #     else:
    #         output = str(response).replace("\\n", "\n")
    #
    #     keyword = "tool_calls=[{"
    #     if keyword in output:
    #         output = output.replace(keyword, "\n" + keyword)
    #
    #     print(output)
    #
    # pretty_print_response(response)

    agent = create_react_agent(
        tools=tools,
        model=model
    )

    TIMEOUT_SECONDS = 180

    # 读取 mcp tool chains.xlsx
    df = pd.read_excel("mcp tool chains.xlsx")
    descriptions = df["Task"].tolist()
    Tool_Chain = df["Tool_Chain"].tolist()


    output_path = "MCP_agent_response_multi_and_plan_client_deepseek.xlsx"

    if os.path.exists(output_path):
        output_df = pd.read_excel(output_path)
    else:
        output_df = df.copy()
        output_df["agent_response"] = [""] * len(output_df)

    for i, desc in enumerate(descriptions):
        print(f"\n====== Running Task {i + 1}: ======\n{desc}\n")

        combined_input = (
            f"You are working on task index {i}.\n"
            f"Task description: {desc}\n\n"
            f"Tools for you to solve that task: {Tool_Chain[i]}\n"

        )

        try:
            # 使用 asyncio.wait_for 添加超时机制
            response = await asyncio.wait_for(
                agent.ainvoke(
                    {"messages": [HumanMessage(content=combined_input)]},
                    config={"recursion_limit": 25}  # 限制25轮
                ),
                timeout=TIMEOUT_SECONDS
            )

            if isinstance(response, str):
                output = response
            else:
                output = str(response).replace("\\n", "\n")

            print("\n===== Response from Agent =====\n")
            print(output)

        except asyncio.TimeoutError:
            print(f"\nTask {i + 1} timed out after {TIMEOUT_SECONDS} seconds. Skipping this task.\n")
            output = f"Task skipped due to timeout ({TIMEOUT_SECONDS} seconds)."

        except GraphRecursionError:
            print(f"\nTask {i + 1} reached recursion limit. Skipping this task.\n")
            output = "Task skipped due to recursion limit."

        # 保存结果
        output_df.at[i, "agent_response"] = output
        output_df.to_excel(output_path, index=False)
        print(f"\nTask {i + 1} response written to '{output_path}'\n")


if __name__ == "__main__":

    asyncio.run(main())
