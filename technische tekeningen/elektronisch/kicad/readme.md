# KiCad-project

Elektrisch schema van de linefollower in **KiCad 10**.

| Bestand | Inhoud |
|---|---|
| `linefollower.kicad_pro` | het project: open dit in KiCad |
| `linefollower.kicad_sch` | het schema |
| `lf_modules.kicad_sym` | eigen symbolen: ESP32-S3 devkit, QTR-8A, TB6612-module, N20-motor met encoder, CN3903-buck |
| `sym-lib-table` | koppelt de eigen symboolbibliotheek aan het project |
| `linefollower.kicad_pcb` | lege print (plan A, PCB-ontwerp volgt) |
| `linefollower.kicad_prl` | lokale weergave-instellingen |

Geen KiCad? Bekijk het schema als [PDF](../elektrisch_schema.pdf) of [SVG](../elektrisch_schema.svg).

Opnieuw exporteren na een wijziging:
```
kicad-cli sch erc linefollower.kicad_sch
kicad-cli sch export pdf -o ../elektrisch_schema.pdf linefollower.kicad_sch
kicad-cli sch export svg -o .. linefollower.kicad_sch
```
ERC: 0 elektrische fouten. Er komen wel meldingen dat de standaardbibliotheken niet in deze map staan.
