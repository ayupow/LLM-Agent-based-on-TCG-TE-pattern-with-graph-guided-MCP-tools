# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_deepseek import ChatDeepSeek
from langchain.prompts import PromptTemplate
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_fireworks import ChatFireworks
import asyncio
import pandas as pd
from langchain.schema import HumanMessage
from langgraph.errors import GraphRecursionError
import warnings
warnings.filterwarnings("ignore")
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")

import warnings

# 忽略弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

os.environ["OPENAI_API_KEY"] = "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"
os.environ["DEEPSEEK_API_KEY"] = "sk-52ed0fadee5d48d5adf4ef46fd65896e"
deepseek_api_key=os.environ["DEEPSEEK_API_KEY"],
api_key = "sk-y5taN0t1fLrciE4Qy0Qb9MYkwOWqingTOlcqZ7Gmiv2VWvMg"  # set this in your environment
URL = "https://chat.cloudapi.vip/v1"


# model = ChatOpenAI(
#     openai_api_key=os.environ["OPENAI_API_KEY"],
#     temperature=0,
#     model_name='gpt-4o'
# )
model = ChatOpenAI(
    # temperature=0.0,
    model_name="claude-sonnet-4-20250514-s",               # <<— replace with the Bailian model name you subscribed to
    openai_api_key=api_key,            # or use env var OPENAI_API_KEY
    openai_api_base=URL,              # sets the base URL to DashScope compatible endpoint
)


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
            
            "failed and recovered ULS performance comparing": {
                "command": "python",
                "transport": "stdio",
                "args": ["mcp_server_07.py"]
            },
        "new_mcp_server": {
            "command": "python",
            "transport": "stdio",
            "args": ["mcp_server_global_planning.py"]
        },
        "global_planning": {
            "command": "python",
            "transport": "stdio",
            "args": ["mcp_server_global_planning.py"]
        },
        "tool_chain_generation": {
            "command": "python",
            "transport": "stdio",
            "args": ["mcp_server_global_planning.py"]
        },
        
        }
    }
},
        "failed facility restoration resource allocating": {
    "command": "python",
    "transport": "stdio",
    "args": [
        "mcp_server_06.py"
    ],
    "tools": {
        "resource_allocation_considering_carbon_emissions_tool": {
            "function": "resource_allocation_considering_carbon_emissions.py",
            "description": {
                "aim": "This tool aims to calculate the daily resource allocation for each node to minimize the total carbon emissions. ",
                "input_output": "It reads data from Global_Data.json, including interdependent_infrastructure_networks_with_different_resource_demand.json; cascading_failure_by_random_attacks.json; and resource_provider_distance.json. The tool outputs resource_allocation_considering_carbon_emissions.json and stores it in Global_Data.json.",
                "expectation": "If the tool runs successfully, you will observe that resource_allocation_considering_carbon_emissions.json has been generated and stored in Global_Data.json."
            }
        },
        "allocate_restoration_resource_considering_carbon_emission": {
            "function": "resource_allocation_considering_carbon_emissions.py",
            "description": {
                "aim": "This tool calculates the daily resource allocation for each node to minimize the total carbon emissions. ",
                "input_output": "It reads data from Global_Data.json, including interdependent_infrastructure_networks_with_different_resource_demand.json; cascading_failure_by_random_attacks.json; and resource_provider_distance.json. The tool outputs resource_allocation_considering_carbon_emissions.json and stores it in file_inventory.json.",
                "expectation": "If the tool runs successfully, you will observe that resource_allocation_considering_carbon_emissions.json has been generated and stored in file_inventory.json."
            }
        }
    }
}
    })


    tools = await client.get_tools()
    print("\nAvailable tools:")
    for tool in tools:
        print(f"- {tool.name}")


        prompt_template = PromptTemplate(
            input_variables=["input"],
            template="""
                You are an expert in urban lifeline system recovery, and your task is to solve the problem step by step using the provided tools.
                __________________________________________________________________
                To solve a task, please use the following format:
                Thought: (reflect on your progress and decide what to do next (based on observation if exist), do not skip)
                Action: (the action name, should be one of the {{tool.name}}. Decide the action based on previous Thought and Observation)
                Action Input: (it can only be a name of .JSON file, decide the .JSON file based on previous Thought and Observation, if thre is no specific input, just input ("Global_Data.json"))
                Observation: (the result of the action)
                (this process can repeat, and you can only process one task at a time)

                OR

                Thought: (review original question and check my total process) 
                Final Answer: (output the final answer to the original input question based on observation)
                __________________________________________________________________
                {input}
                __________________________________________________________________
                REMEMBER:

                1. You can only respond with a single complete "Thought, Action, Action Input, Observation" format OR a single "Final Answer" format.
                2. Don't create files that don't exist yourself.
                3. Before all actions begin, you need to first plan the overall execution steps to complete the task.

                Begin!"""
        )

    agent = create_react_agent(
        tools=tools,
        model=model
    )

    TIMEOUT_SECONDS = 180

    # 读取 mcp tool chains.xlsx
    df = pd.read_excel("mcp tool chains_test.xlsx")
    descriptions = df["Task"].tolist()
    Tool_Chain = df["Tool_Chain"].tolist()

    output_path = "MCP_agent_response_multi_and_plan_client_claude-opus-4_26-50.xlsx"

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
        except Exception as e:  # Added: Catch any other unexpected errors and skip the task
            print(f"\nTask {i + 1} encountered an unexpected error: {str(e)}. Skipping this task.\n")
            output = f"Task skipped due to unexpected error: {str(e)}."

        # 保存结果
        output_df.at[i, "agent_response"] = output
        output_df.to_excel(output_path, index=False)
        print(f"\nTask {i + 1} response written to '{output_path}'\n")


if __name__ == "__main__":
    asyncio.run(main())