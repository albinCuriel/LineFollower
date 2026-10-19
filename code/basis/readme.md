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

Sketch: [basis/basis.ino](basis/basis.ino) (ESP32-S3, compileert).

| Vereiste | Hoe |
|---|---|
| instelbare parameters | commando's `set cycle 500000`, `set debug on`, `start`, `stop`, `get` via USB of wifi ([lf_cmd.h](../lib/lf_core/src/lf_cmd.h)) |
| eeprom | `save` bewaart in het flashgeheugen van de ESP32 (Preferences/NVS, [opslag.h](../lib/lf_esp32/src/opslag.h)); bij opstarten automatisch geladen |
| externe interrupt | drukknop op GPIO21, `attachInterrupt` met 200 ms ontdendering ([hw.h](../lib/lf_esp32/src/hw.h)) |
| draadloze communicatie | eigen wifinetwerk *linefollower*, TCP-terminal naar 192.168.4.1:23 ([comms.h](../lib/lf_esp32/src/comms.h)) |
| cyclus | de statusled wisselt elke cyclus: `set cycle 500000` = 1 Hz knipperen; groen = start, blauw = stop |

```
arduino-cli compile --fqbn esp32:esp32:esp32s3 --library code/lib/lf_core --library code/lib/lf_esp32 code/basis/basis
```
