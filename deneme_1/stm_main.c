#include "main.h"
#include "math.h"
#include "stdio.h"
#include "stdlib.h"

// I2C ve UART tanımlamaları
I2C_HandleTypeDef hi2c1; // I2C haberleşmesi için tanımlama
UART_HandleTypeDef huart1; // UART haberleşmesi için tanımlama

#define ADS1115_ADDRESS 0x48 // ADS1115 I2C adresi

float voltage[4]; // Her kanal için okunan voltajları saklamak için dizi

// Fonksiyon prototipleri
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_USART1_UART_Init(void);

// ADS1115'den voltajları okuyan fonksiyon
void readADS1115Voltages(float *voltages, I2C_HandleTypeDef *hi2c, uint8_t address) {
    uint8_t ADSwrite[3]; // ADS1115'e gönderilecek veriler için tampon
    uint8_t ADSread[2]; // ADS1115'den alınacak veriler için tampon
    int16_t reading; // 16-bitlik ham okuma verisi

    // Tüm kanallardan (A0-A3) veri okumak için döngü
    for (int i = 0; i < 4; i++) {
        ADSwrite[0] = 0x01; // ADS1115 config kaydı adresi
        
        // Kanala göre yapılandırma ayarı
        switch (i) {
            case 0: ADSwrite[1] = 0xC2; break; // Kanal A0
            case 1: ADSwrite[1] = 0xD2; break; // Kanal A1
            case 2: ADSwrite[1] = 0xE2; break; // Kanal A2
            case 3: ADSwrite[1] = 0xF2; break; // Kanal A3
        }
        ADSwrite[2] = 0xE5; // Örnekleme oranı
        
        // Konfigürasyon ayarlarını ADS1115'e gönder
        HAL_I2C_Master_Transmit(hi2c, address << 1, ADSwrite, 3, 100);

        ADSwrite[0] = 0x00; //conversion verisini okumak için adresi ayarlıyoruz
        HAL_I2C_Master_Transmit(hi2c, address << 1, ADSwrite, 1, 100);

        // Ölçüm yapılması için kısa bir gecikme
        HAL_Delay(5); //hacı bunu 5 yaptım ama düşürüp yükseltip deneriz emin olamadım

        // Dönüşüm verisini alıyoruz
        HAL_I2C_Master_Receive(hi2c, address << 1, ADSread, 2, 100);

        // İki baytlık veriyi birleştirerek 16-bitlik okuma değeri elde ediyoruz
        reading = (ADSread[0] << 8) | ADSread[1];

        // Negatif okumaları sıfırla (opsiyonel güvenlik önlemi için) (real-time olduğu için bu işe yarıyor mu gram fikrim yok)
        if (reading < 0) {
            reading = 0;
        }

        // Voltaj değeri olarak sakla, her bir ham okuma değeri 0.000125V'a karşılık gelir
        voltages[i] = reading * 0.000125; //datasheet öyle diyor ???
    }
}

// UART üzerinden voltaj verilerini gönderme fonksiyonu
void sendVoltageData() {
    char uartBuf[50]; // UART gönderim tamponu
    for (int i = 0; i < 4; i++) {
        // Voltaj değerini tamponda formatla ve UART ile gönder
        int len = sprintf(uartBuf, "Voltage[%d]: %.3f\r\n", i, voltage[i]);
        HAL_UART_Transmit(&huart1, (uint8_t *)uartBuf, len, 100);
    }
}

int main(void) {
    HAL_Init(); // STM32 HAL kütüphanesini başlat
    SystemClock_Config(); // Sistem saatini yapılandır
    MX_GPIO_Init(); // GPIO'ları başlat
    MX_I2C1_Init(); // I2C'yi başlat
    MX_USART1_UART_Init(); // UART'ı başlat

    // Sonsuz döngü
    while (1) {
        readADS1115Voltages(voltage, &hi2c1, ADS1115_ADDRESS); // ADS1115'den voltaj verilerini oku
        sendVoltageData(); // Okunan verileri UART ile gönder
        HAL_Delay(10); // Kısa bir gecikme, verileri sürekli göndermemek için (bu da duruma göre değiştirilebilir)
    }
}
