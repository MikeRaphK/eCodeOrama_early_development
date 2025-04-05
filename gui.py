import sys
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from graph import show_graph
from excel import build_codeOrama

# Dummy data report function
def print_report(project_json: dict):
    report = ""
    object_list = project_json["targets"]

    object_count = len(object_list)
    costume_count = sum(len(obj["costumes"]) for obj in object_list)
    sound_count = sum(len(obj["sounds"]) for obj in object_list)
    variable_count = sum(len(obj["variables"]) for obj in object_list)
    list_count = sum(len(obj["lists"]) for obj in object_list)

    report += "This Scratch project consists of:\n"
    report += f"{object_count} objects\n{costume_count} costumes\n"
    report += f"{sound_count} sounds\n{variable_count} variables\n{list_count} lists\n\n\n"
    report += "Printing all objects and blocks in detail...\n"

    for obj in object_list:
        report += f"-----Object '{obj['name']}'-----\n"
        for key, value in obj.items():
            report += f"{key}:\n"
            if key != "blocks":
                report += f"\t{value}\n"
            else:
                for block_id, data in value.items():
                    report += f"\tBlock with id = '{block_id}' and code = '{data['opcode']}':\n"
                    for k, v in data.items():
                        report += f"\t\t{k}\t{v}\n"
        report += "-------------------------\n\n\n"
    return report

def launch_gui(project_json: dict, sprite_communication: dict):
    root = tk.Tk()
    root.title("eCodeOrama")
    root.geometry("900x700")

    button_frame = ttk.Frame(root)
    button_frame.pack(fill=tk.X, pady=5)

    content_frame = ttk.Frame(root)
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Create scrollable Text widget for report
    text_frame = ttk.Frame(content_frame)
    text_scrollbar = ttk.Scrollbar(text_frame)
    text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    report_text = tk.Text(
        text_frame, wrap=tk.WORD, yscrollcommand=text_scrollbar.set,
        font=("Courier", 10)
    )
    report_text.pack(fill=tk.BOTH, expand=True)
    text_scrollbar.config(command=report_text.yview)

    # Plot frame
    plot_frame = ttk.Frame(content_frame)

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.pack_forget()

    def show_report():
        clear_content()
        report_text.delete("1.0", tk.END)
        report_text.insert(tk.END, print_report(project_json))
        text_frame.pack(fill=tk.BOTH, expand=True)

    def show_plot():
        clear_content()
        for widget in plot_frame.winfo_children():
            widget.destroy()

        # Render the graph and capture it as a matplotlib figure
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # Inject the sprite_communication into the graph function
        # Temporarily override plt.show() so it doesn't launch a separate window
        original_show = plt.show
        plt.show = lambda: None  # disable plt.show()

        # Call your graph function to draw on the current figure
        show_graph(sprite_communication)

        plt.show = original_show  # restore original behavior

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plot_frame.pack(fill=tk.BOTH, expand=True)

    def on_close():
        answer = messagebox.askyesno("Exit Confirmation", "Do you want to produce the codeOrama Excel?")
        if answer:
            build_codeOrama(sprite_communication)
        root.destroy()
        sys.exit()

    ttk.Button(button_frame, text="Show Report", command=show_report).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Show Graph", command=show_plot).pack(side=tk.LEFT, padx=10)
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    root.mainloop()
