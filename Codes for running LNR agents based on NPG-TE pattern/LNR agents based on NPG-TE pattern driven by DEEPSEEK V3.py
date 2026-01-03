# Create server parameters for stdio connection
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


warnings.filterwarnings("ignore", category=DeprecationWarning)

os.environ["DEEPSEEK_API_KEY"] = "" #please fill in your API key
deepseek_api_key=os.environ["DEEPSEEK_API_KEY"],


model = ChatDeepSeek(
    temperature=0,
    model_name='deepseek-chat'
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
Begin!""")

    # 读取任务 Excel
    task_df = pd.read_excel("Task_for_client.xlsx")
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
            resp_str = "Timeout: No response within 60 seconds."

        results.append({
            "Task_ID": idx,
            "Tasks": task,
            "Agent_Response": resp_str
        })

        
        output_df = pd.DataFrame(results)
        output_df.to_excel(
            "MCP_agent_response_one_client_deepseek_chat.xlsx",
            index=False
        )
        print(f"Task {idx} saved to MCP_agent_response_one_client_deepseek_chat.xlsx")


if __name__ == "__main__":
    asyncio.run(main())





# 启动异步主程序
if __name__ == "__main__":

    asyncio.run(main())
