# =============================================================================
# LNR Agents based on TCG-TE Pattern driven by DEEPSEEK V3
# Integrated with 5 MCP archives: gis-mcp + PowerMCP + networkx-mcp + EPANET + Math
# Total: 20 servers (~300 tools)
# =============================================================================
# EXISTING (8 servers):
#   mcp_server_01.py              - data processing
#   mcp_server_02.py              - critical infrastructure facility identifying
#   mcp_server_03.py              - cascading failure scenario simulating
#   mcp_server_04.py              - failed facility restoration scheduling
#   mcp_server_05.py              - emergency portable equipment deploying
#   mcp_server_06.py              - failed facility restoration resource allocating
#   mcp_server_07.py              - failed and recovered ULS performance comparing
#   mcp_server_global_planning.py - global task planning
#
# ADDED — gis-mcp (8 servers, ~97 tools):
#   added_gis_geopandas.py        - Vector I/O, joins, overlay (11 tools)
#   added_gis_shapely.py          - Geometric ops, properties (28 tools)
#   added_gis_pyproj.py           - CRS transformations, geodesy (11 tools)
#   added_gis_rasterio.py         - Raster processing, analysis (18 tools)
#   added_gis_pysal.py            - Spatial statistics, regression (18 tools)
#   added_gis_data.py             - Geospatial data download (8 tools)
#   added_gis_visualize.py        - Static + interactive maps (2 tools)
#   added_gis_utilities.py        - Universal save/export (1 tool, cross-cutting)
#
# ADDED — PowerMCP (1 server, 11 tools):
#   added_powerfactory_mcp.py     - DIgSILENT PowerFactory simulation control
#
# ADDED — networkx-mcp (1 server, ~42 tools):
#   added_networkx_mcp.py         - NetworkX graph analysis & algorithms
#
# ADDED — EPANET (1 server, 7 tools):
#   added_epanet_mcp.py           - Water network hydraulic simulation
#
# ADDED — Math (1 server, 22 tools):
#   added_math_mcp.py             - Arithmetic, statistics, trigonometry
# =============================================================================

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
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")
warnings.filterwarnings("ignore", category=DeprecationWarning)

os.environ["OPENAI_API_KEY"] = "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"
os.environ["DEEPSEEK_API_KEY"] = "sk-52ed0fadee5d48d5adf4ef46fd65896e"
deepseek_api_key = os.environ["DEEPSEEK_API_KEY"]

model = ChatDeepSeek(
    temperature=0,
    model_name='deepseek-chat'
)


async def main():
    client = MultiServerMCPClient(
        {
            # =====================================================================
            # EXISTING SERVERS (Infrastructure Resilience Domain)
            # =====================================================================
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
            "global task planning": {
                "command": "python", "transport": "stdio",
                "args": ["mcp_server_global_planning.py"]
            },

            # =====================================================================
            # ADDED: gis-mcp servers (Geospatial Analysis Domain)
            # =====================================================================
            "added_gis_geopandas": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_geopandas.py"]
            },
            "added_gis_shapely": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_shapely.py"]
            },
            "added_gis_pyproj": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_pyproj.py"]
            },
            "added_gis_rasterio": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_rasterio.py"]
            },
            "added_gis_pysal": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_pysal.py"]
            },
            "added_gis_data": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_data.py"]
            },
            "added_gis_visualize": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_visualize.py"]
            },
            "added_gis_utilities": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_utilities.py"]
            },

            # =====================================================================
            # ADDED: PowerMCP — DIgSILENT PowerFactory (Power Systems Domain)
            # =====================================================================
            "added_powerfactory_mcp": {
                "command": "python", "transport": "stdio",
                "args": ["added_powerfactory_mcp.py"]
            },

            # =====================================================================
            # ADDED: networkx-mcp — Graph Analysis & Algorithms
            # =====================================================================
            "added_networkx_mcp": {
                "command": "python", "transport": "stdio",
                "args": ["added_networkx_mcp.py"]
            },

            # =====================================================================
            # ADDED: EPANET — Water Network Hydraulic Simulation
            # =====================================================================
            "added_epanet_mcp": {
                "command": "python", "transport": "stdio",
                "args": ["added_epanet_mcp.py"]
            },

            # =====================================================================
            # ADDED: Math — Mathematical & Statistical Operations
            # =====================================================================
            "added_math_mcp": {
                "command": "python", "transport": "stdio",
                "args": ["added_math_mcp.py"]
            },
        }
    )

    tools = await client.get_tools()
    print("\n===== Available Tools (Existing + Added: 3 archives) =====")
    print(f"Total tools: {len(tools)}")
    for tool in tools:
        print(f"  - {tool.name}")
    print("=" * 60)

    agent = create_react_agent(
        model,
        tools=tools,
        prompt="""You are an expert in interdependent infrastructure networks, geospatial analysis, power systems simulation, and graph theory. Solve problems step by step using the provided tools.
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
1. Don't create files that don't exist yourself. Use the tools provided.
2. Before all actions begin, first plan the overall execution steps.
Begin!""")

    TIMEOUT_SECONDS = 180

    df = pd.read_excel("mcp tool chains.xlsx")
    descriptions = df["Task"].tolist()
    Tool_Chain = df["Tool_Chain"].tolist()

    output_path = "MCP_agent_response_deepseek_with_3_added_archives.xlsx"

    if os.path.exists(output_path):
        output_df = pd.read_excel(output_path)
    else:
        output_df = df.copy()
        output_df["agent_response"] = [""] * len(output_df)

    for i, desc in enumerate(descriptions):
        print(f"\n====== Running Task {i + 1}/{len(descriptions)}: ======\n{desc}\n")

        combined_input = (
            f"You are working on task index {i}.\n"
            f"Task description: {desc}\n\n"
            f"Tools for you to solve that task: {Tool_Chain[i]}\n"
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
            print(f"\nTask {i + 1} timed out after {TIMEOUT_SECONDS}s. Skipping.\n")
            output = f"Task skipped due to timeout ({TIMEOUT_SECONDS}s)."
        except GraphRecursionError:
            print(f"\nTask {i + 1} reached recursion limit. Skipping.\n")
            output = "Task skipped due to recursion limit."

        output_df.at[i, "agent_response"] = output
        output_df.to_excel(output_path, index=False)
        print(f"\nTask {i + 1} response written to '{output_path}'\n")


if __name__ == "__main__":
    asyncio.run(main())
