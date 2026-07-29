
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

model = ChatOpenAI(model_name="gpt-5", openai_api_key=api_key, openai_api_base=URL)


def auto_update_knowledge_graph(kg_file='KGoLNR_original.json', schema_file='KGoLNR_schema_level.txt',
                                 readme_files=None, output_file='KGoLNR_updated.json'):
    if readme_files is None:
        readme_files = ['README_gis_servers.md', 'README_networkx_server.md',
                        'README_powermcp_server.md', 'README_math_server.md', 'README_epanet_server.md']
    with open(kg_file, 'r', encoding='utf-8-sig') as f: original_kg = json.load(f)
    with open(schema_file, 'r', encoding='utf-8') as f: schema_content = f.read()
    readme_contents = {}
    for rf in readme_files:
        try:
            with open(rf, 'r', encoding='utf-8') as f: readme_contents[rf] = f.read()
        except FileNotFoundError: print(f"  [WARN] README not found: {rf}")
    readme_summary = "".join(f"\n=== {n} ===\n{c[:3000]}\n" for n,c in readme_contents.items())
    existing_tools = set()
    for item in original_kg:
        existing_tools.add(item["p"]["start"]["properties"]["name"])
        existing_tools.add(item["p"]["end"]["properties"]["name"])

    kg_update_prompt = PromptTemplate(
        input_variables=["schema", "readme_summary", "existing_tools"],
        template="""You are a knowledge graph engineer. Analyze MCP server READMEs and propose new tool nodes for KGoLNR.

=== KG SCHEMA ===
{schema}

=== EXISTING TOOLS (DO NOT duplicate) ===
{existing_tools}

=== SERVER READMEs ===
{readme_summary}

Output a JSON array of new KG entries:
```json
[{{"p": {{"start": {{"identity": -1, "labels": ["tool"], "properties": {{"name": "existing_tool"}}}}, "end": {{"identity": -1, "labels": ["tool"], "properties": {{"name": "new_tool"}}}}, "segments": [], "length": 1.0}}}}]
```
IMPORTANT: Only output the JSON array. No duplicate tool names. Max 50 entries.
""")
    print("\n" + "=" * 60)
    print("STEP 0: Auto-Updating Knowledge Graph from Server READMEs ...")
    chain = LLMChain(llm=model, prompt=kg_update_prompt)
    llm_response = chain.run(schema=schema_content, readme_summary=readme_summary,
                              existing_tools=", ".join(sorted(existing_tools))).strip()
    try:
        if "```json" in llm_response:
            llm_response = llm_response[llm_response.index("```json")+7:llm_response.index("```", llm_response.index("```json")+7)]
        elif "```" in llm_response:
            llm_response = llm_response[llm_response.index("```")+3:llm_response.index("```", llm_response.index("```")+3)]
        new_entries = json.loads(llm_response)
        print(f"  LLM proposed {len(new_entries)} new entries.")
    except json.JSONDecodeError: print("  [WARN] JSON parse failed."); new_entries = []
    added = 0
    for entry in new_entries:
        try:
            sn, en = entry["p"]["start"]["properties"]["name"], entry["p"]["end"]["properties"]["name"]
            if not any(it["p"]["start"]["properties"]["name"]==sn and it["p"]["end"]["properties"]["name"]==en for it in original_kg):
                original_kg.append(entry); added += 1
        except (KeyError, TypeError): continue
    print(f"  Added {added} new entries. Total: {len(original_kg)}")
    with open(output_file, 'w', encoding='utf-8') as f: json.dump(original_kg, f, indent=2, ensure_ascii=False)
    return output_file


def load_and_generate_tool_graph(input_json_file='KGoLNR_updated.json'):
    with open(input_json_file, 'r', encoding='utf-8-sig') as f: data = json.load(f)
    rels = []
    for it in data:
        if "Server" in it["p"]["start"].get("labels", []) or "Server" in it["p"]["end"].get("labels", []):
            continue
        rels.append((it["p"]["start"]["properties"]["name"], it["p"]["end"]["properties"]["name"]))
    def build(rels):
        chains = [[s,e] for s,e in rels if s=="convert_SHPfile_to_JSONfile"]
        for _ in range(3,6):
            new_c = []
            for c in chains:
                for s,e in rels:
                    if c[-1]==s: new_c.append(c+[e])
            chains.extend(new_c)
        return [list(c) for c in set(tuple(c) for c in chains)]
    chains = build(rels)
    print(f"Tool chains from updated KG: {len(chains)}")
    return [{"chain_id": i+1, "chain": c} for i,c in enumerate(chains)], chains


def build_chain_retriever(chains):
    texts = [" -> ".join(c) for c in chains]
    emb = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key, openai_api_base=URL)
    return FAISS.from_texts(texts, emb), texts


def retrieve_best_chain(task, vs, texts, k=1):
    docs = vs.similarity_search(task, k=k)
    return docs[0].page_content if docs else (texts[0] if texts else "")


async def main():
    updated_kg = auto_update_knowledge_graph(output_file='KGoLNR_updated_L7.json')
    _, raw_chains = load_and_generate_tool_graph(updated_kg)
    vs, chain_texts = build_chain_retriever(raw_chains)

    client = MultiServerMCPClient({
        "data processing": {"command":"python","transport":"stdio","args":["mcp_server_01.py"]},
        "critical infrastructure facility identifying": {"command":"python","transport":"stdio","args":["mcp_server_02.py"]},
        "cascading failure_scenario simulating": {"command":"python","transport":"stdio","args":["mcp_server_03.py"]},
        "failed facility restoration scheduling": {"command":"python","transport":"stdio","args":["mcp_server_04.py"]},
        "emergency portable equipment deploying": {"command":"python","transport":"stdio","args":["mcp_server_05.py"]},
        "failed facility restoration resource allocating": {"command":"python","transport":"stdio","args":["mcp_server_06.py"]},
        "failed and recovered ULS performance comparing": {"command":"python","transport":"stdio","args":["mcp_server_07.py"]},
        "added_gis_data_L7": {"command":"python","transport":"stdio","args":["added_gis_data_L7.py"]},
        "added_gis_geopandas_L7": {"command":"python","transport":"stdio","args":["added_gis_geopandas_L7.py"]},
        "added_gis_pyproj_L7": {"command":"python","transport":"stdio","args":["added_gis_pyproj_L7.py"]},
        "added_gis_pysal_L7": {"command":"python","transport":"stdio","args":["added_gis_pysal_L7.py"]},
        "added_gis_rasterio_L7": {"command":"python","transport":"stdio","args":["added_gis_rasterio_L7.py"]},
        "added_gis_shapely_L7": {"command":"python","transport":"stdio","args":["added_gis_shapely_L7.py"]},
        "added_gis_utilities_L7": {"command":"python","transport":"stdio","args":["added_gis_utilities_L7.py"]},
        "added_gis_visualize_L7": {"command":"python","transport":"stdio","args":["added_gis_visualize_L7.py"]},
        "added_math_L7": {"command":"python","transport":"stdio","args":["added_math_L7.py"]},
        "added_networkx_L7": {"command":"python","transport":"stdio","args":["added_networkx_L7.py"]},
        "added_powerfactory_L7": {"command":"python","transport":"stdio","args":["added_powerfactory_L7.py"]},
    })
    tools = await client.get_tools()
    print(f"\nAvailable tools: {len(tools)}")
    for t in tools: print(f"- {t.name}")

    agent = create_react_agent(tools=tools, model=model)
    df = pd.read_excel("mcp tool chains_test.xlsx")
    descriptions = df["Task"].tolist()
    output_path = "MCP_agent_response_L7_209tools_autoupdate.xlsx"
    output_df = pd.read_excel(output_path) if os.path.exists(output_path) else df.copy()
    if "agent_response" not in output_df.columns: output_df["agent_response"] = [""]*len(output_df)
    if "retrieved_chain" not in output_df.columns: output_df["retrieved_chain"] = [""]*len(output_df)

    for i, desc in enumerate(descriptions):
        print(f"\n====== Task {i+1}: {desc[:50]}... ======")
        best_chain = retrieve_best_chain(desc, vs, chain_texts)
        combined = f"Task {i}. {desc}\n\nSuggested chain (auto-updated KG): {best_chain}\n"
        try:
            resp = await asyncio.wait_for(agent.ainvoke({"messages":[HumanMessage(content=combined)]}, config={"recursion_limit":25}), timeout=180)
            output = str(resp).replace("\\n","\n") if not isinstance(resp,str) else resp
            print("===== Response =====\n", output[:500])
        except asyncio.TimeoutError: output = "Timeout (180s)."
        except GraphRecursionError: output = "Recursion limit."
        except Exception as e: output = f"Error: {e}."
        output_df.at[i, "agent_response"] = output
        output_df.at[i, "retrieved_chain"] = best_chain
        output_df.to_excel(output_path, index=False)

if __name__ == "__main__":
    asyncio.run(main())
