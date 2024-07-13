import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import json5
import os
import subprocess
import threading
import queue

class ConfigEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("Config Editor")
        self.root.geometry("800x600")  # Set the initial size of the window
        self.root.configure(bg='#2e2e2e')
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.config_data = {}
        self.explanations = {
            "debug_level": "Debug levels (10 - Debug, 20 - Info, 30 - Warning, 40 - Error, 50 - Critical)",
            "noise_intensity": "Noise Intensity",
            "mute_original_audio": "Will the audio be muted?",
            "trollface_left_x": "Trollface position from left (X coordinate)",
            "trollface_left_y": "Trollface position from top (Y coordinate)",
            "use_trollface": "Enable Trollface",
            "use_cascade": "Enable face detection",
            "cascade": "What face detection model will be used (not recommended to change)",
            "trollface_folder": "Where the trollfaces are picked",
            "choose_trollface": "What trollface do you want to use (If no value then random will be picked)",
            "audio_file": "Audio file. Will be ignored if pick_random_audio is true",
            "pick_random_audio": "Picks a random audio from resources/audio.json",
            "random_audio_json": "Audio.json file",
            "output_file": "Output file",
            "batch_size": "Batch size for multiprocessing",
            "freeze_frame_duration": "How long until the freeze frame ends (will be ignored if pick_random_audio is true)",
            "start_frame": "How many seconds until the edit starts (will be ignored if pick_random_audio is true)",
            "threads": "How many threads are used for movie.py",
            "trollface_size": "How big will the Trollface is?",
            "use_multiprocessing": "Use multiprocessing for open-cv processing (recommended)",
            "freeze_video": "Freeze the video when the edit starts (freeze-frame)",
            "face": "What face will be used for trollface",
            "use_top_left_for_trollface": "Use top left for trollface (will be ignored if put_trollface_in_middle is true and a face is detected)",
            "change_trollface_size_for_face": "Change the trollface size so its the same as the face",
            "watermark_text": "Watermark Text",
            "fontscale": "Watermark font scale",
            "thickness": "Watermark thickness",
            "put_watermark_in_top_left": "Put the watermark in top left?",
            "watermark_space": "Watermark space",
            "watermark_color": "Watermark color",
            "use_multiple_trollfaces": "Use multiple trollfaces",
            "glitch_cut_chance": "Chance of the video being cut",
            "allow_drawing_lines": "Allow drawing lines for glitch",
            "allow_glitch_cut": "Allow the video being cut",
            "draw_line_chance": "Chance of a line being drawn in the video",
            "line_color": "Line color",
            "allow_pixelation": "Allows pixelation",
            "motion_blur_size_max": "Max motion blur size",
            "motion_blur_size_min": "Min motion blur size",
            "pixelation_chance": "Pixelation chance",
            "allow_color_distortion": "Allows color distortion",
            "color_distortion_chance": "Color distortion chance",
            "allow_recursive_glitch": "Re-runs the glitch() function",
            "recursive_glitch_chance": "Chance of re-running the glitch() function",
            "allow_glitch": "Allows the glitch",
            "glitch_chance": "The chance of the glitch happening",
            "put_trollface_in_middle": "Put the trollface in the middle (will be ignored if a face is detected)",
            "middle_space": "How much will be added in both X and Y coordinates",
            "trollface_x": "Trollface X (If this value is anything other than 0 then ANY trollface related values will be ignored)",
            "trollface_y": "Trollface Y (If this value is anything other than 0 then ANY trollface related values will be ignored)",
            "audio_codec": "Audio codec (recommended to not change)",
            "codec": "Video codec (recommended to not change)",
            "fadein_duration": "Fade-in duration",
            "video": "Video (will not ask the user for a video if this is set)",
            "timestamp": "Same as video but for duration",
            "pixelation_intensity": "Pixelation intensity"
        }

        self.create_widgets()

    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg='#2e2e2e')
        title_frame.grid(row=0, column=0, columnspan=3, sticky='w')

        self.title_label = tk.Label(title_frame, text="Contentfarm Configurator", font=("Helvetica", 14), fg="white", bg='#2e2e2e')
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.author_label = tk.Label(title_frame, text="Made by vproton0", font=("Helvetica", 10), fg="white", bg='#2e2e2e')
        self.author_label.grid(row=1, column=0, padx=10, pady=0, sticky='w')

        button_frame = tk.Frame(self.root, bg='#2e2e2e')
        button_frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=10)

        self.load_button = tk.Button(button_frame, text="Load Config", command=self.load_config)
        self.load_button.pack(side='left', padx=5, pady=10)

        self.save_button = tk.Button(button_frame, text="Save Config", command=self.save_config)
        self.save_button.pack(side='left', padx=5, pady=10)

        self.run_button = tk.Button(button_frame, text="Run", command=self.run_script)
        self.run_button.pack(side='left', padx=5, pady=10)

        self.update_button = tk.Button(button_frame, text="Update", command=self.update_repo)
        self.update_button.pack(side='left', padx=5, pady=10)

        # Scrollable frame for configuration entries
        self.entries_frame_container = tk.Frame(self.root, bg='#2e2e2e')
        self.entries_frame_container.grid(row=2, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)
        self.entries_frame_container.grid_rowconfigure(0, weight=1)
        self.entries_frame_container.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.entries_frame_container, bg='#2e2e2e')
        self.scrollbar = ttk.Scrollbar(self.entries_frame_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#2e2e2e')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Text widget for output display
        # Text widget for output display
        self.output_text = tk.Text(self.root, height=30, width=100, fg="white",
                                   bg='#2e2e2e')  # Increase the height and width
        self.output_text.grid(row=3, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)

        # Configure the row that contains the Text widget to expand
        self.root.grid_rowconfigure(3, weight=1)
        self.output_text.grid_columnconfigure(0, weight=1)

        # Insert initial text
        self.output_text.insert(tk.END, "Press the run button to see the output.\n")

        # Disable typing in the output screen
        self.output_text.config(state='disabled')

        # Scrollbar for output text widget
        self.output_scrollbar = ttk.Scrollbar(self.output_text, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=self.output_scrollbar.set)
        self.output_scrollbar.pack(side="right", fill="y")

    def load_config(self):
        file_path = filedialog.askopenfilename(defaultextension=".jsonc",
                                               filetypes=[("Contentfarm Configuration", "*.jsonc")])
        if file_path:
            with open(file_path, 'r') as file:
                self.config_data = json5.load(file)
            self.display_config()

    def display_config(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        row = 0
        for key, value in self.config_data.items():
            explanation = self.explanations.get(key,
                                                "Unknown config. Check for configurator updates in the GitHub Repo")

            tk.Label(self.scrollable_frame, text=explanation, font=("Helvetica", 10), fg="white", bg='#2e2e2e').grid(
                row=row, column=0, sticky='w', pady=2)

            if isinstance(value, bool):
                # Create a Combobox for boolean values
                combobox = ttk.Combobox(self.scrollable_frame, values=[True, False])
                combobox.set(value)
                combobox.grid(row=row, column=1, pady=2)
                combobox.bind("<<ComboboxSelected>>", lambda e, k=key: self.update_config_data(k, e))
            else:
                entry = tk.Entry(self.scrollable_frame, fg="white", bg="#2e2e2e")
                entry.grid(row=row, column=1, pady=2)
                entry.insert(0, str(value))
                entry.config(fg="white", bg="#2e2e2e")
                entry.bind("<FocusOut>", lambda e, k=key: self.update_config_data(k, e))

            row += 1

    def update_config_data(self, key, event):
        value = event.widget.get()
        if isinstance(event.widget, ttk.Combobox):
            self.config_data[key] = value == "True"
        elif value.isdigit():
            self.config_data[key] = int(value)
        else:
            try:
                self.config_data[key] = float(value)
            except ValueError:
                self.config_data[key] = value

    def save_config(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jsonc",
                                                 filetypes=[("Contentfarm Configuration", "*.jsonc")])
        if file_path:
            with open(file_path, 'w') as file:
                json5.dump(self.config_data, file, indent=2, quote_keys=True)

    def run_script(self):
        # Enable typing in the output screen
        self.output_text.config(state='normal')

        self.output_text.delete(1.0, tk.END)
        self.process_queue = queue.Queue()
        threading.Thread(target=self.execute_script, daemon=True).start()
        self.root.after(100, self.check_output_queue)

    def execute_script(self):
        try:
            process = subprocess.Popen(
                ["python3", "main.py"],
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in iter(process.stdout.readline, ""):
                self.process_queue.put(line)
            for line in iter(process.stderr.readline, ""):
                self.process_queue.put(line)
        except Exception as e:
            self.process_queue.put(f"Failed to run main.py:\n{e}")

    def check_output_queue(self):
        while not self.process_queue.empty():
            line = self.process_queue.get_nowait()
            self.output_text.insert(tk.END, line)
            self.output_text.see(tk.END)
        self.root.after(100, self.check_output_queue)

    def update_repo(self):
        try:
            subprocess.run(["git", "pull"], cwd=os.getcwd(), check=True)
            messagebox.showinfo("Success", "Repository updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update repository:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigEditor(root)
    root.mainloop()
