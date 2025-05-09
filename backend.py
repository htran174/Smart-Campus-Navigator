# backend.py

from map import campus_graph, building_names
from algro import dijkstra, prim, kruskal, merge_sort

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

def sort_tasks(tasks):
    """
    Sort tasks by start time only.
    Keeps all overlapping tasks.
    Used for display and user review.
    """
    if not tasks:
        return []

    def start_time_key(task):
        return task[0].hour * 60 + task[0].minute

    # Wrap with keys for merge sort
    tasks_with_keys = [(start_time_key(task), task) for task in tasks]
    sorted_pairs = merge_sort(tasks_with_keys)

    # Extract and return sorted tasks only
    return [task for _, task in sorted_pairs]


def schedule_tasks(tasks):
    if not tasks:
        return []

    # Enrich with comparable minutes
    enriched = []
    for task in tasks:
        start = task[0].hour * 60 + task[0].minute
        end = task[1].hour * 60 + task[1].minute
        enriched.append((task[3], end, start, task))  # importance, end time, start time, full

    # Sort by end time first (core of activity selection), then by -importance to favor better tasks when tied
    enriched.sort(key=lambda x: (x[1], -x[0]))

    result = []
    last_end = -1

    for imp, end, start, task in enriched:
        if start >= last_end:
            result.append(task)
            last_end = end

    return sorted(result, key=lambda x: x[0])
