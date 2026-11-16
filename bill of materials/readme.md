## bill of materials
<br />

Plan B (gaatjesprint als chassis). Motivatie per onderdeel: zie [ontwerpkeuzes/onderdelenkeuze.md](../ontwerpkeuzes/onderdelenkeuze.md).
Prijzen = werkelijk betaalde prijzen (bestelling 19/10/2026). De kolom *aankoopbron* linkt naar het product. Voor AliExpress is dat een zoeklink, omdat de links van losse verkopers snel verdwijnen: kies de variant uit de kolom *omschrijving*.

De richtprijs uit de specificaties is ±€50. Deze robot kost meer door de keuze voor de originele Pololu-sensor (€19) en een LiPo met hoge ontlaadstroom (€12); de motivatie staat in de ontwerpkeuzes. Een CSV-versie staat in [bom_planB.csv](bom_planB.csv).

|volgnummer|naam|omschrijving|nieuw/recup|kostprijs/stuk|aantal|subtotaal|aankoopbron|
|----------|----|------------|-----------|---------|------|---------|-----------|
|         1|ESP32-S3 devkit N16R8|dual USB-C, wifi, headers gesoldeerd, 16 MB flash, 8 MB PSRAM|nieuw|€6,89|1|€6,89|[AliExpress](https://www.aliexpress.com/w/wholesale-ESP32-S3-N16R8-dual-type-c-devkit.html)|
|         2|Pololu QTR-8A|8 analoge reflectiesensoren, LEDON|nieuw|€19,05|1|€19,05|[Opencircuit](https://opencircuit.shop/product/qtr-8a-reflectance-sensor-array)|
|         3|TB6612FNG module|H-brug, stuurt beide motoren|nieuw|€2,10|1|€2,10|[AliExpress](https://www.aliexpress.com/w/wholesale-TB6612FNG-module.html)|
|         4|N20 6V 10:1 met encoder|1500 rpm, Hall-encoder 7 PPR|nieuw|€7,52|2|€15,04|[AliExpress](https://www.aliexpress.com/w/wholesale-GA12-N20-6V-1500RPM-encoder.html)|
|         5|Pololu wiel 32×7 mm|siliconen band, paar|nieuw|€3,20|1|€3,20|[Opencircuit](https://opencircuit.shop/product/pololu-wheel-32-7mm-pair-white)|
|         6|Pololu motorbeugel|paar, met M2-bouten en moeren|nieuw|€2,15|1|€2,15|[Opencircuit](https://opencircuit.shop/product/pololu-micro-metal-gearmotor-bracket-pair)|
|         7|Pololu ball caster 3/8″|steunpunt vooraan|nieuw|€5,90|1|€5,90|[Opencircuit](https://opencircuit.shop/product/pololu-ball-caster-with-3-8-plastic-ball)|
|         8|LiPo DOGCOM 2S 450 mAh 100C|XT30, JST-XH balans|nieuw|€11,95|1|€11,95|[Droneshop](https://droneshop.nl/dogcom-450mah-100c-2s-74v-lipo-xt30)|
|         9|CN3903 buck 3,3 V|5–30 V in, 3 A|nieuw|€1,60|1|€1,60|[AliExpress](https://www.aliexpress.com/w/wholesale-CN3903-3.3V-buck-module.html)|
|        10|gaatjesprint 9×15 cm|dubbelzijdig, 33 × 54 gaten: chassis + bedrading|nieuw|€3,21|1|€3,21|[AliExpress](https://www.aliexpress.com/w/wholesale-double-sided-prototype-pcb-9x15.html)|
|        11|SS12D00 schuifschakelaar (SW1)|aan/uit|nieuw|€0,12|1|€0,12|[AliExpress](https://www.aliexpress.com/w/wholesale-SS12D00-slide-switch.html)|
|        12|XT30-pigtail male 20AWG|batterijaansluiting|nieuw|€2,48|1|€2,48|[Droneshop](https://droneshop.nl/flywoo-xt30up-m-pigtail-2pcs-20awg-pink)|
|        13|drukknop 6×6 mm (SW2)|start/stop, aan GPIO21|recup|€0,00|1|€0,00|Arduino-kit ([AliExpress](https://www.aliexpress.com/w/wholesale-tactile-switch-6x6.html))|
|        14|weerstand 10 kΩ (R1)|spanningsdeler batterijmeting|recup|€0,00|1|€0,00|Arduino-kit|
|        15|weerstand 5,1 kΩ (R2)|spanningsdeler batterijmeting|recup|€0,00|1|€0,00|Arduino-kit|
|        16|weerstand 330 Ω (R3)|voorschakelweerstand power-led|recup|€0,00|1|€0,00|Arduino-kit|
|        17|led 3 mm rood (D1)|power-led|recup|€0,00|1|€0,00|Arduino-kit|
|        18|elco 100 µF / 16 V (C1, C2)|buffer op VM en op 3V3|recup|€0,00|2|€0,00|Arduino-kit|
|        19|condensator 100 nF (C3, C4)|ontstoring over de motorklemmen|recup|€0,00|2|€0,00|Arduino-kit|
|        20|dupont-draad|bedrading, geknipt en gesoldeerd|recup|€0,00|1|€0,00|Arduino-kit|
|        21|boutjes, moeren, afstandhouders|8× M2×8, 2× M2×25, ±10 M2-moeren, messing M2-afstandhouders (sensor), 2× M3×30 + 6 M3-moeren|nieuw|€1,50|1|€1,50|doe-het-zelfzaak / [Amazon](https://www.amazon.com.be/s?k=M2+afstandhouders+messing+set)|
|        22|spoiler|plaatje 25 × 86 mm (restje print of kunststof)|recup|€0,00|1|€0,00|restmateriaal|
| | | | | | **totaal robot** | **€75,19** | |

Niet in de robot, wel nodig: B3-balanslader, lipo-bag, 2e lipo en reserveonderdelen (zie bestelling hieronder).
Plan A (eigen PCB, enkel ontworpen in KiCad) vervangt 1, 3, 9, 10 en de modules door losse componenten.
De datasheets van alle onderdelen staan in [datasheets](../datasheets/readme.md).

## Bestelling plan B (19/10/2026)

Gebouwd op een gaatjesprint die tegelijk het chassis is. Geen eigen PCB of 3D-print laten maken.

### AliExpress (€47,64, levering 26–30 okt)

| Onderdeel | Variant | Aantal | Prijs/st |
|---|---|---|---|
| ESP32-S3 dual Type-C devkit | besteld als N8R2 weld, geleverd als N16R8 (headers gesoldeerd) | 2 (1 reserve, niet geleverd) | €6,89 |
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
| Flywoo XT30UP-M pigtail 20AWG (2 st., €2,48 per stuk) | 1 | €4,95 |
| Droneshop LiPo Safe Bag medium | 1 | €5,95 |

Zelf al in huis (Arduino-kit): weerstanden (10 kΩ, 5,1 kΩ, 330 Ω), led, drukknoppen, elco's, breadboard, dupont-draadjes, 100 nF condensatoren.

Hoe alles gemonteerd en bedraad wordt: zie de [instructable](../instructable/readme.md).

## Plan A: eigen print (ontwerp)

Alle onderdelen met hun package, rechtstreeks uit het [KiCad-schema van plan A](../technische%20tekeningen/elektronisch/kicad_planA/readme.md) ([csv](../technische%20tekeningen/elektronisch/kicad_planA/bom_planA.csv)). Prijzen = richtprijs LCSC per stuk (november 2026), print = 1/5 van een bestelling van 5 stuks. Motoren, wielen, ball caster en batterij zijn dezelfde als bij plan B.

|volgnummer|naam|package|referenties|aantal|kostprijs/stuk|subtotaal|
|---|---|---|---|---|---|---|
|1|ESP32-S3-WROOM-1-N16R8|module (RF_Module:ESP32-S3-WROOM-1)|U1|1|€4,50|€4,50|
|2|TB6612FNG|SSOP-24 5,3 × 8,2 mm|U3|1|€1,20|€1,20|
|3|AP63203WU buck 3,3 V|TSOT-23-6|U2|1|€0,60|€0,60|
|4|spoel 6,8 µH (Bourns SRN4018)|4 × 4 mm|L1|1|€0,15|€0,15|
|5|QRE1113GR reflectiesensor|OnSemi CASE 100CY (SMD)|Q1–Q8|8|€0,45|€3,60|
|6|AO3400A N-MOSFET|SOT-23|Q9|1|€0,03|€0,03|
|7|B5819W schottky|SOD-123|D1|1|€0,03|€0,03|
|8|led groen|0805|D2|1|€0,02|€0,02|
|9|WS2812B|PLCC4 5 × 5 mm|D3|1|€0,10|€0,10|
|10|USB-C (GCT USB4105)|16P SMD|J4|1|€0,60|€0,60|
|11|XT30PW-M|THT haaks|J1|1|€0,80|€0,80|
|12|JST-ZH 6-pins|THT 1,5 mm|J2, J3|2|€0,10|€0,20|
|13|pinheader 1×4|2,54 mm|J5|1|€0,05|€0,05|
|14|schuifschakelaar PCM12|SMD|SW1|1|€0,30|€0,30|
|15|drukknop TL3342|SMD 5,2 × 5,2 mm|SW2–SW4|3|€0,15|€0,45|
|16|condensator 10 µF 25 V|1206|C1, C10|2|€0,05|€0,10|
|17|condensator 22 µF|1206|C3, C4|2|€0,05|€0,10|
|18|condensator 10 µF|0805|C6|1|€0,03|€0,03|
|19|condensator 1 µF|0805|C8|1|€0,01|€0,01|
|20|condensator 100 nF|0805|C2, C5, C7, C9, C11, C12|6|€0,01|€0,06|
|21|weerstand 10 kΩ|0805|R1, R4, R5|3|€0,01|€0,03|
|22|weerstand 5,1 kΩ|0805|R2, R20, R21|3|€0,01|€0,03|
|23|weerstand 1 kΩ / 100 Ω / 100 kΩ|0805|R3, R6, R7|3|€0,01|€0,03|
|24|weerstand 100 Ω|0603|R10–R17|8|€0,01|€0,08|
|25|weerstand 47 kΩ|0603|R22–R29|8|€0,01|€0,08|
|26|print 100 × 130 mm, 2 lagen|FR4 1,6 mm||1|€1,50|€1,50|
| | | | | | **elektronica plan A** | **±€14,7** |
| | | | | | + motoren, wielen, caster, batterij (plan B nr. 4–8) | €38,24 |
| | | | | | **totaal robot plan A** | **±€53** |
