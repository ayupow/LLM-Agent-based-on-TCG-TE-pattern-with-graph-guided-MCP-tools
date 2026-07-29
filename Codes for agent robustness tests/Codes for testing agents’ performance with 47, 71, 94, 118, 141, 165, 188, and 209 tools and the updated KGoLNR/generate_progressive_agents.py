# Generate 7 progressive agent .py files with increasing tool counts
# Level 1-7: 71, 94, 118, 141, 165, 188, 212 tools (from 47 existing)
import os, random, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
random.seed(42)

# Existing servers & tool counts (unchanged)
EXISTING_SERVERS = {
    "data processing":                        ("mcp_server_01.py", 7),
    "critical infrastructure facility identifying": ("mcp_server_02.py", 6),
    "cascading failure_scenario simulating":        ("mcp_server_03.py", 5),
    "failed facility restoration scheduling":       ("mcp_server_04.py", 10),
    "emergency portable equipment deploying":       ("mcp_server_05.py", 3),
    "failed facility restoration resource allocating": ("mcp_server_06.py", 5),
    "failed and recovered ULS performance comparing":  ("mcp_server_07.py", 11),
}
EXISTING_TOOLS = sum(t[1] for t in EXISTING_SERVERS.values())  # 47

# Available tool directories and their tool files
TOOL_DIRS = {}
for d in os.listdir(BASE):
    if d.startswith('tools_') and os.path.isdir(os.path.join(BASE, d)):
        server_name = d.replace('tools_', '')  # e.g. tools_gis_geopandas -> gis_geopandas
        tools = [f[:-3] for f in os.listdir(os.path.join(BASE, d))
                 if f.endswith('.py') and not f.startswith('_')]
        if tools:
            TOOL_DIRS[server_name] = tools

# Ordered server pool
SERVER_NAMES = sorted(TOOL_DIRS.keys())
print(f"Available servers: {len(SERVER_NAMES)}, total tools: {sum(len(v) for v in TOOL_DIRS.values())}")

# Only use working servers (epanet excluded - needs epyt package not installed)
WORKING_SERVERS = {k: v for k, v in TOOL_DIRS.items() if k != 'epanet'}
SERVER_NAMES = sorted(WORKING_SERVERS.keys())
TOOL_DIRS.clear(); TOOL_DIRS.update(WORKING_SERVERS)

# Target levels
TARGETS = [71, 94, 118, 141, 165, 188, 209]  # 209 = max with available packages

def generate_level(level, target_total):
    """Randomly select servers+tools to reach target_total."""
    needed = target_total - EXISTING_TOOLS
    available_servers = list(SERVER_NAMES)
    random.shuffle(available_servers)

    # Select servers until we have enough tools
    selected = {}  # server_name -> list of tool names
    collected = 0
    for srv in available_servers:
        all_tools = TOOL_DIRS[srv][:]
        random.shuffle(all_tools)
        # Take a random subset (at least 1 tool, at most all)
        take = random.randint(min(3, len(all_tools)), len(all_tools))
        take = min(take, needed - collected)  # don't exceed target
        if take <= 0:
            continue
        selected[srv] = sorted(all_tools[:take])
        collected += take
        if collected >= needed:
            break

    # If still short, add more tools from already-selected servers
    if collected < needed:
        for srv in list(selected.keys()):
            remaining = [t for t in TOOL_DIRS[srv] if t not in selected[srv]]
            random.shuffle(remaining)
            extra = needed - collected
            if extra <= 0: break
            add = min(extra, len(remaining))
            if add > 0:
                selected[srv].extend(remaining[:add])
                collected += add

    actual_total = EXISTING_TOOLS + collected
    return selected, actual_total


def write_server_file(server_name, tool_names, suffix):
    """Write a server .py file exposing only the selected tools."""
    srv_display = server_name.replace('_', ' ')
    fname = f"added_{server_name}_{suffix}.py"
    lines = [f'# added_{server_name}_{suffix} — MCP Server (subset for level {suffix})',
             f'from mcp.server.fastmcp import FastMCP', '']

    for t in tool_names:
        lines.append(f'from {t} import {t}')

    lines.append('')
    lines.append(f'mcp = FastMCP(name="added_{server_name}_{suffix}")')
    lines.append('')

    for t in tool_names:
        lines.append(f'mcp.add_tool({t},')
        lines.append(f'    name="{t}",')
        lines.append(f'    description="Tool: {t} (from {srv_display} server)."')
        lines.append(')')
        lines.append('')

    lines.append('if __name__ == "__main__":')
    lines.append('    mcp.run(transport="stdio")')
    lines.append('')

    path = os.path.join(BASE, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return fname


def write_agent_file(level, target, selected, suffix):
    """Write the agent .py file for this level."""
    fname = f"LNR agents based on TCG-TE pattern driven by GPT-5 (L{level}_{target}tools).py"

    actual = EXISTING_TOOLS + sum(len(v) for v in selected.values())
    server_count = len(EXISTING_SERVERS) + len(selected)

    lines = []
    lines.append(f'# LNR Agents based on TCG-TE Pattern driven by GPT-5 / Claude')
    lines.append(f'# Level {level}: {actual} tools, {server_count} servers')
    lines.append(f'# Existing: {EXISTING_TOOLS} tools (7 servers) + Added: {actual - EXISTING_TOOLS} tools ({len(selected)} servers)')
    lines.append('')
    lines.append('from mcp import ClientSession, StdioServerParameters')
    lines.append('from mcp.client.stdio import stdio_client')
    lines.append('from langchain_openai import ChatOpenAI')
    lines.append('from langchain.agents import Tool, initialize_agent, AgentType')
    lines.append('from langchain_deepseek import ChatDeepSeek')
    lines.append('from langchain.prompts import PromptTemplate')
    lines.append('import os')
    lines.append('from langchain_mcp_adapters.client import MultiServerMCPClient')
    lines.append('from langgraph.prebuilt import create_react_agent')
    lines.append('from langchain_fireworks import ChatFireworks')
    lines.append('import asyncio')
    lines.append('import pandas as pd')
    lines.append('from langchain.schema import HumanMessage')
    lines.append('from langgraph.errors import GraphRecursionError')
    lines.append('import warnings')
    lines.append('warnings.filterwarnings("ignore")')
    lines.append('warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")')
    lines.append('warnings.filterwarnings("ignore", category=DeprecationWarning)')
    lines.append('')
    lines.append('os.environ["OPENAI_API_KEY"] = "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"')
    lines.append('os.environ["DEEPSEEK_API_KEY"] = "sk-52ed0fadee5d48d5adf4ef46fd65896e"')
    lines.append('deepseek_api_key = os.environ["DEEPSEEK_API_KEY"]')
    lines.append('api_key = "sk-y5taN0t1fLrciE4Qy0Qb9MYkwOWqingTOlcqZ7Gmiv2VWvMg"')
    lines.append('URL = "https://chat.cloudapi.vip/v1"')
    lines.append('')
    lines.append('model = ChatOpenAI(')
    lines.append('    model_name="claude-sonnet-4-20250514-s",')
    lines.append('    openai_api_key=api_key,')
    lines.append('    openai_api_base=URL,')
    lines.append(')')
    lines.append('')
    lines.append('')
    lines.append('async def main():')
    lines.append('    client = MultiServerMCPClient(')
    lines.append('        {')

    # Existing servers
    for srv_name, (srv_file, _) in EXISTING_SERVERS.items():
        lines.append(f'            "{srv_name}": {{')
        lines.append(f'                "command": "python", "transport": "stdio",')
        lines.append(f'                "args": ["{srv_file}"]')
        lines.append(f'            }},')

    # Added servers (each with a level-specific file)
    for srv in sorted(selected.keys()):
        srv_display = srv.replace('_', ' ')
        srv_file = f"added_{srv}_{suffix}.py"
        lines.append(f'            "added_{srv}_{suffix}": {{')
        lines.append(f'                "command": "python", "transport": "stdio",')
        lines.append(f'                "args": ["{srv_file}"]')
        lines.append(f'            }},')

    lines.append('        }')
    lines.append('    )')
    lines.append('')
    lines.append('    tools = await client.get_tools()')
    lines.append('    print("\\nAvailable tools:")')
    lines.append('    for tool in tools:')
    lines.append('        print(f"- {tool.name}")')
    lines.append('')
    lines.append('    prompt_template = PromptTemplate(')
    lines.append('        input_variables=["input"],')
    lines.append('        template="""')
    lines.append('            You are an expert in urban lifeline system recovery, and your task is to solve the problem step by step using the provided tools.')
    lines.append('            __________________________________________________________________')
    lines.append('            To solve a task, please use the following format:')
    lines.append('            Thought: (reflect on your progress and decide what to do next)')
    lines.append('            Action: (the action name, should be one of the available tools)')
    lines.append('            Action Input: (a .JSON file name, default "Global_Data.json" if no specific input)')
    lines.append('            Observation: (the result of the action)')
    lines.append('            (this process can repeat)')
    lines.append('')
    lines.append('            OR')
    lines.append('')
    lines.append('            Thought: (review original question and check my total process)')
    lines.append('            Final Answer: (output the final answer to the original input question based on observation)')
    lines.append('            __________________________________________________________________')
    lines.append('            {input}')
    lines.append('            __________________________________________________________________')
    lines.append('            REMEMBER:')
    lines.append('            1. You can only respond with a single complete "Thought, Action, Action Input, Observation" format OR a single "Final Answer" format.')
    lines.append('            2. Do not create files that do not exist yourself.')
    lines.append('            3. Before all actions begin, you need to first plan the overall execution steps to complete the task.')
    lines.append('            Begin!"""')
    lines.append('    )')
    lines.append('')
    lines.append('    agent = create_react_agent(tools=tools, model=model)')
    lines.append('    TIMEOUT_SECONDS = 180')
    lines.append('')
    lines.append(f'    df = pd.read_excel("mcp tool chains_test.xlsx")')
    lines.append(f'    descriptions = df["Task"].tolist()')
    lines.append(f'    Tool_Chain = df["Tool_Chain"].tolist()')
    lines.append(f'    output_path = "MCP_agent_response_L{level}_{actual}tools.xlsx"')
    lines.append('')
    lines.append('    if os.path.exists(output_path):')
    lines.append('        output_df = pd.read_excel(output_path)')
    lines.append('    else:')
    lines.append('        output_df = df.copy()')
    lines.append('        output_df["agent_response"] = [""] * len(output_df)')
    lines.append('')
    lines.append('    for i, desc in enumerate(descriptions):')
    lines.append('        print(f"\\n====== Running Task {i + 1}: ======\\n{desc}\\n")')
    lines.append('        combined_input = (')
    lines.append('            f"You are working on task index {i}.\\n"')
    lines.append('            f"Task description: {desc}\\n\\n"')
    lines.append('            f"Tools for you to solve that task: {Tool_Chain[i]}\\n"')
    lines.append('        )')
    lines.append('        try:')
    lines.append('            response = await asyncio.wait_for(')
    lines.append('                agent.ainvoke(')
    lines.append('                    {"messages": [HumanMessage(content=combined_input)]},')
    lines.append('                    config={"recursion_limit": 25}')
    lines.append('                ),')
    lines.append('                timeout=TIMEOUT_SECONDS')
    lines.append('            )')
    lines.append('            output = str(response).replace("\\\\n", "\\n") if not isinstance(response, str) else response')
    lines.append('            print("\\n===== Response from Agent =====\\n"); print(output)')
    lines.append('        except asyncio.TimeoutError:')
    lines.append('            print(f"\\nTask {i + 1} timed out. Skipping.\\n")')
    lines.append('            output = f"Task skipped due to timeout ({TIMEOUT_SECONDS}s)."')
    lines.append('        except GraphRecursionError:')
    lines.append('            print(f"\\nTask {i + 1} reached recursion limit. Skipping.\\n")')
    lines.append('            output = "Task skipped due to recursion limit."')
    lines.append('        except Exception as e:')
    lines.append('            print(f"\\nTask {i + 1} unexpected error: {e}. Skipping.\\n")')
    lines.append('            output = f"Task skipped: {e}."')
    lines.append('        output_df.at[i, "agent_response"] = output')
    lines.append('        output_df.to_excel(output_path, index=False)')
    lines.append('        print(f"\\nTask {i + 1} response written to \'{output_path}\'\\n")')
    lines.append('')
    lines.append('if __name__ == "__main__":')
    lines.append('    asyncio.run(main())')
    lines.append('')

    path = os.path.join(BASE, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return fname


# === MAIN ===
if __name__ == '__main__':
    for level, target in enumerate(TARGETS, 1):
        suffix = f"L{level}"
        selected, actual = generate_level(level, target)

        # Write server files for this level
        srv_files = []
        for srv, tools in sorted(selected.items()):
            sf = write_server_file(srv, tools, suffix)
            srv_files.append(sf)

        # Write agent file
        af = write_agent_file(level, target, selected, suffix)

        added_tools = actual - EXISTING_TOOLS
        print(f"Level {level} (L{suffix}): target={target}, actual={actual} tools | "
              f"+{added_tools} added across {len(selected)} servers")
        for srv, tools in sorted(selected.items()):
            print(f"    {srv}: {len(tools)} tools -> {', '.join(tools[:4])}{'...' if len(tools)>4 else ''}")

    print(f"\nDone: {len(TARGETS)} levels generated")
