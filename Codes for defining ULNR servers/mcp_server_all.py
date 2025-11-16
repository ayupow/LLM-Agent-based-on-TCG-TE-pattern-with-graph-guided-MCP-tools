from mcp.server.fastmcp import FastMCP
# server01
from convert_SHPfile_to_JSONfile import convert_SHPfile_to_JSONfile
from convert_CSVfile_to_JSONfile import convert_CSVfile_to_JSONfile
from convert_DBFfile_to_JSONfile import convert_DBFfile_to_JSONfile
from convert_DWGfile_to_JSONfile import convert_DWGfile_to_JSONfile
from convert_KMZfile_to_JSONfile import convert_KMZfile_to_JSONfile
from convert_RVTfile_to_JSONfile import convert_RVTfile_to_JSONfile
from generate_interdependence_across_networks import generate_interdependence_across_networks
# server02
from simulate_failure_scenario_under_random_attacks import simulate_failure_scenario_under_random_attacks
from simulate_failure_scenario_under_specific_nodes_targeted_attacks import simulate_failure_scenario_under_specific_nodes_targeted_attacks
from simulate_failure_scenario_under_danger_area_targeted_attacks import simulate_failure_scenario_under_danger_area_targeted_attacks
from simulate_failure_scenario_using_FMEA_analysis import simulate_failure_scenario_using_FMEA_analysis
from simulate_failure_scenario_using_overload_propagation import simulate_failure_scenario_using_overload_propagation
# server03
from identify_critical_facilities_considering_betweenness import identify_critical_facilities_considering_betweenness
from identify_critical_facilities_considering_closeness  import identify_critical_facilities_considering_closeness
from identify_critical_facilities_considering_degree import identify_critical_facilities_considering_degree
from identify_critical_facilities_considering_katz  import identify_critical_facilities_considering_katz
from identify_critical_facilities_considering_kshell import identify_critical_facilities_considering_kshell
from identify_critical_facilities_considering_pagerank import identify_critical_facilities_considering_pagerank
# server04
from schedule_restoration_sequence_considering_degree import schedule_restoration_sequence_considering_degree
from schedule_restoration_sequence_considering_kshell import schedule_restoration_sequence_considering_kshell
from schedule_restoration_sequence_considering_pagerank import schedule_restoration_sequence_considering_pagerank
from schedule_restoration_sequence_considering_betweenness import schedule_restoration_sequence_considering_betweenness
from schedule_restoration_sequence_considering_closeness import schedule_restoration_sequence_considering_closeness
from schedule_restoration_sequence_considering_katz import schedule_restoration_sequence_considering_katz
from schedule_restoration_sequence_considering_population_by_GA import schedule_restoration_sequence_considering_population_by_GA
from schedule_restoration_sequence_considering_population_by_SA import schedule_restoration_sequence_considering_population_by_SA
from schedule_restoration_sequence_considering_GSCC_by_GA import schedule_restoration_sequence_considering_GSCC_by_GA
from schedule_restoration_sequence_considering_GSCC_by_SA import schedule_restoration_sequence_considering_GSCC_by_SA
# server05
from deploy_portable_equipment_considering_connectivity import deploy_portable_equipment_considering_connectivity
from deploy_portable_equipment_considering_efficiency import deploy_portable_equipment_considering_efficiency
from deploy_portable_equipment_considering_population import deploy_portable_equipment_considering_population
# server06
from allocate_restoration_resource_considering_population import allocate_restoration_resource_considering_population
from allocate_restoration_resource_considering_time import allocate_restoration_resource_considering_time
from allocate_restoration_resource_considering_clustering_coefficient import allocate_restoration_resource_considering_clustering_coefficient
from allocate_restoration_resource_considering_cost import allocate_restoration_resource_considering_cost
from allocate_restoration_resource_considering_GSCC import allocate_restoration_resource_considering_GSCC

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

mcp = FastMCP(name="ULSR_master")

mcp.add_tool(convert_SHPfile_to_JSONfile,
    name="convert_SHPfile_to_JSONfile",
    description="This tool is to convert urban lifeline system data stores in SHP files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json "
             )
mcp.add_tool(convert_CSVfile_to_JSONfile,
    name="convert_CSVfile_to_JSONfile",
    description="This tool is to convert urban lifeline system data stores in CSV files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json This tool is to convert urban lifeline system data stores in CSV files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json "
             )
mcp.add_tool(convert_DBFfile_to_JSONfile,
    name="convert_DBFfile_to_JSONfile",
    description="This tool is to convert urban lifeline system data stores in DBF files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json This tool is to convert urban lifeline system data stores in CSV files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json "
                )
mcp.add_tool(convert_DWGfile_to_JSONfile,
    name="convert_DWGfile_to_JSONfile",
    description="This tool is to convert urban lifeline system data stores in DWG files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json This tool is to convert urban lifeline system data stores in CSV files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json "
                )
mcp.add_tool(convert_KMZfile_to_JSONfile,
    name="convert_KMZfile_to_JSONfile",
    description="This tool is to convert urban lifeline system data stores in KMZ files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json This tool is to convert urban lifeline system data stores in CSV files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json "
                )
mcp.add_tool(convert_RVTfile_to_JSONfile,
    name="convert_RVTfile_to_JSONfile",
    description="This tool is to convert urban lifeline system data stores in RVT files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json This tool is to convert urban lifeline system data stores in CSV files into networks in JSON format and save the networks. It reads the shpfile information in infrastructure_information.json from Global_Data.json as input. It outputs the infrastructure_networks.json saved in Global_Data.json.If this function runs, you could observe the network information path in Global_Data.json "
                )
mcp.add_tool(generate_interdependence_across_networks,
    name="generate_interdependence_across_networks",
    description="This tool is to generate interdependent infrastructure networks using service areas. It reads the network information in infrastructure_networks_S2.json from Global_Data.json as input.  It outputs the interdependent infrastructure network in interdependent_infrastructure_networks.json and saves the file in Global_Data.json. If this function runs, you could observe the interdependent network information path in Global_Data.json"
             )


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

mcp.add_tool(identify_critical_facilities_considering_betweenness,
             name="identify_critical_facilities_considering_betweenness",
             description="This tool is to identify relative more important facility using betweenness centrality. It reads the interdependent infrastructure network  in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs  the betweenness centrality-based facility importance of nodes in facility_importance_using_betweenness_centrality.json saved in Global_Data.json. If this function runs, you could observe the facility betweenness centrality information path in Global_Data.json"           )
mcp.add_tool(identify_critical_facilities_considering_closeness,
             name="identify_critical_facilities_considering_closeness",
             description="This tool is to identify relative more important facility using closeness centrality. It reads the interdependent infrastructure network  in interdependent_infrastructure_networks.json from Global_Data.json as input. It outputs  the closeness centrality-based facility importance of nodes in facility_importance_using_closeness_centrality.json saved in Global_Data.json. If this function runs, you could observe the facility closeness centrality information path in Global_Data.json")
mcp.add_tool(identify_critical_facilities_considering_degree,
             name="identify_critical_facilities_considering_degree",
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

mcp.add_tool(schedule_restoration_sequence_considering_degree,
    name="schedule_restoration_sequence_considering_degree",
    description="This tool generates a recovery strategy for interdependent infrastructure networks based on betweenness centrality. It reads the global data file to access the necessary input files, including the network topology, facility importance based on betweenness centrality, and failure information. The function prioritizes the restoration of failed nodes and their associated edges based on their betweenness centrality values. The recovery plan is outputted to recovery_sequence_of_betweenness_centrality.json, and the path to this output file is updated in the global data file. If the function is run, the restoration strategy for failed nodes will be generated and saved as specified."
             )
mcp.add_tool(schedule_restoration_sequence_considering_kshell,
    name="schedule_restoration_sequence_considering_kshell",
    description="This tool generates a recovery strategy for interdependent infrastructure networks based on kshell. It reads the global data file to access the necessary input files, including the network topology, facility importance based on kshell, and failure information. The function prioritizes the restoration of failed nodes and their associated edges based on their kshell values. The recovery plan is outputted to recovery_sequence_of_kshell.json, and the path to this output file is updated in the global data file. If the function is run, the restoration strategy for failed nodes will be generated and saved as specified."
             )
mcp.add_tool(schedule_restoration_sequence_considering_pagerank,
    name="schedule_restoration_sequence_considering_pagerank",
    description="This tool generates a recovery strategy for interdependent infrastructure networks based on pagerank. It reads the global data file to access the necessary input files, including the network topology, facility importance based on PageRank, and failure information. The function prioritizes the restoration of failed nodes and their associated edges based on their pagerank values. The recovery plan is outputted to recovery_sequence_of_pagerank.json, and the path to this output file is updated in the global data file. If the function is run, the restoration strategy for failed nodes will be generated and saved as specified."
             )
mcp.add_tool(schedule_restoration_sequence_considering_betweenness,
    name="schedule_restoration_sequence_considering_betweenness",
    description="This tool generates a recovery strategy for interdependent infrastructure networks based on betweenness centrality. It reads the global data file to access the necessary input files, including the network topology, facility importance based on betweenness centrality, and failure information. The function prioritizes the restoration of failed nodes and their associated edges based on their betweenness centrality values. The recovery plan is outputted to recovery_sequence_of_betweenness_centrality.json, and the path to this output file is updated in the global data file. If the function is run, the restoration strategy for failed nodes will be generated and saved as specified."
             )
mcp.add_tool(schedule_restoration_sequence_considering_closeness,
    name="schedule_restoration_sequence_considering_closeness",
    description="This tool generates a recovery strategy for interdependent infrastructure networks based on closeness_centrality. It reads the global data file to access the necessary input files, including the network topology, facility importance based on closeness_centrality, and failure information. The function prioritizes the restoration of failed nodes and their associated edges based on their closeness_centrality values. The recovery plan is outputted to recovery_sequence_of_closeness_centrality.json, and the path to this output file is updated in the global data file. If the function is run, the restoration strategy for failed nodes will be generated and saved as specified."
             )
mcp.add_tool(schedule_restoration_sequence_considering_katz,
    name="schedule_restoration_sequence_considering_katz",
    description="This tool generates a recovery strategy for interdependent infrastructure networks based on katz_centrality. It reads the global data file to access the necessary input files, including the network topology, facility importance based on katz, and failure information. The function prioritizes the restoration of failed nodes and their associated edges based on their katz values. The recovery plan is outputted to recovery_sequence_of_katz.json, and the path to this output file is updated in the global data file. If the function is run, the restoration strategy for failed nodes will be generated and saved as specified.)"
             )
mcp.add_tool(schedule_restoration_sequence_considering_population_by_GA,
    name="schedule_restoration_sequence_considering_population_by_GA",
    description="This tool generates a recovery strategy for infrastructure networks using a Genetic Algorithm based on the populations. It reads the network information from interdependent_infrastructure_networks. json and the population data from population_data. json as referenced in Global_Data. json, along with the list of failed nodes from cascading_failure_by_random_attacks. json as input. It outputs the recovery strategy to recovery_sequence_of_population_by_GA. json and saved in Global_Data.json. If this function runs, you can observe the recovery strategy file path in Global_Data.json.)"
             )
mcp.add_tool(schedule_restoration_sequence_considering_population_by_SA,
    name="schedule_restoration_sequence_considering_population_by_SA",
    description="This tool generates a recovery strategy for infrastructure networks using a Simulated Annealing based on the populations. It reads the network information from interdependent_infrastructure_networks. json and the population data from population_data. json as referenced in Global_Data. json, along with the list of failed nodes from cascading_failure_by_random_attacks.json.  It outpouts the recovery strategy is outputted to recovery_sequence_of_population_by_SA. json and saved in Global_Data.json.  If this function runs, you can observe the recovery strategy file path in Global_Data.json.)"
             )
mcp.add_tool(schedule_restoration_sequence_considering_GSCC_by_GA,
    name="schedule_restoration_sequence_considering_GSCC_by_GA",
    description="This tool generates a recovery strategy for infrastructure networks using a Genetic Algorithm based on the size of the GSCC. It reads the network information from interdependent_infrastructure_networks.json referenced in Global_Data.json and the failed nodes list from cascading_failure_by_random_attacks.json as input. It outputs the recovery strategy in recovery_sequence_of_GSCC_by_GA.json and saved in Global_Data.json. If this function runs, you can observe the recovery strategy file path in Global_Data.json.)"
             )
mcp.add_tool(schedule_restoration_sequence_considering_GSCC_by_SA,
    name="schedule_restoration_sequence_considering_GSCC_by_SA",
    description="This tool generates a recovery sequence for failed nodes in infrastructure networks using Simulated Annealing with the objective of maximizing the Giant Strongly Connected Component (GSCC) after recovery. It reads the network information from interdependent_infrastructure_networks.json referenced in Global_Data.json and the failed nodes list from cascading_failure_by_random_attacks.json as input. It outputs the recovery strategy in recovery_sequence_of_GSCC_by_SA.json and saved in Global_Data.json. If this function runs, you can observe the recovery strategy file path in Global_Data.json.)"
             )

mcp.add_tool(allocate_restoration_resource_considering_time,
    name="allocate_restoration_resource_considering_time",
    description="This tool calculates the daily resource allocation for each node to minimize the time. It reads data from Global_Data.json, including interdependent_infrastructure_networks_with_different_resource_demand, cascading_failure_identification_under_random_attacks.json, and resource_constraints.json. The tool outputs resource_allocation_considering_time.json and stores it in Global_Data.json.If the tool runs successfully, you will observe that resource_allocation_considering_time.json has been generated and stored in Global_Data.json."
             )
mcp.add_tool(allocate_restoration_resource_considering_GSCC,
    name="allocate_restoration_resource_considering_GSCC",
    description="This tool calculates the daily resource allocation for each node to maximize the GSCC. It reads data from Global_Data.json, including interdependent_infrastructure_networks_with_different_resource_demand, cascading_failure_identification_under_random_attacks.json, and resource_constraints. The tool outputs resource_allocation_considering_GSCC.json and stores it in Global_Data.json.If the tool runs successfully, you will observe that resource_allocation_considering_GSCC.json has been generated and stored in Global_Data.json."
             )
mcp.add_tool(allocate_restoration_resource_considering_population,
    name="allocate_restoration_resource_considering_population",
    description="This tool calculates the daily resource allocation for each node to maximize the served population. It reads data from Global_Data.json, including interdependent_infrastructure_networks_with_different_resource_demand, cascading_failure_identification_under_random_attacks.json, resource_constraints and population_data. The tool outputs resource_allocation_considering_population.json and stores it in Global_Data.json.If the tool runs successfully, you will observe that resource_allocation_considering_population.json has been generated and stored in Global_Data.json."
             )
mcp.add_tool(allocate_restoration_resource_considering_cost,
    name="allocate_restoration_resource_considering_cost",
    description="This tool calculates the daily resource allocation for each node to minimize the total recovery cost. It reads data from Global_Data.json, including interdependent_infrastructure_networks_with_different_resource_demand, cascading_failure_identification_under_random_attacks.json, and resource_constraints_per_day_4_cost. The tool outputs resource_allocation_considering_cost.json and stores it in Global_Data.json.If the tool runs successfully, you will observe that resource_allocation_considering_cost.json has been generated and stored in Global_Data.json."
             )
mcp.add_tool(allocate_restoration_resource_considering_clustering_coefficient,
    name="allocate_restoration_resource_considering_clustering_coefficient",
    description="This tool calculates the daily resource allocation for each node based on their clustering coefficient. It reads data from Global_Data.json, including interdependent_infrastructure_networks_with_different_resource_demand, cascading_failure_identification_under_random_attacks.json, and resource_constraints. The tool outputs resource_allocation_bclustering_coefficient.json and stores it in Global_Data.json.If the tool runs successfully, you will observe that resource_allocation_considering_clustering_coefficient.json has been generated and stored in Global_Data.json."
             )

mcp.add_tool(deploy_portable_equipment_considering_connectivity,
    name="deploy_portable_equipment_considering_connectivity",
    description="This tool is to determine which failed facility in the urban lifeline systems should be replaced with temporary portable equipment in order to maximize overall network connectivity. It reads the infrastructure information in interdependent_infrastructure_networks.json and the failed nodes from cascading_failure_identification_under_big_nodes_attacks.json, both of which are specified in Global_Data.json. The output includes the identifiers of the failed nodes selected for replacement and the resulting network connectivity after temporary recovery. If this function is run, you could observe the path of failed_nodes_replacement_evaluated_by_connectivity.json in Global_Data.json.")
mcp.add_tool(deploy_portable_equipment_considering_efficiency,
    name="deploy_portable_equipment_considering_efficiency",
    description="This tool is to determine which failed facility in the urban lifeline systems should be replaced with temporary portable equipment in order to maximize overall network efficiency. It reads the infrastructure information in interdependent_infrastructure_networks.json and the failed nodes from cascading_failure_identification_under_big_nodes_attacks.json, both of which are specified in Global_Data.json. The output includes the identifiers of the failed nodes selected for replacement and the resulting efficiency after temporary recovery. If this function is run, you could observe the path of failed_nodes_replacement_evaluated_by_efficiency.json in Global_Data.json."
             )
mcp.add_tool(deploy_portable_equipment_considering_population,
    name="deploy_portable_equipment_considering_population",
    description="This tool is to determine which failed facility in the urban lifeline systems should be replaced with temporary portable equipment in order to maximize served population. It reads the infrastructure information in interdependent_infrastructure_networks.json, the failed nodes from cascading_failure_identification_under_big_nodes_attacks.json, and the population information, all of which are specified in Global_Data.json. The output includes the identifiers of the failed nodes selected for replacement and the served population after temporary recovery. If this function is run, you could observe the path of failed_nodes_replacement_evaluated_by_population.json in Global_Data.json."
        )

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