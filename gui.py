import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime

from map import campus_graph, building_names
from backend import find_shortest_path, build_mst, build_mst_kruskal, sort_tasks, schedule_tasks
from visualize import pos as positions

tasks = []
current = {"start": None, "end": None}

# Animation state
current_step = 0
scheduled_path = []
animation_running = False

def run_gui():
    root = tk.Tk()
    root.title("CSUF Campus Navigator")
    root.geometry("1200x600")

    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def draw_graph(highlight_nodes=None, path_edges=None):
        ax.clear()
        G = nx.Graph()
        for u in campus_graph:
            for v, w in campus_graph[u]:
                G.add_edge(u, v, weight=w)
        nx.draw(G, pos=positions, ax=ax, with_labels=True, node_color='lightblue', node_size=800, font_size=8,
                labels={i: name for i, name in enumerate(building_names)})
        nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
        if highlight_nodes:
            nx.draw_networkx_nodes(G, pos=positions, nodelist=highlight_nodes, node_color='orange', node_size=800, ax=ax)
        if path_edges:
            nx.draw_networkx_edges(G, pos=positions, edgelist=path_edges, edge_color='red', width=3, ax=ax)
        canvas.draw()

    draw_graph()

    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    task_frame = tk.Frame(root, relief=tk.GROOVE, bd=2)
    task_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    calendar_frame = tk.Frame(task_frame, relief=tk.SUNKEN, bd=2)
    calendar_frame.pack(side=tk.BOTTOM, pady=10, fill="both", expand=True)

    def open_input_popup():
        popup = tk.Toplevel(root)
        popup.title("Select Start and End")
        popup.geometry("300x200")

        tk.Label(popup, text="Start Location:").pack(pady=5)
        start_cb = ttk.Combobox(popup, values=building_names, state="readonly")
        start_cb.pack()

        tk.Label(popup, text="End Location:").pack(pady=5)
        end_cb = ttk.Combobox(popup, values=building_names, state="readonly")
        end_cb.pack()

        def submit():
            current["start"] = start_cb.get()
            current["end"] = end_cb.get()
            draw_graph()
            popup.destroy()

        tk.Button(popup, text="Confirm", command=submit).pack(pady=10)

    def simulate_path():
        if not current["start"] or not current["end"]:
            messagebox.showwarning("Missing", "Please set both start and end locations.")
            return
        path, _ = find_shortest_path(current["start"], current["end"])
        if path:
            indices = [building_names.index(name) for name in path]
            path_edges = list(zip(indices, indices[1:]))
            draw_graph(highlight_nodes=indices, path_edges=path_edges)
        else:
            messagebox.showerror("Error", "No path found between the selected nodes.")

    def open_task_popup():
        popup = tk.Toplevel(root)
        popup.title("Add Task")
        popup.geometry("300x400")

        tk.Label(popup, text="Start Time (e.g. 9 or 09:00):").pack()
        start_entry = tk.Entry(popup)
        start_entry.pack()

        tk.Label(popup, text="End Time (e.g. 10 or 10:30):").pack()
        end_entry = tk.Entry(popup)
        end_entry.pack()

        tk.Label(popup, text="Location:").pack()
        location_cb = ttk.Combobox(popup, values=building_names, state="readonly")
        location_cb.pack()

        tk.Label(popup, text="Importance:").pack()
        importance_cb = ttk.Combobox(popup, values=["Low (1)", "Normal (2)", "High (3)"], state="readonly")
        importance_cb.pack()

        tk.Label(popup, text="Task Description:").pack()
        content_entry = tk.Entry(popup)
        content_entry.pack()

        def parse_time(text):
            return datetime.strptime(text.strip().zfill(5) if ':' in text else text.zfill(2)+":00", "%H:%M")

        def add_task():
            try:
                start_time = parse_time(start_entry.get())
                end_time = parse_time(end_entry.get())
                location = location_cb.get()
                importance_value = int(importance_cb.get().split('(')[-1][0])
                description = content_entry.get()
                if end_time <= start_time:
                    raise ValueError("End time must be after start time.")
                tasks.append((start_time, end_time, location, importance_value, description))
                update_calendar_view()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(popup, text="Add", command=add_task).pack(pady=10)


    def update_calendar_view():
        for widget in calendar_frame.winfo_children():
            widget.destroy()
        tk.Label(calendar_frame, text="Task Time View", font=("Arial", 11, "bold")).pack(pady=5)
        for start, end, loc, imp, desc in tasks:
            label = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} ({loc}, {imp}) {desc}"
            tk.Label(calendar_frame, text=label, bg="lightyellow", width=45, relief=tk.RIDGE, anchor="w").pack(pady=2, padx=5)

    def update_calendar_with_schedule(scheduled_list):
        for widget in calendar_frame.winfo_children():
            widget.destroy()
        tk.Label(calendar_frame, text="Scheduled Tasks View", font=("Arial", 11, "bold")).pack(pady=5)

        for start, end, loc, imp, desc in scheduled_list:
            label = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')} ({loc}, {imp}) {desc}"
            tk.Label(calendar_frame, text=label, bg="lightgreen", width=45, relief=tk.RIDGE, anchor="w").pack(pady=2, padx=5)

    def show_all_tasks():
        update_calendar_view()

    def show_sorted():
        global tasks
        tasks = sort_tasks(tasks)
        update_calendar_view()

    def show_schedule():
        scheduled = schedule_tasks(tasks)  # Don’t overwrite the full task list
        update_calendar_with_schedule(scheduled)   # Show only scheduled tasks

    def clear_all_tasks():
        global tasks
        tasks.clear()
        update_calendar_view()
        
    top_task_frame = tk.Frame(task_frame, relief=tk.GROOVE, bd=2)
    top_task_frame.pack(side=tk.TOP, anchor="n", pady=10)

    #left panal
    tk.Label(top_task_frame, text="Task Scheduling", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Button(top_task_frame, text="Add Task", command=open_task_popup).pack(pady=2)
    tk.Button(top_task_frame, text="Sort Tasks", command=show_sorted).pack(pady=2)
    tk.Button(top_task_frame, text="Schedule Tasks", command=show_schedule).pack(pady=2)
    tk.Button(top_task_frame, text="Clear Tasks", command=clear_all_tasks).pack(pady=2)
    tk.Button(top_task_frame, text="Show All Tasks", command=show_all_tasks).pack(pady=2)

    #right panal
    tk.Label(control_frame, text="Path Finder", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(control_frame, text="Set Start and End", command=open_input_popup).pack(pady=10)
    tk.Button(control_frame, text="Highlight Shortest Path", command=simulate_path).pack(pady=10)
    

    def highlight_mst():
        # Get MST edges from backend (with building names)
        mst_edges, _ = build_mst()

        # Redraw graph with ONLY MST edges
        def filtered_draw():
            ax.clear()
            G_mst = nx.Graph()
            for u, v, w in mst_edges:
                G_mst.add_edge(building_names.index(u), building_names.index(v), weight=w)
            nx.draw(G_mst, pos=positions, ax=ax, with_labels=True, node_color='lightblue', node_size=800, font_size=8,
                    labels={i: name for i, name in enumerate(building_names)})
            nx.draw_networkx_edge_labels(G_mst, pos=positions,
                                        edge_labels={(building_names.index(u), building_names.index(v)): w for u, v, w in mst_edges},
                                        ax=ax)
            canvas.draw()

        filtered_draw()

    def reset_graph():
        draw_graph()

    tk.Button(control_frame, text="Show MST (Prim)", command=highlight_mst).pack(pady=5)
    tk.Button(control_frame, text="Reset Graph", command=reset_graph).pack(pady=5)

    def animate_segment(start, end):
        draw_graph(path_edges=[(start, end)])

    def show_day():
        global scheduled_path, current_step

        scheduled = schedule_tasks(tasks)
        scheduled.sort(key=lambda task: task[0])

        scheduled_path = []

        for i in range(len(scheduled) - 1):
            start_building = scheduled[i][2]
            end_building = scheduled[i + 1][2]
            path, _ = find_shortest_path(start_building, end_building)

            if path and len(path) >= 2:
                indices = [building_names.index(name) for name in path]
                path_edges = list(zip(indices, indices[1:]))
                scheduled_path.append(path_edges)

        current_step = 0
        show_current_step()  

    def step_through_day():
        global current_step, animation_running

        if not animation_running or current_step >= len(scheduled_path):
            return

        path_edges = scheduled_path[current_step]  # ✅ use entire list of edges
        draw_graph(path_edges=path_edges)

        current_step += 1
        root.after(1500, step_through_day)

    def show_current_step():
        global current_step
        if 0 <= current_step < len(scheduled_path):
            path_edges = scheduled_path[current_step]
            draw_graph(path_edges=path_edges)

    def next_task_path():
        global current_step
        if current_step < len(scheduled_path) - 1:
            current_step += 1
            show_current_step()

    def prev_task_path():
        global current_step
        if current_step > 0:
            current_step -= 1
            show_current_step()
            
    tk.Button(top_task_frame, text="Show Day", command=show_day).pack(pady=2)
    tk.Button(top_task_frame, text="Next", command=next_task_path).pack(pady=2)
    tk.Button(top_task_frame, text="Prev", command=prev_task_path).pack(pady=2)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
