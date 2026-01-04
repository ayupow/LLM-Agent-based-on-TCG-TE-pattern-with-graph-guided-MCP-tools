from mcp.server.fastmcp import FastMCP
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

mcp = FastMCP(name="failed facility restoration scheduling")
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
mcp.run(transport="stdio")