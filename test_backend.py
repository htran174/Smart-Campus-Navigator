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
    print("\nTesting Task Sorting (by Importance then Start Time):\n")

    tasks = [
        (datetime(2025,5,5,12,0), datetime(2025,5,5,13,0), "Library", 1, "Study"),   # Low
        (datetime(2025,5,5,9,0), datetime(2025,5,5,10,0), "TSU", 3, "Club Meeting"), # High
        (datetime(2025,5,5,10,30), datetime(2025,5,5,11,30), "Rec Center", 2, "Gym") # Normal
    ]

    print("Before Sorting:")
    for start, end, location, importance, desc in tasks:
        print(f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} @ {location} [{importance}] {desc}")

    sorted_tasks = backend.sort_tasks(tasks)

    print("\nAfter Sorting:")
    for start, end, location, importance, desc in sorted_tasks:
        print(f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} @ {location} [{importance}] {desc}")

def test_schedule_tasks():
    print("\nTesting Task Scheduling (Greedy, Prefer Higher Importance):\n")

    tasks = [
        (datetime(2025,5,5,9,0), datetime(2025,5,5,12,0), "Library", 2, "Study"),     # Normal
        (datetime(2025,5,5,10,0), datetime(2025,5,5,11,0), "TSU", 3, "Club Meeting"), # High (overlaps)
        (datetime(2025,5,5,12,0), datetime(2025,5,5,13,0), "Rec Center", 1, "Workout")# Low
    ]

    print("Before Scheduling:")
    for start, end, location, importance, desc in tasks:
        print(f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} @ {location} [{importance}] {desc}")

    scheduled_tasks = backend.schedule_tasks(tasks)

    print("\nAfter Scheduling (Selected Non-Overlapping Tasks):")
    for start, end, location, importance, desc in scheduled_tasks:
        print(f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} @ {location} [{importance}] {desc}")


def test_sort_tasks_with_overlap():
    print("\n🔍 Testing sort_tasks() — Keeps Overlapping Tasks, Sorted by Start Time:\n")

    tasks = [
        (datetime(2025, 5, 5, 10, 0), datetime(2025, 5, 5, 11, 0), "TSU", 3, "Club Meeting"),
        (datetime(2025, 5, 5, 9, 0), datetime(2025, 5, 5, 12, 0), "Library", 2, "Study Session"),
        (datetime(2025, 5, 5, 12, 0), datetime(2025, 5, 5, 13, 0), "Rec Center", 1, "Workout")
    ]

    print("📋 Original Task Order:")
    for start, end, loc, imp, desc in tasks:
        print(f"{start.strftime('%H:%M')}–{end.strftime('%H:%M')} @ {loc} [{imp}] {desc}")

    sorted_tasks = backend.sort_tasks(tasks)

    print("\n✅ Sorted by Start Time (Overlaps Allowed):")
    for start, end, loc, imp, desc in sorted_tasks:
        print(f"{start.strftime('%H:%M')}–{end.strftime('%H:%M')} @ {loc} [{imp}] {desc}")

if __name__ == "__main__":
    #test_shortest_paths()
    #test_mst_prim()
    #test_mst_kruskal()
    #test_sort_tasks()
    #test_schedule_tasks()
    test_sort_tasks_with_overlap()
