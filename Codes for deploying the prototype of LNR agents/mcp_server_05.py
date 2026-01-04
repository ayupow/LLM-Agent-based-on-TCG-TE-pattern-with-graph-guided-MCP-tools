from evaluate_ULS_performance_by_average_path_length import evaluate_ULS_performance_by_average_path_length
from evaluate_ULS_performance_by_connectivily import evaluate_ULS_performance_by_connectivily
from evaluate_ULS_performance_by_diameter import evaluate_ULS_performance_by_diameter
from evaluate_ULS_performance_by_global_network_efficiency import evaluate_ULS_performance_by_global_network_efficiency
from evaluate_ULS_performance_by_node_reachability import evaluate_ULS_performance_by_node_reachability
from evaluate_ULS_performance_by_population_betweenness import evaluate_ULS_performance_by_population_betweenness
from evaluate_ULS_performance_by_population_katz import evaluate_ULS_performance_by_population_katz
from evaluate_ULS_performance_by_population_closeness import evaluate_ULS_performance_by_population_closeness
from evaluate_ULS_performance_by_population_degree import evaluate_ULS_performance_by_population_degree
from evaluate_ULS_performance_by_population_kshell import evaluate_ULS_performance_by_population_kshell
from evaluate_ULS_performance_by_population_pagerank import evaluate_ULS_performance_by_population_pagerank


from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="failed and recovered ULS performance comparing")

mcp.add_tool(evaluate_ULS_performance_by_average_path_length,
    name="evaluate_ULS_performance_by_average_path_length",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by average path length under random attacks. It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs the average path length of the interdependent infrastructure network before and after ramdom attacks in evaluate_ULS_performance_by_average_path_length.json,  and the path to this file is updated in `Global_Data.json'. If this function is run, you could observe the path of evaluate_ULS_performance_by_average_path_length in Global_Data.json"
             )
mcp.add_tool(evaluate_ULS_performance_by_connectivily,
    name="evaluate_ULS_performance_by_connectivily",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by connectivity under random attacks.It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs the ratio of the proportion of nodes in the largest connected subgraph after removing certain nodes or connections to the proportion of nodes in the largest connected subgraph of the original network in evaluate_ULS_performance_by_connectivity.json, and the path to this file is updated in `Global_Data.json'. If this function is run, you could observe the path of evaluate_ULS_performance_by_connectivity in Global_Data.json"
             )
mcp.add_tool(evaluate_ULS_performance_by_diameter,
    name="evaluate_ULS_performance_by_diameter",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by diameter under random attacks. It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs the ratio of the diameter of the largest weakly connected component before and after ramdom attacks in evaluate_ULS_performance_by_diameter.json, and the path to this file is updated in `Global_Data.json'.If this function is run, you could observe the path of evaluate_ULS_performance_by_diameter in Global_Data.json"
             )
mcp.add_tool(evaluate_ULS_performance_by_global_network_efficiency,
    name="evaluate_ULS_performance_by_global_network_efficiency",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by global_network_efficiency under random attacks.It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs the global_network_efficiency under random attacks in evaluate_ULS_performance_by_global_network_efficiency.json,  and the path to this file is updated in `Global_Data.json'.If this function is run, you could observe the path of evaluate_ULS_performance_by_global_network_efficiency in Global_Data.json"
             )
mcp.add_tool(evaluate_ULS_performance_by_node_reachability,
    name="evaluate_ULS_performance_by_node_reachability",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by node_reachability under random attacks. It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs the ratio of the proportion of pairs that can reach each other before and after ramdom attacks in evaluate_ULS_performance_by_node_reachability.json, and the path to this file is updated in `Global_Data.json'. If this function is run, you could observe the path of evaluate_ULS_performance_by_node_reachability in Global_Data.json"
             )
mcp.add_tool(evaluate_ULS_performance_by_population_betweenness,
    name="evaluate_ULS_performance_by_population_betweenness",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by calculating the served population during recovery. The recovery order is determined based on node importance ranked by betweenness centrality. It reads the network information from interdependent_infrastructure_networks.json and the population data from population_data.json, and cascading_failure_identification_under_random_attacks.json from Global_Data.json as input. It outputs the calculated served population which are saved to evaluate_ULS_performance_by_population_betweenness_centrality.json and Global_Data.json is updated with the path to this file. If this function runs, you can observe the assessment file path in Global_Data.json."
             )
mcp.add_tool(evaluate_ULS_performance_by_population_katz,
    name="evaluate_ULS_performance_by_population_katz",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by calculating the served population during recovery. The recovery order is determined based on node importance ranked by katz centrality. It reads the network information from interdependent_infrastructure_networks.json and the population data from population_data.json, and cascading_failure_identification_under_random_attacks.json from Global_Data.json as input. It outputs the calculated served population which are saved to evaluate_ULS_performance_by_population_katz_centrality.json and Global_Data.json is updated with the path to this file. If this function runs, you can observe the assessment file path in Global_Data.json."
             )
mcp.add_tool(evaluate_ULS_performance_by_population_closeness,
    name="evaluate_ULS_performance_by_population_closeness",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by calculating the served population during recovery. The recovery order is determined based on node importance ranked by closeness centrality. It reads the network information from interdependent_infrastructure_networks.json and the population data from population_data.json, and cascading_failure_identification_under_random_attacks.json from Global_Data.json as input. It outputs the calculated served population which are saved to evaluate_ULS_performance_by_population_closeness_centrality.json and Global_Data.json is updated with the path to this file. If this function runs, you can observe the assessment file path in Global_Data.json."
             )
mcp.add_tool(evaluate_ULS_performance_by_population_degree,
    name="evaluate_ULS_performance_by_population_degree",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by calculating the served population during recovery. The recovery order is determined based on node importance ranked by degree centrality. It reads the network information from interdependent_infrastructure_networks.json and the population data from population_data.json, and cascading_failure_identification_under_random_attacks.json from Global_Data.json as input. It outputs the calculated served population which are saved to evaluate_ULS_performance_by_population_degree_centrality.json and Global_Data.json is updated with the path to this file. If this function runs, you can observe the assessment file path in Global_Data.json."
             )
mcp.add_tool(evaluate_ULS_performance_by_population_kshell,
    name="evaluate_ULS_performance_by_population_kshell",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by calculating the served population during recovery. The recovery order is determined based on node importance ranked by kshell centrality. It reads the network information from interdependent_infrastructure_networks.json and the population data from population_data.json, and cascading_failure_identification_under_random_attacks.json from Global_Data.json as input. It outputs the calculated served population which are saved to evaluate_ULS_performance_by_population_kshell.json and Global_Data.json is updated with the path to this file. If this function runs, you can observe the assessment file path in Global_Data.json."
             )
mcp.add_tool(evaluate_ULS_performance_by_population_pagerank,
    name="evaluate_ULS_performance_by_population_pagerank",
    description="This tool is to compare the performance of failed and recovered urban lifeline systems by calculating the served population during recovery. The recovery order is determined based on node importance ranked by pagerank centrality. It reads the network information from interdependent_infrastructure_networks.json and the population data from population_data.json, and cascading_failure_identification_under_random_attacks.json from Global_Data.json as input. It outputs the calculated served population which are saved to evaluate_ULS_performance_by_population_pagerank.json and Global_Data.json is updated with the path to this file. If this function runs, you can observe the assessment file path in Global_Data.json."
             )

mcp.run(transport="stdio")