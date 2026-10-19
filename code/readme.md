# Code

Arduino-code voor de ESP32-S3 (core **esp32 by Espressif 3.x**, bord *ESP32S3 Dev Module*).

| Map / bestand | Inhoud | Status |
|---|---|---|
| [board.h](board.h) | hardwarelaag: alle pinnen en PWM-instellingen. Wissel je naar het backupbord (ATmega32U4), dan verandert enkel dit bestand | klaar |
| [proof of concepts](proof%20of%20concepts/readme.md) | 4 kleine programma's die elk één onderdeel testen: sensor, H-brug, start/stop-interrupt, wifi | compileren, nog te testen op hardware |
| [basis](basis/readme.md) | basisprogramma: instellingen via commando's, EEPROM, cyclustijd, start/stop | volgt |
| [finaal](finaal/readme.md) | finale linefollower-code met kalibratie en PID | volgt |

Elke sketchmap bevat een kopie van `board.h`, omdat Arduino enkel bestanden uit de eigen sketchmap meeneemt. Pas je de pinnen aan, doe dat dan in `code/board.h` en kopieer het bestand naar de sketchmappen.

Compileren en uploaden: zie [instructable stap 13](../instructable/readme.md).
