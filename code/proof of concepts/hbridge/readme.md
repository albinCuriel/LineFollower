# H-Bridge proof of concept

minimale hard- & software + stappenplan dat aantoont dat 2 motoren onafhankelijk van elkaar kunnen draaien, en (traploos) regelbaar zijn in snelheid en draairichting.

### hardware
| TB6612FNG | ESP32-S3 / motor |
|---|---|
| PWMA, AIN1, AIN2 | GPIO12, GPIO13, GPIO14 |
| PWMB, BIN1, BIN2 | GPIO15, GPIO16, GPIO17 |
| STBY | GPIO18 |
| AO1/AO2 · BO1/BO2 | motor links · motor rechts |
| VM / VCC | VBAT (2S lipo) / 3V3 |

Volledige bedrading: [draadlijst stap 8 en 9](../../../technische%20tekeningen/elektronisch/draadlijst.md).

### werking
[poc_hbridge.ino](poc_hbridge/poc_hbridge.ino) stuurt PWM op 20 kHz (niet hoorbaar) met een resolutie van 10 bit (0–1023). Het teken van de snelheid bepaalt de draairichting via AIN1/AIN2. Beide motoren versnellen en vertragen traploos (ramp), eerst links, dan rechts, dan samen.

### gebruiksaanwijzing
1. Zet de robot op een doosje: **wielen in de lucht**.
2. Upload `poc_hbridge`, batterij aan, SW1 aan.

### resultaat
- [ ] links vooruit en achteruit, traploos
- [ ] rechts vooruit en achteruit, traploos
- [ ] beide samen
