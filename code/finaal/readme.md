# Finale code

Sketch: [linefollower/linefollower.ino](linefollower/linefollower.ino). Compileert voor de ESP32-S3 (70 % flash). Uploaden: `.\upload.ps1 finaal -Monitor` vanuit de map `code`.

```
arduino-cli compile --fqbn esp32:esp32:esp32s3 --library code/lib/lf_core --library code/lib/lf_esp32 code/finaal/linefollower
arduino-cli upload  --fqbn esp32:esp32:esp32s3 -p COM5 code/finaal/linefollower
```

## Wat zit erin
- **Sensoren**: elke cyclus meten met IR-leds aan én uit (omgevingslicht weg), kalibratie per sensor, normalisatie 0..1000, lijnpositie als zwaartepunt (±1 mm), lijn kwijt -> draai naar de laatste kant, kruispunt -> rechtdoor.
- **Regeling** ([lf_core](../lib/lf_core/readme.md)): PID op de lijnpositie, boost op rechte stukken, meteen remmen bij een bocht (op fout én afgeleide), PI-snelheidsregeling per wiel met de encoders, batterijcompensatie.
- **Veiligheid**: stopt als de lijn 0,5 s kwijt is of de batterij onder `vbatmin` zakt; motoren uit (STBY laag) in stilstand.
- **Communicatie**: zelfde commando's via USB en wifi (netwerk *linefollower*, TCP 192.168.4.1:23).
- **Opslag**: elke `set` en elke kalibratie wordt meteen bewaard in het flashgeheugen (tijdens het rijden: zodra de robot stopt). Bij het opstarten worden de laatste instellingen geladen.
- **Cyclus**: vaste regelcyclus (`set cycle`, standaard 1000 µs); `debug` toont de cyclustijd en de langste rekentijd.
- **Statusled**: groen = rijden, rood = stil, blauw = kalibreren, oranje = batterij laag.
- Standaardparameters = resultaat van de [simulatie](../../simulatie/resultaat_tune.md).

## Commando's
| Commando | Wat |
|---|---|
| `help` | lijst |
| `start` / `stop` | rijden / stoppen (ook met de knop) |
| `get` / `get kp` | parameters tonen |
| `set kp 0.03` | parameter zetten (zie `get` voor alle namen) |
| `save` / `load` / `reset` | bewaren (gebeurt ook automatisch) / terughalen / standaardwaarden |
| `debug` | cyclustijd + langste rekentijd sinds de vorige `debug` |
| `invert sensor` / `motorl` / `motorr` / `encl` / `encr` | richting omkeren zonder te hersolderen (wordt bewaard); `invert` alleen toont de toestand |
| `cal` ... `cal stop` | kalibreren: robot met de hand over de lijn heen en weer schuiven |
| `calibrate white` / `calibrate black` | kalibreren: alle sensoren op wit / op zwart |
| `sensors` | ruwe waarden (aan/uit), reflectie, genormaliseerd, positie |
| `status` | batterij, positie, wielsnelheden, encodertellers, langste cyclus |
| `motor l 0.3 500` | motortest: links, duty 0,3, 500 ms |
| `set debug on` / `debug on` | elke 20 ms: `t, positie, v_doel, v_links, v_rechts, duty_l, duty_r, vbat` (CSV, ook voor de simulatie) |

## Testen per bouwstap (zie [instructable](../../instructable/readme.md))
| Stap | Test met deze firmware |
|---|---|
| 7 ESP32 | `status`: vbat klopt met de multimeter (±0,1 V) |
| 8 H-brug | `motor l 0.3 500` en `motor r 0.3 500` |
| 9 motoren + encoders | `motor l 0.3 1000`: het linkerwiel draait vooruit en de encoderteller links stijgt. Fout? `invert motorl` of `invert encl` (rechts: `motorr`, `encr`) |
| 10 sensor | `sensors`: `refl` hoog op wit, laag op zwart, per sensor. Reageert de verkeerde kant? `invert sensor`. Dan `cal`, schuiven, `cal stop` |
| 11 knop | knop indrukken: `START` / `STOP` en de led wisselt |
| rijden | eerst traag: `set vbocht 0.4`, `set vrecht 0.6`, `start`; daarna stap voor stap naar de simulatiewaarden |
