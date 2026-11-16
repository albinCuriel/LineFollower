# Code

Arduino-code voor de ESP32-S3 (core **esp32 by Espressif 3.3.12**, bord *ESP32S3 Dev Module*, PSRAM "OPI PSRAM" voor de N16R8).

[![compileer firmware](https://github.com/albinCuriel/LineFollower/actions/workflows/compile.yml/badge.svg)](https://github.com/albinCuriel/LineFollower/actions/workflows/compile.yml)
Elke push wordt automatisch gecompileerd door een [GitHub Action](../.github/workflows/compile.yml). Lokaal resultaat (16/11/2026, `arduino-cli compile --fqbn esp32:esp32:esp32s3 --library code/lib/lf_core --library code/lib/lf_esp32 <map>`):

| Sketch | Flashgebruik |
|---|---|
| basis/basis | 896 301 bytes (68 %) |
| finaal/linefollower | 926 576 bytes (70 %) |
| poc_blink | 298 746 bytes (22 %) |
| poc_sensor | 313 578 bytes (23 %) |
| poc_hbridge | 309 745 bytes (23 %) |
| poc_interrupt | 304 850 bytes (23 %) |
| poc_wifi | 860 264 bytes (65 %) |

Testen op de robot gebeurt per bouwstap (zie de testtabel in [finaal](finaal/readme.md)).

| Map / bestand | Inhoud | Status |
|---|---|---|
| [board.h](board.h) | pinverdeling: de enige plaats om pinnen te wijzigen | klaar |
| [lib](lib/readme.md) | `lf_core` (regelkern, ook gebruikt door de simulatie) + `lf_esp32` (hardwarelaag) | klaar, 133 unit tests |
| [proof of concepts](proof%20of%20concepts/readme.md) | 5 kleine programma's die elk één onderdeel testen (blink, sensor, H-brug, interrupt, wifi) | compileren |
| [upload.ps1](upload.ps1) | compileert en uploadt een sketch: `.\upload.ps1 finaal -Monitor` | PowerShell |
| [basis](basis/readme.md) | basisprogramma volgens de cursus: commando's, flash, cyclus, interrupt, wifi | compileert |
| [finaal](finaal/readme.md) | volledige linefollower: kalibratie, PID, boost/rem, encoders, testcommando's per bouwstap | compileert |
| [sync_board.py](sync_board.py) | kopieert `board.h` naar de sketchmappen en `lib/lf_esp32` | `py -3 sync_board.py` |

De parameters zijn vooraf afgesteld in de [simulatie](../simulatie/readme.md), die dezelfde `lf_core`-code gebruikt.

Compileren en uploaden: zie [instructable stap 13](../instructable/readme.md).
