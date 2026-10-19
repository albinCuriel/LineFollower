# Elektronisch

![elektrisch schema](elektrisch_schema.svg)

| Bestand | Wat | Openen |
|---|---|---|
| [elektrisch_schema.pdf](elektrisch_schema.pdf) | volledig schema (A4) | PDF, opent op GitHub |
| [elektrisch_schema.svg](elektrisch_schema.svg) | hetzelfde schema als afbeelding | browser |
| [bekabelingsplan.pdf](bekabelingsplan.pdf) | **9 pagina's A3**: plaatsing, 1 pagina per bouwstap (nieuwe draden dik en genummerd, vorige grijs), controleblad | PDF |
| `bekabelingsplan_pNN_*.png` | dezelfde pagina's als afbeelding, ook ingevoegd in de [instructable](../../instructable/readme.md) | afbeelding |
| [bekabelingsplan_boormal_1op1.pdf](bekabelingsplan_boormal_1op1.pdf) | bovenzijde op ware grootte: plaats van elk onderdeel en boorgat | afdrukken op 100 % (A4) |
| [bekabelingsplan_draadlijst.md](bekabelingsplan_draadlijst.md) | alle 52 draden als afvinklijst: van gat, naar gat, kleur, lengte | GitHub |
| [kabels/](kabels/readme.md) | batterij-, motor- en sensorkabels (WireViz) | afbeelding |
| [bedradingslijst.md](bedradingslijst.md) | verbindingen per onderdeel + controles vóór inschakelen | GitHub |
| [kicad/](kicad/readme.md) | KiCad 10-project van het schema | KiCad |
| [bekabeling_config.py](bekabeling_config.py) | **de gegevens**: plaats van elk onderdeel (gat per pin), boorgaten, verboden zones, alle draden per stap | aanpassen |
| [perfplan.py](perfplan.py) | **de motor**: routeert de draden door vrije gaten en tekent alle pagina's | `py -3 perfplan.py bekabeling_config.py` |
| [easyeda_linefollower_planB.json](easyeda_linefollower_planB.json) | voorbeeldschema van de docent (Pro Micro, DRV8833), enkel ter referentie | EasyEDA |

## Overzicht

| Blok | Onderdeel | Aansluiting |
|---|---|---|
| Voeding | LiPo 2S 450 mAh → XT30 → SW1 (SS12D00) | VBAT 6,4–8,4 V |
| 3,3 V | CN3903-buck | ESP32, QTR-8A, TB6612-logica, encoders |
| Batterijmeting | 100 kΩ / 33 kΩ | GPIO9 |
| Sensor | QTR-8A | OUT1–8 → GPIO1–8, LEDON → GPIO11 |
| Motorsturing | TB6612FNG | PWMA/AIN1/AIN2 → 12/13/14, PWMB/BIN1/BIN2 → 15/16/17, STBY → 18 |
| Encoders | N20 Hall | links 39/40, rechts 41/42 |
| Bediening | start/stop-knop | GPIO21 (interne pull-up) |
| Status | ingebouwde RGB-led van de devkit | GPIO48 |

Dezelfde pinverdeling staat in [code/board.h](../../code/board.h).

## Bekabelingsplan lezen

![stap 8](bekabelingsplan_p04_stap08.png)

- Elk gat heeft een naam: **rij (letter) + kolom (nummer)**, bv. **T10**. De letters en nummers staan op alle 4 randen.
- Kolom 1 = achterkant, kolom 47 = voorkant. Rij A = robot links.
- De stappagina's tonen de **soldeerkant**, gespiegeld: rij A ligt daar onderaan. Zo zie je het als je de print omdraait rond de lange as.
- Nieuwe draden van de stap: dik, in kleur, met een nummer. Vorige stappen: grijs. Rood kader = onderdeel dat je in deze stap plaatst.
- Gestreept grijs = onderdelen aan de onderkant (motoren, beugels, caster): daar loopt geen draad.
- De draden lopen langs de gatenrijen en gaan nooit door een pin van een ander onderdeel. Liggen er meerdere draden in dezelfde rij, dan staan ze naast elkaar getekend (bundel).

Iets verplaatsen of een draad toevoegen? Pas `bekabeling_config.py` aan en draai `py -3 perfplan.py bekabeling_config.py`. Alle pagina's, de boormal en de draadlijst worden opnieuw gemaakt (±10 s).
