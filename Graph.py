import matplotlib.pyplot as plt
import networkx as nx


G = nx.Graph()
G.add_weighted_edges_from([
    ("SRC", "KHS", 6),
    ("KHS", "PL", 5),
    ("SRC", "PL", 6),
    ("PL", "EC", 4),
    ("PL", "MH", 1),
    ("MH", "DBH", 3),
    ("TSU", "PL", 7),
    ("TSU", "MH", 4)
])


pos = {
    "SRC": (-1, 2),
    "KHS": (0, 2),
    "TSU": (-1, 0),
    "PL": (0, 1),
    "EC": (1, 1),
    "MH": (0, 0),
    "DBH": (0, -1),
}


highlight_path = ["SRC", "PL", "MH"]
highlight_edges = list(zip(highlight_path, highlight_path[1:]))


node_colors = []
for node in G.nodes():
    if node == highlight_path[0]:
        node_colors.append("green")
    elif node == highlight_path[-1]:
        node_colors.append("red")
    else:
        node_colors.append("skyblue")


plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=12, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)


nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color="red", width=3)

plt.title("Manual Highlight Test: SRC → PL → MH")
plt.axis("off")
plt.tight_layout()
plt.show()
