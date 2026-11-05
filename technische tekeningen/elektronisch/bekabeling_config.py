"""Bekabelingsplan linefollower (plan B, gaatjesprint 120 x 90 mm, 47 x 33 gaten) - projectgegevens voor perfplan.py.

Maak het plan:  py -3 perfplan.py bekabeling_config.py
Gat (r, c): r = rij 0.. (A = robot LINKS in bovenaanzicht), c = kolom 0.. (kolom 1 = achterrand, 47 = voorrand).
Elk gat ligt 2,54 mm uit elkaar. Posities komen overeen met het 3D-model (mechanisch/model_linefollower.py),
afgerond op het raster.
"""

BOARD = dict(
    titel="Linefollower - gaatjesprint",
    prefix="bekabelingsplan",
    rijen=33, kolommen=47, pitch=2.54, voorkant="rechts",
    voettekst="HOGENT Elektromechanica - linefollower plan B - gemaakt met perfplan.py",
    plaatsing_uitleg="Kijk op de componentenkant. Kolom 1 = achterkant (batterij), kolom 47 = voorkant (sensor). "
                     "Rij A = robot links. Rood omcirkeld = pin 1 / referentiepin.",
    plaatsing_notities=[
        "Zaag de print in de lengte op 47 gaten (breedte 90 mm\nblijft: 33 gaten). Rij A = eerste gatenrij links.",
        "Markeer met stift elke 5e rij en kolom: dan vind je\nelk gat snel terug.",
        "Oranje kruisen = boorgaten (beugels, caster, QTR, spoiler).",
        "Gestreept grijs = onderdelen aan de ONDERkant\n(motoren, beugels, caster): daar komen geen draden.",
        "Rood gekruist = uitsparing: wegsnijden (doorvoer encoderkabels).",
        "Motorkabels komen door de uitsparing naar boven; de\nQTR-kabel komt van onderen in zijn gat.",
    ],
)

# ------------------------------------------------------------------ onderdelen
ESP_J1 = ["3V3", "3V3", "RST", "4", "5", "6", "7", "15", "16", "17", "18", "8", "3", "46", "9", "10",
          "11", "12", "13", "14", "5V", "GND"]
ESP_J3 = ["GND", "43", "44", "1", "2", "42", "41", "40", "39", "38", "37", "36", "35", "0", "45", "48",
          "47", "21", "20", "19", "GND", "GND"]
ESP_PINS, ESP_LAB, ESP_OFF = {}, {}, {}
for k in range(22):
    for rij, lijst, r, dy in (("J1", ESP_J1, 21, -0.95), ("J3", ESP_J3, 11, 0.95)):
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
TB_PINS = {n: (18, 9 + i) for i, n in enumerate(TB_LOGIC)}
TB_PINS.update({n: (25, 9 + i) for i, n in enumerate(TB_POWER)})
TB_OFF = {n: (0, -0.95) for n in TB_LOGIC}
TB_OFF.update({n: (0, 0.95) for n in TB_POWER})
TB_LAB = {"GND2": "GND", "GND3": "GND"}

MOTOR = ["M1", "GND", "A", "B", "VCC", "M2"]
QTR = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "LEDON", "VCC", "GND"]

PARTS = [
    # stap 5 - voeding
    dict(naam="SW1", kort="SW1", label="SW1 aan/uit", stap=5, kleur="#1e88e5", omtrek=(0, 10.6, 0.4, 13.4),
         pins={"1": (0, 11), "2": (0, 12), "3": (0, 13)}, pinlabels={"1": "VBAT", "2": "BATT+", "3": "-"},
         pinlabel_offset=(0, 0.95), pin1="2", labelpos=(12, 1.9)),
    dict(naam="XT30", kort="XT30", label="XT30\npigtail", stap=5, kleur="#f9a825", omtrek=(2.6, 15.6, 5.4, 18.4),
         pins={"+": (3, 16), "-": (5, 16)}, pinlabels={"+": "+ rood", "-": "- zwart"}, pinlabel_offset=(1.6, 0),
         pin1="+", labelpos=(18.6, 4)),
    dict(naam="BUCK", kort="buck", label="CN3903\nbuck 3,3V", stap=5, kleur="#1565c0", omtrek=(8, 8, 14, 16),
         pins={"IN+": (8, 8), "IN-": (14, 8), "OUT+": (8, 16), "OUT-": (14, 16)}, pinlabel_offset=(0, 0.95),
         pin1="IN+"),
    dict(naam="R3", kort="R3", label="R3 330", stap=5, kleur="#8d6e63", omtrek=(1, 18, 1, 22),
         pins={"a": (1, 18), "b": (1, 22)}, pinlabels={"a": "", "b": ""}, labelpos=(20, 0.1)),
    dict(naam="D1", kort="D1", label="D1", stap=5, kleur="#43a047", omtrek=(1, 23, 1, 24),
         pins={"A": (1, 23), "K": (1, 24)}, pinlabels={"A": "+", "K": "-"}, labelpos=(23.5, 0.1), pin1="A"),
    # stap 6 - batterijmeting
    dict(naam="R1", kort="R1", label="R1 100k", stap=6, kleur="#8d6e63", omtrek=(24, 30, 24, 34),
         pins={"a": (24, 30), "b": (24, 34)}, pinlabels={"a": "", "b": ""}, labelpos=(32, 25.1)),
    dict(naam="R2", kort="R2", label="R2 33k", stap=6, kleur="#8d6e63", omtrek=(24, 35, 24, 39),
         pins={"a": (24, 35), "b": (24, 39)}, pinlabels={"a": "", "b": ""}, labelpos=(37, 25.1)),
    # stap 7 - ESP32
    dict(naam="ESP", kort="ESP", label="ESP32-S3 devkit (USB vooraan)", stap=7, kleur="#283593",
         omtrek=(10, 21, 22, 46), pins=ESP_PINS, pinlabels=ESP_LAB, pinlabel_offsets=ESP_OFF, pinlabel_rot=90,
         pin1="J1-1", labelpos=(34, 16)),
    dict(naam="C2", kort="C2", label="C2", stap=7, kleur="#3949ab", omtrek=(24, 22, 24, 23),
         pins={"+": (24, 22), "-": (24, 23)}, pinlabel_offset=(0, 0.95), pin1="+", labelpos=(22.5, 25.4)),
    # stap 8 - H-brug
    dict(naam="TB", kort="TB6612", label="TB6612FNG", stap=8, kleur="#e53935", omtrek=(18, 9, 25, 16),
         pins=TB_PINS, pinlabels=TB_LAB, pinlabel_offsets=TB_OFF, pinlabel_rot=90, pin1="PWMA",
         labelpos=(12.5, 21.5)),
    dict(naam="C1", kort="C1", label="C1", stap=8, kleur="#3949ab", omtrek=(28, 9, 28, 10),
         pins={"+": (28, 9), "-": (28, 10)}, pinlabel_offset=(0, 0.95), pin1="+", labelpos=(11.6, 28)),
    # stap 9 - motoren (aansluitpunten: kabel komt van onderen)
    dict(naam="ML", kort="motor L", label="kabel\nmotor L", stap=9, kleur="#6d4c41", omtrek=(14, 1, 14, 6),
         pins={n: (14, 1 + i) for i, n in enumerate(MOTOR)}, pinlabel_offset=(0, 0.95), pinlabel_rot=90,
         pin1="M1", labelpos=(4.5, 9.5)),
    dict(naam="MR", kort="motor R", label="kabel\nmotor R", stap=9, kleur="#6d4c41", omtrek=(18, 1, 18, 6),
         pins={n: (18, 1 + i) for i, n in enumerate(MOTOR)}, pinlabel_offset=(0, -0.95), pinlabel_rot=90,
         pin1="M1", labelpos=(4.5, 23.5)),
    # stap 10 - sensor (aansluitpunten: kabel van de QTR-8A)
    dict(naam="QTR", kort="QTR", label="kabel\nQTR-8A", stap=10, kleur="#c62828", omtrek=(22, 45, 32, 45),
         pins={n: (22 + i, 45) for i, n in enumerate(QTR)}, pinlabel_offset=(-1.3, 0), pin1="S1",
         labelpos=(43.2, 31.2)),
    # stap 11 - bediening
    dict(naam="KNOP", kort="knop", label="start/stop", stap=11, kleur="#fdd835", omtrek=(0, 31, 2, 33),
         pins={"1": (0, 31), "2": (2, 33)}, pinlabel_offset=(0, 0), pin1="1", labelpos=(32, 3.3)),
]

# Onderdelen aan de ONDERkant: hier geen draden (r0, c0, r1, c1, label)
KEEPOUTS = [
    (0, 2, 11, 7, "motor L"),
    (21, 2, 32, 7, "motor R"),
    (0, 0, 2, 9, ""),            # beugel links
    (30, 0, 32, 9, ""),          # beugel rechts
    (13, 36, 19, 40, "caster"),   # caster x=84 mm (onder de ESP32, bouten voor het solderen van de ESP)
]
# Uitsparingen (r0, c0, r1, c1, label, labelrij): wegsnijden. Encoderkabel N20 (achterkant motor, binnenkant)
# gaat hier recht naar boven i.p.v. onder de motor door (hangt anders tegen de grond).
UITSPARINGEN = [
    (12, 2, 13, 5, "uitsparing", 11.1),
    (19, 2, 20, 5, "uitsparing", 21.9),
]

# Boorgaten (r, c, diameter mm, label) - mogen tussen de rastergaten liggen
BOORGATEN = [
    (0.84, 1.86, 2.2, "beugel"), (0.84, 8.95, 2.2, "beugel"),
    (31.3, 1.86, 2.2, "beugel"), (31.3, 8.95, 2.2, "beugel"),
    (13.34, 38.5, 2.2, "caster"), (18.66, 38.5, 2.2, "caster"),
    (2.24, 42.75, 2.2, "QTR"), (29.76, 42.75, 2.2, "QTR"),
    (2.6, 0.68, 3.2, "spoiler"), (29.4, 0.68, 3.2, "spoiler"),
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
    7: ("ESP32-S3 devkit", "Devkit met de USB-poorten naar VOOR (kolom 47). Pin J1-1 (3V3) in gat V23.",
        ["Eerst doorgangstest 3V3 <-> GND: geen kortsluiting.",
         "Test met enkel USB: poc_interrupt -> rode led."]),
    8: ("H-brug TB6612FNG", "Module met de stuurpinnen (PWMA ... GND) naar het midden (rij S).",
        ["Pinvolgorde volgens de OPDRUK van jouw module.", "Test: 1 motor los aan AO1/AO2 + poc_hbridge."]),
    9: ("motoren en encoders", "De 6-draadskabels gaan door de uitsparing achter de encoder naar boven. Steek elk draadje van boven in zijn gat.",
        ["Volgorde op het motorprintje controleren\n(M1, GND, A, B, VCC, M2).",
         "100 nF over M1/M2 op het motorprintje.",
         "Knip de pootjes boven af: de batterij komt erover."]),
    10: ("sensor QTR-8A", "11 draadjes van de QTR (onder de voorrand) naar de aansluitpunten in kolom 46.",
         ["Jumper 3.3V BYPASS op de QTR dicht.", "Sensor 1 = robot links."]),
    11: ("start/stop-knop", "Drukknop aan de linkerrand, schuine pootjes gebruiken.",
         ["Test: poc_interrupt, rood <-> groen."]),
}
