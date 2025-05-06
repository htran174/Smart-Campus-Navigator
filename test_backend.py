# test_backend.py

import backend
from datetime import datetime


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

def test_sort_tasks():
    print("\nTesting Task Sorting:\n")

    tasks = [
        (datetime(2025,5,5,12,0), datetime(2025,5,5,13,0), "Library"),
        (datetime(2025,5,5,9,0), datetime(2025,5,5,10,0), "TSU"),
        (datetime(2025,5,5,10,30), datetime(2025,5,5,11,30), "Rec Center")
    ]

    print("Before Sorting:")
    for start, end, location in tasks:
        print(f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} @ {location}")

    sorted_tasks = backend.sort_tasks(tasks)

    print("\nAfter Sorting:")
    for start, end, location in sorted_tasks:
        print(f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} @ {location}")

if __name__ == "__main__":
    #test_shortest_paths()
    #test_mst_prim()
    #test_mst_kruskal()
    test_sort_tasks()
