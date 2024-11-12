import tkinter as tk
import random

# Dummy data function for testing without a real device
def generate_dummy_data():
    return random.uniform(10, 100)  # Random float between 10 and 100

# Calculate functions with dummy data
def calculate_speed():
    return generate_dummy_data()

def calculate_torque():
    return generate_dummy_data()

def calculate_electrical_power():
    return generate_dummy_data()

def calculate_mechanical_power():
    return generate_dummy_data()

def calculate_efficiency(electrical_power, mechanical_power):
    if mechanical_power != 0:
        return (electrical_power / mechanical_power) * 100
    return 0

# GUI update function with dummy data
def update_gui(speed_label, torque_label, power_label, mechanical_label, efficiency_label):
    # Generate dummy values
    speed = calculate_speed()
    torque = calculate_torque()
    electrical_power = calculate_electrical_power()
    mechanical_power = calculate_mechanical_power()
    efficiency = calculate_efficiency(electrical_power, mechanical_power)

    # Update labels with dummy data
    speed_label.config(text=f"{speed:.2f} km/h")
    torque_label.config(text=f"{torque:.2f} Nm")
    power_label.config(text=f"{electrical_power:.2f} W")
    mechanical_label.config(text=f"{mechanical_power:.2f} W")
    efficiency_label.config(text=f"{efficiency:.2f} %")

    # Repeat every 1 second
    speed_label.after(1000, update_gui, speed_label, torque_label, power_label, mechanical_label, efficiency_label)

# Main function to initialize GUI
def main():
    root = tk.Tk()
    root.title("Real-Time Data Display")
    root.geometry("1000x800")
    root.configure(bg="#4d4d4d")

    # Device name
    device_name_label = tk.Label(root, text="ADS1115", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="white", width=30, height=2)
    device_name_label.place(relx=0.5, rely=0.1, anchor="center")

    # Speed
    speed_label_title = tk.Label(root, text="SPEED", font=("Helvetica", 18, "bold"), bg="#4d4d4d", fg="white")
    speed_label_title.place(relx=0.3, rely=0.3, anchor="center")
    speed_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 16), bg="#2c3e50", fg="black", width=35, height=3)
    speed_value_label.place(relx=0.3, rely=0.37, anchor="center")

    # Torque
    torque_label_title = tk.Label(root, text="TORQUE", font=("Helvetica", 18, "bold"), bg="#4d4d4d", fg="white")
    torque_label_title.place(relx=0.7, rely=0.3, anchor="center")
    torque_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 16), bg="#2c3e50", fg="black", width=35, height=3)
    torque_value_label.place(relx=0.7, rely=0.37, anchor="center")

    # Electrical Power
    electrical_power_label_title = tk.Label(root, text="ELECTRICAL POWER", font=("Helvetica", 18, "bold"), bg="#4d4d4d", fg="white")
    electrical_power_label_title.place(relx=0.3, rely=0.5, anchor="center")
    electrical_power_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 16), bg="#2c3e50", fg="black", width=35, height=3)
    electrical_power_value_label.place(relx=0.3, rely=0.57, anchor="center")

    # Mechanical Power
    mechanical_power_label_title = tk.Label(root, text="MECHANICAL POWER", font=("Helvetica", 18, "bold"), bg="#4d4d4d", fg="white")
    mechanical_power_label_title.place(relx=0.7, rely=0.5, anchor="center")
    mechanical_power_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 16), bg="#2c3e50", fg="black", width=35, height=3)
    mechanical_power_value_label.place(relx=0.7, rely=0.57, anchor="center")

    # Efficiency
    efficiency_label_title = tk.Label(root, text="EFFICIENCY", font=("Helvetica", 18, "bold"), bg="#4d4d4d", fg="white")
    efficiency_label_title.place(relx=0.5, rely=0.7, anchor="center")
    efficiency_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 16), bg="#2c3e50", fg="black", width=35, height=3)
    efficiency_value_label.place(relx=0.5, rely=0.77, anchor="center")

    # Footer
    footer_label = tk.Label(root, text="POWERED BY ALI KAGAN MART", font=("Helvetica", 12), bg="#4d4d4d", fg="white")
    footer_label.place(relx=0.95, rely=0.95, anchor="se")

    # Start updating the GUI with dummy data
    update_gui(speed_value_label, torque_value_label, electrical_power_value_label, mechanical_power_value_label, efficiency_value_label)
    
    root.mainloop()

# Run the main function
main()
