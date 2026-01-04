from allocate_restoration_resource_considering_population import allocate_restoration_resource_considering_population
from allocate_restoration_resource_considering_time import allocate_restoration_resource_considering_time
from allocate_restoration_resource_considering_clustering_coefficient import allocate_restoration_resource_considering_clustering_coefficient
from allocate_restoration_resource_considering_cost import allocate_restoration_resource_considering_cost
from allocate_restoration_resource_considering_GSCC import allocate_restoration_resource_considering_GSCC

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="failed facility restoration resource allocating")
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

mcp.run(transport="stdio")