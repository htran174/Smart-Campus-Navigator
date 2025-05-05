# test_backend.py

import backend

def test_shortest_paths():
    print("Testing Shortest Paths:\n")

    paths_to_test = [
        ("Library", "Mihaylo"),
        ("Library", "Rec"),
        ("TSU", "Gordon"),
        ("VAC", "Wellness"),
        ("Dan Black", "KIN")
    ]

    for start, end in paths_to_test:
        path, total_time = backend.find_shortest_path(start, end)
        if path is None or total_time is None:
            print(f"No path found from {start} to {end}.\n")
        else:
            path_str = " -> ".join(path)
            print(f"Path from {start} to {end}: {path_str} (Total time: {total_time} mins)\n")

def test_mst_prim():
    print("\nTesting MST (Prim's Algorithm):\n")
    mst_edges, total_cost = backend.build_mst()
    for u, v, weight in mst_edges:
        print(f"{u} <--> {v} ({weight} mins)")
    print(f"Total time to connect campus (Prim): {total_cost} mins\n")

def test_mst_kruskal():
    print("\nTesting MST (Kruskal's Algorithm):\n")
    mst_edges, total_cost = backend.build_mst_kruskal()
    for u, v, weight in mst_edges:
        print(f"{u} <--> {v} ({weight} mins)")
    print(f"Total time to connect campus (Kruskal): {total_cost} mins\n")

if __name__ == "__main__":
    test_shortest_paths()
    test_mst_prim()
    test_mst_kruskal()
