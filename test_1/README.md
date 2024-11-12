## YAZILIMSAL OLARAK DİKKAT EDİLMESİ GEREKENLER
- VSCode yüklü olursa terminal açısından daha mantıklı olur ama başka IDE de kullanılabilir
- pcde python yüklü olmalı (python sitesinden indirilecek python3)
- python indirildikten sonra terminale pip install pyserial yazılıp enterlanacak ve pyserial indirilmiş olacak.
- serial port doğru yazılmalı python kodunda (bkz. SERIAL_PORT = 'COM3')
- baud rate aynı olmalı python ve stm32de

## KOD BAZINDA DİKKAT EDİLMESİ GEREKENLER:
- stm32 kodunu zaten ellemedim sadece hesaplamaları ve nextion kısmını çıkardım veri okuma kısmı neredeyse aynı sadece uart haberleşme ekledim sanırım
- bu python kodu sadece haberleşme düzgün oluyor mu olmuyor mu onu görmek için kodun çıktısına terminalden bakarız

## DONANIMSAL OLARAK DİKKAT EDİLMESİ GEREKENLER
- I2C haberleşmenin düzgün olabilmesi için scl ve sda pinlerine dikkat
- I2C haberleşme stabil değilse, dalgalıysa (osiloskop ile bakılabilir) pull-up direnç eklenebilirmiş datasheette öyle yazıyor.
- benim elimde fiziksel bir stm32 yok şuan o yüzden bu uart bağlantıyı nasıl yapıcan sana bırakıyorum.
