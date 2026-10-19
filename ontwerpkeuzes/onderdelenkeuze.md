# Onderdelenkeuze en elektrisch ontwerp

Doel: het schoolrecord (0,97 m/s, 2021) verbreken, binnen ±€50, met onderdelen die in plan B (breadboard) en plan A (eigen PCB) **elektrisch identiek** zijn, zodat de code ongewijzigd meegaat.

## 1. Wat leren de resultaten van 2025-26?

Analyse van de specs in 47 repositories van vorig jaar.

| Snelheid | Microcontroller | Motoren | H-brug | Sensor | Batterij | Gewicht |
|---|---|---|---|---|---|---|
| 0,80 m/s | Nano | N20 500 rpm | DRV8833 | QTR-8A | 2× 18650 | 265 g |
| 0,77 m/s | ESP32 | N20 50:1 | DRV8833 | QTR-8A | 18650 | ? |
| 0,74 m/s | Leonardo | N20 30:1 500 rpm | TB6612FNG | HY-S301 | 2× 18650 (13A) | 244 g |
| 0,70–0,72 m/s (5 teams) | Nano / 32U4 | N20 30:1 500 rpm | DRV8833 | HY-S301 | 2× 18650 | 214 g |
| 0,66–0,67 m/s | ESP32 | N20 1000 rpm | DRV8833 / TB6612 | QTR-8A | 2S lipo / RCR123 | ? |
| 0,60 m/s | ESP32 | Pololu 600 rpm | DRV8833 | QTR-8RC | 2× 18650 | **134 g** |
| 0,14–0,35 m/s | diverse | 150–300 rpm | | | **AA, 9V, NiMH** | 300 g+ |

Besluiten:
1. **AA, 9V-blok en NiMH halen nooit meer dan 0,35 m/s.** Alle snelle robots gebruiken 2S lithium.
2. **Motoren van 150–300 rpm zijn te traag.** De top gebruikt ±500 rpm, maar zit daarmee ook vast rond 0,7–0,8 m/s: 500 rpm × π × 34 mm ≈ 0,9 m/s onbelast bij 6V. **Voor meer dan 1 m/s is ±1000 rpm nodig.**
3. De snelle robots wegen 200–265 g. Een lichtere robot trekt sneller op en remt sneller af, en daar gaat volgens de cursus het meeste vermogen naartoe.
4. **Niemand gebruikte encoders of een snelheidsprofiel** (hard op rechte stukken, afremmen voor bochten). Daar ligt de winst.

### Waarom ±1 m/s een muur is
In een bocht met straal r is de maximale snelheid voordat de banden slippen v = √(μ·g·r).
Met rubberen banden (μ ≈ 0,9) en de kleinste bocht (r = 0,10 m) geeft dat **v ≈ 0,94 m/s**. Een robot met constante snelheid kan dus nooit veel sneller dan het record. Wie het record wil verbreken, moet:
- **op rechte stukken sneller** rijden dan 1 m/s en **vóór bochten afremmen** (snelheidsprofiel), en
- **meer grip** hebben: zachte siliconen banden, een laag zwaartepunt en een lichte robot.

### Andere jaren (buiten de gegeven lijst)
| Snelheid | Jaar | Kern van het ontwerp |
|---|---|---|
| **0,906 m/s** | 2022 | Nano, **motoren 10:1** (9V), **TB6612**, QTR-8A, **3S lipo**, 220 g, sensor 110 mm voor de as, **boost/brake-code** (versnellen op rechte stukken, kort remmen voor bocht), ball caster in plaats van bout, batterij net vóór de motoras |
| 0,774 m/s | 2022 | Nano, motoren 30:1 1000 rpm (9V), DRV8833, 2× 18650, 210 g, sensor 125 mm voor de as |
| 0,72 m/s | 2024 | Nano, 50:1, DRV8833, QTR-8A, 2× 18650, 315 g |

De snelste HOGENT-robot die we terugvonden (0,906 m/s) gebruikte al **snelle motoren (10:1) en een snelheidsprofiel**.

### Wedstrijdrobots buiten HOGENT
| Robot | Kern |
|---|---|
| GRUZIK 2.0/3.0 (PL) | **69 g**, Pololu HPCB **10:1**, per motor 2 kanalen TB6612 **parallel**, 150 mAh 2S-lipo (10 g), Mini-Z-banden, magnetische encoders + gyro, **parcours in kaart brengen en daarna geoptimaliseerd rijden** |
| HyperLine V3 (RO, wereldfinale InfoMatrix) | **±100 g**, geen zuigventilator, siliconen wielen, PCB = chassis, 16 sensoren. Even snel als robots van 300 g met zuigventilator |
| Kwark (PL) | STM32, 12 sensoren, Pololu 10:1 HPCB, 2× TB6612 parallel, magnetische encoders |
| Semreh (BR), Suckbot (Pololu) | Zuigventilator (downforce) + brushless motoren. Topklasse, niet goedkoop |

Het patroon bij alle snelle robots: **licht (70–120 g), motoren 10:1, parallelle H-brugkanalen, encoders, grippy siliconen banden, snelheidsprofiel of parcours in kaart brengen.**

### Parcours doorgerekend (parcours3.svg uit de template)
- Lijnlengte **±7,8 m**: **5,6 m recht (71%)** en 2,2 m bocht.
- **Alle bochten hebben een straal van ±10 cm** (28 stukken van 45°).

Theoretische rondetijd (perfect volgen, geen fouten):

| Strategie | Bochtsnelheid | Gem. snelheid |
|---|---|---|
| Constante snelheid, rubber (μ≈0,8) | 0,90 m/s | 0,90 m/s |
| Constante snelheid, siliconen (μ≈1,2) | 1,10 m/s | 1,10 m/s |
| Boost/brake, rubber, 5 m/s², max 1,8 m/s | 0,90 m/s | 1,18 m/s |
| **Boost/brake, siliconen, 8 m/s², max 2,5 m/s** | 1,10 m/s | **1,47 m/s** |
| Boost/brake, siliconen, 10 m/s², max 3 m/s | 1,15 m/s | 1,57 m/s |
| Zuigventilator (μ_eff≈3) | 1,74 m/s | 2,19 m/s |

**1,5 m/s kan theoretisch zonder zuigventilator.** Daarvoor zijn nodig: siliconen banden, een lichte robot (±100–120 g) die 8–10 m/s² kan optrekken en remmen, een topsnelheid van 2,5–3 m/s op rechte stukken, en een regeling die weet waar de bochten komen (encoders en eventueel gyro). In de praktijk haal je 70–85% van het theoretische maximum, dus **realistisch 1,1–1,3 m/s** en met veel tuning 1,5 m/s. Met zuigventilator is 1,5 m/s veel zekerder. Vraag eerst aan de docent of die toegelaten is.

## 2. Gekozen onderdelen

| Blok | Keuze | Waarom (en waarom niet het alternatief) |
|---|---|---|
| **Microcontroller** | **ESP32-S3** (module **ESP32-S3-WROOM-1**). Plan B: **ESP32-S3-DevKitC-1-N8R8** (de N8-devkit is stopgezet). Pinverdeling vermijdt GPIO35–37, zodat ze op N8 én N8R8 werkt. Backup: ATmega32U4 (Arduino Micro) | Gekozen omdat **debuggen en tunen** de prioriteit zijn (zie §2b): live telemetrie via wifi naar een webdashboard, volledige rondes loggen in 512 kB RAM, draadloos nieuwe code uploaden (OTA), en een ingebouwde JTAG-debugger via USB. 10 ADC1-kanalen: 8 sensoren + batterij passen, ook met wifi aan. Hardware-teller (PCNT) leest beide encoders volledig (A én B) zonder processortijd. De module is met de hand te solderen. |
| **Motoren** | **N20 6V 10:1 (±1500 rpm) met magnetische encoder** ×2 (AliExpress). Meteen starten: **Aslong JGA12-N20-10** (10:1, 1500 rpm, zonder encoder, TinyTronics). Terugval: N20 6V ±1000 rpm met encoder | Voor 2,5–3 m/s op rechte stukken met wielen van 32 mm is ±1500–1800 rpm aan de wielen nodig. 10:1 zoals de recordrobots: 1500 rpm bij 6V, ±1850 rpm bij 7,4V → ±3,1 m/s onbelast. Aslong 10:1: blokkeerkoppel 0,013 N·m, blokkeerstroom 0,55 A bij 6V → met 2 motoren op een robot van 120 g ±8 m/s² gemiddelde versnelling, precies wat de simulatie vraagt. Traag tunen gebeurt met de encoders (PI-snelheidsregeling per wiel). Beide varianten passen in dezelfde beugel. *Pololu HPCB 10:1 is de beste keuze, maar kost ±€20 per stuk en breekt het budget.* |
| **H-brug** | **TB6612FNG**. Plan A: **2 chips, per motor beide kanalen parallel** | 1,2 A continu en 3,2 A piek per kanaal, parallel dus 2,4 A continu. Snelle motoren trekken bij het optrekken en remmen op 8,4V meer dan 2 A, en daar zit de DRV8833 op zijn grens. Zo doen GRUZIK en Kwark het ook. De behuizing (SSOP-24) is met de hand te solderen. De DRV8833 heeft een thermische pad onder de chip. Parallel schakelen kost geen extra pinnen. |
| **Banden** | **Siliconen banden** (Mini-Z-stijl of gegoten) op 32 mm velgen | Meer grip = hogere bochtsnelheid en harder remmen. Dat is de grootste winst per euro (zie berekening). |
| **Gyro (optioneel, plan A)** | IMU (bv. MPU-6050 of LSM6DS3), I²C | Samen met de encoders kan de robot zo het parcours in kaart brengen: waar zijn de rechte stukken, waar de bochten. Daarna rijdt hij geoptimaliseerd. Kost ±€2. |
| **Sensor-leds (debug)** | **8 adresseerbare RGB-leds** (WS2812/SK6812), 1 pin | Toont per sensor live of hij de lijn ziet, en de status van de robot (kalibratie, run, fout, batterij laag). Je ziet een sensor- of kalibratiefout meteen, zonder laptop. |
| **Sensoren** | Plan B: **Pololu QTR-8A** (met LEDON-pin, werkt op 3,3V). Plan A: **8× SMD-reflectiesensor** (QRE1113-type) op de eigen print, zelfde afstand 9,5 mm | Via de LEDON-pin kan je elke meting doen met de IR-leds aan én uit en die twee aftrekken. Zo filter je zonlicht, tl-licht en de IR van een fototoestel weg, wat de specs expliciet vragen. De plan A-sensor gebruikt hetzelfde type fototransistor, dus kalibratie en code blijven dezelfde. |
| **Batterij** | **2S lipo 450–550 mAh, ≥30C** | ±30 g in plaats van ±100 g voor 2× 18650 met houder. Dat is ±70 g minder op een robot van ±150 g, en het lage inwendige weerstand geeft sterke acceleratiestromen. Autonomie: gemiddeld ±0,5 A → ±50 minuten rijden. **Nodig:** een balanslader en een lipo-bag. |
| **Voeding logica** | Plan B: buck-module **3,3V** (ingang tot ≥20V). Plan A: **AP63203** (3,3V vast, 2 A, 3,8–32V) + 100 µF bij de module | Wifi trekt pieken tot ±500 mA. Een LDO van 8,4V naar 3,3V zou dan ±2,5 W verstoken, en een te zwakke voeding geeft resets (brown-out). Een buck van 2 A met een buffercondensator vangt dat op. |
| **Draadloos** | **Wifi van de ESP32-S3** (robot = eigen access point) + webdashboard | De robot maakt zijn eigen wifinetwerk, dus je hebt het schoolnetwerk niet nodig. Pc en smartphone (ook iPhone) openen gewoon een webpagina, zonder app of installatie. Via WebSocket: schuifregelaars voor alle instellingen, live-grafieken, kalibratieknop, logbestanden downloaden, en draadloos code uploaden (OTA). Reserve: een USB-kabel geeft dezelfde commando's via de seriële monitor. |
| **Bediening** | Schuifschakelaar (power), drukknop (start/stop via interrupt), groene led (power) en een tweede led (run/communicatie) | Volgens de specs. Geen lcd. |
| **Steunpunt voor** | Twee gladde glijders onder de sensorprint (bv. nylon schroefkopjes) of een kleine metalen ball caster | Dat houdt de sensoren op een vaste hoogte van ±3 mm, de optimale afstand voor dit type sensor. |

## 2b. Waarom afwijken van de ATmega32U4? (de vier vragen uit de cursus)

**1. Waarom? Wat is de meerwaarde?**
Niet de snelheid van de processor. Die beperkt de robot niet (zie §1). De meerwaarde is **sneller en beter debuggen en tunen**, en dat is precies wat de eindsnelheid bepaalt:

| Debug-/tuningfunctie | ATmega32U4 + HC-05 | ESP32-S3 + wifi |
|---|---|---|
| Live telemetrie tijdens het rijden | ±11 kB/s (115200 baud) → ±100 metingen/s van een paar waarden | wifi → **alle** waarden (8 sensoren, positie, fout, P/I/D-termen, PWM, wielsnelheden, batterij) aan **500–1000 metingen/s** |
| Een ronde loggen en achteraf analyseren | 2,5 kB RAM → een paar honderd metingen | 512 kB RAM → **volledige ronde aan 1 kHz** (±80 kB), daarna downloaden als CSV |
| Instellingen aanpassen | tekstcommando's via een terminal-app | **webdashboard** met schuifregelaars, direct toegepast, knop "bewaar in EEPROM" |
| Nieuwe code uploaden | USB-kabel, robot oppakken | **draadloos (OTA)** terwijl hij op de baan staat |
| Echte debugger (breakpoints, variabelen bekijken) | enkel met extra programmer (en nauwelijks bruikbaar) | **ingebouwde JTAG via dezelfde USB-kabel** |
| Extra module | HC-05 (±€4, ±5 g, 4 draden) | niets, alles zit in de chip |
| Werkt op | pc + Android (Bluetooth SPP) | pc + Android + iPhone (browser) |

**2. Heb je al met het platform gewerkt?**
Nee. De ESP32-S3 werkt wel in de gewone Arduino-omgeving (`arduino-cli`, core `esp32:esp32`), met dezelfde functies (`analogRead`, `attachInterrupt`, `EEPROM`). Het grootste verschil (3,3V-logica, wifi) zit in één code-module.

**3. Hoeveel tijd maximaal voor de proof-of-concepts?**
**1 week** (2 labosessies) voor de vier PoC's: sensor, H-brug, interrupt en draadloze communicatie. Werkt dat niet binnen die tijd, dan schakelen we over naar het backupplan.

**4. Backupplan?**
**ATmega32U4 (Arduino Micro) + HC-05.** Alle andere onderdelen (QTR-8A op 3,3V of 5V, TB6612FNG, N20-motoren met encoder, lipo, sensor-leds) werken op beide. De firmware is opgebouwd met **één hardwarelaag** (`board.h`: pinnen, ADC, PWM, encoders, communicatie). De rest (kalibratie, PID, snelheidsprofiel) is identiek en compileert voor beide borden. Overschakelen kost dus een ander bord (±€12) en één bestand, geen herontwerp.

## 2c. Ontworpen om te debuggen

Hardware:
- **8 RGB-leds** tonen per sensor of hij de lijn ziet en de status van de robot. Een foute kalibratie of een dode sensor zie je meteen.
- **Batterijspanning** wordt gemeten en in het dashboard getoond, met onderspanningsbeveiliging.
- **Encoders met A en B** (volledige kwadratuur via PCNT): echte wielsnelheid en afgelegde afstand.
- Plan A: **testpunten** op de PCB (VBAT, 3V3, GND, motoruitgangen, sensorlijnen), **RESET- en BOOT-knop**, **USB-C** voor uploaden en JTAG, en een **jumper om de motorvoeding los te koppelen** (alles testen zonder dat de robot wegrijdt).
- **Sensorprint op een connector:** vervangbaar zonder te solderen.
- **Testbok** (3D-print): robot met de wielen in de lucht, zodat je motoren en encoders test zonder te rijden.

Software:
- Webdashboard op de robot: live-grafieken, schuifregelaars, kalibratie, start/stop, log opnemen en downloaden, OTA-update.
- Dezelfde commando's via USB-serieel (`debug on/off`, `set kp …`, `calibrate …`), zoals de gebruiksaanwijzing van de template vraagt.
- Pc-script (Python) dat een gelogde ronde analyseert: fout langs het parcours, oversturen, waar de robot remt.
- **Simulatie** van de robot op het parcours, om PID-waarden en het snelheidsprofiel voor te tunen vóór de hardware er is.

## 3. Elektrisch blokschema

```
2S lipo 7,4V (6,4–8,4V)
  │
  ├─ schakelaar ─┬──[jumper motorvoeding]──► 2× TB6612FNG VM ──► motor L / motor R
  │              │                   (100 µF + 100 nF bij VM, 100 nF over elke motor)
  │              ├─ buck 3,3V (2 A) ─┬──► ESP32-S3 (3V3, + 100 µF buffer)
  │              │                   ├──► TB6612FNG VCC (logica)
  │              │                   ├──► sensor array + IR-leds (via LEDON)
  │              │                   ├──► encoders (Hall)
  │              │                   ├──► 8× RGB-led (sensorweergave)
  │              │                   └──► power-led
  │              └─ deler 100k/33k ──► ADC (batterijspanning, 8,4V → 2,08V)
```

Rood (onbeveiligde batterijspanning) gaat enkel naar de H-brug, de buck en de spanningsdeler, net zoals in het blokschema van de cursus.

### Pinverdeling ESP32-S3 (identiek voor plan B en plan A)

| Functie | GPIO | Opmerking |
|---|---|---|
| Sensor 1–8 | 1–8 | ADC1_CH0–7 (werkt met wifi aan) |
| Batterijspanning | 9 | ADC1_CH8, deler 100k/33k |
| Sensor-leds aan/uit (LEDON) | 11 | omgevingslicht wegfilteren |
| Motor L: PWM / IN1 / IN2 | 12 / 13 / 14 | beide TB6612-kanalen parallel, PWM 20 kHz (LEDC) |
| Motor R: PWM / IN1 / IN2 | 15 / 16 / 17 | idem |
| TB6612 STBY | 18 | laag = motoren vrij (veilig bij opstarten) |
| USB D− / D+ | 19 / 20 | uploaden, seriële monitor, JTAG |
| Start/stop-drukknop | 21 | interne pull-up, interrupt |
| Gyro I²C SDA / SCL | 10 / 44 | GPIO35–37 zijn bezet door PSRAM op de N8R8 |
| Encoder L A / B | 39 / 40 | PCNT, volledige kwadratuur |
| Encoder R A / B | 41 / 42 | PCNT, volledige kwadratuur |
| Status-led | 48 | ingebouwde RGB-led van de devkit (de WS2812-strip is niet besteld) |

Niet gebruiken: 0, 3, 45, 46 (strapping; GPIO3 enkel als analoge ingang), 26–32 (flash), 33–37 (PSRAM op R8), 38 (RGB-led op sommige DevKitC-1-versies), 43 (opstartlog).

### Stroombudget 3,3V

| Verbruiker | Stroom |
|---|---|
| ESP32-S3 met wifi (pieken) | 100–500 mA |
| Sensor-leds QTR-8A | ±100 mA |
| 8× RGB-led (gedimd) | ±20–50 mA |
| Encoders + leds | ±20 mA |
| **Totaal** | **±0,7 A piek** → buck van 2 A heeft ruime marge |

### Batterijspanning in software
- **Onderspanningsbeveiliging:** stoppen onder 6,6V (3,3V per cel), anders beschadig je de lipo.
- **Spanningscompensatie:** PWM × (7,4V / Vbat). Daardoor rijdt de robot even snel met een volle als met een halflege batterij, en blijven je PID-instellingen geldig.

## 4. Mechanisch ontwerp (eerste richtlijnen)

- **Breedte maximaal 11 cm** (chronobrug 12 cm binnenmaat, met marge). Spoorbreedte ±9 cm.
- **Sensor ±9–10 cm vóór de wielas.** De snelste robots van vorig jaar zaten op 9,9–12 cm. Verder vooruit kijken maakt de regeling stabieler bij hoge snelheid.
- **Zwaartepunt laag en dicht bij de wielas.** Lipo boven of net vóór de motoren. Zo is er meer druk op de aangedreven wielen (meer grip) en rust er minder gewicht op de glijders.
- **Plan A:** de PCB is zelf het chassis. De motoren zitten met beugels op de print, de sensoren staan vooraan op dezelfde print (of op een tweede printje met een vaste connector).
- **Wielen:** 32–34 mm met zachte siliconen banden, voor grip in de 10 cm-bochten.
- **Doelgewicht: ±100–120 g** (vorig jaar 200–265 g voor de snelle robots; wedstrijdrobots 70–100 g). Kleine lipo (300–450 mAh, ±20–25 g).
- Spoiler: niet vergeten (specs). Uitgewerkt: het afgezaagde stuk gaatjesprint op 2× M3×30 achteraan (zie [mechanisch](../technische%20tekeningen/mechanisch/readme.md)).

## 5. Richtbudget plan A

| Onderdeel | ≈ € |
|---|---|
| ESP32-S3-WROOM-1 N8 + USB-C | 5 |
| 8× RGB-led (sensorweergave) | 2 |
| TB6612FNG | 2 |
| Buck AP63203 + spoel + condensatoren | 2 |
| 8× reflectiesensor | 6 |
| 2× N20 6V ±2000 rpm met encoder | 12 |
| 2× TB6612FNG (parallel) i.p.v. 1 | +2 |
| siliconen banden | 3 |
| 2× wiel | 2 |
| 2S lipo 450–550 mAh | 8 |
| PCB (5 stuks) | 5 |
| USB-C, knoppen, schakelaar, leds, connectoren, weerstanden, condensatoren | 4 |
| Glijders / ball caster | 1 |
| **Totaal** | **±€54** (zonder lader) |
