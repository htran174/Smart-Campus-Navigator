# algro.py

import heapq

# =====================
# Dijkstra's Algorithm
# =====================

def dijkstra(graph, start, end):
    n = len(graph)
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}

    dist[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        if u == end:
            break

        if current_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    # Rebuild path
    path = []
    at = end
    if dist[end] == float('inf'):
        return None, None

    while at is not None:
        path.append(at)
        at = prev[at]

    path.reverse()
    return path, dist[end]

# =====================
# Prim's Algorithm (MST)
# =====================

def prim(graph, n):
    visited = set()
    mst_edges = []
    total_cost = 0

    min_heap = [(0, 0, -1)]  # (cost, current_node, parent_node)

    while min_heap and len(visited) < n:
        cost, u, parent = heapq.heappop(min_heap)

        if u in visited:
            continue

        visited.add(u)
        if parent != -1:
            mst_edges.append((parent, u, cost))
            total_cost += cost

        for v, weight in graph[u]:
            if v not in visited:
                heapq.heappush(min_heap, (weight, v, u))

    return total_cost, mst_edges

# =====================
# Kruskal's Algorithm (MST)
# =====================

def find(parent, u):
    if parent[u] != u:
        parent[u] = find(parent, parent[u])
    return parent[u]

def union(parent, rank, u, v):
    root_u = find(parent, u)
    root_v = find(parent, v)

    if root_u != root_v:
        if rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        elif rank[root_u] > rank[root_v]:
            parent[root_v] = root_u
        else:
            parent[root_v] = root_u
            rank[root_u] += 1

def kruskal(graph, n):
    edges = []
    for u in graph:
        for v, weight in graph[u]:
            if u < v:  # avoid double counting
                edges.append((u, v, weight))

    edges.sort(key=lambda x: x[2])

    parent = [i for i in range(n)]
    rank = [0] * n

    mst_edges = []
    total_cost = 0

    for u, v, weight in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_edges.append((u, v, weight))
            total_cost += weight

    return total_cost, mst_edges

# =====================
# Merge Sort
# =====================

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# =====================
# Knuth-Morris-Pratt (KMP) String Matching
# =====================

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    i = j = 0

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            return True  # Found
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return False

# =====================
# Activity Selection Problem
# =====================

def activity_selection(activities):
    activities.sort(key=lambda x: x[1])  # Sort by end times
    selected = []
    last_end = -1

    for start, end in activities:
        if start >= last_end:
            selected.append((start, end))
            last_end = end

    return selected
