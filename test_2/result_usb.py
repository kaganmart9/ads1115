import serial
import time
import tkinter as tk

# USB CDC bağlantısı için seri port ayarları
USB_PORT = 'COM3'  # STM32 cihazının USB ile bağlı olduğu uygun portu belirtin
BAUD_RATE = 9600
TIMEOUT = 1  # 1 saniye timeout

# USB üzerinden veri okuma fonksiyonu
def read_data(serial_connection):
    try:
        data = serial_connection.readline().decode('utf-8').strip()
        if data:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

# Hesaplama fonksiyonları
def calculate_speed(raw_data):
    return float(raw_data) * 2  # Gerçek hesaplamayı burada yapın

def calculate_torque(raw_data):
    return float(raw_data) * 1.5  # Gerçek hesaplamayı burada yapın

def calculate_electrical_power(raw_data):
    return float(raw_data) * 0.8  # Gerçek hesaplamayı burada yapın

def calculate_mechanical_power(raw_data):
    return float(raw_data) * 0.9  # Gerçek hesaplamayı burada yapın

def calculate_efficiency(electrical_power, mechanical_power):
    if mechanical_power != 0:
        return (electrical_power / mechanical_power) * 100
    return 0

# GUI güncelleme fonksiyonu
def update_gui(serial_connection, speed_label, torque_label, power_label, mechanical_label, efficiency_label):
    raw_data = read_data(serial_connection)
    if raw_data is not None:
        try:
            # Hesaplamaları yap ve GUI'yi güncelle
            speed = calculate_speed(raw_data)
            torque = calculate_torque(raw_data)
            electrical_power = calculate_electrical_power(raw_data)
            mechanical_power = calculate_mechanical_power(raw_data)
            efficiency = calculate_efficiency(electrical_power, mechanical_power)

            # Değerleri GUI'ye yazdır
            speed_label.config(text=f"{speed:.2f} km/h")
            torque_label.config(text=f"{torque:.2f} Nm")
            power_label.config(text=f"{electrical_power:.2f} W")
            mechanical_label.config(text=f"{mechanical_power:.2f} W")
            efficiency_label.config(text=f"{efficiency:.2f} %")
        except ValueError:
            print("Invalid data received for calculation")

    # Her 1 saniyede bir fonksiyonu tekrar çalıştır
    speed_label.after(1000, update_gui, serial_connection, speed_label, torque_label, power_label, mechanical_label, efficiency_label)

# Ana fonksiyon
def main():
    # USB CDC bağlantısını başlat
    serial_connection = serial.Serial(USB_PORT, BAUD_RATE, timeout=TIMEOUT)

    root = tk.Tk()
    root.title("Real-Time Data Display")
    root.geometry("800x600")
    root.configure(bg="#4d4d4d")

    # Device name
    device_name_label = tk.Label(root, text="CIHAZ ISMI", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="white", width=20, height=2)
    device_name_label.place(relx=0.5, rely=0.1, anchor="center")

    # Speed
    speed_label_title = tk.Label(root, text="SPEED", font=("Helvetica", 12, "bold"), bg="#4d4d4d", fg="white")
    speed_label_title.place(relx=0.3, rely=0.3, anchor="center")
    speed_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 10), bg="#2c3e50", fg="black", width=25, height=2)
    speed_value_label.place(relx=0.3, rely=0.35, anchor="center")

    # Torque
    torque_label_title = tk.Label(root, text="TORQUE", font=("Helvetica", 12, "bold"), bg="#4d4d4d", fg="white")
    torque_label_title.place(relx=0.7, rely=0.3, anchor="center")
    torque_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 10), bg="#2c3e50", fg="black", width=25, height=2)
    torque_value_label.place(relx=0.7, rely=0.35, anchor="center")

    # Electrical Power
    electrical_power_label_title = tk.Label(root, text="ELECTRICAL POWER", font=("Helvetica", 12, "bold"), bg="#4d4d4d", fg="white")
    electrical_power_label_title.place(relx=0.3, rely=0.5, anchor="center")
    electrical_power_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 10), bg="#2c3e50", fg="black", width=25, height=2)
    electrical_power_value_label.place(relx=0.3, rely=0.55, anchor="center")

    # Mechanical Power
    mechanical_power_label_title = tk.Label(root, text="MECHANICAL POWER", font=("Helvetica", 12, "bold"), bg="#4d4d4d", fg="white")
    mechanical_power_label_title.place(relx=0.7, rely=0.5, anchor="center")
    mechanical_power_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 10), bg="#2c3e50", fg="black", width=25, height=2)
    mechanical_power_value_label.place(relx=0.7, rely=0.55, anchor="center")

    # Efficiency
    efficiency_label_title = tk.Label(root, text="EFFICIENCY", font=("Helvetica", 12, "bold"), bg="#4d4d4d", fg="white")
    efficiency_label_title.place(relx=0.5, rely=0.7, anchor="center")
    efficiency_value_label = tk.Label(root, text="Calculating...", font=("Helvetica", 10), bg="#2c3e50", fg="black", width=25, height=2)
    efficiency_value_label.place(relx=0.5, rely=0.75, anchor="center")

    # Footer
    footer_label = tk.Label(root, text="POWERED BY ALI KAGAN MART", font=("Helvetica", 8), bg="#4d4d4d", fg="white")
    footer_label.place(relx=0.95, rely=0.95, anchor="se")

    # GUI'yi başlat ve seri veriyi güncelle
    update_gui(serial_connection, speed_value_label, torque_value_label, electrical_power_value_label, mechanical_power_value_label, efficiency_value_label)
    
    root.mainloop()

# Uncomment below to run the code.
main()
