"""Maten van de plan A-print (mm). Gebruikt door bouw_pcb.py (KiCad) en maattekening.py (tekening).

Assen: x = 0 is de linkerrand, y = 0 is de VOORKANT (sensoren), y = LANG is de achterkant.
De print is het chassis: motoren, caster en spoiler worden rechtstreeks op de print geschroefd.
"""
BREED, LANG = 100.0, 130.0
HOEK_R = 3.0                     # afgeronde hoeken

# Uitsparingen voor de wielen: zo blijft de robot 100 mm breed (chronobrug: 120 mm)
WIEL_UIT = dict(diepte=11.0, y0=86.0, y1=122.0)   # wiel 32 x 7 mm + speling
AS_Y = 104.0                     # wielas
SENSOR_Y = 5.0                   # sensorlijn -> 99 mm voor de wielas (zoals plan B)
SENSOR_STEEK = 9.5               # zoals de QTR-8A

# Boorgaten: (x, y, diameter, waarvoor)
GATEN = [
    (16.5, AS_Y - 9.0, 2.2, "motorbeugel L"), (16.5, AS_Y + 9.0, 2.2, "motorbeugel L"),
    (83.5, AS_Y - 9.0, 2.2, "motorbeugel R"), (83.5, AS_Y + 9.0, 2.2, "motorbeugel R"),
    (50 - 6.75, 30.0, 2.2, "ball caster"), (50 + 6.75, 30.0, 2.2, "ball caster"),
    (6.0, 126.0, 3.2, "spoiler"), (94.0, 126.0, 3.2, "spoiler"),
]


def omtrek():
    """Hoekpunten van de omtrek (met de klok mee), zonder de afrondingen."""
    d, y0, y1 = WIEL_UIT["diepte"], WIEL_UIT["y0"], WIEL_UIT["y1"]
    return [(0, 0), (BREED, 0), (BREED, y0), (BREED - d, y0), (BREED - d, y1), (BREED, y1), (BREED, LANG),
            (0, LANG), (0, y1), (d, y1), (d, y0), (0, y0)]
