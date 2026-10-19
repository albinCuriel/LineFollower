# Instructable

Een instructable is een stappenplan - zonder verdere uitleg - hoe je vertrekkend van de bill of materials en gebruik makend van de technische tekeningen de robot kan nabouwen. Ook de nodige stappen om de microcontroller te compileren en te uploaden staan beschreven.

Werk stap per stap en doe de **test** aan het einde van elke stap vóór je verder gaat.

| Document | Waarvoor |
|---|---|
| [Bill of materials](../bill%20of%20materials/readme.md) | wat je nodig hebt |
| [Elektrisch schema (PDF)](../technische%20tekeningen/elektronisch/elektrisch_schema.pdf) | welke pin waarmee verbonden is |
| [Boormal 1:1 (PDF)](../technische%20tekeningen/elektronisch/boormal_1op1.pdf) | plaats van elk onderdeel en boorgat, afdrukken op 100 % |
| [Bekabelingsplan 2:1 (PDF)](../technische%20tekeningen/elektronisch/bekabelingsplan.pdf) | elke draad aan de soldeerkant, met nummer |
| [Draadlijst](../technische%20tekeningen/elektronisch/draadlijst.md) | dezelfde draden als afvinklijst, per stap |
| [Samenstellingstekening (PDF)](../technische%20tekeningen/mechanisch/tekening_linefollower.pdf) | maten van de robot |

![plaatsing bovenzijde](../technische%20tekeningen/elektronisch/boormal_1op1.png)

---

### stap 1
bestel alle componenten uit de bill of materials

### stap 2: gereedschap en klaarleggen
- soldeerbout (fijne punt), soldeertin met flux
- multimeter, kniptang, striptang, pincet
- kleine zaag, vijl, boortjes 2,2 mm en 5 mm, priem
- lokaal kopen: 8× M2×8, 2× M2×25, ±10 M2-moeren, 2× M3×30 + 6 M3-moeren, klittenband
- draad: dupont-draadjes, stekkers eraf geknipt. Rood = VBAT, oranje = 3V3, zwart = GND
- druk de [boormal](../technische%20tekeningen/elektronisch/boormal_1op1.pdf) af op **100 %** en meet de controlemaat van 50 mm na

### stap 3: onderdelen nameten
Meet na met een schuifmaat. Wijkt een maat meer dan 1 mm af, pas dan `MATEN` aan in [model_linefollower.py](../technische%20tekeningen/mechanisch/model_linefollower.py) en teken opnieuw (zie [mechanisch](../technische%20tekeningen/mechanisch/readme.md)).

| Onderdeel | Te meten | In het model | Gemeten |
|---|---|---|---|
| ESP32-S3 devkit | lengte × breedte | 63,5 × 28,0 mm | |
| ESP32-S3 devkit | afstand tussen de 2 pinrijen | 25,4 mm = 10 gaatjes | |
| ESP32-S3 devkit | pin van de RGB-led (opdruk) | GPIO48 | |
| TB6612-module | lengte × breedte, pinvolgorde | 20,3 × 20,3 mm | |
| CN3903 buck | lengte × breedte, ligging IN/OUT | 22 × 17 mm | |
| N20 + encoder | lengte zonder as | 31 mm | |
| N20-encoder | volgorde van de 6 draden | M1, GND, A, B, VCC, M2 | |
| LiPo 2S 450 mAh | L × B × H, gewicht | 60 × 17 × 15 mm | |

### stap 4: print inkorten en boren
1. Zaag de gaatjesprint in op **120 × 90 mm** langs een gatenrij. Vijl de rand glad. **Bewaar het afgezaagde stuk (30 × 90 mm): dat wordt de spoiler.**
2. Plak de boormal erop en prik de gaten aan.
3. Boor 4× 2,2 mm (motorbeugels), 2× 2,2 mm (caster, dwars), 2× 2,2 mm (QTR, voorrand), 2× 3,2 mm (spoiler, achteraan) en 2× 5 mm (motorkabels).
4. Spoiler: zaag het reststuk op 25 × 86 mm en boor er 2 gaten van 3,2 mm in, 68 mm uit elkaar (zelfde plaats als in de print).

**Test:** beugels en caster passen zonder forceren op hun gaten.

### stap 5: voeding
Soldeer XT30-pigtail, SW1, buck, R3 + power-led D1, C1 en C2. Draden **nr. 1–13** uit de [draadlijst](../technische%20tekeningen/elektronisch/draadlijst.md).
- XT30: rood = +, zwart = −. Leid de draad eerst door 2 gaatjes (trekontlasting).
- SW1: middelste pin = BATT+.
- Buck: IN+ = VBAT, IN− = GND, OUT+ = 3V3, OUT− = GND (volg de opdruk).
- Elco: streepje = min.

**Test** (batterij aan, nog geen ESP32/TB6612):
- [ ] power-led brandt
- [ ] buck OUT+ ↔ GND = 3,25–3,35 V
- [ ] VBAT ↔ GND = 7,4–8,4 V
- [ ] SW1 uit = 0 V op VBAT

### stap 6: batterijmeting
R1 100 kΩ van VBAT naar het meetpunt, R2 33 kΩ van het meetpunt naar GND. Draden **nr. 14–16**.

**Test:** meetpunt ↔ GND = 2,08 V bij 8,4 V (VBAT × 33/133).

### stap 7: ESP32-S3 devkit
1. Doorgangstest: 3V3 en GND zijn **niet** kortgesloten.
2. Devkit met de USB-poorten naar voren. J1-pin 1 (3V3) rechts achteraan. Soldeer alle pinnen.
3. Enkel USB aangesloten (SW1 uit): laad [poc_interrupt](../code/proof%20of%20concepts/interrupt/readme.md).

**Test:** de RGB-led brandt rood. Met batterij en SW1 aan geeft `analogReadMilliVolts(9) * 133 / 33` dezelfde spanning als de multimeter op VBAT (± 0,1 V).

### stap 8: H-brug
TB6612 rechts naast de ESP32, stuurpinnen naar het midden. Volg de **opdruk** van je module. Draden **nr. 17–25**.

**Test:** één motor los aan AO1/AO2, laad [poc_hbridge](../code/proof%20of%20concepts/hbridge/readme.md): de motor versnelt, stopt en draait om.

### stap 9: motoren, beugels, wielen, encoders
1. Soldeer 100 nF rechtstreeks over de motorklemmen M1/M2.
2. Motor in de Pololu-beugel, beugel met 2× M2×8 aan de **onderkant** van de print. Tandwielkast naar buiten.
3. Kabel door het gat van 5 mm naar de soldeerkant, op lengte knippen.
4. Wielen op de D-as, 1 mm speling tot de print.
5. Draden **nr. 26–35**.

**Test:** wielen vrij, poc_hbridge: eerst links, dan rechts, beide vooruit en achteruit. Draait een wiel verkeerd om, wissel dan AO1/AO2 of BO1/BO2. Draai een wiel 1 toer met de hand: de encoder telt **280** (7 PPR × 4 × 10:1).

### stap 10: sensor
1. Soldeer de jumper **"3.3V BYPASS"** op de QTR-8A dicht.
2. Soldeer 11 draadjes: OUT1–8, LEDON, VCC, GND. Sensor 1 = robot **links**.
3. QTR onder de voorrand met 2× M2×25. Stel met de moeren **3 mm** tussen sensoren en grond af (boortje van 3 mm als voeler).
4. Draden **nr. 36–46**.

**Test:** [poc_sensor](../code/proof%20of%20concepts/sensor/readme.md): wit = lage waarde, zwarte tape = hoge waarde, elke sensor apart.

### stap 11: start/stop-knop
Knop aan de linkerrand. GPIO21 en GND. Draden **nr. 47–48**.

**Test:** poc_interrupt: elke druk wisselt de led rood/groen.

### stap 12: afwerking
1. Ball caster met beide meegeleverde afstandsringen + M2-moeren tot 12,4 mm tegen de onderkant van de print. De print moet waterpas staan.
2. Batterij met klittenband **dwars boven de wielas**.
3. Spoiler: 2× M3×30 van onderen door de print, moer erop, dan met 2 moeren de spoiler op **20 mm** boven de print klemmen.
4. Draden samenbinden, niets onder de QTR laten hangen.
5. Laad [poc_wifi](../code/proof%20of%20concepts/wireless%20communication/readme.md) en stuur een bericht via de gsm.

**Eindcontrole:**
- [ ] breedte ≤ 110 mm
- [ ] sensorhoogte 3 mm over de hele breedte
- [ ] SW1 uit = alles spanningsloos
- [ ] gewicht ±110–120 g
- [ ] de 4 PoC's werken op de afgewerkte robot

### stap 13: compileren en uploaden
1. Arduino IDE 2 of [arduino-cli](https://arduino.github.io/arduino-cli/) met de core **esp32 by Espressif** (3.x).
2. Bord **ESP32S3 Dev Module**, USB CDC On Boot = Enabled, PSRAM = QSPI.
3. USB-C-poort met opdruk **USB** (native). Lukt uploaden niet: BOOT ingedrukt houden, kort RST, BOOT los.
4. Command line:
   ```
   arduino-cli compile --fqbn esp32:esp32:esp32s3 "code/proof of concepts/sensor/poc_sensor"
   arduino-cli upload  --fqbn esp32:esp32:esp32s3 -p COM5 "code/proof of concepts/sensor/poc_sensor"
   ```
   De COM-poort vind je met `arduino-cli board list`.
