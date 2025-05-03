"""
======================================================================================================

                                            algro.py
                                        Created by Hien Tran
                            Holds all the algrothims that is needed for project

======================================================================================================
"""

import heapq

# -----------------------------
# Dijkstra's Algorithm
# -----------------------------
def dijkstra(graph, source):
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]

    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev

# -----------------------------
# Prim's Algorithm
# -----------------------------
def prim(graph, n):
    visited = [False] * n
    min_heap = [(0, 0)]
    total_cost = 0

    while min_heap:
        cost, u = heapq.heappop(min_heap)
        if visited[u]:
            continue
        visited[u] = True
        total_cost += cost

        for v, weight in graph[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (weight, v))

    return total_cost

# -----------------------------
# Kruskal's Algorithm
# -----------------------------
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, rank, x, y):
    rootX = find(parent, x)
    rootY = find(parent, y)
    if rootX != rootY:
        if rank[rootX] < rank[rootY]:
            parent[rootX] = rootY
        elif rank[rootX] > rank[rootY]:
            parent[rootY] = rootX
        else:
            parent[rootY] = rootX
            rank[rootX] += 1

def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])
    parent = [i for i in range(n)]
    rank = [0] * n
    mst_cost = 0
    mst_edges = []

    for u, v, weight in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_cost += weight
            mst_edges.append((u, v))

    return mst_cost, mst_edges

# -----------------------------
# Reconstruct Path from Dijkstra
# -----------------------------
def reconstruct_path(prev, start, end):
    path = []
    at = end
    while at is not None:
        path.append(at)
        at = prev[at]
    path.reverse()
    return path if path[0] == start else []

# -----------------------------
# Merge Sort
# -----------------------------
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# -----------------------------
# KMP Algorithm
# -----------------------------
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
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
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    positions = []
    i = j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return positions

# -----------------------------
# Activity Selection Problem
# -----------------------------
def activity_selection(activities):
    # activities: list of (start_time, end_time)
    activities.sort(key=lambda x: x[1])  # Sort by end times

    selected = []
    last_end_time = -1

    for start, end in activities:
        if start >= last_end_time:
            selected.append((start, end))
            last_end_time = end

    return selected
