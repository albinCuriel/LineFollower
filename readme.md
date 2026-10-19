# LineFollower

Syntheseproject HOGENT Elektromechanica: een snelle linefollower (doel ≥ 1 m/s) met een ESP32-S3. De robot is gebouwd op een gaatjesprint die tegelijk het chassis is (plan B). De eigen print (plan A) wordt enkel ontworpen.

![3D-model linefollower](technische%20tekeningen/mechanisch/3d_iso_voor_links.png)

## specifications

| | |
|---|---|
| microcontroller | ESP32-S3 devkit N8R2 (dual USB-C), backup ATmega32U4 ([waarom](ontwerpkeuzes/onderdelenkeuze.md)) |
| motors | 2× GA12-N20 6V 10:1 (±1500 rpm) met Hall-encoder 7 PPR |
| h-bridge | TB6612FNG (1 module voor beide motoren) |
| sensors | Pololu QTR-8A (8 analoge reflectiesensoren, LEDON) |
| batteries | LiPo 2S 450 mAh 100C (XT30), 3,3 V via een CN3903-buck |
| wireless communication | wifi: eigen netwerk + TCP-terminal (gsm of laptop) |
| distance sensor - motors | 98,7 mm |
| weight | ±123 g (berekend uit de onderdelen, wordt gewogen na de bouw) |
| speed | simulatie op parcours 3: ±0,9–1,1 m/s gemiddeld; wordt gemeten op het parcours |
| afmetingen | 121 × 106 × 48 mm (L × B × H, met spoiler) |

## inhoud van deze repository

| Map | Inhoud |
|---|---|
| [bill of materials](bill%20of%20materials/readme.md) | onderdelenlijst met prijzen en bestelling |
| [ontwerpkeuzes](ontwerpkeuzes/readme.md) | waarom deze onderdelen, vergelijking van microcontrollers, snelheidsberekening |
| [technische tekeningen](technische%20tekeningen/readme.md) | elektrisch schema, bekabelingsplan, boormal, 3D-model, samenstellingstekening |
| [instructable](instructable/readme.md) | stappenplan om de robot te bouwen |
| [code](code/readme.md) | proof of concepts, basisprogramma en finale code |
| [simulatie](simulatie/readme.md) | de robot virtueel op parcours 3, met dezelfde regelcode: PID vooraf afgesteld |
| [gebruiksaanwijzing](gebruiksaanwijzing/readme.md) | opladen, verbinden, commando's, kalibreren |
| [datasheets](datasheets/readme.md) | datasheets van alle onderdelen |
| [parcours](parcours/readme.md) | testparcours |
| [images](images/readme.md) | foto's |
