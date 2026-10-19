# start/stop interrupt proof of concept
minimale hard- en software die de correcte werking van een start/stop drukknop aantoont, gebruik makend van een hardware interrupt

### hardware
Drukknop tussen **GPIO21** en **GND**. De interne pull-up staat aan, dus er is geen weerstand nodig. Status op de ingebouwde RGB-led van de devkit.

### werking
[poc_interrupt.ino](poc_interrupt/poc_interrupt.ino) gebruikt een hardware-interrupt op de dalende flank. De ontdendering werkt met de tijd: een nieuwe druk telt pas als hij meer dan 200 ms na de vorige komt. De hoofdlus hoeft de knop dus nooit zelf uit te lezen.

### gebruiksaanwijzing
1. Upload `poc_interrupt` (USB volstaat).
2. Druk op de knop.

### resultaat
- [ ] elke druk wisselt rood (stop) en groen (rijden)
- [ ] snel drukken geeft geen dubbele wissels
