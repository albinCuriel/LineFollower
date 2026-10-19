# Datasheets

Datasheets van de onderdelen in deze robot. De links gaan naar de officiële bron, zodat je altijd de actuele versie hebt.

| Onderdeel | Datasheet / documentatie | Belangrijk voor dit project |
|---|---|---|
| ESP32-S3 (chip) | [Espressif ESP32-S3 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf) | ADC1 = GPIO1–10 (werkt met wifi aan), PCNT voor de encoders |
| ESP32-S3-WROOM-1 (module) | [WROOM-1 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) | N8R2 = 8 MB flash, 2 MB PSRAM (quad) |
| ESP32-S3 devkit | [DevKitC-1 user guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html) | pinvolgorde J1/J3, RGB-led, BOOT/RST |
| Pololu QTR-8A | [gebruikershandleiding](https://www.pololu.com/docs/0J12), [maattekening](https://www.pololu.com/file/0J1288/qtr-8x-reflectance-sensor-array-dimensions.pdf) | 3,3V-bypass-jumper, LEDON, optimale hoogte 3 mm |
| QRE1113 (sensor op de QTR) | [datasheet](https://www.pololu.com/file/0J117/QRE1113GR.pdf) | reflectie-optokoppelaar |
| TB6612FNG | [Toshiba datasheet](https://toshiba.semicon-storage.com/info/docget.jsp?did=10660) | VM tot 13,5 V; 1,2 A continu / 3,2 A piek per kanaal; PWM tot 100 kHz |
| CN3903 | zoek "CN3903 datasheet" (Consonance) | synchrone buck, 5–30 V in, uitgang vast 3,3 V |
| GA12-N20 met encoder | geen officiële datasheet. Referentie: [Pololu micro metal gearmotors](https://www.pololu.com/category/60/micro-metal-gearmotors) | 6 V, 10:1, ±1500 rpm, Hall-encoder 7 PPR |
| Pololu wiel 32×7 mm | [productpagina](https://www.pololu.com/product/1087) | Ø32 mm, D-as 3 mm |
| Pololu ball caster 3/8″ | [maattekening](https://www.pololu.com/file/0J1636/pololu-ball-caster-with-0-375in-ball.pdf) | hoogte 10,1 mm + afstandsringen |
| Pololu motorbeugel | [productpagina](https://www.pololu.com/product/989) | M2/#2-bouten |
| LiPo DOGCOM 2S 450 mAh | [Droneshop](https://www.droneshop.nl) | 7,4 V nominaal, 8,4 V vol, nooit onder 6,4 V ontladen |
| XT30 | [Amass](https://www.amass.com.cn) | 15 A continu |
