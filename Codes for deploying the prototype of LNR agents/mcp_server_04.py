from mcp.server.fastmcp import FastMCP
from deploy_portable_equipment_considering_connectivity import deploy_portable_equipment_considering_connectivity
from deploy_portable_equipment_considering_efficiency import deploy_portable_equipment_considering_efficiency
from deploy_portable_equipment_considering_population import deploy_portable_equipment_considering_population

mcp = FastMCP(name="emergency portable equipment deploying")
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

mcp.run(transport="stdio")