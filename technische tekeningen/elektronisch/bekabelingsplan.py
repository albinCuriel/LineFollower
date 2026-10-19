"""Bekabelingsplan gaatjesprint: tekening (boven- en onderzijde) + draadlijst in markdown.

Eén bron voor tekening en tabel: de lijsten PINNEN en DRADEN hieronder.
Posities = dezelfde als het 3D-model (mechanisch/model_linefollower.py), in mm.
Assen: X = vooruit, Y = links. Oorsprong: midden wielas.
Gebruik:  py -3 bekabelingsplan.py  ->  bekabelingsplan.png / .pdf + draadlijst.md
"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

HIER = pathlib.Path(__file__).parent
P = 2.54
PRINT = (-15.0, 105.0, -45.0, 45.0)          # x_min, x_max, y_min, y_max (ingekort tot 120 mm)

# ---------------------------------------------------------------- pinnen ESP32-S3 devkit (bovenaanzicht, USB vooraan)
# Volgorde = Espressif DevKitC-1 (J1 / J3). Pin 1 ligt achteraan (kant van de antenne).
J1 = ["3V3", "3V3", "RST", "4", "5", "6", "7", "15", "16", "17", "18", "8", "3", "46", "9", "10",
      "11", "12", "13", "14", "5V", "GND"]
J3 = ["GND", "43", "44", "1", "2", "42", "41", "40", "39", "38", "37", "36", "35", "0", "45", "48",
      "47", "21", "20", "19", "GND", "GND"]
X_ESP, RIJ = 39.5, 12.7


def esp(naam, rij="J1"):
    lijst = J1 if rij == "J1" else J3
    k = lijst.index(naam)
    return (X_ESP + 2.55 + P * k, -RIJ if rij == "J1" else RIJ)


TB_LOGIC = ["PWMA", "AIN2", "AIN1", "STBY", "BIN1", "BIN2", "PWMB", "GND"]   # rij naar het midden
TB_POWER = ["VM", "VCC", "GND", "AO1", "AO2", "BO2", "BO1", "GND"]           # rij naar de buitenrand
X_TB = 8.0


def tb(naam, rij="logic"):
    lijst = TB_LOGIC if rij == "logic" else TB_POWER
    return (X_TB + 1.27 + P * lijst.index(naam), -5.3 if rij == "logic" else -23.0)


PUNT = {  # vaste soldeerpunten (mm)
    "XT30+": (21.0, 33.5), "XT30-": (21.0, 28.5),
    "SW1.1": (11.6, 43.0), "SW1.2": (14.1, 43.0), "SW1.3": (16.6, 43.0),
    "BUCK_IN+": (9.5, 19.5), "BUCK_IN-": (9.5, 5.5), "BUCK_OUT+": (28.5, 19.5), "BUCK_OUT-": (28.5, 5.5),
    "R3": (24.5, 38.0), "D1": (29.6, 38.0),
    "R1": (77.6, -20.3), "R2": (77.6, -27.9), "C1+": (34.6, -30.0), "C1-": (32.0, -30.0),
    "C2+": (37.0, -17.7), "C2-": (37.0, -20.3),
    "KNOP.1": (60.5, 39.5), "KNOP.2": (65.5, 39.5),
    "GAT_MOTOR_L": (5.5, 8.0), "GAT_MOTOR_R": (5.5, -8.0),
    "QTR": (96.0, 0.0),
}
for i in range(8):  # QTR-uitgangen: sensor 1 = links (+Y)
    PUNT[f"QTR.{i + 1}"] = (96.0, 30.0 - i * 6.0)
PUNT["QTR.LEDON"], PUNT["QTR.VCC"], PUNT["QTR.GND"] = (99.5, -20.0), (99.5, -26.0), (99.5, -32.0)

KLEUR = {"BATT+": "#d32f2f", "VBAT": "#d32f2f", "3V3": "#ef6c00", "GND": "#212121",
         "PWM": "#fbc02d", "DIR": "#2e7d32", "MOTOR": "#6d4c41", "ENC": "#1565c0",
         "SENS": "#7b1fa2", "BEDIENING": "#00838f"}

# nr, stap, van, naar, net, soort, opmerking
DRADEN = [
    # stap 3: voeding
    (1, 3, "XT30+", "SW1.2", "BATT+", "BATT+", "rode draad van de pigtail (20AWG)"),
    (2, 3, "XT30-", "BUCK_IN-", "GND", "GND", "zwarte draad pigtail = GND-sterpunt"),
    (3, 3, "SW1.1", "BUCK_IN+", "VBAT", "VBAT", ""),
    (4, 3, "BUCK_IN+", tb("VM", "power"), "VBAT", "VBAT", "dik draadje (24AWG of dikker)"),
    (5, 3, "BUCK_IN-", tb("GND", "power"), "GND", "GND", "motorstroom terug"),
    (6, 3, "BUCK_OUT+", esp("3V3"), "3V3", "3V3", "devkit gevoed via 3V3-pin, NIET via USB-5V"),
    (7, 3, "BUCK_OUT-", esp("GND", "J3"), "GND", "GND", ""),
    (8, 3, esp("3V3"), "C2+", "3V3", "3V3", "C2 100 uF, + naar 3V3"),
    (9, 3, esp("GND", "J3"), "C2-", "GND", "GND", ""),
    (10, 3, tb("VM", "power"), "C1+", "VBAT", "VBAT", "C1 100 uF vlak bij VM"),
    (11, 3, tb("GND", "power"), "C1-", "GND", "GND", ""),
    (12, 3, "BUCK_OUT+", "R3", "3V3", "3V3", "R3 330 ohm -> power-led D1 -> GND"),
    (13, 3, "D1", "BUCK_IN-", "GND", "GND", "kathode (korte poot) naar GND"),
    (14, 4, "SW1.1", "R1", "VBAT", "VBAT", "R1 100k van VBAT naar meetpunt"),
    (15, 4, "R1", esp("9"), "VBAT_SENSE", "SENS", "meetpunt R1/R2 -> GPIO9"),
    (16, 4, "R2", esp("GND"), "GND", "GND", "R2 33k van meetpunt naar GND"),
    # stap 6: H-brug
    (17, 6, esp("3V3"), tb("VCC", "power"), "3V3", "3V3", "logische voeding TB6612"),
    (18, 6, tb("GND", "logic"), esp("GND"), "GND", "GND", ""),
    (19, 6, tb("PWMA"), esp("12"), "PWMA", "PWM", "motor links snelheid"),
    (20, 6, tb("AIN1"), esp("13"), "AIN1", "DIR", ""),
    (21, 6, tb("AIN2"), esp("14"), "AIN2", "DIR", ""),
    (22, 6, tb("PWMB"), esp("15"), "PWMB", "PWM", "motor rechts snelheid"),
    (23, 6, tb("BIN1"), esp("16"), "BIN1", "DIR", ""),
    (24, 6, tb("BIN2"), esp("17"), "BIN2", "DIR", ""),
    (25, 6, tb("STBY"), esp("18"), "STBY", "DIR", "laag = motoren uit"),
    # stap 7: motoren
    (26, 7, "GAT_MOTOR_L", tb("AO1", "power"), "MOT_L+", "MOTOR", "motor links M1 (+100 nF over de motorklemmen)"),
    (27, 7, "GAT_MOTOR_L", tb("AO2", "power"), "MOT_L-", "MOTOR", "motor links M2"),
    (28, 7, "GAT_MOTOR_R", tb("BO1", "power"), "MOT_R+", "MOTOR", "motor rechts M1 (+100 nF)"),
    (29, 7, "GAT_MOTOR_R", tb("BO2", "power"), "MOT_R-", "MOTOR", "motor rechts M2"),
    (30, 7, "GAT_MOTOR_L", esp("39", "J3"), "ENC_L_A", "ENC", "encoder links A"),
    (31, 7, "GAT_MOTOR_L", esp("40", "J3"), "ENC_L_B", "ENC", "encoder links B"),
    (32, 7, "GAT_MOTOR_R", esp("41", "J3"), "ENC_R_A", "ENC", "encoder rechts A"),
    (33, 7, "GAT_MOTOR_R", esp("42", "J3"), "ENC_R_B", "ENC", "encoder rechts B"),
    (34, 7, "GAT_MOTOR_L", "BUCK_OUT+", "3V3", "3V3", "encoder VCC links + rechts samen"),
    (35, 7, "GAT_MOTOR_L", "BUCK_OUT-", "GND", "GND", "encoder GND links + rechts samen"),
    # stap 8: sensor
    (36, 8, "QTR.1", esp("1", "J3"), "S1", "SENS", "sensor 1 = uiterst links"),
    (37, 8, "QTR.2", esp("2", "J3"), "S2", "SENS", ""),
    (38, 8, "QTR.3", esp("3"), "S3", "SENS", ""),
    (39, 8, "QTR.4", esp("4"), "S4", "SENS", ""),
    (40, 8, "QTR.5", esp("5"), "S5", "SENS", ""),
    (41, 8, "QTR.6", esp("6"), "S6", "SENS", ""),
    (42, 8, "QTR.7", esp("7"), "S7", "SENS", ""),
    (43, 8, "QTR.8", esp("8"), "S8", "SENS", "sensor 8 = uiterst rechts"),
    (44, 8, "QTR.LEDON", esp("11"), "LEDON", "SENS", "IR-leds aan/uit"),
    (45, 8, "QTR.VCC", esp("3V3"), "3V3", "3V3", "jumper 3.3V BYPASS op de QTR dicht!"),
    (46, 8, "QTR.GND", esp("GND"), "GND", "GND", ""),
    # stap 9: bediening
    (47, 9, "KNOP.1", esp("21", "J3"), "BTN", "BEDIENING", "start/stop, interne pull-up"),
    (48, 9, "KNOP.2", esp("GND", "J3"), "GND", "GND", ""),
]


def pos(p):
    return PUNT[p] if isinstance(p, str) else p


def naam(p):
    if isinstance(p, str):
        return p.replace("_", " ")
    for rij, lijst in (("J1", J1), ("J3", J3)):
        for k, n in enumerate(lijst):
            if esp(n, rij) == p:
                return f"ESP {rij}-{k + 1} ({'GPIO' + n if n.isdigit() else n})"
    for rij, lijst in (("logic", TB_LOGIC), ("power", TB_POWER)):
        for n in lijst:
            if tb(n, rij) == p:
                return f"TB6612 {n}"
    return str(p)


def teken(ax, onderzijde):
    """onderzijde=True: gespiegeld (zoals je de print omgedraaid in je hand houdt)."""
    sy = -1 if onderzijde else 1
    rect = lambda x, y, w, h, **kw: ax.add_patch(Rectangle((x, sy * y if sy > 0 else -(y + h)), w, h, **kw))
    x0, x1, y0, y1 = PRINT
    rect(x0, y0, x1 - x0, y1 - y0, fc="#e8f5e9", ec="#2e7d32", lw=1.5)
    # gaatjesraster
    import numpy as np
    gx = np.arange(x0 + 2.0, x1 - 1, P); gy = np.arange(y0 + 2.0, y1 - 1, P)
    X, Y = np.meshgrid(gx, gy)
    ax.plot(X.ravel(), (sy * Y).ravel(), ".", ms=0.8, color="#a5d6a7", zorder=1)
    stijl_top = dict(fill=False, lw=1.2, zorder=3) if onderzijde else dict(alpha=0.85, lw=1, zorder=3)
    stijl_bot = dict(alpha=0.6, lw=1, zorder=2) if onderzijde else dict(fill=False, ls="--", lw=1, zorder=2)
    # bovenzijde-onderdelen
    for (x, y, w, h, kl, label) in [
        (-14, -30, 17, 60, "#616161", "LiPo 2S\n(dwars, klittenband)"),
        (7, 27, 16, 8, "#f9a825", "XT30"),
        (8, 4, 22, 17, "#1565c0", "buck 3,3V"),
        (8, -24.3, 20.3, 20.3, "#e53935", "TB6612"),
        (X_ESP, -14, 63.5, 28, "#283593", "ESP32-S3 devkit\n(USB vooraan)"),
        (10, 41.4, 8.6, 3.6, "#1e88e5", "SW1"),
        (59.5, 37, 6, 6, "#fdd835", "start"),
    ]:
        rect(x, y, w, h, ec=kl, fc=kl if not onderzijde else "none", **({k: v for k, v in stijl_top.items() if k != "fill"} if not onderzijde else stijl_top))
        ax.text(x + w / 2, sy * (y + h / 2), label, ha="center", va="center", fontsize=6.5,
                color="white" if not onderzijde and kl not in ("#f9a825", "#fdd835") else "#333", zorder=6)
    # onderzijde-onderdelen
    for (x, y, w, h, kl, label) in [
        (-6, 10, 12, 33, "#90a4ae", "motor L"), (-6, -43, 12, 33, "#90a4ae", "motor R"),
        (92.35, -37.45, 12.7, 74.9, "#c62828", "QTR-8A (sensoren naar beneden)"),
        (27.95, -9.55, 12.1, 19.1, "#616161", "caster"),
    ]:
        rect(x, y, w, h, ec=kl, fc=kl if onderzijde else "none", **({k: v for k, v in stijl_bot.items() if k != "fill"} if onderzijde else stijl_bot))
        ax.text(x + w / 2, sy * (y + h / 2), label, ha="center", va="center", fontsize=6.5,
                rotation=90 if h > 30 else 0, color="#333", zorder=6)
    # boorgaten M2 (2,2 mm) en kabelgaten (5 mm)
    gaten = [(-9, 38.5), (9, 38.5), (-9, -38.5), (9, -38.5), (34.0, 6.75), (34.0, -6.75), (94.85, 34.95), (94.85, -34.95)]
    for (x, y) in gaten:
        ax.add_patch(Circle((x, sy * y), 1.6, fc="white", ec="k", lw=1, zorder=7))
    rect(-15, -43, 25, 86, fill=False, ec="#ff6f00", ls="-.", lw=1.2, zorder=4)   # spoiler 20 mm boven de print
    ax.text(-2.5, sy * 41, "spoiler (omtrek)", fontsize=5.5, color="#e65100", ha="center", zorder=6)
    for (x, y) in [(-12, 34), (-12, -34)]:   # M3 spoiler: 3,2 mm
        ax.add_patch(Circle((x, sy * y), 1.8, fc="white", ec="#ff6f00", lw=1.2, zorder=7))
    for k in ("GAT_MOTOR_L", "GAT_MOTOR_R"):
        x, y = PUNT[k]
        ax.add_patch(Circle((x, sy * y), 2.5, fc="white", ec="#6d4c41", lw=1.2, zorder=7))
    # ESP-pinnen
    for rij, lijst in (("J1", J1), ("J3", J3)):
        for n in lijst:
            x, y = esp(n, rij)
            ax.plot(x, sy * y, "s", ms=2.6, color="#ffd54f", mec="k", mew=0.3, zorder=8)
            ax.text(x, sy * y + (2.2 if (y > 0) == (sy > 0) else -2.2), n, fontsize=4.2, ha="center",
                    va="center", rotation=90, zorder=8)
    for rij, lijst in (("logic", TB_LOGIC), ("power", TB_POWER)):
        for n in lijst:
            x, y = tb(n, rij)
            ax.plot(x, sy * y, "s", ms=2.4, color="#ffd54f", mec="k", mew=0.3, zorder=8)
            ax.text(x, sy * y + (-2.0 if rij == "logic" else 2.0) * sy, n, fontsize=4, ha="center",
                    va="center", rotation=90, zorder=8)
    if onderzijde:
        for nr, stap, a, b, net, soort, _ in DRADEN:
            (xa, ya), (xb, yb) = pos(a), pos(b)
            kl = KLEUR[soort]
            ax.plot([xa, xb, xb], [sy * ya, sy * ya, sy * yb], color=kl, lw=1.1, zorder=5, alpha=0.9,
                    solid_capstyle="round")
            ax.text(xb, sy * (ya + yb) / 2, str(nr), fontsize=5, color=kl, ha="center", va="center",
                    zorder=9, bbox=dict(fc="white", ec="none", pad=0.15))
    ax.annotate("", xy=(x1 + 9, 0), xytext=(x1 + 1, 0), arrowprops=dict(arrowstyle="-|>", lw=1.5))
    ax.text(x1 + 5, 3, "rijrichting", fontsize=7, ha="center")
    ax.axis("off")
    links = "links" if not onderzijde else "rechts"
    ax.text(x0, 49, f"bovenkant = robot {'links' if not onderzijde else 'RECHTS (gespiegeld)'}", fontsize=7, color="#555")


XB = (PRINT[0] - 5, PRINT[1] + 12); YB = (-52, 52)
leg = [plt.Line2D([], [], color=k, lw=2, label=s) for s, k in KLEUR.items() if s != "BATT+"]


def blad(bestand, onderzijde, schaal, papier, titel, voet):
    """Tekening op exacte schaal: 1 data-mm = schaal mm papier."""
    B, H = papier
    fig = plt.figure(figsize=(B / 25.4, H / 25.4))
    w, h = (XB[1] - XB[0]) * schaal, (YB[1] - YB[0]) * schaal
    ax = fig.add_axes([(B - w) / 2 / B, (H - h) / 2 / H, w / B, h / H])
    teken(ax, onderzijde)
    ax.set_xlim(*XB); ax.set_ylim(*YB); ax.set_aspect("auto")
    ax.plot([PRINT[0], PRINT[0] + 50], [-50, -50], color="k", lw=2)
    ax.text(PRINT[0] + 25, -48.6, "controlemaat 50 mm", fontsize=6, ha="center")
    fig.text(0.04, 0.955, titel, fontsize=13, fontweight="bold")
    fig.text(0.04, 0.02, voet, fontsize=7.5)
    if onderzijde:
        fig.legend(handles=leg, loc="lower right", fontsize=8, ncol=5, frameon=False, bbox_to_anchor=(0.97, 0.05))
    for ext in ("png", "pdf"):
        fig.savefig(HIER / f"{bestand}.{ext}", dpi=150 if ext == "png" else None)
    plt.close(fig)


blad("boormal_1op1", False, 1.0, (297, 210),
     "BOORMAL + PLAATSING BOVENZIJDE - schaal 1:1 (A4 liggend, afdrukken op 100 %)",
     "Controleer de 50 mm-maat na het afdrukken. Uitknippen, met plakband op de print leggen, gaten aanprikken.\n"
     "Witte gaten: M2 = 2,2 mm boren (beugels, caster, QTR); oranje = 3,2 mm (M3, spoiler); bruin = 5 mm (motorkabels). Stippellijn = onderdelen aan de onderzijde.")
blad("bekabelingsplan", True, 2.0, (420, 297),
     "BEKABELINGSPLAN - ONDERZIJDE / SOLDEERKANT (gespiegeld) - schaal 2:1 (A3 liggend)",
     "Alle draden liggen aan de soldeerkant. Nummer bij elke draad = nummer in draadlijst.md. "
     "Je kijkt op de omgedraaide print: robot-RECHTS ligt nu bovenaan. Posities = 3D-model (mechanisch/model_linefollower.py).")

# draadlijst in markdown
STAPNAAM = {3: "Stap 5 - voeding", 4: "Stap 6 - batterijmeting", 6: "Stap 8 - H-brug", 7: "Stap 9 - motoren en encoders",
            8: "Stap 10 - sensor", 9: "Stap 11 - bediening"}   # stapnummers = instructable/readme.md
regels = ["# Draadlijst (automatisch gemaakt door bekabelingsplan.py)", "",
          "Stappen = [instructable](../../instructable/readme.md). Nummers = nummers op [bekabelingsplan.pdf](bekabelingsplan.pdf). Alle draden liggen aan de **onderzijde** (soldeerkant).",
          "Kleur = aanbevolen draadkleur. Vink af tijdens het solderen.", ""]
huidig = None
for nr, stap, a, b, net, soort, opm in DRADEN:
    if stap != huidig:
        regels += ["", f"## {STAPNAAM[stap]}", "", "| ✓ | nr | van | naar | net | kleur | opmerking |", "|---|---|---|---|---|---|---|"]
        huidig = stap
    kleurnaam = {"BATT+": "rood", "VBAT": "rood", "3V3": "oranje", "GND": "zwart", "PWM": "geel", "DIR": "groen",
                 "MOTOR": "motorkabel", "ENC": "encoderkabel", "SENS": "wit/paars", "BEDIENING": "blauw"}[soort]
    regels.append(f"| ☐ | {nr} | {naam(a)} | {naam(b)} | {net} | {kleurnaam} | {opm} |")
(HIER / "draadlijst.md").write_text("\n".join(regels) + "\n", encoding="utf-8")
print("klaar:", len(DRADEN), "draden")
