from mcp.server.fastmcp import FastMCP
from convert_SHPfile_to_JSONfile import convert_SHPfile_to_JSONfile
from convert_CSVfile_to_JSONfile import convert_CSVfile_to_JSONfile
from convert_DBFfile_to_JSONfile import convert_DBFfile_to_JSONfile
from convert_DWGfile_to_JSONfile import convert_DWGfile_to_JSONfile
from convert_KMZfile_to_JSONfile import convert_KMZfile_to_JSONfile
from convert_RVTfile_to_JSONfile import convert_RVTfile_to_JSONfile
from generate_interdependence_across_networks import generate_interdependence_across_networks

mcp = FastMCP(name="data processing")
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

mcp.run(transport="stdio")