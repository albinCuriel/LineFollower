# Ontwerpkeuzes

Waarom de robot er zo uitziet en welke onderdelen gekozen zijn.

| Bestand | Inhoud |
|---|---|
| [onderdelenkeuze.md](onderdelenkeuze.md) | analyse van vorige jaren, snelheidsberekening en simulatie, keuze per onderdeel met motivatie, pinverdeling, budget, backupplan |
| [microcontroller-vergelijking.md](microcontroller-vergelijking.md) | vergelijking van de mogelijke microcontrollers |

Samengevat: de ESP32-S3 is gekozen omdat debuggen en fijnafstellen via wifi veel sneller gaan: live meetwaarden, instellingen en een rondelog. De backup is de ATmega32U4. Dankzij [code/board.h](../code/board.h) verandert dan enkel de hardwarelaag.
