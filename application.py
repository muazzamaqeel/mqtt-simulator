import sys
import json
from pathlib import Path
import threading
from tkinter import Tk, Button, Label, messagebox
from simulator import Simulator

# Utility functions to handle config files
def default_settings():
    base_folder = Path(__file__).resolve().parent
    settings_file = base_folder / 'config/settings.json'
    return settings_file

def load_config(settings_file):
    with open(settings_file, 'r') as f:
        return json.load(f)

def save_config(settings_file, config):
    with open(settings_file, 'w') as f:
        json.dump(config, f, indent=4)

def add_pacifier(settings_file):
    config = load_config(settings_file)
    pacifier_list = config['TOPICS'][0]['LIST']
    last_pacifier = pacifier_list[-1]
    last_number = int(last_pacifier.split('/')[0])
    new_number = last_number + 1
    pacifier_list.append(f"{new_number}/ppg")
    pacifier_list.append(f"{new_number}/imu")
    save_config(settings_file, config)
    print(f"Pacifier {new_number} added.")
    messagebox.showinfo("Pacifier Added", f"Pacifier {new_number} added.")

def delete_pacifier(settings_file):
    config = load_config(settings_file)
    pacifier_list = config['TOPICS'][0]['LIST']
    if len(pacifier_list) >= 2:
        removed_imu = pacifier_list.pop()
        removed_ppg = pacifier_list.pop()
        save_config(settings_file, config)
        print(f"Pacifier {removed_imu.split('/')[0]} removed.")
        messagebox.showinfo("Pacifier Removed", f"Pacifier {removed_imu.split('/')[0]} removed.")
    else:
        print("No pacifiers left to remove.")
        messagebox.showwarning("Warning", "No pacifiers left to remove.")

# The main application class
class SimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Simulator")
        self.root.geometry("400x300")
        self.root.config(bg="#2c3e50")

        # Simulator variable
        self.simulator = None

        # Title Label
        title_label = Label(root, text="MQTT Simulator Control", font=("Arial", 14, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=10)

        # Start Button
        self.start_button = Button(root, text="Start Simulator", font=("Arial", 12, "bold"), bg="#27ae60", fg="white",
                                   command=self.start_simulator)
        self.start_button.pack(pady=5, fill='x', padx=20)

        # Stop Button
        self.stop_button = Button(root, text="Stop Simulator", font=("Arial", 12, "bold"), bg="#c0392b", fg="white",
                                  command=self.stop_simulator)
        self.stop_button.pack(pady=5, fill='x', padx=20)

        # Add Pacifier Button
        self.add_pacifier_button = Button(root, text="Add Pacifier", font=("Arial", 12, "bold"), bg="#3498db", fg="white",
                                          command=self.add_pacifier)
        self.add_pacifier_button.pack(pady=5, fill='x', padx=20)

        # Delete Pacifier Button
        self.delete_pacifier_button = Button(root, text="Delete Pacifier", font=("Arial", 12, "bold"), bg="#f39c12", fg="white",
                                             command=self.delete_pacifier)
        self.delete_pacifier_button.pack(pady=5, fill='x', padx=20)

    def start_simulator(self):
        if not self.simulator:
            settings_file = default_settings()
            self.simulator = Simulator(settings_file)
            self.simulator_thread = threading.Thread(target=self.simulator.run)
            self.simulator_thread.daemon = True
            self.simulator_thread.start()
            print("Simulator started.")
            messagebox.showinfo("Simulator", "Simulator started.")

    def stop_simulator(self):
        if self.simulator:
            self.simulator.loop = False  # Stop the simulator loop
            self.simulator = None
            print("Simulator stopped.")
            messagebox.showinfo("Simulator", "Simulator stopped.")
        self.root.quit()

    def add_pacifier(self):
        settings_file = default_settings()
        add_pacifier(settings_file)

    def delete_pacifier(self):
        settings_file = default_settings()
        delete_pacifier(settings_file)

# Main loop to run the Tkinter application
if __name__ == "__main__":
    root = Tk()
    app = SimulatorApp(root)
    root.mainloop()
