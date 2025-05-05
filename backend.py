# backend.py

from map import campus_graph, building_names
from algro import dijkstra, prim, kruskal

# Helper Functions for id to names
def building_name_to_index(name):
    try:
        return building_names.index(name)
    except ValueError:
        return None

def building_index_to_name(index):
    if 0 <= index < len(building_names):
        return building_names[index]
    return None

# Find shortest path using Dijkstra
def find_shortest_path(start_name, end_name):
    start = building_name_to_index(start_name)
    end = building_name_to_index(end_name)

    if start is None or end is None:
        return None, None

    path_indices, total_time = dijkstra(campus_graph, start, end)
    if path_indices is None:
        return None, None

    path_names = [building_index_to_name(i) for i in path_indices]
    return path_names, total_time

# Build Minimum Spanning Tree using Prim's Algorithm
def build_mst():
    n = len(building_names)
    total_cost, mst_edges = prim(campus_graph, n)
    # mst_edges will contain (u, v, weight), u and v are indices
    readable_edges = [(building_index_to_name(u), building_index_to_name(v), weight) for u, v, weight in mst_edges]
    return readable_edges, total_cost

# Build Minimum Spanning Tree using Kruskal's Algorithm
def build_mst_kruskal():
    n = len(building_names)
    total_cost, mst_edges = kruskal(campus_graph, n)
    readable_edges = [(building_index_to_name(u), building_index_to_name(v), weight) for u, v, weight in mst_edges]
    return readable_edges, total_cost
