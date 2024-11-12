import serial
import time

# Seri port ayar (DİKKAT)
SERIAL_PORT = 'COM3'  # STM32 seri portu neyse o ubuntuda için ls /dev/tty* komutuyla bulucaz ve tam yolu yazıcaz örn : "/dev/ttyACM0"
BAUD_RATE = 9600      # STM32 baudrate girilecek

# PySerial ile bağlantı kurar
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Bağlandı: {SERIAL_PORT}")
except serial.SerialException:
    print(f"Port {SERIAL_PORT} Bağlanamadı! Doğru portu seç.")
    exit()

# Veriyi sürekli okuma
try:
    while True:
        # STM32'den gelen veriyi oku
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()  # Veriyi UTF-8 olarak çözecek, sonundaki boşlukları temizleyecek
            print("Gelen veri:", line)  # Gelen veriyi ekrana yazar
        time.sleep(0.1)  # 0.1 saniye delay verdik

except KeyboardInterrupt:
    print("Program durduruldu.")

finally:
    # Program kapatılırken seri bağlantıyı sonlandır
    ser.close()
    print("Bağlantı kapatıldı.")
