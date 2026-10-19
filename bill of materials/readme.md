## bill of materials
<br />

Plan B (gaatjesprint als chassis). Motivatie per onderdeel: zie [ontwerpkeuzes/onderdelenkeuze.md](../ontwerpkeuzes/onderdelenkeuze.md).
Prijzen = werkelijk betaalde prijzen (bestelling 19/10/2026).

|volgnummer|naam|omschrijving|nieuw/recup|kostprijs/stuk|aantal|subtotaal|
|----------|----|------------|-----------|---------|------|---------|
|         1|ESP32-S3 devkit N8R2|dual USB-C, wifi, headers gesoldeerd|nieuw|€6,89|1|€6,89|
|         2|Pololu QTR-8A|8 analoge reflectiesensoren, LEDON|nieuw|€19,05|1|€19,05|
|         3|TB6612FNG module|H-brug, stuurt beide motoren|nieuw|€2,10|1|€2,10|
|         4|N20 6V 10:1 met encoder|1500 rpm, Hall-encoder 7PPR|nieuw|€7,52|2|€15,04|
|         5|Pololu wiel 32×7 mm|siliconen band, paar|nieuw|€3,20|1|€3,20|
|         6|Pololu motorbeugel|paar|nieuw|€2,15|1|€2,15|
|         7|Pololu ball caster 3/8″|steunpunt vooraan|nieuw|€5,90|1|€5,90|
|         8|LiPo 2S 450 mAh 100C|XT30, JST-XH balans|nieuw|€11,95|1|€11,95|
|         9|CN3903 buck 3,3V|5–30V in, 3A|nieuw|€1,60|1|€1,60|
|        10|gaatjesprint 9×15 cm|chassis + bedrading, ingekort tot 12 cm|nieuw|€3,21|1|€3,21|
|        11|SS12D00 schuifschakelaar|aan/uit|nieuw|€0,12|1|€0,12|
|        12|XT30-pigtail (male)|batterijaansluiting|nieuw|€2,98|1|€2,98|
|        13|drukknop 6×6, weerstanden, led, condensatoren|start/stop, R 100k/33k/330, 100µF, 100nF|recup|€0,00|1|€0,00|
|        14|dupont-draad|bedrading, geknipt en gesoldeerd|recup|€0,00|1|€0,00|
|        15|boutjes en moeren|8× M2×8, 2× M2×25, ±10 M2-moeren, 2× M3×30 + 6 M3-moeren|nieuw (lokaal)|€1,50|1|€1,50|
|        16|spoiler|afgezaagd stuk van de gaatjesprint (25 × 86 mm)|recup|€0,00|1|€0,00|
| | | | | | **totaal robot** | **±€75** |

Niet in de robot, wel nodig: B3-balanslader, lipo-bag, 2e lipo en reserveonderdelen (zie bestelling hieronder).
Plan A (eigen PCB, enkel ontworpen in KiCad) vervangt 1, 3, 9, 10 en de modules door losse componenten.

## Bestelling plan B (19/10/2026)

Gebouwd op een gaatjesprint die tegelijk het chassis is. Geen eigen PCB of 3D-print laten maken.

### AliExpress (€47,64, levering 26–30 okt)

| Onderdeel | Variant | Aantal | Prijs/st |
|---|---|---|---|
| ESP32-S3 dual Type-C devkit | N8R2 weld (headers gesoldeerd) | 2 (1 reserve) | €6,89 |
| GA12-N20 6V met Hall-encoder 7PPR | 1500 RPM (10:1) | 2 | €7,52 |
| TB6612FNG module | TB6612 | 2 (1 reserve) | €2,10 |
| CN3903 buck 5–30V → 3,3V 3A | 3.3V | 2 (1 reserve) | €1,60 |
| Gaatjesprint dubbelzijdig | 9×15 cm | 1 | €3,21 |
| SS12D00 schuifschakelaar | 4 mm, 20 st. | 1 | €2,49 |
| Imax B3 balanslader 2–3S | 10W EU-stekker | 1 | €5,72 |

### Opencircuit (€40,45 incl. verzending, besteld)
| Onderdeel | Aantal | Prijs/st |
|---|---|---|
| Pololu QTR-8A | 1 | €19,05 |
| Pololu wiel 32×7 mm, paar (siliconen band) | 2 | €3,20 |
| Pololu ball caster 3/8″ plastic | 1 | €5,90 |
| Pololu micro metal gearmotor bracket, paar | 1 | €2,15 |

### Droneshop.nl (€34,80 + verzending)
| Onderdeel | Aantal | Prijs/st |
|---|---|---|
| DOGCOM 450 mAh 2S 100C XT30 | 2 | €11,95 |
| Flywoo XT30UP-M pigtail 20AWG (2 st.) | 1 | €4,95 |
| Droneshop LiPo Safe Bag medium | 1 | €5,95 |

Zelf al in huis (Arduino-kit): weerstanden (100 kΩ, 33 kΩ, 330 Ω), led, drukknoppen, elco's, breadboard, dupont-draadjes, 100 nF condensatoren.

Hoe alles gemonteerd en bedraad wordt: zie de [instructable](../instructable/readme.md).
