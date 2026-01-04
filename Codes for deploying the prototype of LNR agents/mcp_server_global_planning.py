from mcp.server.fastmcp import FastMCP
from list_all_tools import list_all_tools
from load_tool_graph import load_tool_graph
from retrieve_relevant_tools_aliyun import retrieve_relevant_tools_aliyun

mcp = FastMCP(name="global_task_planning")
mcp.add_tool(list_all_tools,
    name="list_all_tools",
    description="This tool is used to find all candidate tools from MCP_server_01 to MCP_server_N, it should be used firstly to plan the task."
             )
mcp.add_tool(load_tool_graph,
    name="load_tool_graph",
    description="This tool is used to load the external knowledge stores as a knowledge graph for planning the tasks, it should be used secondly to plan the task."
             )
mcp.add_tool(retrieve_relevant_tools_aliyun,
    name="retrieve_relevant_tools",
    description="This tool is used to find most relevant tools for each task, it should be used thirdly to plan the task."
             )
mcp.run(transport="stdio")