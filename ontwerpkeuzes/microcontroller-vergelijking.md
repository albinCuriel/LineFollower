# Keuze microcontroller: volledige vergelijking

Beoordeeld voor déze linefollower: ≥8 analoge sensoren + batterijmeting, 2 motoren (PWM + richting), 2 encoders, start/stop-knop met interrupt, draadloze communicatie, EEPROM-instellingen, een vaste cyclustijd van ±1 ms, en later een **eigen PCB die met de hand gesoldeerd moet kunnen worden**. Prijzen zijn richtprijzen.

## Snel overzicht

| µC | Kern / klok | FPU | Analoge ingangen | Draadloos | Echte EEPROM | Bord (plan B) | Chip (plan A) | Handsolderen chip |
|---|---|---|---|---|---|---|---|---|
| ATmega328P (Nano) | AVR 8-bit, 16 MHz | nee | 8 (10-bit) | nee | 1 kB | ±€4 | ±€2 | ja (TQFP-32) |
| **ATmega32U4 (Micro / Pro Micro)** | AVR 8-bit, 16 MHz | nee | 12 (10-bit) | nee | 1 kB | ±€6–8 | ±€4 | ja (TQFP-44) |
| ATmega4809 (Nano Every) | AVR-0 8-bit, 20 MHz | nee | 16 (10-bit), 8 op het bord | nee | 256 B | ±€12 | ±€2 | ja (TQFP-48) |
| ESP8266 | 32-bit, 80/160 MHz | nee | **1** (0–1V) | wifi | nee (flash) | ±€3 | ±€2 (module) | ja (module) |
| ESP32 (WROOM-32) | 2× 32-bit, 240 MHz | ja | 6 bruikbaar (ADC1) | wifi + BT classic + BLE | nee (flash) | ±€5 | ±€3 (module) | ja (module) |
| ESP32-S3 | 2× 32-bit, 240 MHz | ja | 10 (ADC1) | wifi + BLE | nee (flash) | ±€8 | ±€4 (module) | ja (module) |
| STM32F103 (blue pill) | Cortex-M3, 72 MHz | nee | 10 (12-bit) | nee | nee (flash) | ±€4 + ST-Link €3 | ±€3 | ja (LQFP-48) |
| STM32F411 (black pill) | Cortex-M4F, 100 MHz | ja | 16 (12-bit) | nee | nee (flash) | ±€7 | ±€5 | moeilijk (QFN-48) |
| STM32G431 | Cortex-M4F, 170 MHz | ja | 2 ADC's, ±17 kanalen (12-bit, 4 MS/s) | nee | nee (flash) | ±€7 | ±€4 | ja (LQFP-48) |
| RP2040 (Pico) | 2× Cortex-M0+, 133 MHz | nee | **3–4** (12-bit) | nee (Pico W: wifi/BLE) | nee (flash) | ±€4 | ±€1 + flash + kristal | moeilijk (QFN-56) |
| RP2350 (Pico 2) | 2× Cortex-M33, 150 MHz | ja | **3–4** (8 op RP2350B) | nee (Pico 2 W: wifi/BLE) | nee (flash) | ±€5 | ±€1,5 + flash | moeilijk (QFN) |

---

## 1. ATmega328P — Arduino Nano

**Voordelen**
- Het bekendste Arduino-platform. Je gebruikte het al in vorige vakken, en er zijn talloze voorbeelden.
- Goedkoop: ±€4 voor een Nano-kloon.
- 8 analoge ingangen (A0–A7) plus echte EEPROM (1 kB) voor de instellingen.
- 5V-logica: past direct bij de QTR-8A, de TB6612 en de HC-05.
- De chip (TQFP-32) is makkelijk met de hand te solderen.
- De snelste HOGENT-robot (0,906 m/s) en de meeste snelle robots van vorig jaar draaiden hierop. Bewezen.

**Nadelen**
- **Maar één UART, en die deelt hij met USB.** De HC-05 moet eraf om te uploaden, en je kan niet tegelijk via USB debuggen en via Bluetooth praten.
- 8 analoge pinnen = 8 sensoren, dus **geen pin meer vrij voor de batterijmeting**. A6 en A7 zijn bovendien alleen analoog.
- Maar 2 externe interrupts (D2, D3) voor de knop en 2 encoders.
- 2 kB RAM, geen FPU (een float-berekening duurt tientallen µs), 16 MHz.
- In plan A heb je een aparte USB-seriële chip nodig (CH340), of je programmeert via ISP.

## 2. ATmega32U4 — Arduino Micro / Pro Micro / Leonardo  (backupplan)

**Voordelen**
- Dezelfde AVR-familie en Arduino-omgeving als de Nano, dus KISS zoals de cursus aanraadt. Het is ook de chip uit het voorbeeldschema van de docent.
- **USB zit in de chip zelf:** `Serial` (USB) en `Serial1` (HC-05) zijn gescheiden. Je kan debuggen via USB en tegelijk draadloos werken, en uploaden lukt met de HC-05 aangesloten.
- **12 analoge ingangen:** 8 sensoren + batterijmeting + reserve.
- 5 externe interrupts + pin-change interrupts: genoeg voor knop en encoders.
- **Timer4 is een snelle PWM-timer** (tot 64 MHz klok): stille motorsturing op ±20 kHz.
- Echte EEPROM (1 kB).
- In plan A heb je geen extra USB-chip nodig: chip + kristal + een paar condensatoren + USB-connector. TQFP-44 is met de hand te solderen.
- Nieuwe chips komen met een USB-bootloader (DFU) uit de fabriek.

**Nadelen**
- Traag: 16 MHz, 8-bit, geen FPU.
- 2,5 kB RAM: krap als je later een grote parcourskaart wil opslaan (±200 segmenten past nog).
- Standaard AD-conversie ±110 µs. **Oplossing:** de ADC-prescaler op 16 zetten geeft ±13 µs per conversie, met iets minder nauwkeurigheid die voor sensoren geen rol speelt.
- **Pro Micro:** maar 9 analoge pinnen op de header, te weinig. **Micro:** alles bereikbaar, maar duurder (kloon ±€8). **Leonardo:** alles bereikbaar, maar groot.
- Geen ingebouwd draadloos: HC-05 nodig (±€4, ±5 g).

## 3. ATmega4809 — Arduino Nano Every

**Voordelen**
- 20 MHz en 6 kB RAM: iets sneller en veel meer werkgeheugen dan de 328P.
- 16 analoge kanalen in de chip (8 op het Nano Every-bord).
- USB via een aparte chip op het bord, dus `Serial1` (D0/D1) is vrij voor Bluetooth.
- Plan A: programmeren via UPDI met één draad, met een goedkope adapter.
- 5V-logica, Arduino-omgeving.

**Nadelen**
- **Nieuwe AVR-0-architectuur:** registers en timers zijn anders dan bij de klassieke AVR. De meeste tips en voorbeelden (Timer1-PWM, ADC-prescaler) werken niet zomaar.
- Het bord geeft maar 8 analoge pinnen, dus op plan B hetzelfde probleem als bij de Nano.
- EEPROM maar 256 B (genoeg voor instellingen, niet voor een kaart).
- Officieel bord ±€12, weinig kloons.
- Vorig jaar gebruikt door één team (0,25 m/s): weinig voorbeelden in dit project.

## 4. ESP8266

**Voordelen**
- Heel goedkoop, 80/160 MHz, 32-bit.
- Wifi ingebouwd, zelfs een webserver erop voor instellingen.
- Arduino-compatibel.

**Nadelen**
- **Maar 1 analoge ingang (0–1V).** Je hebt een externe multiplexer of ADC nodig. Dat is extra hardware, extra tijd per meting (omschakelen en insettelen), en extra fouten.
- Weinig bruikbare GPIO's (±9), waarvan meerdere bootstrap-pinnen die bij opstarten een bepaald niveau moeten hebben.
- Geen Bluetooth, wifi trekt stroompieken.
- 3,3V-logica, geen echte EEPROM.
- Voor dit project duidelijk de slechtste keuze.

## 5. ESP32 (klassiek, WROOM-32)

**Voordelen**
- 240 MHz, twee kernen, FPU, 520 kB RAM: rekenkracht in overvloed.
- **Wifi én Bluetooth Classic ingebouwd:** geen HC-05 nodig. Je pc ziet hem als seriële poort (SPP), een smartphone-app werkt, en een webinterface kan ook.
- Hardware-pulsteller (PCNT) voor encoders en een speciale motor-PWM-module (MCPWM).
- Goedkoop: devkit ±€5, module ±€3. Module = makkelijk solderen op een PCB.
- Vorig jaar door meerdere teams gebruikt (tot 0,77 m/s).

**Nadelen**
- **ADC:** op de WROOM-module zijn maar **6 pinnen van ADC1** bereikbaar. **ADC2 werkt niet als wifi aan staat.** 8 sensoren + batterij lukt dus niet zonder toegevingen.
- ADC is niet lineair en ruisgevoelig, vooral aan de randen van het bereik.
- Geen echte EEPROM (wordt nagebootst in flash).
- 3,3V-logica: andere aansluitingen en spanningen dan in de cursus.
- Draadloos trekt stroompieken van 300–500 mA: kans op brown-out resets als de voeding niet goed is ontworpen.
- Bootstrap-pinnen en uploaden (auto-reset) zijn minder plug-and-play. Op de PCB heb je een USB-seriële chip en een auto-reset-schakeling nodig.
- Cursus: afwijken van de Arduino vraagt verantwoording en een backupplan.

## 6. ESP32-S3  ✅ gekozen

**Voordelen**
- Alles van de ESP32, plus **10 bruikbare ADC1-kanalen** (8 sensoren + batterij passen).
- USB zit in de chip: op de PCB geen aparte USB-seriële chip nodig.
- Wifi + BLE, PCNT voor encoders, 240 MHz met FPU, veel RAM.
- Webinterface mogelijk via wifi of Web Bluetooth.

**Nadelen**
- **Geen Bluetooth Classic, alleen BLE:** een pc ziet hem niet als seriële poort. Je hebt een eigen BLE-programma of webpagina nodig.
- ADC nog altijd minder goed dan bij een STM32, 3,3V-logica, stroompieken, bootstrap-pinnen.
- Veel bordvarianten (N8, N16R8, …): sommige pinnen zijn bezet door PSRAM.
- Geen ervaring mee in de cursus, niet KISS.

## 7. STM32F103 — "blue pill"

**Voordelen**
- 72 MHz 32-bit, 12-bit ADC met ±1 µs per conversie + **DMA**: alle sensoren lezen terwijl de processor verder rekent.
- **Hardware-encodermodus in de timers:** encoders kosten geen processortijd.
- 3 UART's, veel timers, goedkoop.
- Arduino-compatibel via STM32duino.
- LQFP-48: met de hand te solderen.

**Nadelen**
- **Veel namaak** (CKS32, fake chips): gedrag en flash verschillen, en uren frustratie zoals de cursus waarschuwt.
- Vaak **geen bootloader**: je hebt een ST-Link-programmer nodig (±€3).
- Bekende hardwarefout op veel bordjes: een verkeerde USB-pull-up (weerstand R10).
- Geen FPU.
- 3,3V-logica, geen EEPROM.
- Verouderd: de F411 en G431 zijn beter voor dezelfde prijs.

## 8. STM32F411 — "black pill" (WeAct)

**Voordelen**
- 100 MHz Cortex-M4 **met FPU**, 128 kB RAM.
- 12-bit ADC (2,4 MS/s) met DMA, encodermodus in de timers.
- **USB-bootloader in de chip** (DFU): uploaden zonder programmer.
- WeAct-bord is betrouwbaar en goedkoop (±€7).

**Nadelen**
- **De chip zit in een QFN-48-behuizing:** zonder pootjes, bijna niet met de hand te solderen voor plan A.
- Maar één ADC (sensoren na elkaar, niet parallel).
- Nieuwe omgeving (STM32duino of STM32CubeIDE), niet KISS.
- 3,3V-logica, geen EEPROM, geen draadloos.

## 9. STM32G431

**Voordelen**
- Technisch de sterkste kandidaat voor een linefollower: **170 MHz met FPU**, **2 ADC's van 4 MS/s** (twee sensoren tegelijk), DMA.
- Geavanceerde motortimers, encodermodus, ingebouwde op-amps en comparators, CORDIC-rekenhulp.
- Verkrijgbaar in **LQFP-48** (met de hand te solderen), chip ±€4.
- Arduino-compatibel via STM32duino.

**Nadelen**
- Kleinste hobbygemeenschap van deze lijst: minder voorbeelden en fora.
- Nieuwe omgeving, geen ervaring mee, niet KISS. Voor dit project betekent dat een groot risico op tijdverlies.
- Plan B-bordjes minder gangbaar (WeAct G431 ±€7).
- 3,3V-logica, geen EEPROM, geen draadloos.
- De extra rekenkracht is pas nodig bij 12–16 sensoren of route-optimalisatie.

## 10. RP2040 — Raspberry Pi Pico

**Voordelen**
- 133 MHz, 2 kernen, 264 kB RAM, spotgoedkoop (Pico ±€4, chip ±€1).
- **PIO:** kleine programmeerbare hardware-blokken, ideaal voor encoders en exacte timing.
- Uploaden via USB-drag-and-drop, goede Arduino-ondersteuning (arduino-pico).
- Pico W: wifi en BLE.

**Nadelen**
- **Maar 3 analoge ingangen op de Pico** (4 in de chip): multiplexer nodig voor 8 sensoren (zoals bij de ESP8266).
- De ADC heeft bekende fouten (sprongen op bepaalde waarden).
- Geen FPU.
- Plan A: chip in QFN-56, plus een externe flashchip en kristal. Moeilijk met de hand.
- 3,3V-logica, geen EEPROM.

## 11. RP2350 — Raspberry Pi Pico 2

**Voordelen**
- 150 MHz, 2× Cortex-M33 **met FPU**, 520 kB RAM, PIO, goedkoop.
- Pico 2 W met wifi en BLE.

**Nadelen**
- **Ook maar 3–4 analoge ingangen** (8 enkel op de RP2350B-variant, die niet op de Pico 2 zit).
- QFN-behuizing plus externe flash: moeilijk voor plan A.
- Nieuw platform, weinig linefollower-voorbeelden.

## Niet verder bekeken
- **Teensy 4.0** (600 MHz): ±€25, ver boven budget.
- **Arduino Nano ESP32 / Uno R4:** ±€20, te duur voor wat ze bieden. De Uno R4 heeft maar 6 analoge pinnen.

---

## Besluit

Eerste besluit (op prestaties): **ATmega32U4**. Het haalt alle harde eisen, en rekenkracht beperkt de robot niet: de grip in bochten van 10 cm doet dat (v ≈ √(μ·g·r)).

**Herzien besluit (prioriteit: zo makkelijk mogelijk debuggen en tunen): ESP32-S3.**

| Criterium | 32U4 + HC-05 | **ESP32-S3** |
|---|---|---|
| Live telemetrie tijdens het rijden | ±100 metingen/s, weinig waarden | **500–1000 metingen/s, alle waarden** |
| Volledige ronde loggen | nee (2,5 kB RAM) | **ja (512 kB RAM)** |
| Instellingen aanpassen | terminal-commando's | **webdashboard met schuifregelaars** |
| Code uploaden op de baan | USB-kabel | **draadloos (OTA)** |
| Echte debugger | nee | **ingebouwde JTAG via USB** |
| 8 sensoren + batterij | ja | ja (10 ADC1-kanalen) |
| Encoders | interrupts, kanaal A | **hardware-teller, A + B** |
| Extra module draadloos | HC-05 | geen |
| Past bij cursus (KISS) | ja | nee → verantwoord in onderdelenkeuze.md §2b |

Tunen bepaalt de eindsnelheid, en elk van deze functies maakt een tuningronde korter en beter onderbouwd. Dat is de meerwaarde die de cursus vraagt.

**Backupplan:** ATmega32U4 (Arduino Micro) + HC-05. Alle andere hardware is gelijk, de firmware heeft één hardwarelaag (`board.h`), en de proof-of-concepts krijgen maximaal 1 week. De STM32G431 blijft de keuze als ooit rekenkracht (12–16 sensoren, route-optimalisatie) nodig blijkt.
