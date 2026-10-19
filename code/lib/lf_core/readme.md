# lf_core

De regelkern van de linefollower, in gewone C++ zonder Arduino. Daardoor draait **dezelfde code** op de ESP32 en in de [simulatie](../../../simulatie/readme.md) op de pc.

| Bestand | Inhoud |
|---|---|
| [lf_params.h](src/lf_params.h) | alle instelbare parameters met standaardwaarde, grenzen en uitleg (tabel `PARAM_DEFS`) |
| [lf_sensor.h](src/lf_sensor.h) | reflectie met leds aan/uit, kalibratie (wit/zwart per sensor), normalisatie 0..1000, interpolatie (zwaartepunt), lijn kwijt, kruispunt |
| [lf_control.h](src/lf_control.h) | regelaar: PID op de lijnpositie -> snelheidsverschil; snelheidsprofiel (boost/remmen); per wiel voorwaartse sturing + PI op de encodersnelheid; batterijcompensatie |
| [lf_cmd.h](src/lf_cmd.h) | commando's `set <naam> <waarde>` / `get [naam]` |
| [lf_core.h](src/lf_core.h) | alles in één include |

## Signaalverloop
```
ADC (leds uit) - ADC (leds aan) = reflectie       -> kalibratie + normalisatie -> zwart 0..1000 per sensor
zwaartepunt rond de hoogste sensor                -> lijnpositie (mm, + = links)
PID(positie)                                      -> snelheidsverschil dv (m/s)
profiel: rechtdoor -> boost, bocht -> remmen      -> basissnelheid v (m/s)
v_links = v - dv, v_rechts = v + dv               -> per wiel: duty = v / (v_per_volt * Vbat) + PI(encoder)
```

Getest met [simulatie/test_core.cpp](../../../simulatie/test_core.cpp) (133 testen).
