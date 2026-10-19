# Code

Arduino-code voor de ESP32-S3 (core **esp32 by Espressif 3.x**, bord *ESP32S3 Dev Module*). Alles compileert; testen op de robot volgt na de levering.

| Map / bestand | Inhoud | Status |
|---|---|---|
| [board.h](board.h) | pinverdeling: de enige plaats om pinnen te wijzigen | klaar |
| [lib](lib/readme.md) | `lf_core` (regelkern, ook gebruikt door de simulatie) + `lf_esp32` (hardwarelaag) | klaar, 133 unit tests |
| [proof of concepts](proof%20of%20concepts/readme.md) | 4 kleine programma's die elk één onderdeel testen | compileren |
| [basis](basis/readme.md) | basisprogramma volgens de cursus: commando's, flash, cyclus, interrupt, wifi | compileert |
| [finaal](finaal/readme.md) | volledige linefollower: kalibratie, PID, boost/rem, encoders, testcommando's per bouwstap | compileert |
| [sync_board.py](sync_board.py) | kopieert `board.h` naar de sketchmappen en `lib/lf_esp32` | `py -3 sync_board.py` |

De parameters zijn vooraf afgesteld in de [simulatie](../simulatie/readme.md), die dezelfde `lf_core`-code gebruikt.

Compileren en uploaden: zie [instructable stap 13](../instructable/readme.md).
