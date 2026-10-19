"""Bekabelingsplan linefollower (plan B, gaatjesprint 120 x 90 mm) - projectgegevens voor perfplan.py.

Maak het plan:  py -3 perfplan.py bekabeling_config.py
Gat (r, c): r = rij 0.. (A = robot LINKS in bovenaanzicht), c = kolom 0.. (kolom 1 = achterrand, 47 = voorrand).
Elk gat ligt 2,54 mm uit elkaar. Posities komen overeen met het 3D-model (mechanisch/model_linefollower.py),
afgerond op het raster.
"""

BOARD = dict(
    titel="Linefollower - gaatjesprint",
    prefix="bekabelingsplan",
    rijen=35, kolommen=47, pitch=2.54, voorkant="rechts",
    voettekst="HOGENT Elektromechanica - linefollower plan B - gemaakt met perfplan.py",
    plaatsing_uitleg="Kijk op de componentenkant. Kolom 1 = achterkant (batterij), kolom 47 = voorkant (sensor). "
                     "Rij A = robot links. Rood omcirkeld = pin 1 / referentiepin.",
    plaatsing_notities=[
        "Zaag de print eerst op 47 x 35 gaten (120 x 90 mm).",
        "Markeer met stift elke 5e rij en kolom: dan vind je\nelk gat snel terug.",
        "Oranje kruisen = boorgaten (beugels, caster, QTR, spoiler).",
        "Gestreept grijs = onderdelen aan de ONDERkant\n(motoren, beugels, caster): daar komen geen draden.",
        "Kabels van motoren en sensor komen van onderen:\nsteek de draadjes van onderen in hun gat.",
    ],
)

# ------------------------------------------------------------------ onderdelen
ESP_J1 = ["3V3", "3V3", "RST", "4", "5", "6", "7", "15", "16", "17", "18", "8", "3", "46", "9", "10",
          "11", "12", "13", "14", "5V", "GND"]
ESP_J3 = ["GND", "43", "44", "1", "2", "42", "41", "40", "39", "38", "37", "36", "35", "0", "45", "48",
          "47", "21", "20", "19", "GND", "GND"]
ESP_PINS, ESP_LAB, ESP_OFF = {}, {}, {}
for k in range(22):
    for rij, lijst, r, dy in (("J1", ESP_J1, 22, -0.95), ("J3", ESP_J3, 12, 0.95)):
        pin = f"{rij}-{k + 1}"
        ESP_PINS[pin] = (r, 22 + k)
        ESP_LAB[pin] = lijst[k] if not lijst[k].isdigit() else "IO" + lijst[k]
        ESP_OFF[pin] = (0, dy)


def gpio(n):
    """'9' -> 'ESP.J1-15'"""
    for rij, lijst in (("J1", ESP_J1), ("J3", ESP_J3)):
        if str(n) in lijst:
            return f"ESP.{rij}-{lijst.index(str(n)) + 1}"
    raise KeyError(n)


TB_LOGIC = ["PWMA", "AIN2", "AIN1", "STBY", "BIN1", "BIN2", "PWMB", "GND"]
TB_POWER = ["VM", "VCC", "GND2", "AO1", "AO2", "BO2", "BO1", "GND3"]
TB_PINS = {n: (19, 9 + i) for i, n in enumerate(TB_LOGIC)}
TB_PINS.update({n: (26, 9 + i) for i, n in enumerate(TB_POWER)})
TB_OFF = {n: (0, -0.95) for n in TB_LOGIC}
TB_OFF.update({n: (0, 0.95) for n in TB_POWER})
TB_LAB = {"GND2": "GND", "GND3": "GND"}

MOTOR = ["M1", "GND", "A", "B", "VCC", "M2"]
QTR = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "LEDON", "VCC", "GND"]

PARTS = [
    # stap 5 - voeding
    dict(naam="SW1", kort="SW1", label="SW1 aan/uit", stap=5, kleur="#1e88e5", omtrek=(0, 9.6, 0.4, 12.4),
         pins={"1": (0, 10), "2": (0, 11), "3": (0, 12)}, pinlabels={"1": "VBAT", "2": "BATT+", "3": "-"},
         pinlabel_offset=(0, 0.95), pin1="2", labelpos=(11, 1.9)),
    dict(naam="XT30", kort="XT30", label="XT30\npigtail", stap=5, kleur="#f9a825", omtrek=(3.6, 15.6, 6.4, 18.4),
         pins={"+": (4, 16), "-": (6, 16)}, pinlabels={"+": "+ rood", "-": "- zwart"}, pinlabel_offset=(1.6, 0),
         pin1="+", labelpos=(18.6, 5)),
    dict(naam="BUCK", kort="buck", label="CN3903\nbuck 3,3V", stap=5, kleur="#1565c0", omtrek=(9, 8, 15, 16),
         pins={"IN+": (9, 8), "IN-": (15, 8), "OUT+": (9, 16), "OUT-": (15, 16)}, pinlabel_offset=(0, 0.95),
         pin1="IN+"),
    dict(naam="R3", kort="R3", label="R3 330", stap=5, kleur="#8d6e63", omtrek=(2, 18, 2, 22),
         pins={"a": (2, 18), "b": (2, 22)}, pinlabels={"a": "", "b": ""}, labelpos=(20, 1.1)),
    dict(naam="D1", kort="D1", label="D1", stap=5, kleur="#43a047", omtrek=(2, 23, 2, 24),
         pins={"A": (2, 23), "K": (2, 24)}, pinlabels={"A": "+", "K": "-"}, labelpos=(23.5, 1.1), pin1="A"),
    # stap 6 - batterijmeting
    dict(naam="R1", kort="R1", label="R1 100k", stap=6, kleur="#8d6e63", omtrek=(25, 30, 25, 34),
         pins={"a": (25, 30), "b": (25, 34)}, pinlabels={"a": "", "b": ""}, labelpos=(32, 26.1)),
    dict(naam="R2", kort="R2", label="R2 33k", stap=6, kleur="#8d6e63", omtrek=(25, 35, 25, 39),
         pins={"a": (25, 35), "b": (25, 39)}, pinlabels={"a": "", "b": ""}, labelpos=(37, 26.1)),
    # stap 7 - ESP32
    dict(naam="ESP", kort="ESP", label="ESP32-S3 devkit (USB vooraan)", stap=7, kleur="#283593",
         omtrek=(11, 21, 23, 46), pins=ESP_PINS, pinlabels=ESP_LAB, pinlabel_offsets=ESP_OFF, pinlabel_rot=90,
         pin1="J1-1", labelpos=(34, 17)),
    dict(naam="C2", kort="C2", label="C2", stap=7, kleur="#3949ab", omtrek=(25, 22, 25, 23),
         pins={"+": (25, 22), "-": (25, 23)}, pinlabel_offset=(0, 0.95), pin1="+", labelpos=(22.5, 26.4)),
    # stap 8 - H-brug
    dict(naam="TB", kort="TB6612", label="TB6612FNG", stap=8, kleur="#e53935", omtrek=(19, 9, 26, 16),
         pins=TB_PINS, pinlabels=TB_LAB, pinlabel_offsets=TB_OFF, pinlabel_rot=90, pin1="PWMA",
         labelpos=(12.5, 22.5)),
    dict(naam="C1", kort="C1", label="C1", stap=8, kleur="#3949ab", omtrek=(29, 9, 29, 10),
         pins={"+": (29, 9), "-": (29, 10)}, pinlabel_offset=(0, 0.95), pin1="+", labelpos=(11.6, 29)),
    # stap 9 - motoren (aansluitpunten: kabel komt van onderen)
    dict(naam="ML", kort="motor L", label="kabel\nmotor L", stap=9, kleur="#6d4c41", omtrek=(13, 1, 13, 6),
         pins={n: (13, 1 + i) for i, n in enumerate(MOTOR)}, pinlabel_offset=(0, -0.95), pinlabel_rot=90,
         pin1="M1", labelpos=(3.5, 15.2)),
    dict(naam="MR", kort="motor R", label="kabel\nmotor R", stap=9, kleur="#6d4c41", omtrek=(21, 1, 21, 6),
         pins={n: (21, 1 + i) for i, n in enumerate(MOTOR)}, pinlabel_offset=(0, 0.95), pinlabel_rot=90,
         pin1="M1", labelpos=(3.5, 18.8)),
    # stap 10 - sensor (aansluitpunten: kabel van de QTR-8A)
    dict(naam="QTR", kort="QTR", label="kabel\nQTR-8A", stap=10, kleur="#c62828", omtrek=(24, 45, 34, 45),
         pins={n: (24 + i, 45) for i, n in enumerate(QTR)}, pinlabel_offset=(-1.3, 0), pin1="S1",
         labelpos=(43.2, 33.2)),
    # stap 11 - bediening
    dict(naam="KNOP", kort="knop", label="start/stop", stap=11, kleur="#fdd835", omtrek=(1, 31, 3, 33),
         pins={"1": (1, 31), "2": (3, 33)}, pinlabel_offset=(0, 0), pin1="1", labelpos=(32, 4.3)),
]

# Onderdelen aan de ONDERkant: hier geen draden (r0, c0, r1, c1, label)
KEEPOUTS = [
    (0, 2, 12, 7, "motor L"),
    (22, 2, 34, 7, "motor R"),
    (0, 0, 3, 9, ""),            # beugel links
    (31, 0, 34, 9, ""),          # beugel rechts
    (14, 36, 20, 40, "caster"),   # caster x=84 mm (onder de ESP32, bouten voor het solderen van de ESP)
]
# Boorgaten (r, c, diameter mm, label) - mogen tussen de rastergaten liggen
BOORGATEN = [
    (1.84, 1.86, 2.2, "beugel"), (1.84, 8.95, 2.2, "beugel"),
    (32.3, 1.86, 2.2, "beugel"), (32.3, 8.95, 2.2, "beugel"),
    (14.34, 38.5, 2.2, "caster"), (19.66, 38.5, 2.2, "caster"),
    (3.24, 42.75, 2.2, "QTR"), (30.76, 42.75, 2.2, "QTR"),
    (3.6, 0.68, 3.2, "spoiler"), (30.4, 0.68, 3.2, "spoiler"),
]

# ------------------------------------------------------------------ draden
# (nr, stap, van, naar, soort, opmerking)
WIRES = [
    (1, 5, "XT30.+", "SW1.2", "BATT+", "rode draad pigtail"),
    (2, 5, "XT30.-", "BUCK.IN-", "GND", "zwarte draad pigtail = GND-sterpunt"),
    (3, 5, "SW1.1", "BUCK.IN+", "VBAT", ""),
    (4, 5, "BUCK.OUT+", "R3.a", "3V3", ""),
    (5, 5, "R3.b", "D1.A", "BRUG", "soldeerbrug: poot R3 tegen + led"),
    (6, 5, "D1.K", "BUCK.OUT-", "GND", "korte poot led = -"),
    (7, 6, "BUCK.IN+", "R1.a", "VBAT", ""),
    (8, 6, "R1.b", "R2.a", "BRUG", "soldeerbrug = meetpunt"),
    (9, 6, "R2.b", "BUCK.IN-", "GND", ""),
    (10, 7, "BUCK.OUT+", "ESP.J1-1", "3V3", "devkit via 3V3-pin voeden"),
    (11, 7, "BUCK.OUT-", "ESP.J3-1", "GND", ""),
    (12, 7, "R1.b", gpio("9"), "SENS", "meetpunt -> GPIO9"),
    (13, 7, "ESP.J1-1", "C2.+", "3V3", "C2: streep op elco = -"),
    (14, 7, "C2.-", "ESP.J3-1", "GND", ""),
    (15, 8, "BUCK.IN+", "TB.VM", "VBAT", "motorvoeding"),
    (16, 8, "BUCK.IN-", "TB.GND2", "GND", "motorstroom terug"),
    (17, 8, "TB.VM", "C1.+", "VBAT", "C1 vlak bij VM"),
    (18, 8, "C1.-", "TB.GND2", "GND", ""),
    (19, 8, "ESP.J1-2", "TB.VCC", "3V3", "logica TB6612"),
    (20, 8, "TB.GND", "BUCK.OUT-", "GND", ""),
    (21, 8, "TB.PWMA", gpio("12"), "PWM", ""),
    (22, 8, "TB.AIN1", gpio("13"), "DIR", ""),
    (23, 8, "TB.AIN2", gpio("14"), "DIR", ""),
    (24, 8, "TB.PWMB", gpio("15"), "PWM", ""),
    (25, 8, "TB.BIN1", gpio("16"), "DIR", ""),
    (26, 8, "TB.BIN2", gpio("17"), "DIR", ""),
    (27, 8, "TB.STBY", gpio("18"), "DIR", "laag = motoren uit"),
    (28, 9, "ML.M1", "TB.AO1", "MOTOR", ""),
    (29, 9, "ML.M2", "TB.AO2", "MOTOR", ""),
    (30, 9, "MR.M1", "TB.BO1", "MOTOR", ""),
    (31, 9, "MR.M2", "TB.BO2", "MOTOR", ""),
    (32, 9, "ML.A", gpio("39"), "ENC", ""),
    (33, 9, "ML.B", gpio("40"), "ENC", ""),
    (34, 9, "MR.A", gpio("41"), "ENC", ""),
    (35, 9, "MR.B", gpio("42"), "ENC", ""),
    (36, 9, "ML.VCC", "BUCK.OUT+", "3V3", "encoder L"),
    (37, 9, "ML.GND", "BUCK.OUT-", "GND", "encoder L"),
    (38, 9, "MR.VCC", "ML.VCC", "3V3", "encoder R"),
    (39, 9, "MR.GND", "ML.GND", "GND", "encoder R"),
    (40, 10, "QTR.S1", gpio("1"), "SENS", ""),
    (41, 10, "QTR.S2", gpio("2"), "SENS", ""),
    (42, 10, "QTR.S3", gpio("3"), "SENS", ""),
    (43, 10, "QTR.S4", gpio("4"), "SENS", ""),
    (44, 10, "QTR.S5", gpio("5"), "SENS", ""),
    (45, 10, "QTR.S6", gpio("6"), "SENS", ""),
    (46, 10, "QTR.S7", gpio("7"), "SENS", ""),
    (47, 10, "QTR.S8", gpio("8"), "SENS", ""),
    (48, 10, "QTR.LEDON", gpio("11"), "SENS", ""),
    (49, 10, "QTR.VCC", "ESP.J1-2", "3V3", ""),
    (50, 10, "QTR.GND", "ESP.J1-22", "GND", ""),
    (51, 11, "KNOP.1", gpio("21"), "BEDIENING", "schuine pootjes = altijd geschakeld"),
    (52, 11, "KNOP.2", "ESP.J3-22", "GND", ""),
]

KLEUREN = {  # soort -> (kleur op tekening, draadkleur)
    "BATT+": ("#d32f2f", "rood"), "VBAT": ("#ff5252", "rood"), "3V3": ("#ef6c00", "oranje"),
    "GND": ("#212121", "zwart"), "PWM": ("#f9a825", "geel"), "DIR": ("#2e7d32", "groen"),
    "MOTOR": ("#795548", "bruin"), "ENC": ("#1565c0", "blauw"), "SENS": ("#8e24aa", "paars/wit"),
    "BEDIENING": ("#00838f", "grijs"), "BRUG": ("#757575", "soldeer/blank draadje"),
}

# stap -> (titel, uitleg, notities)  - nummers = instructable/readme.md
STAPPEN = {
    5: ("voeding", "XT30-pigtail, aan/uit-schakelaar SW1, buck 3,3 V, power-led. Nog GEEN ESP32, TB6612 of motoren.",
        ["Meet daarna: buck OUT+ -> GND = 3,25-3,35 V.", "SW1 uit = 0 V op VBAT.", "Led-poot lang = +."]),
    6: ("batterijmeting", "Spanningsdeler R1/R2: 8,4 V wordt 2,08 V op het meetpunt.",
        ["Meet: meetpunt -> GND = VBAT x 33/133."]),
    7: ("ESP32-S3 devkit", "Devkit met de USB-poorten naar VOOR (kolom 47). Pin J1-1 (3V3) in gat W23.",
        ["Eerst doorgangstest 3V3 <-> GND: geen kortsluiting.",
         "Test met enkel USB: poc_interrupt -> rode led."]),
    8: ("H-brug TB6612FNG", "Module met de stuurpinnen (PWMA ... GND) naar het midden (rij T).",
        ["Pinvolgorde volgens de OPDRUK van jouw module.", "Test: 1 motor los aan AO1/AO2 + poc_hbridge."]),
    9: ("motoren en encoders", "De 6-draadskabels komen van onderen. Steek elk draadje van onderen in zijn gat.",
        ["Volgorde op het motorprintje controleren\n(M1, GND, A, B, VCC, M2).",
         "100 nF over M1/M2 op het motorprintje.",
         "Knip de pootjes boven af: de batterij komt erover."]),
    10: ("sensor QTR-8A", "11 draadjes van de QTR (onder de voorrand) naar de aansluitpunten in kolom 46.",
         ["Jumper 3.3V BYPASS op de QTR dicht.", "Sensor 1 = robot links."]),
    11: ("start/stop-knop", "Drukknop aan de linkerrand, schuine pootjes gebruiken.",
         ["Test: poc_interrupt, rood <-> groen."]),
}
