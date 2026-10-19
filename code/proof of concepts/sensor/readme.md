# Sensoren proof of concept

minimale hard- en software die aantoont dat minimaal 6 sensoren onafhankelijk van elkaar kunnen uitgelezen worden (geen calibratie, normalisatie of interpolatie). Hierbij moet een zo groot mogelijk bereik van de AD converter benut worden (indien van toepassing)

### hardware
| QTR-8A | ESP32-S3 |
|---|---|
| OUT1 … OUT8 | GPIO1 … GPIO8 (ADC1) |
| LEDON | GPIO11 |
| VCC / GND | 3V3 / GND |

Soldeer de jumper **3.3V BYPASS** op de QTR-8A dicht. Volledige bedrading: [draadlijst stap 10](../../../technische%20tekeningen/elektronisch/draadlijst.md).

### werking
Elke cyclus meet [poc_sensor.ino](poc_sensor/poc_sensor.ino) alle 8 sensoren twee keer: één keer met de IR-leds aan en één keer met de leds uit. Het verschil is de echte reflectie, zonder zonlicht of tl-licht.
De ADC staat op 12 bit en 11 dB demping (0 tot ±3,1 V). Zo gebruikt de meting het volledige bereik, omdat de QTR ook op 3,3 V werkt.

### gebruiksaanwijzing
1. Upload `poc_sensor` en open de seriële monitor op 115200 baud.
2. Schuif een stuk zwarte tape onder de sensoren.

### resultaat
- [ ] elke sensor reageert apart
- [ ] wit: lage waarde, zwart: hoge waarde (in te vullen: ___ / ___)
