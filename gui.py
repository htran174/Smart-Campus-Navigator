# gui_base_app.py

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime

# ====== Campus graph definition ======
G = nx.Graph()
G.add_edge("SRC", "KHS", weight=5)
G.add_edge("KHS", "PL", weight=2)
G.add_edge("PL", "MH", weight=1)
G.add_edge("MH", "DBH", weight=3)
G.add_edge("PL", "EC", weight=4)
G.add_edge("SRC", "TSU", weight=7)
G.add_edge("TSU", "PL", weight=2)

positions = nx.spring_layout(G, seed=42)

# Store tasks as (start_time, end_time, description)
tasks = []

def run_gui():
    root = tk.Tk()
    root.title("CSUF Campus Navigator")
    root.geometry("1200x600")

    # Graph display area
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def draw_graph(highlight_nodes=None, path_edges=None):
        ax.clear()
        nx.draw(G, pos=positions, ax=ax, with_labels=True, node_color='lightblue', node_size=800, font_size=10)
        nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)

        if highlight_nodes:
            nx.draw_networkx_nodes(G, pos=positions, nodelist=highlight_nodes, node_color='orange', node_size=800, ax=ax)

        if path_edges:
            nx.draw_networkx_edges(G, pos=positions, edgelist=path_edges, edge_color='red', width=3, ax=ax)

        canvas.draw()

    draw_graph()

    # Control Panel
    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    task_frame = tk.Frame(root, relief=tk.GROOVE, bd=2)
    task_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    calendar_frame = tk.Frame(task_frame)
    calendar_frame.pack(pady=10, fill="both", expand=True)

    current = {"start": None, "end": None}

    def open_input_popup():
        popup = tk.Toplevel(root)
        popup.title("Select Start and End")
        popup.geometry("300x200")

        tk.Label(popup, text="Start Location:").pack(pady=5)
        start_cb = ttk.Combobox(popup, values=list(G.nodes), state="readonly")
        start_cb.pack()

        tk.Label(popup, text="End Location:").pack(pady=5)
        end_cb = ttk.Combobox(popup, values=list(G.nodes), state="readonly")
        end_cb.pack()

        def submit():
            current["start"] = start_cb.get()
            current["end"] = end_cb.get()
            draw_graph(highlight_nodes=[current["start"], current["end"]])
            popup.destroy()

        tk.Button(popup, text="Confirm", command=submit).pack(pady=10)

    def simulate_path():
        if not current["start"] or not current["end"]:
            messagebox.showwarning("Missing", "Please set both start and end locations.")
            return

        try:
            path = nx.shortest_path(G, source=current["start"], target=current["end"], weight='weight')
            path_edges = list(zip(path, path[1:]))
            draw_graph(highlight_nodes=path, path_edges=path_edges)
        except nx.NetworkXNoPath:
            messagebox.showerror("Error", "No path found between the selected nodes.")

    def open_task_popup():
        popup = tk.Toplevel(root)
        popup.title("Add Task")
        popup.geometry("300x250")

        tk.Label(popup, text="Start Time (e.g. 9 or 09:00):").pack()
        start_entry = tk.Entry(popup)
        start_entry.pack()

        tk.Label(popup, text="End Time (e.g. 10 or 10:30):").pack()
        end_entry = tk.Entry(popup)
        end_entry.pack()

        tk.Label(popup, text="Task Description:").pack()
        content_entry = tk.Entry(popup)
        content_entry.pack()

        def parse_time(text):
            if ":" in text:
                return datetime.strptime(text, "%H:%M")
            else:
                return datetime.strptime(text.zfill(2) + ":00", "%H:%M")

        def add_task():
            try:
                start_str = start_entry.get().strip()
                end_str = end_entry.get().strip()
                content = content_entry.get().strip()

                start_time = parse_time(start_str)
                end_time = parse_time(end_str)

                if end_time <= start_time:
                    raise ValueError("End time must be after start time.")
                if not content:
                    raise ValueError("Please enter a task description.")

                tasks.append((start_time, end_time, content))
                update_calendar_view()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(popup, text="Add", command=add_task).pack(pady=10)

    def update_calendar_view():
        for widget in calendar_frame.winfo_children():
            widget.destroy()
        tk.Label(calendar_frame, text="🕒 Task Time View", font=("Arial", 11, "bold")).pack(pady=5)
        for start, end, content in tasks:
            label = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}  {content}"
            tk.Label(calendar_frame, text=label, bg="lightyellow", width=40, relief=tk.RIDGE, anchor="w").pack(pady=2, padx=5)

    tk.Label(task_frame, text="📅 Task Scheduling", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(task_frame, text="Add Task", command=open_task_popup).pack(pady=5)

    tk.Label(control_frame, text="🗺️ Path Finder", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(control_frame, text="Set Start and End", command=open_input_popup).pack(pady=10)
    tk.Button(control_frame, text="Highlight Shortest Path", command=simulate_path).pack(pady=10)

    root.mainloop()

# Entry point
if __name__ == "__main__":
    run_gui()
