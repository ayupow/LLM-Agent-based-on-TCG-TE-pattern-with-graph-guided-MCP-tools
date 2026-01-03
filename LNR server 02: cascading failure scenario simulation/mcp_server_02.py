from mcp.server.fastmcp import FastMCP
from simulate_failure_scenario_under_random_attacks import simulate_failure_scenario_under_random_attacks
from simulate_failure_scenario_under_specific_nodes_targeted_attacks import simulate_failure_scenario_under_specific_nodes_targeted_attacks
from simulate_failure_scenario_under_danger_area_targeted_attacks import simulate_failure_scenario_under_danger_area_targeted_attacks
from simulate_failure_scenario_using_FMEA_analysis import simulate_failure_scenario_using_FMEA_analysis
from simulate_failure_scenario_using_overload_propagation import simulate_failure_scenario_using_overload_propagation

mcp = FastMCP(name="cascading failure scenario simulating")
mcp.add_tool(simulate_failure_scenario_under_specific_nodes_targeted_attacks,
    name="simulate_failure_scenario_under_specific_nodes_targeted_attacks",
    description="This tool is to simulate cascading failures in interdependent urban lifeline networks under big nods-targeted attacks. It reads the interdependent infrastructure network and facilities importance in facility_importance_using_betweenness_centrality.json OR facility_importance_using_closeness_centrality.json OR facility_importance_using_degree_centrality.json OR facility_importance_using_katz_centrality.json OR facility_importance_using_kshell.json OR facility_importance_using_pagerank.json from Global_Data.json as input (BASED ON THE QUESTION). It outputs the affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures saved to cascading_failure_identification_under_big_nodes_attacks.json, and the path to this file is updated in `Global_Data.json`. If this function is run, you could observe the pathes of affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures in Global_Data.json"
             )
mcp.add_tool(simulate_failure_scenario_under_random_attacks,
    name="simulate_failure_scenario_under_random_attacks",
    description="This tool is to simulate cascading failures in interdependent urban lifeline networks under random attacks. It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs the affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures saved in cascading_failure_identification_under_random_attacks.json, and the path to this file is updated in `Global_Data.json`. If this function runs, you could observe the paths of affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures in Global_Data.json" )

mcp.add_tool(simulate_failure_scenario_under_danger_area_targeted_attacks,
    name="simulate_failure_scenario_under_danger_area_targeted_attacks",
    description="This tool is to simulate cascading failures in interdependent urban lifeline networks under dangerous area-targeted attacks. It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs the affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures saved to cascading_failure_identification_under_danger_area_targeted_attacks.json, and the path to this file is updated in `Global_Data.json`. If this function is run, you could observe the pathes of affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures in Global_Data.json"
             )
mcp.add_tool(simulate_failure_scenario_using_FMEA_analysis,
    name="simulate_failure_scenario_using_FMEA_analysis",
    description="This tool is to simulate cascading failures in interdependent urban lifeline networks by using Failure Modes and Effects Analysis (FMEA). It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs the affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures saved in cascading_failure_identification_using_FMEA_analysis.json, and the path to this file is updated in `Global_Data.json`. If this function runs, you could observe the paths of affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures in Global_Data.json" )

mcp.add_tool(simulate_failure_scenario_using_overload_propagation,
    name="simulate_failure_scenario_using_overload_propagation",
    description="This tool is to simulate cascading failures in interdependent urban lifeline networks by using overload spread analysis. It reads the interdependent infrastructure network in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs the affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures saved in cascading_failure_identification_using_overload_propagation.json, and the path to this file is updated in `Global_Data.json`. If this function runs, you could observe the paths of affected facilities due to cascading failures and the interdependent infrastructure networks with cascading failures in Global_Data.json."
             )

mcp.run(transport="stdio")