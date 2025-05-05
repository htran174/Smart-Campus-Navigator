# visualize.py

import networkx as nx
import matplotlib.pyplot as plt
from map import campus_graph, building_names

# Fixed positions for buildings
pos = {
    8: (1, 8),   # Rec (top left)
    1: (5, 8),   # KIN (top middle right)
    2: (7, 8),   # Wellness (top far right)

    7: (2, 6),   # TSU (under Rec)
    0: (5, 6),   # Library (center)
    3: (7, 6),   # EC (right of Library)

    9: (0, 5),   # VAC (under TSU, left)
    4: (3, 5),   # Arts (under TSU, right next to VAC)

    5: (4, 4),   # MH (under Library)
    6: (7, 5),   # HUM (right of MH)

    10: (7, 4),  # Gordon (far right of HUM)

    11: (4, 3),  # Dan Black (bottom left under MH)
    12: (6.5, 3),  # Langsdorf (bottom right under HUM)
    13: (7.5, 2)   # Mihaylo (bottom right under Gordon)
}

def draw_campus_graph():
    G = nx.Graph()

    # Add nodes
    for i, name in enumerate(building_names):
        G.add_node(i, label=name)

    # Add edges
    for u in campus_graph:
        for v, weight in campus_graph[u]:
            if not G.has_edge(u, v):  # Prevent double edges
                G.add_edge(u, v, weight=weight)

    # Draw graph
    plt.figure(figsize=(10, 7))  # Make it bigger and easier to see
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="skyblue")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    nx.draw_networkx_labels(G, pos, labels={i: name for i, name in enumerate(building_names)}, font_size=8)

    plt.title("CSUF Campus Map Visualization")
    plt.axis('off')
    plt.show()

# Only run if this file is executed directly
if __name__ == "__main__":
    draw_campus_graph()
