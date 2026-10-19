# Bedradingslijst (plan B, gaatjesprint)

Zelfde netten als `kicad/linefollower.kicad_sch` (ERC: 0 fouten). Schema als PDF: [elektrisch_schema.pdf](elektrisch_schema.pdf).
Draad: 24AWG silicone. Rood = VBAT/BATT+, oranje = 3V3, zwart = GND, overige kleuren = signalen.

## Voeding

| Van | Naar | Net | Opmerking |
|---|---|---|---|
| LiPo + (XT30) | SW1 midden (pin 2) | BATT+ | XT30-pigtail op de print |
| SW1 pin 1 | TB6612 **VM**, buck **IN+**, R1, C1 + | VBAT | 6,4–8,4 V |
| LiPo − (XT30) | alle GND | GND | één sterpunt bij de XT30 |
| Buck **OUT+** | ESP32 **3V3**, QTR **VCC**, TB6612 **VCC**, encoders VCC (2×), WS2812 **VCC**, R3, C2 + | 3V3 | buck vooraf op 3,3 V meten! |
| C1 100 µF | VM ↔ GND, vlak bij de TB6612 | | let op polariteit |
| C2 100 µF | 3V3 ↔ GND, vlak bij de ESP32 | | let op polariteit |
| R3 330 Ω + D1 (power-led) | 3V3 → R3 → led anode, kathode → GND | LED_PWR | |

## Batterijmeting

| Van | Naar | Net |
|---|---|---|
| VBAT | R1 100 kΩ | |
| R1 / R2-knoop | ESP32 **GPIO9** | VBAT_SENSE (8,4 V → 2,08 V) |
| R2 33 kΩ | GND | |

## Sensor (QTR-8A)

| QTR-8A | ESP32 |
|---|---|
| OUT1 … OUT8 | GPIO1 … GPIO8 |
| LEDON | GPIO11 |
| VCC / GND | 3V3 / GND |

Soldeer de jumper **"3.3V BYPASS"** op de QTR-8A dicht, anders branden de IR-leds te zwak op 3,3 V.

## Motorsturing (TB6612FNG, 1 module voor beide motoren)

| TB6612 | ESP32 / motor |
|---|---|
| PWMA, AIN1, AIN2 | GPIO12, GPIO13, GPIO14 |
| PWMB, BIN1, BIN2 | GPIO15, GPIO16, GPIO17 |
| STBY | GPIO18 (laag = motoren uit, veilig bij opstarten) |
| AO1 / AO2 | motor links M1 / M2 |
| BO1 / BO2 | motor rechts M1 / M2 |

100 nF (C3, C4) **rechtstreeks over de motorklemmen** solderen.

## Encodermotoren (ZH1.5 6-pins kabel)

| Motorkabel | Links | Rechts |
|---|---|---|
| 1 M1 / 6 M2 | AO1 / AO2 | BO1 / BO2 |
| 5 VCC / 2 GND | 3V3 / GND | 3V3 / GND |
| 3 ENC_A | GPIO39 | GPIO41 |
| 4 ENC_B | GPIO40 | GPIO42 |

**Controleer de pinvolgorde op het encoderprintje van de motor** (opdruk M1/GND/C1/C2/VCC/M2). Deze volgorde is de gangbare, maar verschilt soms per verkoper.
Draaien de motoren of encoders verkeerd om: AO1/AO2 (of A/B) omwisselen, of het teken in de software omkeren.

## Bediening en weergave

| Onderdeel | Aansluiting |
|---|---|
| Start/stop-knop SW2 | GPIO21 ↔ GND (interne pull-up) |
| WS2812-strip | DIN → GPIO47, VCC → 3V3, GND → GND |
| Gyro (optioneel, later) | SDA GPIO10, SCL GPIO44 |

## Controle vóór de eerste keer inschakelen
1. Zonder ESP32 in de headers: buck-uitgang meten (3,25–3,35 V).
2. Weerstand VBAT ↔ GND en 3V3 ↔ GND meten: geen kortsluiting.
3. Pas dan de ESP32 inpluggen en via USB een testsketch laden.
