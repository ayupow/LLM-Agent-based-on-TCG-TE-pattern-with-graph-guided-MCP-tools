# Shared helpers for NetworkX MCP tools
import networkx as nx
from typing import Any, Dict

# Global in-memory graph store (keyed by graph name)
_graphs: Dict[str, nx.Graph] = {}

def _get_graphs():
    return _graphs
def _require_graph(graph_name: str) -> nx.Graph:
    if graph_name not in _graphs:
        raise ValueError(f"Graph '{graph_name}' not found")
    return _graphs[graph_name]
