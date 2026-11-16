# TB6612FNG module (breakout) – pinout

De chipdatasheet staat in [TB6612FNG_datasheet.pdf](TB6612FNG_datasheet.pdf). Wij gebruiken de rode breakoutmodule van AliExpress (zelfde pinvolgorde als de SparkFun- en Pololu-carrier). Deze pagina geeft de pinout van die module.

Bronnen: opdruk op de module zelf (nagemeten), verkoperpagina AliExpress (bestelling 8/10/2026), [Pololu TB6612FNG carrier](https://www.pololu.com/product/713).

## Afmetingen

| Maat | Waarde |
|---|---|
| Print | ±20 × 20 mm |
| Pinrijen | 2 × 8 pinnen, steek 2,54 mm |
| Afstand tussen de 2 pinrijen | **15,24 mm (0,6″ = 6 gaten op de gaatjesprint)** |

## Pinout (bovenaanzicht, opdruk leesbaar)

| Linkerrij | Functie | | Rechterrij | Functie |
|---|---|---|---|---|
| PWMA | PWM motor A → GPIO12 | | VM | motorvoeding 2,5–13,5 V (batterij) |
| AIN2 | richting A → GPIO14 | | VCC | logica 2,7–5,5 V (3V3) |
| AIN1 | richting A → GPIO13 | | GND | massa |
| STBY | standby (hoog = actief) → GPIO18 | | AO1 | motor A + |
| BIN1 | richting B → GPIO15 | | AO2 | motor A − |
| BIN2 | richting B → GPIO16 | | BO2 | motor B − |
| PWMB | PWM motor B → GPIO17 | | BO1 | motor B + |
| GND | massa | | GND | massa |

Motor A = links, motor B = rechts. De GPIO-nummers komen uit [board.h](../code/board.h).

## Waarheidstabel (per kanaal)

| IN1 | IN2 | PWM | STBY | Uitgang |
|---|---|---|---|---|
| H | H | x | H | kortsluitremmen |
| L | H | H | H | achteruit (CCW) |
| H | L | H | H | vooruit (CW) |
| L | H/L | L | H | kortsluitremmen |
| L | L | H | H | vrijloop (stop) |
| x | x | x | L | standby, alles uit |

## Grenswaarden (chip)

| Eigenschap | Waarde |
|---|---|
| Uitgangsstroom | 1,2 A continu, 3,2 A piek per kanaal |
| Motorspanning VM | max. 15 V (aanbevolen ≤ 13,5 V) |
| PWM-frequentie | max. 100 kHz (wij: 20 kHz) |
| Aan-weerstand | ±0,5 Ω per kanaal (boven + onder) |

Op de module zitten al ontkoppelcondensatoren op VM en VCC. Wij plaatsen een extra 100 µF op VM, vlak bij de module (C1).
