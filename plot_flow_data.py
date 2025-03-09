import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d

# -----------------------------
# Data Preparation Functions
# -----------------------------

def normalize(y):
    """Normalize y data to fit within 0 and 1 (min-max scaling)."""
    if np.nanmax(y) == np.nanmin(y):
        return y
    else:
        return (y - np.nanmin(y)) / (np.nanmax(y) - np.nanmin(y))
    
def resample_fluorescence(data, m_end):
    N, M = data.shape
    new_data = np.zeros((N, m_end))
    
    for i in range(N):
        m_sample = np.max(np.nonzero(data[i])[0]) + 1 if np.any(data[i]) else 1
        if m_sample < 2:
            new_data[i] = data[i, 0]
            continue
        
        x_original = np.linspace(0, 1, m_sample)
        x_new = np.linspace(0, 1, m_end)
        f = interp1d(x_original, data[i, :m_sample], kind='linear', fill_value='extrapolate')
        new_data[i] = f(x_new)
    
    return new_data

def prepare_single_data(path, n_resample=1000):
    df = pd.read_csv(path, sep='\t', header=None)
    # Convert cell IDs using pandas numeric conversion (non-numeric become NaN)
    cell_ids = pd.to_numeric(df.values[0], errors='coerce')
    if np.isnan(cell_ids).any():
        print(f"Warning: Some cell IDs in {path} could not be converted to int. Replacing with -1.")
        cell_ids = np.nan_to_num(cell_ids, nan=-1).astype(int)
    else:
        cell_ids = cell_ids.astype(int)
    recordings = df.values[1:].T
    recordings_resampled = resample_fluorescence(recordings, n_resample)
    label = path.split('_')[-2]
    return cell_ids, recordings_resampled, label

def prepare_data(paths, n_resample=1000):
    cell_ids_list, recordings_list, labels = [], [], []
    for path in paths:
        cell_ids, recordings, label = prepare_single_data(path, n_resample)
        cell_ids_list.append(cell_ids)
        recordings_list.append(recordings)
        labels.append(label)
    return cell_ids_list, recordings_list, labels

# -----------------------------
# Plotting Functions
# -----------------------------

def plot_intensity(cell_id_interest, cell_ids_list, recordings_list, labels_list, canvas, ax,
                   figure_size, colors, show_y_tick, log_scale, normalize_data, grid, show_x_ticks, 
                   y_label, x_label, title):
    ax.clear()
    # Find the index corresponding to the selected cell ID
    cell_id_idx = np.where(cell_ids_list[0] == cell_id_interest)[0][0]
    
    for i, data_current in enumerate(recordings_list):
        curve = data_current[cell_id_idx]
        if normalize_data:
            max_val = np.max(curve)
            if max_val != 0:
                curve = curve / max_val
        ax.plot(curve, label=f'{labels_list[i]}\nMax: {round(np.max(curve),0)}', color=colors[i % len(colors)])
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if title is not None and title != "":
        ax.set_title(title)
    else:
        ax.set_title(f'Cell ID: {cell_id_interest}')
    
    if not show_y_tick:
        ax.set_yticks([])
    if not show_x_ticks:
        ax.set_xticks([])
    if log_scale:
        ax.set_yscale('log')
    if grid:
        ax.grid(True)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.subplots_adjust(right=0.75)
    canvas.draw()

def plot_average_intensity(cell_ids_list, recordings_list, labels_list, canvas, ax,
                           figure_size, colors, show_y_tick, log_scale, normalize_data, grid, show_x_ticks, 
                           y_label, x_label, title, variability_type, percentile_range):
    ax.clear()
    for i, data_current in enumerate(recordings_list):
        if normalize_data:
            data_current = np.apply_along_axis(normalize, 1, data_current)  # Normalize each row (trial)
            
        avg_profile = np.nanmean(data_current, axis=0)

        ax.plot(avg_profile, label=f'{labels_list[i]}', color=colors[i % len(colors)])
   
        if variability_type == "Standard Deviation":
            variability = np.nanstd(data_current, axis=0) 
            lower_bound = avg_profile - variability
            upper_bound = avg_profile + variability
        elif variability_type == "Standard Error":
            variability = (np.nanstd(data_current, axis=0) / np.sqrt(data_current.shape[0]))
            lower_bound = avg_profile - variability
            upper_bound = avg_profile + variability
        elif variability_type == "Percentiles":
            try:
                low, high = map(float, percentile_range.split(','))
            except Exception:
                low, high = 25.0, 75.0
            lower_bound = np.nanpercentile(data_current, low, axis=0)  # 25th percentile
            upper_bound = np.nanpercentile(data_current, high, axis=0)  # 75th percentile

        else:
            lower_bound, upper_bound = avg_profile, avg_profile

        if lower_bound is not None and upper_bound is not None:
            ax.fill_between(range(len(avg_profile)), lower_bound, upper_bound,
                            color=colors[i % len(colors)], alpha=0.3)

    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if title is not None and title != "":
        ax.set_title(title)
    else:
        ax.set_title('Average Intensity Across All Cells')
    
    if not show_y_tick:
        ax.set_yticks([])
    if not show_x_ticks:
        ax.set_xticks([])
    if log_scale:
        ax.set_yscale('log')
    if grid:
        ax.grid(True)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.subplots_adjust(right=0.75)
    canvas.draw()


def save_plot(ax, file_path):
    ax.get_figure().savefig(file_path, format='jpeg', dpi=300)

# -----------------------------
# GUI Functions and Navigation
# -----------------------------

def create_canvas(figure_size):
    global fig, ax, canvas
    if 'canvas' in globals() and canvas is not None:
        try:
            canvas.get_tk_widget().destroy()
        except:
            pass
    fig, ax = plt.subplots(figsize=figure_size)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
    return fig, ax, canvas

def update_plot(figure_size_var, colors_var, show_y_tick_var, log_scale_var,
                normalize_data_var, grid_var, show_x_ticks_var, y_label_var, x_label_var, title_var):
    global fig, ax, canvas, cell_id_var
    try:
        figure_size = tuple(map(int, figure_size_var.get().split(',')))
    except Exception as e:
        figure_size = (6, 4)
    colors = colors_var.get().split(',')
    show_y_tick = show_y_tick_var.get()
    log_scale = log_scale_var.get()
    normalize_data = normalize_data_var.get()
    grid = grid_var.get()
    show_x_ticks = show_x_ticks_var.get()
    y_label = y_label_var.get()
    x_label = x_label_var.get()
    title = title_var.get()
    create_canvas(figure_size)
    cell_id_interest = cell_id_var.get()
    plot_intensity(cell_id_interest, cell_ids_list, recordings_list, labels, canvas, ax,
                   figure_size, colors, show_y_tick, log_scale, normalize_data, grid, show_x_ticks,
                   y_label, x_label, title)

def update_average_plot(figure_size_var, colors_var, show_y_tick_var, log_scale_var,
                        normalize_data_var, grid_var, show_x_ticks_var, y_label_var, x_label_var, title_var,
                        variability_type_var, percentile_range_var):
    global fig, ax, canvas
    try:
        figure_size = tuple(map(int, figure_size_var.get().split(',')))
    except Exception as e:
        figure_size = (6, 4)
    colors = colors_var.get().split(',')
    show_y_tick = show_y_tick_var.get()
    log_scale = log_scale_var.get()
    normalize_data = normalize_data_var.get()
    grid = grid_var.get()
    show_x_ticks = show_x_ticks_var.get()
    y_label = y_label_var.get()
    x_label = x_label_var.get()
    title = title_var.get()
    variability_type = variability_type_var.get()
    percentile_range = percentile_range_var.get()
    create_canvas(figure_size)
    plot_average_intensity(cell_ids_list, recordings_list, labels, canvas, ax,
                           figure_size, colors, show_y_tick, log_scale, normalize_data, grid, show_x_ticks,
                           y_label, x_label, title, variability_type, percentile_range)

def save_current_plot():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpeg",
                                             filetypes=[("JPEG files", "*.jpeg"), ("All files", "*.*")])
    if file_path:
        save_plot(ax, file_path)

def back_to_file_selection():
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    plot_frame.pack_forget()
    file_selection_frame.pack()

def switch_to_individual():
    plot_intensity_page()

def switch_to_average():
    plot_average_page()

def plot_intensity_page():
    global cell_id_var, canvas, fig, ax
    # Clear previous widgets in the plot frame
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    # Navigation Frame
    nav_frame = tk.Frame(plot_frame)
    nav_frame.pack(side=tk.TOP, fill=tk.X)
    tk.Button(nav_frame, text="Back to File Selection", command=back_to_file_selection).pack(side=tk.LEFT)
    tk.Button(nav_frame, text="Switch to Average Plot", command=switch_to_average).pack(side=tk.LEFT)
    tk.Button(nav_frame, text="Save Plot", command=save_current_plot).pack(side=tk.LEFT)
    
    # Parameter Frame
    param_frame = tk.Frame(plot_frame)
    param_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
    
    tk.Label(param_frame, text="Select Cell ID: ").grid(row=0, column=0, padx=5, pady=2)
    cell_id_var = tk.IntVar()
    if len(cell_ids_list[0]) > 0:
        cell_id_var.set(cell_ids_list[0][0])
    tk.OptionMenu(param_frame, cell_id_var, *cell_ids_list[0]).grid(row=0, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Figure Size (w,h): ").grid(row=1, column=0, padx=5, pady=2)
    figure_size_var = tk.StringVar(value='6,4')
    tk.Entry(param_frame, textvariable=figure_size_var).grid(row=1, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Colors (comma separated): ").grid(row=2, column=0, padx=5, pady=2)
    colors_var = tk.StringVar(value='blue,red')
    tk.Entry(param_frame, textvariable=colors_var).grid(row=2, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Show Y-Tick: ").grid(row=3, column=0, padx=5, pady=2)
    show_y_tick_var = tk.BooleanVar(value=True)
    tk.Checkbutton(param_frame, variable=show_y_tick_var, text="Show Y-Tick").grid(row=3, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Log Scale: ").grid(row=4, column=0, padx=5, pady=2)
    log_scale_var = tk.BooleanVar(value=False)
    tk.Checkbutton(param_frame, variable=log_scale_var, text="Log Scale").grid(row=4, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Normalize Data: ").grid(row=5, column=0, padx=5, pady=2)
    normalize_data_var = tk.BooleanVar(value=True)
    tk.Checkbutton(param_frame, variable=normalize_data_var, text="Normalize Data").grid(row=5, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Grid: ").grid(row=6, column=0, padx=5, pady=2)
    grid_var = tk.BooleanVar(value=False)
    tk.Checkbutton(param_frame, variable=grid_var, text="Grid").grid(row=6, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Show X-Ticks: ").grid(row=7, column=0, padx=5, pady=2)
    show_x_ticks_var = tk.BooleanVar(value=True)
    tk.Checkbutton(param_frame, variable=show_x_ticks_var, text="Show X-Ticks").grid(row=7, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Y Label: ").grid(row=8, column=0, padx=5, pady=2)
    y_label_var = tk.StringVar(value='Intensity')
    tk.Entry(param_frame, textvariable=y_label_var).grid(row=8, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="X Label: ").grid(row=9, column=0, padx=5, pady=2)
    x_label_var = tk.StringVar(value='Distance - Normalised')
    tk.Entry(param_frame, textvariable=x_label_var).grid(row=9, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Title: ").grid(row=10, column=0, padx=5, pady=2)
    title_var = tk.StringVar(value='')
    tk.Entry(param_frame, textvariable=title_var).grid(row=10, column=1, padx=5, pady=2)
    
    tk.Button(param_frame, text="Plot",
              command=lambda: update_plot(figure_size_var, colors_var, show_y_tick_var, log_scale_var,
                                          normalize_data_var, grid_var, show_x_ticks_var, y_label_var, x_label_var, title_var)
              ).grid(row=11, column=0, columnspan=2, pady=5)

def plot_average_page():
    global canvas, fig, ax
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    nav_frame = tk.Frame(plot_frame)
    nav_frame.pack(side=tk.TOP, fill=tk.X)
    tk.Button(nav_frame, text="Back to File Selection", command=back_to_file_selection).pack(side=tk.LEFT)
    tk.Button(nav_frame, text="Switch to Individual Plot", command=switch_to_individual).pack(side=tk.LEFT)
    tk.Button(nav_frame, text="Save Plot", command=save_current_plot).pack(side=tk.LEFT)
    
    param_frame = tk.Frame(plot_frame)
    param_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
    
    tk.Label(param_frame, text="Figure Size (w,h): ").grid(row=0, column=0, padx=5, pady=2)
    figure_size_var = tk.StringVar(value='6,4')
    tk.Entry(param_frame, textvariable=figure_size_var).grid(row=0, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Colors (comma separated): ").grid(row=1, column=0, padx=5, pady=2)
    colors_var = tk.StringVar(value='blue,red')
    tk.Entry(param_frame, textvariable=colors_var).grid(row=1, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Show Y-Tick: ").grid(row=2, column=0, padx=5, pady=2)
    show_y_tick_var = tk.BooleanVar(value=True)
    tk.Checkbutton(param_frame, variable=show_y_tick_var, text="Show Y-Tick").grid(row=2, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Log Scale: ").grid(row=3, column=0, padx=5, pady=2)
    log_scale_var = tk.BooleanVar(value=False)
    tk.Checkbutton(param_frame, variable=log_scale_var, text="Log Scale").grid(row=3, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Normalize Data: ").grid(row=4, column=0, padx=5, pady=2)
    normalize_data_var = tk.BooleanVar(value=True)
    tk.Checkbutton(param_frame, variable=normalize_data_var, text="Normalize Data").grid(row=4, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Grid: ").grid(row=5, column=0, padx=5, pady=2)
    grid_var = tk.BooleanVar(value=False)
    tk.Checkbutton(param_frame, variable=grid_var, text="Grid").grid(row=5, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Show X-Ticks: ").grid(row=6, column=0, padx=5, pady=2)
    show_x_ticks_var = tk.BooleanVar(value=True)
    tk.Checkbutton(param_frame, variable=show_x_ticks_var, text="Show X-Ticks").grid(row=6, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Y Label: ").grid(row=7, column=0, padx=5, pady=2)
    y_label_var = tk.StringVar(value='Intensity')
    tk.Entry(param_frame, textvariable=y_label_var).grid(row=7, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="X Label: ").grid(row=8, column=0, padx=5, pady=2)
    x_label_var = tk.StringVar(value='Distance - Normalised')
    tk.Entry(param_frame, textvariable=x_label_var).grid(row=8, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Title: ").grid(row=9, column=0, padx=5, pady=2)
    title_var = tk.StringVar(value='')
    tk.Entry(param_frame, textvariable=title_var).grid(row=9, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Percentile Range (low, high): ").grid(row=10, column=0, padx=5, pady=2)
    percentile_range_var = tk.StringVar(value='25,75')
    tk.Entry(param_frame, textvariable=percentile_range_var).grid(row=10, column=1, padx=5, pady=2)
    
    tk.Label(param_frame, text="Variability Type: ").grid(row=11, column=0, padx=5, pady=2)
    variability_type_var = tk.StringVar(value='None')
    variability_options = ['None', 'Standard Deviation', 'Standard Error', 'Percentiles']
    tk.OptionMenu(param_frame, variability_type_var, *variability_options).grid(row=11, column=1, padx=5, pady=2)
    
    tk.Button(param_frame, text="Plot",
              command=lambda: update_average_plot(figure_size_var, colors_var, show_y_tick_var, log_scale_var,
                                                    normalize_data_var, grid_var, show_x_ticks_var, y_label_var, x_label_var, title_var,
                                                    variability_type_var, percentile_range_var)
              ).grid(row=12, column=0, columnspan=2, pady=5)

def proceed_to_plot(plot_type):
    global cell_ids_list, recordings_list, labels
    if file_paths:
        cell_ids_list, recordings_list, labels = prepare_data(file_paths)
        file_selection_frame.pack_forget()
        plot_frame.pack()
        if plot_type == 'individual':
            plot_intensity_page()
        elif plot_type == 'average':
            plot_average_page()

def select_files():
    global cell_ids_list, recordings_list, labels, file_paths
    new_files = filedialog.askopenfilenames(title='Select Fluorescence Data Files')
    if new_files:
        file_paths.extend(new_files)
        file_listbox.delete(0, tk.END)
        for path in file_paths:
            file_listbox.insert(tk.END, path)

def remove_selected_file():
    selected = file_listbox.curselection()
    for index in reversed(selected):
        file_paths.pop(index)
        file_listbox.delete(index)

# -----------------------------
# Main GUI Setup
# -----------------------------

def main():
    global root, file_selection_frame, plot_frame, cell_id_var, canvas, fig, ax, file_listbox, file_paths
    root = tk.Tk()
    root.title("Fluorescence Data Viewer")
    
    file_paths = []
    
    file_selection_frame = tk.Frame(root)
    file_selection_frame.pack()
    
    tk.Label(file_selection_frame, text="Select Fluorescence Data Files").pack(pady=5)
    tk.Button(file_selection_frame, text="Select Files", command=select_files).pack(pady=2)
    
    file_listbox = tk.Listbox(file_selection_frame, width=80, height=10)
    file_listbox.pack(pady=5)
    
    tk.Button(file_selection_frame, text="Remove Selected", command=remove_selected_file).pack(pady=2)
    
    tk.Button(file_selection_frame, text="Plot Individual Cells",
              command=lambda: proceed_to_plot('individual')).pack(pady=2)
    tk.Button(file_selection_frame, text="Plot Average Intensity",
              command=lambda: proceed_to_plot('average')).pack(pady=2)
    
    plot_frame = tk.Frame(root)
    
    cell_id_var = tk.IntVar()
    
    root.mainloop()

if __name__ == "__main__":
    main()