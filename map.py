# map.py

from collections import defaultdict

# Building names (shortened with full names as comments)
building_names = [
    "Library",    # 0 - Pollak Library
    "KIN",        # 1 - Kinesiology & Health Science
    "Wellness",   # 2 - Student Wellness
    "EC",         # 3 - Education Classroom
    "Arts",       # 4 - Visual Arts Center
    "MH",         # 5 - McCarthy Hall
    "HUM",        # 6 - Humanities Building
    "TSU",        # 7 - Titan Student Union
    "Rec",        # 8 - Student Recreation Center
    "VAC",        # 9 - Visual Arts Complex
    "Gordon",     # 10 - Gordon Hall
    "Dan Black",  # 11 - Dan Black Hall
    "Langsdorf",  # 12 - Langsdorf Hall
    "Mihaylo"     # 13 - Mihaylo Hall
]

# Edge list: (from_node, to_node, distance)
campus_edges = [
    # Library connections
    (0, 1, 3),   # Library - KIN
    (0, 2, 4),   # Library - Wellness
    (0, 3, 2),   # Library - EC
    (0, 4, 2),   # Library - Arts
    (0, 5, 4),   # Library - MH
    (0, 6, 3),   # Library - HUM
    (0, 7, 4),   # Library - TSU

    # TSU connections
    (7, 8, 3),   # TSU - Rec
    (7, 9, 2),   # TSU - VAC
    (7, 1, 4),   # TSU - KIN
    (7, 4, 2),   # TSU - Arts

    # KIN connections
    (1, 8, 3),   # KIN - Rec
    (1, 2, 2),   # KIN - Wellness

    # Wellness connections
    (2, 3, 4),   # Wellness - EC

    # EC connections
    (3, 6, 2),   # EC - HUM
    (3, 5, 5),   # EC - MH
    (3, 4, 4),   # EC - Arts

    # Arts connections
    (4, 9, 3),   # Arts - VAC
    (4, 5, 2),   # Arts - MH
    (4, 6, 5),   # Arts - HUM

    # HUM connections
    (6, 5, 3),   # HUM - MH
    (6, 10, 3),  # HUM - Gordon

    # MH connections
    (5, 11, 1),  # MH - Dan Black
    (5, 12, 2),  # MH - Langsdorf
    (5, 10, 2),  # MH - Gordon

    # Dan Black connections
    (11, 12, 1), # Dan Black - Langsdorf
    (11, 10, 2), # Dan Black - Gordon

    # Mihaylo connections
    (13, 12, 1), # Mihaylo - Langsdorf
    (13, 10, 1)  # Mihaylo - Gordon
]

# Build the adjacency list (undirected)
campus_graph = defaultdict(list)

for u, v, weight in campus_edges:
    campus_graph[u].append((v, weight))
    campus_graph[v].append((u, weight))  # Automatically add reverse connection
