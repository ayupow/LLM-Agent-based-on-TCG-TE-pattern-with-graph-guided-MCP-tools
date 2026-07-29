

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_deepseek import ChatDeepSeek
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
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
    model_name="gpt-4.1",
    openai_api_key=api_key,
    openai_api_base=URL,
)


# ==========================================
# STEP 0: Auto-Update Knowledge Graph from Server READMEs
# ==========================================
def auto_update_knowledge_graph(kg_file='KGoLNR.json', schema_file='KGoLNR_schema_level.txt',
                                 readme_files=None, output_file='KGoLNR_updated.json'):
    """
    Use LLM to read server READMEs and KG schema, then propose new tool nodes
    and relationships to merge into the knowledge graph.
    Returns the path to the updated KG file.
    """
    if readme_files is None:
        readme_files = [
            'README_gis_servers.md',
            'README_networkx_server.md',
            'README_powermcp_server.md',
            'README_math_server.md',
            'README_epanet_server.md',
        ]

    # Read original KG
    with open(kg_file, 'r', encoding='utf-8-sig') as f:
        original_kg = json.load(f)

    # Read schema
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_content = f.read()

    # Read all READMEs
    readme_contents = {}
    for rf in readme_files:
        try:
            with open(rf, 'r', encoding='utf-8') as f:
                readme_contents[rf] = f.read()
        except FileNotFoundError:
            print(f"  [WARN] README file not found: {rf}, skipping.")

    # Build LLM prompt to propose new KG entries
    readme_summary = ""
    for name, content in readme_contents.items():
        # Only send first 3000 chars of each README to keep prompt manageable
        readme_summary += f"\n=== {name} ===\n{content[:3000]}\n"

    # Extract existing tool names for the LLM to avoid duplicates
    existing_tools = set()
    for item in original_kg:
        existing_tools.add(item["p"]["start"]["properties"]["name"])
        existing_tools.add(item["p"]["end"]["properties"]["name"])

    kg_update_prompt = PromptTemplate(
        input_variables=["schema", "readme_summary", "existing_tools"],
        template="""You are a knowledge graph engineer. Your task is to analyze MCP server README files and propose new tool nodes and relationships to enrich the existing Knowledge Graph of Lifeline Network Recovery (KGoLNR).

=== KNOWLEDGE GRAPH SCHEMA ===
{schema}

=== EXISTING TOOL NAMES (DO NOT duplicate these) ===
{existing_tools}

=== SERVER README CONTENTS ===
{readme_summary}

=== YOUR TASK ===
Based on the README files, identify NEW tools (not already in the existing tools list above) that would be useful for urban lifeline system recovery tasks (power, water, gas, transportation networks).

For each new tool, propose:
1. A meaningful tool name (snake_case, descriptive)
2. Which existing tool it should connect to (FEEDS relationship)

Output your proposals as a valid JSON array of KG entries, matching this exact format:

```json
[
  {{
    "p": {{
      "start": {{ "identity": -1, "labels": ["tool"], "properties": {{ "name": "existing_tool_name" }} }},
      "end": {{ "identity": -1, "labels": ["tool"], "properties": {{ "name": "new_tool_name" }} }},
      "segments": [],
      "length": 1.0
    }}
  }}
]
```

IMPORTANT RULES:
- DO NOT duplicate any tool name from the existing tools list
- Only output the JSON array, no other text
- Connect new tools to relevant existing tools via FEEDS relationships
- Focus on tools that support lifeline recovery workflows (simulation, analysis, optimization, visualization)
- Maximum 50 new entries
"""
    )

    print("\n" + "=" * 60)
    print("STEP 0: Auto-Updating Knowledge Graph from Server READMEs ...")
    print(f"  Existing tools in KG: {len(existing_tools)}")
    print(f"  README files to analyze: {len(readme_contents)}")

    chain = LLMChain(llm=model, prompt=kg_update_prompt)
    llm_response = chain.run(
        schema=schema_content,
        readme_summary=readme_summary,
        existing_tools=", ".join(sorted(existing_tools))
    ).strip()

    # Parse LLM JSON response
    try:
        # Extract JSON from possible markdown code block
        if "```json" in llm_response:
            json_start = llm_response.index("```json") + 7
            json_end = llm_response.index("```", json_start)
            llm_response = llm_response[json_start:json_end].strip()
        elif "```" in llm_response:
            json_start = llm_response.index("```") + 3
            json_end = llm_response.index("```", json_start)
            llm_response = llm_response[json_start:json_end].strip()

        new_entries = json.loads(llm_response)
        print(f"  LLM proposed {len(new_entries)} new KG entries.")
    except json.JSONDecodeError as e:
        print(f"  [WARN] Could not parse LLM response as JSON: {e}")
        print(f"  Response preview: {llm_response[:500]}...")
        new_entries = []

    # Merge new entries into original KG, avoiding duplicates
    added_count = 0
    for entry in new_entries:
        try:
            start_name = entry["p"]["start"]["properties"]["name"]
            end_name = entry["p"]["end"]["properties"]["name"]

            # Check if this relationship already exists
            exists = False
            for item in original_kg:
                if (item["p"]["start"]["properties"]["name"] == start_name and
                        item["p"]["end"]["properties"]["name"] == end_name):
                    exists = True
                    break

            if not exists:
                original_kg.append(entry)
                added_count += 1
        except (KeyError, TypeError):
            continue

    print(f"  Actually added {added_count} new entries (duplicates filtered).")
    print(f"  Updated KG: {len(original_kg)} total entries.")

    # Save updated KG
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(original_kg, f, indent=2, ensure_ascii=False)
    print(f"  Updated KG saved to: {output_file}")

    return output_file


# ==========================================
# TCG_tool: Dynamic Tool Chain Generation
# ==========================================
def load_and_generate_tool_graph(input_json_file='KGoLNR_updated.json'):
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
    print(f"Tool chains generated from UPDATED KG: {len(tool_chains)} unique chains extracted.")
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
    # --- Step 0: Auto-update Knowledge Graph from READMEs ---
    updated_kg_path = auto_update_knowledge_graph(
        kg_file='KGoLNR_original.json',
        schema_file='KGoLNR_schema_level.txt',
        readme_files=[
            'README_gis_servers.md',
            'README_networkx_server.md',
            'README_powermcp_server.md',
            'README_math_server.md',
            'README_epanet_server.md',
        ],
        output_file='KGoLNR_updated_L1.json'
    )

    # --- Step 1: Generate tool chains from UPDATED KG ---
    print("=" * 60)
    print("Step 1: Generating tool chains from UPDATED KGoLNR ...")
    numbered_chains, raw_chains = load_and_generate_tool_graph(updated_kg_path)
    vectorstore, chain_texts = build_chain_retriever(raw_chains)

    # --- Step 2: Connect to MCP servers (L1 config) ---
    print("=" * 60)
    print("Step 2: Connecting to MCP servers (L1: 10 servers, 71 tools) ...")
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
            "added_gis_pyproj_L1": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_pyproj_L1.py"]
            },
            "added_gis_pysal_L1": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_pysal_L1.py"]
            },
            "added_gis_visualize_L1": {
                "command": "python", "transport": "stdio",
                "args": ["added_gis_visualize_L1.py"]
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

    # --- Step 3: Read tasks and retrieve tool chains from UPDATED KG ---
    print("=" * 60)
    print("Step 3: Reading tasks and retrieving best matching tool chains ...")
    df = pd.read_excel("Task_for_client.xlsx")
    descriptions = df["Task"].tolist()
    output_path = "MCP_agent_response_L1_71tools_autoupdate.xlsx"

    if os.path.exists(output_path):
        output_df = pd.read_excel(output_path)
    else:
        output_df = df.copy()
        output_df["agent_response"] = [""] * len(output_df)
        output_df["retrieved_chain"] = [""] * len(output_df)

    for i, desc in enumerate(descriptions):
        print(f"\n====== Running Task {i + 1}: ======\n{desc}\n")

        best_chain = retrieve_best_chain(desc, vectorstore, chain_texts, k=1)
        print(f"  -> Retrieved chain (from auto-updated KG): {best_chain}")

        combined_input = (
            f"You are working on task index {i}.\n"
            f"Task description: {desc}\n\n"
            f"Suggested tool chain (from auto-updated Knowledge Graph): {best_chain}\n"
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
