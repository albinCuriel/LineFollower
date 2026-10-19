# Instructable

Een instructable is een stappenplan - zonder verdere uitleg - hoe je vertrekkend van de bill of materials en gebruik makend van de technische tekeningen de robot kan nabouwen. Ook de nodige stappen om de microcontroller te compileren en te uploaden staan beschreven.

Werk stap per stap en doe de **test** aan het einde van elke stap vóór je verder gaat.

| Document | Waarvoor |
|---|---|
| [Bill of materials](../bill%20of%20materials/readme.md) | wat je nodig hebt |
| [Elektrisch schema (PDF)](../technische%20tekeningen/elektronisch/elektrisch_schema.pdf) | welke pin waarmee verbonden is |
| [Bekabelingsplan (PDF, 9 pagina's A3)](../technische%20tekeningen/elektronisch/bekabelingsplan.pdf) | plaatsing + 1 pagina per bouwstap met elke draad, gat per gat |
| [Boormal 1:1 (PDF)](../technische%20tekeningen/elektronisch/bekabelingsplan_boormal_1op1.pdf) | bovenzijde op ware grootte, afdrukken op 100 % |
| [Draadlijst](../technische%20tekeningen/elektronisch/bekabelingsplan_draadlijst.md) | alle 52 draden als afvinklijst, met gatcoördinaten en lengte |
| [Kabels (WireViz)](../technische%20tekeningen/elektronisch/kabels/readme.md) | batterij-, motor- en sensorkabel pin per pin |
| [Samenstellingstekening (PDF)](../technische%20tekeningen/mechanisch/tekening_linefollower.pdf) | maten van de robot |

**Zo lees je het bekabelingsplan:** elk gat heeft een naam zoals **F22** = rij F, kolom 22. De letters en cijfers staan op alle randen van de tekening. Kolom 1 = achterkant (batterij), kolom 47 = voorkant (sensor), rij A = robot links. Zet met een stift een streepje bij elke 5e rij en kolom op je print, dan vind je elk gat meteen terug.

![plaatsing](../technische%20tekeningen/elektronisch/bekabelingsplan_p00_plaatsing.png)

---

### stap 1
bestel alle componenten uit de bill of materials

### stap 2: gereedschap en klaarleggen
- soldeerbout (fijne punt), soldeertin met flux
- multimeter, kniptang, striptang, pincet, stift
- kleine zaag, vijl, boortjes 2,2 mm en 3,2 mm, priem
- lokaal kopen: 8× M2×8, 2× M2×25, ±10 M2-moeren, 2× M3×30 + 6 M3-moeren, klittenband
- draad: dupont-draadjes, stekkers eraf geknipt. Rood = VBAT, oranje = 3V3, zwart = GND (zie de legende)
- druk de [boormal](../technische%20tekeningen/elektronisch/bekabelingsplan_boormal_1op1.pdf) af op **100 %** en controleer: 10 gaten = 25,4 mm

### stap 3: onderdelen nameten
Meet na met een schuifmaat. Wijkt een maat meer dan 1 mm af, pas dan `MATEN` aan in [model_linefollower.py](../technische%20tekeningen/mechanisch/model_linefollower.py) en teken opnieuw (zie [mechanisch](../technische%20tekeningen/mechanisch/readme.md)). Wijkt een pinafstand af, pas dan [bekabeling_config.py](../technische%20tekeningen/elektronisch/bekabeling_config.py) aan.

| Onderdeel | Te meten | In het plan | Gemeten |
|---|---|---|---|
| ESP32-S3 devkit | lengte × breedte | 63,5 × 28,0 mm | |
| ESP32-S3 devkit | afstand tussen de 2 pinrijen | 25,4 mm = 10 gaten | |
| ESP32-S3 devkit | pin van de RGB-led (opdruk) | GPIO48 | |
| TB6612-module | pinvolgorde + afstand tussen de pinrijen | 7 gaten | |
| CN3903 buck | ligging IN/OUT-pads | IN links, OUT rechts, 8 gaten uit elkaar | |
| N20-encoder | volgorde van de 6 draden | M1, GND, A, B, VCC, M2 | |
| LiPo 2S 450 mAh | L × B × H, gewicht | 60 × 17 × 15 mm | |

### stap 4: print inkorten en boren
1. Zaag de gaatjesprint in op **47 × 35 gaten (120 × 90 mm)** langs een gatenrij. Vijl de rand glad. **Bewaar het afgezaagde stuk: dat wordt de spoiler.**
2. Zet de stiftstreepjes bij elke 5e rij en kolom.
3. Plak de boormal erop en prik de oranje kruisen aan.
4. Boor 4× 2,2 mm (motorbeugels), 2× 2,2 mm (caster, dwars), 2× 2,2 mm (QTR, voorrand) en 2× 3,2 mm (spoiler, achteraan).
5. Spoiler: zaag het reststuk op 25 × 86 mm en boor er 2 gaten van 3,2 mm in, 68 mm uit elkaar.

6. **Monteer de ball caster nu al**, vóór de ESP32 erop komt: hij zit onder de ESP32 (op 84 mm voor de wielas, vlak achter de sensor). Steek 2× M2-bout **met lage kop** (≤ 1,5 mm) van boven door de print. Onderaan: de 2 meegeleverde afstandsringen + M2-moeren tot 12,4 mm, dan de caster. De print moet waterpas staan.

**Test:** beugels en caster passen zonder forceren; de boutkoppen steken minder dan 2,5 mm uit (de ESP32 staat 2,5 mm hoog op zijn pinheader).

### stap 5: voeding
Plaats SW1, de XT30-pigtail, de buck, R3 en de power-led D1. Draden **1–6**.

![stap 5](../technische%20tekeningen/elektronisch/bekabelingsplan_p01_stap05.png)

- XT30: rood = +, zwart = −.
- SW1: middelste pin = BATT+.
- Buck: IN+ = VBAT, IN− = GND, OUT+ = 3V3, OUT− = GND (volg de opdruk).

**Test** (batterij aan):
- [ ] power-led brandt
- [ ] buck OUT+ ↔ GND = 3,25–3,35 V
- [ ] VBAT ↔ GND = 7,4–8,4 V
- [ ] SW1 uit = 0 V op VBAT

### stap 6: batterijmeting
R1 100 kΩ en R2 33 kΩ, met een soldeerbrug ertussen (= meetpunt). Draden **7–9**.

![stap 6](../technische%20tekeningen/elektronisch/bekabelingsplan_p02_stap06.png)

**Test:** meetpunt ↔ GND = 2,08 V bij 8,4 V (VBAT × 33/133).

### stap 7: ESP32-S3 devkit
1. Doorgangstest: 3V3 en GND zijn **niet** kortgesloten.
2. Devkit met de USB-poorten naar voren. Pin J1-1 (3V3) in gat **W23**. Soldeer alle pinnen. Plaats C2 (streepje = min).
3. Draden **10–14**.
4. Enkel USB aangesloten (SW1 uit): laad [poc_interrupt](../code/proof%20of%20concepts/interrupt/readme.md).

![stap 7](../technische%20tekeningen/elektronisch/bekabelingsplan_p03_stap07.png)

**Test:** de RGB-led brandt rood. Met batterij en SW1 aan geeft `analogReadMilliVolts(9) * 133 / 33` dezelfde spanning als de multimeter op VBAT (± 0,1 V).

### stap 8: H-brug
TB6612 met PWMA in gat **T10**, de stuurpinnen naar het midden. Volg de **opdruk** van je module. Plaats C1 vlak bij VM. Draden **15–27**.

![stap 8](../technische%20tekeningen/elektronisch/bekabelingsplan_p04_stap08.png)

**Test:** één motor los aan AO1/AO2, laad [poc_hbridge](../code/proof%20of%20concepts/hbridge/readme.md): de motor versnelt, stopt en draait om.

### stap 9: motoren, beugels, wielen, encoders
1. Soldeer 100 nF rechtstreeks over de motorklemmen M1/M2 op het motorprintje.
2. Motor in de Pololu-beugel, beugel met 2× M2×8 aan de **onderkant** van de print. Tandwielkast naar buiten.
3. Knip de motorkabel op lengte en steek elk draadje **van onderen** in zijn gat: motor L in **N2–N7**, motor R in **V2–V7** (zie [kabels](../technische%20tekeningen/elektronisch/kabels/readme.md)).
4. Wielen op de D-as, 1 mm speling tot de print.
5. Draden **28–39**.

![stap 9](../technische%20tekeningen/elektronisch/bekabelingsplan_p05_stap09.png)

**Test:** wielen vrij, poc_hbridge: eerst links, dan rechts, beide vooruit en achteruit. Draait een wiel verkeerd om, wissel dan de draden in N2/N7 (of V2/V7). Draai een wiel 1 toer met de hand: de encoder telt **280** (7 PPR × 4 × 10:1).

### stap 10: sensor
1. Soldeer de jumper **"3.3V BYPASS"** op de QTR-8A dicht.
2. Soldeer 11 draadjes aan de QTR (OUT1–8, LEDON, VCC, GND). Sensor 1 = robot **links**.
3. QTR onder de voorrand met 2× M2×25. Stel met de moeren **3 mm** tussen sensoren en grond af (boortje van 3 mm als voeler).
4. Steek de 11 draadjes van onderen in **Y46–AI46** (zie [kabels](../technische%20tekeningen/elektronisch/kabels/readme.md)).
5. Draden **40–50**.

![stap 10](../technische%20tekeningen/elektronisch/bekabelingsplan_p06_stap10.png)

**Test:** [poc_sensor](../code/proof%20of%20concepts/sensor/readme.md): wit = lage waarde, zwarte tape = hoge waarde, elke sensor apart.

### stap 11: start/stop-knop
Knop aan de linkerrand, pootjes in **B32** en **D34** (schuin tegenover elkaar = altijd geschakeld). Draden **51–52**.

![stap 11](../technische%20tekeningen/elektronisch/bekabelingsplan_p07_stap11.png)

**Test:** poc_interrupt: elke druk wisselt de led rood/groen.

### stap 12: afwerking
1. Controleer dat de print waterpas staat op de wielen en de caster (stap 4). Sensorhoogte 3 mm.
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
   arduino-cli compile --fqbn esp32:esp32:esp32s3 --library code/lib/lf_core --library code/lib/lf_esp32 code/finaal/linefollower
   arduino-cli upload  --fqbn esp32:esp32:esp32s3 -p COM5 code/finaal/linefollower
   ```
   De COM-poort vind je met `arduino-cli board list`.
