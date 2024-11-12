import serial
import time
import concurrent.futures

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

# Hesaplama fonksiyonları (örneğin hız, tork vb.)
def calculate_speed(raw_data):
    # Basit bir örnek hesaplama
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

# Ana fonksiyon
def main():
    # Seri port bağlantısını aç
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud rate")
            
            while True:
                # Veriyi oku
                raw_data = read_data(ser)
                
                if raw_data:
                    print(f"Raw Data: {raw_data}")
                    
                    # Veriyi paralel olarak işlemek için ProcessPoolExecutor kullan
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

                        # Verim hesaplaması için iki sonucu kullan
                        efficiency = calculate_efficiency(electrical_power, mechanical_power)

                        # Sonuçları yazdır
                        print(f"Speed: {speed} km/h")
                        print(f"Torque: {torque} Nm")
                        print(f"Electrical Power: {electrical_power} W")
                        print(f"Mechanical Power: {mechanical_power} W")
                        print(f"Efficiency: {efficiency:.2f} %")
                    
                    # Bekleme süresi (örneğin 1 saniye)
                    time.sleep(1)
                else:
                    print("No data received.")
                    time.sleep(1)
                
    except Exception as e:
        print(f"Error with serial connection: {e}")

if __name__ == "__main__":
    main()
