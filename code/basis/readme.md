# basis programma

volgende zaken werken samen in dit template project  

* instelbare parameters mbv. SerialCommands 
  * cyclus tijd
  * debug on/off
  * start/stop
* parameters worden opgeslagen in eeprom geheugen
* start/stop kan ook geactiveerd worden mbv. een externe interrupt
* draadloze communicatie

Met behulp van de cyclus kan je bvb. een knipperende led programmeren.

## Uitwerking

Sketch: [basis/basis.ino](basis/basis.ino) (ESP32-S3). Uploaden: `.\upload.ps1 basis -Monitor` vanuit de map `code`.

| Vereiste uit de cursus | Hoe |
|---|---|
| SerialCommand: commando's inlezen zonder te blokkeren | [comms.h](../lib/lf_esp32/src/comms.h) leest teken per teken en geeft pas een regel terug als hij volledig is. [lf_cmd.h](../lib/lf_core/src/lf_cmd.h) splitst de regel in commandowoord + argumenten en roept de juiste handler op (`onSet`, `onDebug`, `onUnknown`). Zelfde opbouw als de bibliotheek SerialCommand, maar ze werkt ook over wifi. |
| instelbare parameters | `set cycle 500000`, `set debug on`, `start`, `stop`, `get` |
| EEPROM | alle parameters zitten in één struct (`lf::Params`). Elke `set` schrijft de struct meteen naar het flashgeheugen (Preferences/NVS, de EEPROM van de ESP32, [opslag.h](../lib/lf_esp32/src/opslag.h)). Bij het opstarten wordt hij teruggelezen. |
| cyclus | het cyclische deel loopt om de `cycle` microseconden. De rekentijd wordt gemeten. Het commando `debug` toont de cyclustijd en de langste rekentijd sinds de vorige `debug`. In het cyclische deel wordt niet naar de seriële poort geschreven. |
| externe interrupt | drukknop op GPIO21, `attachInterrupt` op de dalende flank met 200 ms ontdendering ([hw.h](../lib/lf_esp32/src/hw.h)) |
| draadloze communicatie | eigen wifinetwerk *linefollower*, TCP-terminal naar 192.168.4.1:23 |
| knipperende led | de statusled wisselt elke cyclus: `set cycle 500000` = 1 Hz knipperen. Groen = gestart, blauw = gestopt. |

### testen
```
set cycle 500000      led knippert 1 Hz
debug                 cycle time: 500000 us / calculation time (max): ... us
set debug on          elke seconde een bericht (non-blocking wait)
start                 led knippert groen; de knop doet hetzelfde
```
Trek de USB-kabel uit en steek hem weer in: de led knippert nog steeds op 1 Hz (parameter teruggelezen uit het flashgeheugen).

```
arduino-cli compile --fqbn esp32:esp32:esp32s3 --library code/lib/lf_core --library code/lib/lf_esp32 code/basis/basis
```
