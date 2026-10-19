# Draadlijst (automatisch gemaakt door bekabelingsplan.py)

Stappen = [instructable](../../instructable/readme.md). Nummers = nummers op [bekabelingsplan.pdf](bekabelingsplan.pdf). Alle draden liggen aan de **onderzijde** (soldeerkant).
Kleur = aanbevolen draadkleur. Vink af tijdens het solderen.


## Stap 5 - voeding

| ✓ | nr | van | naar | net | kleur | opmerking |
|---|---|---|---|---|---|---|
| ☐ | 1 | XT30+ | SW1.2 | BATT+ | rood | rode draad van de pigtail (20AWG) |
| ☐ | 2 | XT30- | BUCK IN- | GND | zwart | zwarte draad pigtail = GND-sterpunt |
| ☐ | 3 | SW1.1 | BUCK IN+ | VBAT | rood |  |
| ☐ | 4 | BUCK IN+ | TB6612 VM | VBAT | rood | dik draadje (24AWG of dikker) |
| ☐ | 5 | BUCK IN- | TB6612 GND | GND | zwart | motorstroom terug |
| ☐ | 6 | BUCK OUT+ | ESP J1-1 (3V3) | 3V3 | oranje | devkit gevoed via 3V3-pin, NIET via USB-5V |
| ☐ | 7 | BUCK OUT- | ESP J3-1 (GND) | GND | zwart |  |
| ☐ | 8 | ESP J1-1 (3V3) | C2+ | 3V3 | oranje | C2 100 uF, + naar 3V3 |
| ☐ | 9 | ESP J3-1 (GND) | C2- | GND | zwart |  |
| ☐ | 10 | TB6612 VM | C1+ | VBAT | rood | C1 100 uF vlak bij VM |
| ☐ | 11 | TB6612 GND | C1- | GND | zwart |  |
| ☐ | 12 | BUCK OUT+ | R3 | 3V3 | oranje | R3 330 ohm -> power-led D1 -> GND |
| ☐ | 13 | D1 | BUCK IN- | GND | zwart | kathode (korte poot) naar GND |

## Stap 6 - batterijmeting

| ✓ | nr | van | naar | net | kleur | opmerking |
|---|---|---|---|---|---|---|
| ☐ | 14 | SW1.1 | R1 | VBAT | rood | R1 100k van VBAT naar meetpunt |
| ☐ | 15 | R1 | ESP J1-15 (GPIO9) | VBAT_SENSE | wit/paars | meetpunt R1/R2 -> GPIO9 |
| ☐ | 16 | R2 | ESP J1-22 (GND) | GND | zwart | R2 33k van meetpunt naar GND |

## Stap 8 - H-brug

| ✓ | nr | van | naar | net | kleur | opmerking |
|---|---|---|---|---|---|---|
| ☐ | 17 | ESP J1-1 (3V3) | TB6612 VCC | 3V3 | oranje | logische voeding TB6612 |
| ☐ | 18 | TB6612 GND | ESP J1-22 (GND) | GND | zwart |  |
| ☐ | 19 | TB6612 PWMA | ESP J1-18 (GPIO12) | PWMA | geel | motor links snelheid |
| ☐ | 20 | TB6612 AIN1 | ESP J1-19 (GPIO13) | AIN1 | groen |  |
| ☐ | 21 | TB6612 AIN2 | ESP J1-20 (GPIO14) | AIN2 | groen |  |
| ☐ | 22 | TB6612 PWMB | ESP J1-8 (GPIO15) | PWMB | geel | motor rechts snelheid |
| ☐ | 23 | TB6612 BIN1 | ESP J1-9 (GPIO16) | BIN1 | groen |  |
| ☐ | 24 | TB6612 BIN2 | ESP J1-10 (GPIO17) | BIN2 | groen |  |
| ☐ | 25 | TB6612 STBY | ESP J1-11 (GPIO18) | STBY | groen | laag = motoren uit |

## Stap 9 - motoren en encoders

| ✓ | nr | van | naar | net | kleur | opmerking |
|---|---|---|---|---|---|---|
| ☐ | 26 | GAT MOTOR L | TB6612 AO1 | MOT_L+ | motorkabel | motor links M1 (+100 nF over de motorklemmen) |
| ☐ | 27 | GAT MOTOR L | TB6612 AO2 | MOT_L- | motorkabel | motor links M2 |
| ☐ | 28 | GAT MOTOR R | TB6612 BO1 | MOT_R+ | motorkabel | motor rechts M1 (+100 nF) |
| ☐ | 29 | GAT MOTOR R | TB6612 BO2 | MOT_R- | motorkabel | motor rechts M2 |
| ☐ | 30 | GAT MOTOR L | ESP J3-9 (GPIO39) | ENC_L_A | encoderkabel | encoder links A |
| ☐ | 31 | GAT MOTOR L | ESP J3-8 (GPIO40) | ENC_L_B | encoderkabel | encoder links B |
| ☐ | 32 | GAT MOTOR R | ESP J3-7 (GPIO41) | ENC_R_A | encoderkabel | encoder rechts A |
| ☐ | 33 | GAT MOTOR R | ESP J3-6 (GPIO42) | ENC_R_B | encoderkabel | encoder rechts B |
| ☐ | 34 | GAT MOTOR L | BUCK OUT+ | 3V3 | oranje | encoder VCC links + rechts samen |
| ☐ | 35 | GAT MOTOR L | BUCK OUT- | GND | zwart | encoder GND links + rechts samen |

## Stap 10 - sensor

| ✓ | nr | van | naar | net | kleur | opmerking |
|---|---|---|---|---|---|---|
| ☐ | 36 | QTR.1 | ESP J3-4 (GPIO1) | S1 | wit/paars | sensor 1 = uiterst links |
| ☐ | 37 | QTR.2 | ESP J3-5 (GPIO2) | S2 | wit/paars |  |
| ☐ | 38 | QTR.3 | ESP J1-13 (GPIO3) | S3 | wit/paars |  |
| ☐ | 39 | QTR.4 | ESP J1-4 (GPIO4) | S4 | wit/paars |  |
| ☐ | 40 | QTR.5 | ESP J1-5 (GPIO5) | S5 | wit/paars |  |
| ☐ | 41 | QTR.6 | ESP J1-6 (GPIO6) | S6 | wit/paars |  |
| ☐ | 42 | QTR.7 | ESP J1-7 (GPIO7) | S7 | wit/paars |  |
| ☐ | 43 | QTR.8 | ESP J1-12 (GPIO8) | S8 | wit/paars | sensor 8 = uiterst rechts |
| ☐ | 44 | QTR.LEDON | ESP J1-17 (GPIO11) | LEDON | wit/paars | IR-leds aan/uit |
| ☐ | 45 | QTR.VCC | ESP J1-1 (3V3) | 3V3 | oranje | jumper 3.3V BYPASS op de QTR dicht! |
| ☐ | 46 | QTR.GND | ESP J1-22 (GND) | GND | zwart |  |

## Stap 11 - bediening

| ✓ | nr | van | naar | net | kleur | opmerking |
|---|---|---|---|---|---|---|
| ☐ | 47 | KNOP.1 | ESP J3-18 (GPIO21) | BTN | blauw | start/stop, interne pull-up |
| ☐ | 48 | KNOP.2 | ESP J3-1 (GND) | GND | zwart |  |
