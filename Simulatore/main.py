import tkinter as tk
import csv
import os
import shutil
from tkinter import Menu, messagebox, filedialog
from PIL import ImageTk, Image

from sensor import add_sensor, sensors
from sim import start_simulation, stop_simulation, interaction, update_sensors
from point import add_point, points
from wall import draw_line_window, walls
from read import read_coordinates_from_file, draw_points, draw_walls, draw_sensors, draw_devices, draw_doors
from graph import show_graphs
from device import add_device, devices
from door import draw_line_door, doors
from activity import monitor_activities, close_current_activity
from timer import TimerApp
from log import show_log, show_activity_log
from automatic import launch_automatic_interface
from log import start_interaction_log_session, stop_interaction_log_session
from common import sensor_states


window: tk.Tk | None = None
canvas: tk.Canvas | None = None
timer_frame: tk.Frame | None = None
activity_label: tk.Label | None = None

file_menu: Menu | None = None
simulation_menu: Menu | None = None

load_active = False  # true only if we are reading file

r_points = []  #read points
read_walls = []
read_sensors = []
read_devices = []
read_doors = []


# ==============================
#    Scenario construction
# ==============================

def create_door():
    draw_line_door(canvas, window, load_active)


def create_point():
    canvas.bind("<Button-1>", lambda event: add_point(canvas, event, load_active))
    file_menu.entryconfig("Add points", state="disabled")
    file_menu.entryconfig("Add sensors", state="normal")
    file_menu.entryconfig("Add devices", state="normal")


def create_device():
    canvas.bind("<Button-1>", lambda event: add_device(canvas, event, load_active))
    file_menu.entryconfig("Add devices", state="disabled")
    file_menu.entryconfig("Add sensors", state="normal")
    file_menu.entryconfig("Add points", state="normal")


def create_sensor():
    canvas.bind("<Button-1>", lambda event: add_sensor(canvas, event, load_active))
    file_menu.entryconfig("Add sensors", state="disabled")
    file_menu.entryconfig("Add devices", state="normal")
    file_menu.entryconfig("Add points", state="normal")


def create_wall():
    draw_line_window(canvas, window, load_active)
    file_menu.entryconfig("Add sensors", state="normal")
    file_menu.entryconfig("Add devices", state="normal")
    file_menu.entryconfig("Add points", state="normal")


# =================
#    Log/Graphs
# =================

def show_sensors_log():
    show_log(canvas, sensor_states, load_active)


def activity_log():
    show_activity_log()


def show_sensors_graphs():
    show_graphs(canvas, sensor_states)


# ==============================
#    Load / Save Scenario
# ==============================

def read_points():
    global r_points, read_walls, read_sensors, read_devices, read_doors, load_active
    load_active = True
    r_points, read_walls, read_sensors, read_devices, read_doors = read_coordinates_from_file("read_scenario.csv")
    draw_points(r_points, canvas)
    draw_walls(read_walls, r_points, canvas)
    draw_sensors(read_sensors, canvas)
    draw_devices(read_devices, canvas)
    draw_doors(read_doors, canvas)
    print(load_active)
    print("Scenario read from file\n")

# Export current scenario to 'saved.csv' in sections: Positions, Walls, Sensors, Devices, Doors.
def save():
    answer = messagebox.askyesno("Save", "Do you want to confirm saving?")
    if not answer:
        return

    with open("saved.csv", "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Positions
        csvwriter.writerow(["Positions"])
        if not load_active:
            for name, x, y in points:
                csvwriter.writerow([name, x, y])
        else:
            for name, x, y in r_points:
                csvwriter.writerow([name, x, y])

        # Walls
        csvwriter.writerow([])
        csvwriter.writerow(["Walls"])
        if not load_active:
            for i in range(0, len(walls), 2):
                if i + 1 < len(walls):
                    point1 = walls[i]
                    point2 = walls[i + 1]
                    csvwriter.writerow([point1, point2])
        else:
            for point1, point2 in read_walls:
                csvwriter.writerow([point1, point2])

        # Sensors
        csvwriter.writerow([])
        csvwriter.writerow(["Sensors"])
        if not load_active:
            for name, x, y, type, min_val, max_val, step, state, direction, consumption, associated_device in sensors:
                min_val = float(min_val); max_val = float(max_val); step = float(step); state = float(state)
                consumption = float(consumption) if consumption is not None else "None"
                csvwriter.writerow([name, x, y, type, min_val, max_val, step, state,
                                    direction if direction is not None else "None",
                                    consumption, associated_device])
        else:
            for name, x, y, type, min_val, max_val, step, state, direction, consumption, associated_device in read_sensors:
                min_val = float(min_val); max_val = float(max_val); step = float(step); state = float(state)
                consumption = float(consumption) if consumption is not None else "None"
                csvwriter.writerow([name, x, y, type, min_val, max_val, step, state,
                                    direction if direction is not None else "None",
                                    consumption, associated_device])

        # Devices
        csvwriter.writerow([])
        csvwriter.writerow(["Devices"])
        if not load_active:
            for name, x, y, type, power, state, min_consumption, max_consumption, current_consumption, consumption_direction in devices:
                x = int(x); y = int(y); power = float(power); state = int(state)
                min_consumption = float(min_consumption); max_consumption = float(max_consumption)
                current_consumption = float(current_consumption)
                csvwriter.writerow([name, x, y, type, power, state, min_consumption, max_consumption,
                                    current_consumption, consumption_direction if consumption_direction is not None else "None"])
        else:
            for name, x, y, type, power, state, min_consumption, max_consumption, current_consumption, consumption_direction in read_devices:
                x = int(x); y = int(y); power = float(power); state = int(state)
                min_consumption = float(min_consumption); max_consumption = float(max_consumption)
                current_consumption = float(current_consumption)
                csvwriter.writerow([name, x, y, type, power, state, min_consumption, max_consumption,
                                    current_consumption, consumption_direction if consumption_direction is not None else "None"])

        # Doors
        csvwriter.writerow([])
        csvwriter.writerow(["Doors"])
        if not load_active:
            for door in doors:
                x1, y1, x2, y2, state = door
                csvwriter.writerow([x1, y1, x2, y2, state])
        else:
            for door in read_doors:
                x1, y1, x2, y2, state = door
                csvwriter.writerow([x1, y1, x2, y2, state])

    print("Scenario saved successfully.")


def delete_all():
    global canvas
    answer = messagebox.askyesno("Delete", "Are you sure to delete the scenario?")
    if not answer:
        return

    for tag in ['point', 'wall', 'sensor', 'line', 'device', 'door', 'fov']:
        canvas.delete(tag)
    for list in [points, walls, sensors, devices, doors, r_points, read_walls, read_sensors,
                  read_devices, read_doors]:
        list.clear()


def exit():
    answer = messagebox.askyesno("Exit", "Are you sure you want to close the application??")
    if answer:
        window.quit()


# ===========================
#    Export Simulation Log
# ===========================
# Pick the most recent logs/*/interactions.csv and let the user choose a destination file.
def export_simulation_csv():
    # Export user path (movements, interactions with devices and sensors)
    logs_root = "logs"
    if not os.path.isdir(logs_root):
        messagebox.showwarning("No log", "No folder 'logs' found.\nStart manual simulation before export.")
        return

    candidates = []
    for name in os.listdir(logs_root):
        folder = os.path.join(logs_root, name)
        if os.path.isdir(folder):
            csv_path = os.path.join(folder, "interactions.csv")
            if os.path.isfile(csv_path):
                candidates.append((os.path.getmtime(csv_path), csv_path))

    if not candidates:
        messagebox.showwarning("No file", "'interactions.csv' not found.\nStart manual simulation and retry.")
        return

    candidates.sort(reverse=True)
    src_csv = candidates[0][1]

    dest = filedialog.asksaveasfilename(
        title="Export simulation (CSV)",
        defaultextension=".csv",
        initialfile="simulation_interactions.csv",
        filetypes=[("CSV", "*.csv"), ("All files", "*.*")]
    )
    if not dest:
        return

    try:
        shutil.copyfile(src_csv, dest)
        messagebox.showinfo("Exported", f"File exported in:\n{dest}")
    except Exception as e:
        messagebox.showerror("Error", f"Impossible to export the file:\n{e}")


# ==============================
#    Manual Simulation
# ==============================

def start_sim():
    global activity_label

    s_sensors = read_sensors if load_active else sensors
    if not s_sensors:
        messagebox.showwarning("Error", "No sensors found to start the simulation.")
        return

    # Timer + callback that start when START is pressed in the timer
    timer_app_instance = TimerApp(
        timer_frame,
        start_callback=lambda: (
            start_simulation(canvas, timer_app_instance, load_active, activity_label),
            monitor_activities(canvas, load_active, activity_label, timer_app_instance),
            # start CSV session of interactions (label = simulated time)
            start_interaction_log_session(timer_app_instance.get_simulated_time()),
            canvas.bind("<Button-1>", lambda event: interaction(canvas, timer_app_instance, event, load_active, activity_label))
        ),
        stop_callback=lambda: (
            stop_simulation(timer_app_instance),
            close_current_activity(timer_app_instance, activity_label),
            stop_interaction_log_session(),
            canvas.unbind("<Button-1>")
        )
    )

    activity_label = tk.Label(timer_frame, text="Activity: None", font=("Helvetica", 16), bg="white", fg="black")
    activity_label.pack(pady=10)

    # Periodic sensors update
    update_sensors(canvas, timer_app_instance, load_active, activity_label)

    # Disable scenario menu items during simulation
    file_menu.entryconfig("Add points", state="disabled")
    file_menu.entryconfig("Add sensors", state="disabled")
    file_menu.entryconfig("Add devices", state="disabled")
    file_menu.entryconfig("Add walls", state="disabled")
    file_menu.entryconfig("Add doors", state="disabled")

# Re-enable scenario editing after the simulation ends.
def enable_all_menus():
    file_menu.entryconfig("Add points", state="normal")
    file_menu.entryconfig("Add sensors", state="normal")
    file_menu.entryconfig("Add devices", state="normal")
    file_menu.entryconfig("Add walls", state="normal")
    file_menu.entryconfig("Add doors", state="normal")


# ==============================
#    Interface Creation
# ==============================

def load_image(canvas_obj, file_path):
    image = Image.open(file_path)
    image = image.resize((1200, 1200))
    photo = ImageTk.PhotoImage(image)
    canvas_obj.create_image(0, 0, anchor=tk.NW, image=photo, tags="background_image")
    canvas_obj.image = photo
    canvas_obj.config(scrollregion=canvas_obj.bbox(tk.ALL))


def _build_home_ui(win: tk.Tk):
    #Builds the initial interface (home) inside 'win'.

    global canvas, timer_frame, file_menu, simulation_menu, window
    window = win  # keep global reference

    image_frame = tk.Frame(win, width=900, height=900)
    image_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Scrollbar
    h_scroll = tk.Scrollbar(image_frame, orient=tk.HORIZONTAL)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    v_scroll = tk.Scrollbar(image_frame, orient=tk.VERTICAL)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Image Canvas
    canvas = tk.Canvas(image_frame, width=900, height=900, xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    h_scroll.config(command=canvas.xview)
    v_scroll.config(command=canvas.yview)

    # Load background image
    image_path = 'images/grid_25.PNG'
    load_image(canvas, image_path)

    # Frame timer
    timer_container = tk.Frame(win, bg="lightgrey", width=400)
    timer_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    timer_canvas = tk.Canvas(timer_container, bg="lightgrey")
    timer_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    timer_frame = tk.Frame(timer_canvas, bg="lightgrey", width=400)
    timer_canvas.create_window((0, 0), window=timer_frame, anchor="nw")

    # Menu
    menu_bar = Menu(win)
    win.config(menu=menu_bar)

    # Scenario Menu
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Scenario", menu=file_menu)
    file_menu.add_command(label="Add points", command=create_point)
    file_menu.add_separator()
    file_menu.add_command(label="Add devices", command=create_device)
    file_menu.add_separator()
    file_menu.add_command(label="Add walls", command=create_wall)
    file_menu.add_separator()
    file_menu.add_command(label="Add doors", command=create_door)
    file_menu.add_separator()
    file_menu.add_command(label="Add sensors", command=create_sensor)
    file_menu.add_separator()
    file_menu.add_command(label="Load file", command=read_points)
    file_menu.add_separator()
    file_menu.add_command(label="Delete", command=delete_all)
    file_menu.add_separator()
    file_menu.add_command(label="Save", command=save)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit)

    # Simulation Menu
    simulation_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Simulation", menu=simulation_menu)
    simulation_menu.add_command(label="Automatic", command=lambda: launch_automatic_interface(win))
    simulation_menu.add_separator()
    simulation_menu.add_command(label="Manual", command=start_sim)
    simulation_menu.add_separator()
    simulation_menu.add_command(label="Generate log", command=show_sensors_log)
    simulation_menu.add_separator()
    simulation_menu.add_command(label="Activity Log", command=activity_log)
    simulation_menu.add_separator()
    simulation_menu.add_command(label="Generate graphs", command=show_sensors_graphs)
    simulation_menu.add_separator()
    simulation_menu.add_command(label="Export simulations (CSV)", command=export_simulation_csv)
    simulation_menu.add_separator()


def rebuild_main_interface(win: tk.Tk):
    # Clear window and rebuild the home UI (used by the Automatic interface's "Return" button).
    for w in win.winfo_children():
        w.destroy()
    win.title("Simulator")
    _build_home_ui(win)


# ==============================
#    Run project
# ==============================

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Simulator")
    _build_home_ui(window)
    window.mainloop()
