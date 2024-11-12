import serial
import time
import concurrent.futures
import tkinter as tk
from tkinter import ttk

# Seri port ayarları
SERIAL_PORT = 'COM3'  # Uygun portu girin
BAUD_RATE = 9600
TIMEOUT = 1  # 1 saniye timeout

# UART üzerinden veri okuma fonksiyonu
def read_data(serial_connection):
    # STM32'den gelen veriyi oku
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
    speed = float(raw_data) * 2  # Gerçek hesaplamayı burada yapın
    return speed

def calculate_torque(raw_data):
    torque = float(raw_data) * 1.5  # Gerçek hesaplamayı burada yapın
    return torque

def calculate_electrical_power(raw_data):
    electrical_power = float(raw_data) * 0.8  # Gerçek hesaplamayı burada yapın
    return electrical_power

def calculate_mechanical_power(raw_data):
    mechanical_power = float(raw_data) * 0.9  # Gerçek hesaplamayı burada yapın
    return mechanical_power

def calculate_efficiency(electrical_power, mechanical_power):
    if mechanical_power != 0:
        efficiency = (electrical_power / mechanical_power) * 100  # Verim hesaplama
    else:
        efficiency = 0
    return efficiency

# GUI güncelleme fonksiyonu
def update_gui(speed_label, torque_label, power_label, mechanical_label, efficiency_label, raw_data):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Paralel işleme fonksiyonlarına ham veriyi gönder
        future_speed = executor.submit(calculate_speed, raw_data)
        future_torque = executor.submit(calculate_torque, raw_data)
        future_electrical_power = executor.submit(calculate_electrical_power, raw_data)
        future_mechanical_power = executor.submit(calculate_mechanical_power, raw_data)

        # Hesaplamaları bekle ve al
        speed = future_speed.result()
        torque = future_torque.result()
        electrical_power = future_electrical_power.result()
        mechanical_power = future_mechanical_power.result()

        # Verim hesaplaması
        efficiency = calculate_efficiency(electrical_power, mechanical_power)

        # GUI elemanlarını güncelle
        speed_label.config(text=f"Speed: {speed:.2f} km/h")
        torque_label.config(text=f"Torque: {torque:.2f} Nm")
        power_label.config(text=f"Electrical Power: {electrical_power:.2f} W")
        mechanical_label.config(text=f"Mechanical Power: {mechanical_power:.2f} W")
        efficiency_label.config(text=f"Efficiency: {efficiency:.2f} %")

# Ana fonksiyon
def main():
    # Tkinter GUI oluşturma
    root = tk.Tk()
    root.title("Real-Time Data Display")
    root.geometry("400x400")
    root.configure(bg="#2c3e50")
    
    # Başlık etiketleri
    title_label = tk.Label(root, text="Real-Time Data", font=("Helvetica", 16), bg="#2c3e50", fg="white")
    title_label.pack(pady=10)

    # Sonuçları gösterecek etiketler
    speed_label = ttk.Label(root, text="Speed: 0 km/h", font=("Helvetica", 12), foreground="white", background="#2c3e50")
    speed_label.pack(pady=5)
    
    torque_label = ttk.Label(root, text="Torque: 0 Nm", font=("Helvetica", 12), foreground="white", background="#2c3e50")
    torque_label.pack(pady=5)
    
    power_label = ttk.Label(root, text="Electrical Power: 0 W", font=("Helvetica", 12), foreground="white", background="#2c3e50")
    power_label.pack(pady=5)

    mechanical_label = ttk.Label(root, text="Mechanical Power: 0 W", font=("Helvetica", 12), foreground="white", background="#2c3e50")
    mechanical_label.pack(pady=5)

    efficiency_label = ttk.Label(root, text="Efficiency: 0%", font=("Helvetica", 12), foreground="white", background="#2c3e50")
    efficiency_label.pack(pady=5)
    
    # Seri port bağlantısını aç
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud rate")
            
            while True:
                # Veriyi oku
                raw_data = read_data(ser)
                
                if raw_data:
                    print(f"Raw Data: {raw_data}")
                    update_gui(speed_label, torque_label, power_label, mechanical_label, efficiency_label, raw_data)
                
                # GUI'yi güncelle
                root.update_idletasks()
                root.update()

                # Bekleme süresi (örneğin 1 saniye)
                time.sleep(1)
                
    except Exception as e:
        print(f"Error with serial connection: {e}")
        root.quit()

    root.mainloop()

if __name__ == "__main__":
    main()
