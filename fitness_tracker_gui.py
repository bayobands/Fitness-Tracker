import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

DATA_FILE = "fitness_tracker.json"
WORKOUT_DAYS = {
    "Day 1 - Chest & Back": ["Bench Press", "Incline Dumbbell Press", "Pull-Downs", "Seated Cable Rows"],
    "Day 2 - Shoulders & Arms": ["Shoulder Press", "Lateral Raises", "Bicep Curls", "Tricep Pulldowns"],
    "Day 3 - Legs": ["Squats", "Deadlifts", "Leg Press", "Hamstring Curls"],
    "Day 4 - Rest": []
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Progress Tracker")
        self.root.configure(bg="#f7f7f7")
        self.data = load_data()

        # Header
        header = tk.Label(root, text="Workout Tracker", font=("Arial", 16, "bold"), bg="#4caf50", fg="white", pady=10)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Workout Day Selection
        frame = tk.Frame(root, bg="#e0e0e0", padx=10, pady=10, relief="groove", bd=2)
        frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.day_label = tk.Label(frame, text="Select Workout Day:", font=("Arial", 12), bg="#e0e0e0")
        self.day_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.day_var = tk.StringVar()
        self.day_menu = ttk.Combobox(frame, textvariable=self.day_var, state="readonly", font=("Arial", 10))
        self.day_menu["values"] = list(WORKOUT_DAYS.keys())
        self.day_menu.grid(row=0, column=1, padx=5, pady=5)
        self.day_menu.bind("<<ComboboxSelected>>", self.update_exercise_menu)

        # Exercise Selection
        self.exercise_label = tk.Label(frame, text="Select Exercise:", font=("Arial", 12), bg="#e0e0e0")
        self.exercise_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.exercise_var = tk.StringVar()
        self.exercise_menu = ttk.Combobox(frame, textvariable=self.exercise_var, state="readonly", font=("Arial", 10))
        self.exercise_menu.grid(row=1, column=1, padx=5, pady=5)

        # Max Weight Entry
        self.weight_label = tk.Label(frame, text="Enter Max Weight (lbs):", font=("Arial", 12), bg="#e0e0e0")
        self.weight_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.weight_entry = tk.Entry(frame, font=("Arial", 10))
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        self.log_button = tk.Button(root, text="Log Max Weight", bg="#4caf50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, command=self.log_max_weight)
        self.log_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.view_button = tk.Button(root, text="View Progress", bg="#2196f3", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, command=self.view_progress)
        self.view_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    def update_exercise_menu(self, event):
        selected_day = self.day_var.get()
        self.exercise_menu["values"] = WORKOUT_DAYS.get(selected_day, [])

    def log_max_weight(self):
        day = self.day_var.get()
        exercise = self.exercise_var.get()
        weight = self.weight_entry.get()
        if not day or not exercise or not weight:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        try:
            weight = float(weight)
        except ValueError:
            messagebox.showerror("Error", "Weight must be a number.")
            return
        self.data.setdefault(day, {})
        self.data[day][exercise] = max(weight, self.data[day].get(exercise, 0))
        save_data(self.data)
        messagebox.showinfo("Success", f"Max weight for {exercise} updated to {self.data[day][exercise]} lbs.")

    def view_progress(self):
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Progress")
        row = 0
        for day, exercises in self.data.items():
            tk.Label(progress_window, text=f"{day}:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            row += 1
            for exercise, weight in exercises.items():
                tk.Label(progress_window, text=f"  {exercise}: {weight} lbs", font=("Arial", 10)).grid(row=row, column=0, sticky="w", padx=20, pady=2)
                row += 1
        if not self.data:
            tk.Label(progress_window, text="No progress logged yet.", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
