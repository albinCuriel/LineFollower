# Datasheets

Datasheets van alle onderdelen in deze robot. Elke datasheet staat als **pdf in deze map** (links kunnen verdwijnen). Waar de fabrikant geen datasheet publiceert (webwinkelonderdelen), staan de specificaties met de bron in een `.md`-bestand.

| Onderdeel | Bestand in deze map | Bron | Belangrijk voor dit project |
|---|---|---|---|
| ESP32-S3 (chip) | [ESP32-S3_datasheet.pdf](ESP32-S3_datasheet.pdf) | [Espressif](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf) | ADC1 = GPIO1–10 (werkt met wifi aan), PCNT voor de encoders |
| ESP32-S3-WROOM-1 (module) | [ESP32-S3-WROOM-1_datasheet.pdf](ESP32-S3-WROOM-1_datasheet.pdf) | [Espressif](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) | geleverd: N16R8 = 16 MB flash, 8 MB PSRAM (octal: in de Arduino IDE "OPI PSRAM" kiezen, GPIO35–37 bezet) |
| ESP32-S3 devkit (pinout) | – (online handleiding) | [DevKitC-1 user guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html) | pinvolgorde J1/J3, RGB-led, BOOT/RST |
| Pololu QTR-8A | [QTR-8A_gebruikershandleiding.pdf](QTR-8A_gebruikershandleiding.pdf), [Pololu_QTR-8A_maattekening.pdf](Pololu_QTR-8A_maattekening.pdf) | [Pololu](https://www.pololu.com/docs/0J12) | 3,3V-bypass-jumper, LEDON, optimale hoogte 3 mm |
| QRE1113 (sensor op de QTR) | [QRE1113_datasheet.pdf](QRE1113_datasheet.pdf) | [Pololu](https://www.pololu.com/file/0J117/QRE1113GR.pdf) | reflectie-optokoppelaar |
| TB6612FNG (chip) | [TB6612FNG_datasheet.pdf](TB6612FNG_datasheet.pdf) | [Toshiba, via Pololu](https://www.pololu.com/file/0J86/TB6612FNG.pdf) | VM tot 13,5 V; 1,2 A continu / 3,2 A piek per kanaal; PWM tot 100 kHz |
| TB6612FNG (module) | [TB6612FNG_module.md](TB6612FNG_module.md) | opdruk module, verkoper | **pinout van onze module**, pinrijen 0,6″ (6 gaten) uit elkaar |
| CN3903 buck 3,3 V | [CN3903.md](CN3903.md) | [Chipnet-datasheet](https://datasheet4u.com/datasheets/Chipnet/CN3903/1563378) | 4,5–36 V in, 3,3 V vast uit, ±2 A |
| GA12-N20 met encoder | [GA12-N20.md](GA12-N20.md), referentie [Pololu_micro_metal_gearmotors.pdf](Pololu_micro_metal_gearmotors.pdf) | verkoper + Pololu | 6 V, 10:1, ±1500 rpm, Hall-encoder 7 PPR, **pinvolgorde encoderprintje** |
| Pololu wiel 32×7 mm | – | [productpagina](https://www.pololu.com/product/1087) | Ø32 mm, D-as 3 mm |
| Pololu ball caster 3/8″ | [Pololu_ball_caster_3-8in.pdf](Pololu_ball_caster_3-8in.pdf) | [Pololu](https://www.pololu.com/file/0J1636/pololu-ball-caster-with-0-375in-ball.pdf) | hoogte 10,1 mm + afstandsringen |
| Pololu motorbeugel | – | [productpagina](https://www.pololu.com/product/989) | M2/#2-bouten |
| LiPo DOGCOM 2S 450 mAh | [LiPo_2S_450mAh.md](LiPo_2S_450mAh.md) | [Droneshop](https://www.droneshop.nl) | 7,4 V nominaal, 8,4 V vol, nooit onder 6,4 V ontladen |
| XT30 | – | [Amass](https://www.amass.com.cn) | 15 A continu |
