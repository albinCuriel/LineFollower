# Bibliotheken

| Map | Inhoud | Gebruikt door |
|---|---|---|
| [lf_core](lf_core/readme.md) | hardware-onafhankelijke kern: parameters, sensorverwerking (kalibratie, normalisatie, interpolatie), PID, snelheidsprofiel, commando's | firmware (basis, finaal) **en** de [simulatie](../../simulatie/readme.md) |
| [lf_esp32](lf_esp32/readme.md) | ESP32-S3-hardwarelaag: sensoren met LEDON, motoren, encoders (PCNT), batterij, knop, statusled, wifi/USB-commando's, opslag in flash | firmware (basis, finaal) |

Compileren met beide bibliotheken:
```
arduino-cli compile --fqbn esp32:esp32:esp32s3 --library code/lib/lf_core --library code/lib/lf_esp32 code/finaal/linefollower
```
Arduino IDE: *Schets > Bibliotheek gebruiken > .ZIP-bibliotheek toevoegen* en kies de map `lf_core`, daarna `lf_esp32`.
