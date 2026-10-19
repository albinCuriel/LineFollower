# lf_esp32

Hardwarelaag voor de ESP32-S3 (plan B). Wissel je naar het backupbord (ATmega32U4), dan vervang je enkel deze bibliotheek; `lf_core` blijft dezelfde.

| Bestand | Inhoud |
|---|---|
| [board.h](src/board.h) | pinverdeling (kopie van [code/board.h](../../board.h), bijwerken met `py -3 code/sync_board.py`) |
| [hw.h](src/hw.h) | sensoren lezen met LEDON aan/uit, motoren (PWM 20 kHz), encoders via de hardwareteller PCNT (kwadratuur x4, snelheid over 10 ms), batterijspanning, start/stop-knop met interrupt en ontdendering, statusled |
| [comms.h](src/comms.h) | commando's via USB en wifi tegelijk (eigen netwerk "linefollower", TCP-poort 23) |
| [opslag.h](src/opslag.h) | parameters en kalibratie bewaren in het flashgeheugen (Preferences/NVS) |

Wachtwoord van het wifinetwerk: `WIFI_WACHTWOORD` in [comms.h](src/comms.h) - aanpassen vóór gebruik.
