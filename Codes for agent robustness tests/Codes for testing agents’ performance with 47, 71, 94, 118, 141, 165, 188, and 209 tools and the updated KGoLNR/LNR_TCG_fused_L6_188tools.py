


from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_deepseek import ChatDeepSeek
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
import os
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_fireworks import ChatFireworks
import asyncio
import pandas as pd
from langchain.schema import HumanMessage
from langgraph.errors import GraphRecursionError
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")
warnings.filterwarnings("ignore", category=DeprecationWarning)

api_key = ""
URL = "https://chat.cloudapi.vip/v1"

model = ChatOpenAI(
    model_name="claude-sonnet-4-20250514-s",
    openai_api_key=api_key,
    openai_api_base=URL,
)


def load_and_generate_tool_graph(input_json_file='KGoLNR.json'):
    with open(input_json_file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    relationships = []
    for item in data:
        if "Server" in item["p"]["start"].get("labels", []) or "Server" in item["p"]["end"].get("labels", []):
            continue
        start_tool = item["p"]["start"]["properties"]["name"]
        end_tool = item["p"]["end"]["properties"]["name"]
        relationships.append((start_tool, end_tool))

    def build_tool_chains(rel_list):
        chain_list = []
        for start_tool, end_tool in rel_list:
            if start_tool == "convert_SHPfile_to_JSONfile":
                chain_list.append([start_tool, end_tool])

        max_chain_length = 5
        for _ in range(3, max_chain_length + 1):
            new_chains = []
            for chain in chain_list:
                last_tool = chain[-1]
                for start_tool, end_tool in rel_list:
                    if last_tool == start_tool:
                        new_chain = chain + [end_tool]
                        new_chains.append(new_chain)
            chain_list.extend(new_chains)

        unique_chain_set = set(tuple(chain) for chain in chain_list)
        unique_chain_list = [list(chain) for chain in unique_chain_set]
        return unique_chain_list

    tool_chains = build_tool_chains(relationships)
    numbered_chains = [{"chain_id": idx + 1, "chain": chain} for idx, chain in enumerate(tool_chains)]
    print(f"Tool chains generated from KG: {len(tool_chains)} unique chains extracted.")
    return numbered_chains, tool_chains


def build_chain_retriever(tool_chains):
    chain_texts = [" -> ".join(chain) for chain in tool_chains]
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key,
        openai_api_base=URL
    )
    vectorstore = FAISS.from_texts(chain_texts, embedding_model)
    print(f"Chain retriever built: {len(chain_texts)} chains indexed.")
    return vectorstore, chain_texts


def retrieve_best_chain(task_description, vectorstore, chain_texts, k=1):
    retrieved_docs = vectorstore.similarity_search(task_description, k=k)
    if not retrieved_docs:
        return chain_texts[0] if chain_texts else ""
    return retrieved_docs[0].page_content


async def main():
    print("=" * 60)
    print("Step 1: Generating tool chains from KGoLNR.json ...")
    numbered_chains, raw_chains = load_and_generate_tool_graph('KGoLNR.json')
    vectorstore, chain_texts = build_chain_retriever(raw_chains)

    print("=" * 60)
    print("Step 2: Connecting to MCP servers (L6: 18 servers, 188 tools) ...")
    client = MultiServerMCPClient(
        {
            "data processing": {
                "command": "python", "transport": "stdio",
                "args": ["mcp_server_01.py"]
            },
            "critical infrastructure facility identifying": {
                "command": "python", "transport": "stdio",
                "args": ["mcp_server_02.py"]
            },
            "cascading failure_scenario simulating": {
                "command": "python", "transport": "stdio",
                "args": ["mcp_server_03.py"]
            },
            "failed facility restoration scheduling": {
                "command": "python", "transport": "stdio",
                "args": ["mcp_server_04.py"]
            },
            "emergency portable equipment deploying": {
                "command": "python", "transport": "stdio",
                "args": ["mcp_server_05.py"]
            },
            "failed facility restoration resource allocating": {
                "command": "python", "transport": "stdio",
                "args": ["mcp_server_06.py"]
            },
            "failed and recovered ULS performance comparing": {
                "command": "python", "transport": "stdio",
                "args": ["mcp_server_07.py"]
            },
            "added_gis_data_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_data_L6.py"]
            },
            "added_gis_geopandas_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_geopandas_L6.py"]
            },
            "added_gis_pyproj_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_pyproj_L6.py"]
            },
            "added_gis_pysal_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_pysal_L6.py"]
            },
            "added_gis_rasterio_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_rasterio_L6.py"]
            },
            "added_gis_shapely_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_shapely_L6.py"]
            },
            "added_gis_utilities_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_utilities_L6.py"]
            },
            "added_gis_visualize_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_visualize_L6.py"]
            },
            "added_math_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_math_L6.py"]
            },
            "added_networkx_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_networkx_L6.py"]
            },
            "added_powerfactory_L6": {
                "command": "python", "transport": "stdio",
                "args": ["added_powerfactory_L6.py"]
            },
        }
    )

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
            Thought: (reflect on your progress and decide what to do next)
            Action: (the action name, should be one of the available tools)
            Action Input: (a .JSON file name, default "Global_Data.json" if no specific input)
            Observation: (the result of the action)
            (this process can repeat)

            OR

            Thought: (review original question and check my total process)
            Final Answer: (output the final answer to the original input question based on observation)
            __________________________________________________________________
            {input}
            __________________________________________________________________
            REMEMBER:
            1. You can only respond with a single complete "Thought, Action, Action Input, Observation" format OR a single "Final Answer" format.
            2. Do not create files that do not exist yourself.
            3. Before all actions begin, you need to first plan the overall execution steps to complete the task.
            Begin!"""
    )

    agent = create_react_agent(tools=tools, model=model)
    TIMEOUT_SECONDS = 180

    print("=" * 60)
    print("Step 3: Reading tasks and retrieving best matching tool chains ...")
    df = pd.read_excel("Task_for_client.xlsx")
    descriptions = df["Task"].tolist()
    output_path = "MCP_agent_response_L6_188tools_fused.xlsx"

    if os.path.exists(output_path):
        output_df = pd.read_excel(output_path)
    else:
        output_df = df.copy()
        output_df["agent_response"] = [""] * len(output_df)
        output_df["retrieved_chain"] = [""] * len(output_df)

    for i, desc in enumerate(descriptions):
        print(f"\n====== Running Task {i + 1}: ======\n{desc}\n")

        best_chain = retrieve_best_chain(desc, vectorstore, chain_texts, k=1)
        print(f"  -> Retrieved chain: {best_chain}")

        combined_input = (
            f"You are working on task index {i}.\n"
            f"Task description: {desc}\n\n"
            f"Suggested tool chain (dynamically generated from Knowledge Graph): {best_chain}\n"
        )
        try:
            response = await asyncio.wait_for(
                agent.ainvoke(
                    {"messages": [HumanMessage(content=combined_input)]},
                    config={"recursion_limit": 25}
                ),
                timeout=TIMEOUT_SECONDS
            )
            output = str(response).replace("\\n", "\n") if not isinstance(response, str) else response
            print("\n===== Response from Agent =====\n"); print(output)
        except asyncio.TimeoutError:
            print(f"\nTask {i + 1} timed out. Skipping.\n")
            output = f"Task skipped due to timeout ({TIMEOUT_SECONDS}s)."
        except GraphRecursionError:
            print(f"\nTask {i + 1} reached recursion limit. Skipping.\n")
            output = "Task skipped due to recursion limit."
        except Exception as e:
            print(f"\nTask {i + 1} unexpected error: {e}. Skipping.\n")
            output = f"Task skipped: {e}."
        output_df.at[i, "agent_response"] = output
        output_df.at[i, "retrieved_chain"] = best_chain
        output_df.to_excel(output_path, index=False)
        print(f"\nTask {i + 1} response written to '{output_path}'\n")

if __name__ == "__main__":
    asyncio.run(main())
