from mcp.server.fastmcp import FastMCP
from identify_critical_facilities_considering_betweenness import identify_critical_facilities_considering_betweenness
from identify_critical_facilities_considering_closeness  import identify_critical_facilities_considering_closeness
from identify_critical_facilities_considering_degree import identify_critical_facilities_considering_degree
from identify_critical_facilities_considering_katz  import identify_critical_facilities_considering_katz
from identify_critical_facilities_considering_kshell import identify_critical_facilities_considering_kshell
from identify_critical_facilities_considering_pagerank import identify_critical_facilities_considering_pagerank

mcp = FastMCP(name="critical infrastructure facility identifying")
mcp.add_tool(identify_critical_facilities_considering_betweenness,
             name="identify_critical_facilities_considering_betweenness",
             description="This tool is to identify relative more important facility using betweenness centrality. It reads the interdependent infrastructure network  in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs  the betweenness centrality-based facility importance of nodes in facility_importance_using_betweenness_centrality.json saved in Global_Data.json. If this function runs, you could observe the facility betweenness centrality information path in Global_Data.json"           )
mcp.add_tool(identify_critical_facilities_considering_closeness,
             name="identify_critical_facilities_considering_closeness",
             description="This tool is to identify relative more important facility using closeness centrality. It reads the interdependent infrastructure network  in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs  the closeness centrality-based facility importance of nodes in facility_importance_using_closeness_centrality.json saved in Global_Data.json. If this function runs, you could observe the facility closeness centrality information path in Global_Data.json")
mcp.add_tool(identify_critical_facilities_considering_degree,
             name="midentify_critical_facilities_considering_degree",
             description="This tool is to identify relative more important facility using degree centrality. It reads the interdependent infrastructure network  in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs  the degree centrality-based facility importance of nodes in facility_importance_using_degree_centrality.json saved in Global_Data.json. If this function runs, you could observe the facility degree centrality information path in Global_Data.json")
mcp.add_tool(identify_critical_facilities_considering_katz,
             name="identify_critical_facilities_considering_katz",
             description="This tool is to identify relative more important facility using katz centrality. It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs  the katz centrality-based facility importance of nodes in facility_importance_using_katz_centrality.json saved in Global_Data.json. If this function runs, you could observe the facility katz centrality information path in Global_Data.json")
mcp.add_tool(identify_critical_facilities_considering_kshell,
             name="identify_critical_facilities_considering_kshell",
             description="This tool is to identify relative more important facility using kshell centrality. It reads the interdependent infrastructure network  in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs  the kshell-based facility importance of nodes in facility_importance_using_kshell.json saved in Global_Data.json. If this function runs, you could observe the facility kshell information path in Global_Data.json")
mcp.add_tool(identify_critical_facilities_considering_pagerank,
             name="identify_critical_facilities_considering_pagerank",
             description="This tool is to identify relative more important facility using pagerank centrality. It reads the interdependent infrastructure network  in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs  the pagerank-based facility importance of nodes in facility_importance_using_pagerank.json saved in Global_Data.json. If this function runs, you could observe the facility pagerank information path in Global_Data.json")

mcp.run(transport="stdio")