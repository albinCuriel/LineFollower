"""Bouwtekeningen "zoals gebouwd" voor stap 9, 10 en 11 (telling van de bouwer).

Telling: BOVENKANT, sensor van je weg. Letter = rij vanaf de voorkant (A..Z, AA..AZ, BA, BB),
nummer = gat vanaf links (1..33). Grijs = al geplaatst in een vorige stap, kleur = nieuw in deze stap.

  uv run --with matplotlib python als_gebouwd.py      (of: py -3 als_gebouwd.py met matplotlib)
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HIER = os.path.dirname(os.path.abspath(__file__))
G = "#9e9e9e"

# ESP32-S3 devkit: J1 (rechts) in kolom 22, J3 (links) in kolom 12; pin 1 achteraan (rij AF), pin 22 vooraan (rij K)
ESP_J1 = ["3V3", "3V3", "RST", "4", "5", "6", "7", "15", "16", "17", "18", "8", "3", "46", "9", "10",
          "11", "12", "13", "14", "5V", "GND"]
ESP_J3 = ["GND", "43", "44", "1", "2", "42", "41", "40", "39", "38", "37", "36", "35", "0", "45", "48",
          "47", "21", "20", "19", "GND", "GND"]


def lt(n):
    return chr(64 + n) if n <= 26 else ("A" + chr(64 + n - 26) if n <= 52 else "B" + chr(64 + n - 52))


def pt(code):
    i = 0
    while code[i].isalpha():
        i += 1
    s, m = code[:i], int(code[i:])
    n = ord(s[0]) - 64 if len(s) == 1 else (26 if s[0] == "A" else 52) + ord(s[1]) - 64
    return m, -n


def esp(naam):
    """'IO39' / '3V3' / 'GND_J3' -> gatcode van die ESP-pin."""
    for lijst, kol in ((ESP_J1, 22), (ESP_J3, 12)):
        if naam in lijst:
            return f"{lt(32 - lijst.index(naam))}{kol}"
    raise KeyError(naam)


class Blad:
    def __init__(self, titel):
        self.fig, self.ax = plt.subplots(figsize=(10, 14.5))
        ax = self.ax
        ax.set_aspect("equal")
        ax.add_patch(Rectangle((-0.5, -57.5), 35, 58, fc="#2e7d32", ec="k", alpha=0.12))
        for y0 in (-0.5, -57.5):
            ax.add_patch(Rectangle((-0.5, y0), 35, 2, fc="#bdbdbd", alpha=0.5))
        ax.text(17, 0.5, "padstrook VOOR (sensor)", ha="center", va="center", fontsize=9)
        ax.text(17, -56.5, "padstrook ACHTER (wielen)", ha="center", va="center", fontsize=9)
        for n in range(1, 55):
            for m in range(1, 34):
                ax.plot(m, -n, "o", ms=2.2, mfc="white", mec="#bdbdbd", mew=0.5)
            for x, ha in ((-0.1, "right"), (34.1, "left")):
                ax.text(x, -n, lt(n), ha=ha, va="center", fontsize=6.5, color="#1b5e20")
        for m in (1, 5, 10, 12, 15, 20, 22, 25, 31, 33):
            ax.text(m, 1.9, str(m), ha="center", fontsize=7.5, color="#1b5e20",
                    weight="bold" if m in (12, 22, 25, 31) else None)
        ax.annotate("VOOR", xy=(36.8, -3), xytext=(36.8, -12), ha="center", fontsize=11, weight="bold",
                    color="#1565c0", arrowprops=dict(arrowstyle="->", color="#1565c0", lw=2))
        ax.set_title(titel + "\nBOVENKANT, sensor van je weg | letter = rij vanaf voor, nummer = gat vanaf links",
                     fontsize=11)
        self.al_geplaatst()

    # ---------------------------------------------------------------- grijze laag
    def zone(self, m0, n0, m1, n1, txt, hatch=None, kleur=G, fs=7):
        self.ax.add_patch(Rectangle((m0 - 0.5, -n1 - 0.5), m1 - m0 + 1, n1 - n0 + 1,
                                    fc="#eeeeee" if hatch else "none", ec=kleur, ls="--", lw=1.1, hatch=hatch,
                                    alpha=0.9, zorder=2))
        self.ax.text((m0 + m1) / 2, -(n0 + n1) / 2, txt, ha="center", va="center", fontsize=fs, color="#757575",
                     zorder=3)

    def al_geplaatst(self):
        ax = self.ax
        self.zone(3, 9, 32, 11, "")
        ax.text(6.5, -10, "QTR-sensor (onderkant)", fontsize=6.5, color="#757575", va="center")
        self.zone(15, 13, 19, 18, "voor-\nwiel")
        self.zone(1, 45, 11, 54, "motor L\n(onderkant)")
        self.zone(23, 45, 33, 54, "motor R\n(onderkant)")
        self.zone(8, 45, 10, 50, "", hatch="///")
        self.zone(24, 45, 26, 50, "", hatch="///")
        # ESP32
        ax.add_patch(Rectangle((11.3, -32.7), 11.4, 22.4, fc="#263238", alpha=0.07, ec=G, lw=1.2, zorder=2))
        ax.text(17, -22, "ESP32-S3", ha="center", va="center", fontsize=9, color="#757575")
        ax.text(17, -9.9, "USB", ha="center", va="center", fontsize=7, color="#757575")
        for k in range(22):
            for kol in (12, 22):
                ax.plot(kol, -(32 - k), "s", ms=3.5, mfc="#e0e0e0", mec=G, zorder=3)
        # buck + R1/R2
        ax.add_patch(Rectangle((0.6, -30.5), 6.4, 5, fc="#eeeeee", alpha=0.7, ec=G, ls="--", zorder=2))
        ax.text(3.8, -28, "buck", ha="center", va="center", fontsize=7.5, color="#757575")
        for p_, t_ in (((1.2, -29.8), "IN+"), ((1.2, -26.0), "IN-"), ((6.2, -26.0), "OUT-"), ((6.2, -29.8), "OUT+")):
            ax.plot(*p_, "s", ms=5, mfc="#e0e0e0", mec=G, zorder=3)
            ax.text(p_[0] + 0.35, p_[1] + 0.5, t_, fontsize=6, color="#757575", zorder=3)
        ax.add_patch(Rectangle((0.9, -35.6), 0.6, 5.2, fc="#e0e0e0", ec=G, zorder=3))
        ax.text(1.8, -34.5, "R1/R2", fontsize=6, color="#757575", zorder=3)
        # TB6612 + C1
        ax.add_patch(Rectangle((24.4, -41.6), 7.2, 8.2, fc="#eeeeee", alpha=0.7, ec=G, lw=1.2, zorder=2))
        ax.text(28, -35.2, "TB6612", ha="center", va="center", fontsize=8, color="#757575")
        for i, (l, r) in enumerate(zip(["PWMA", "AIN2", "AIN1", "STBY", "BIN1", "BIN2", "PWMB", "GND"],
                                       ["VM", "VCC", "GND", "AO1", "AO2", "BO2", "BO1", "GND"])):
            y = -(34 + i)
            ax.plot(25, y, "s", ms=4, mfc="#e0e0e0", mec=G, zorder=3)
            ax.plot(31, y, "s", ms=4, mfc="#e0e0e0", mec=G, zorder=3)
            ax.text(25.4, y, l, ha="left", va="center", fontsize=5.5, color="#9e9e9e", zorder=3)
            if r not in ("AO1", "AO2", "BO1", "BO2"):
                ax.text(30.6, y, r, ha="right", va="center", fontsize=5.5, color="#9e9e9e", zorder=3)
        ax.add_patch(Rectangle((30.6, -32.45), 2.8, 0.9, fc="#e0e0e0", ec=G, zorder=3))
        ax.text(32, -31.2, "C1", ha="center", fontsize=6, color="#757575")

    # ---------------------------------------------------------------- nieuwe onderdelen
    def gat(self, code, kleur, label=None, dx=0.45, dy=0.0, ha="left", fs=6.5):
        x, y = pt(code)
        self.ax.plot(x, y, "s", ms=6.5, mfc=kleur, mec="k", zorder=7)
        if label:
            self.ax.text(x + dx, y + dy, label, ha=ha, va="center", fontsize=fs, weight="bold", zorder=9,
                         bbox=dict(fc="white", ec="none", pad=0.3, alpha=0.85))

    def draad(self, punten, kleur, nr, idx=None, lw=2.0, ls="-"):
        pts = [pt(p) if isinstance(p, str) else p for p in punten]
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color=kleur, lw=lw, ls=ls, zorder=5, solid_capstyle="round")
        if idx is None:
            idx = len(pts) // 2
        (x0, y0), (x1, y1) = pts[idx - 1], pts[idx]
        self.ax.text((x0 + x1) / 2, (y0 + y1) / 2, str(nr), fontsize=7.5, weight="bold", ha="center", va="center",
                     bbox=dict(boxstyle="circle", fc="white", ec=kleur, pad=0.15), zorder=8)

    def onderschrift(self, tekst):
        self.ax.text(17, -59.2, tekst, ha="center", va="top", fontsize=8, family="monospace")

    def bewaar(self, naam, ymin=-72):
        self.ax.set_xlim(-2, 39)
        self.ax.set_ylim(ymin, 3)
        self.ax.axis("off")
        self.fig.savefig(os.path.join(HIER, naam), dpi=130, bbox_inches="tight")
        plt.close(self.fig)
        print("->", naam)


# =================================================================== stap 9: motoren + encoders
def stap9():
    b = Blad("Stap 9: motoren en encoders (draden 28-39)")
    BR, BL, OR, ZW = "#795548", "#1565c0", "#ef6c00", "#212121"
    rijen = ["AV", "AW", "AX", "AY", "AZ", "BA"]            # volgorde = stekker op het motorprintje
    namen = ["M1", "GND", "C1", "C2", "VCC", "M2"]
    kleur = [BR, ZW, BL, BL, OR, BR]
    for kol, kant in ((13, "L"), (21, "R")):
        b.ax.add_patch(Rectangle((kol - 0.5, -53.5), 1, 6, fc="#ffe0b2", ec="#e65100", lw=1.3, zorder=4))
        for r, n, k in zip(rijen, namen, kleur):
            b.gat(f"{r}{kol}", k, n, dx=0.5 if kant == "R" else -0.5, ha="left" if kant == "R" else "right")
        b.ax.text(kol, -54.4, f"kabel\nmotor {kant}", ha="center", va="top", fontsize=7, weight="bold", color="#e65100")
    # de encoderkabel komt door de uitsparing naar boven
    for x0, x1 in ((9, 12.4), (25, 21.6)):
        b.ax.annotate("", xy=(x1, -50.5), xytext=(x0, -47.5),
                      arrowprops=dict(arrowstyle="->", color="#e65100", lw=1.5, ls="--"), zorder=6)
    b.ax.text(17, -46.3, "kabel door de uitsparing naar boven", ha="center", fontsize=6.5, color="#e65100")
    # motordraden -> TB6612 (kolom 31): AO1 AK, AO2 AL, BO2 AM, BO1 AN
    for code, lab in (("AK31", "AO1"), ("AL31", "AO2"), ("AM31", "BO2"), ("AN31", "BO1")):
        b.gat(code, BR, lab, dx=-0.45, ha="right")
    b.draad(["AV13", (13, -44.9), (33.9, -44.9), (33.9, -37), "AK31"], BR, 28, idx=2)
    b.draad(["BA13", (14.2, -53), (14.2, -44.3), (33.4, -44.3), (33.4, -38), "AL31"], BR, 29, idx=3)
    b.draad(["AV21", (21, -43.7), (32.4, -43.7), (32.4, -40), "AN31"], BR, 30, idx=2)
    b.draad(["BA21", (22.2, -53), (22.2, -43.1), (32.9, -43.1), (32.9, -39), "AM31"], BR, 31, idx=3)
    # encoders -> ESP J3 (kolom 12)
    for io, lab in (("39", "IO39"), ("40", "IO40"), ("41", "IO41"), ("42", "IO42")):
        b.gat(esp(io), BL, f"{lab} {esp(io)}", dx=0.45)
    b.draad(["AX13", (11.4, -50), (11.4, -24), esp("39")], BL, 32, idx=2, lw=1.6)
    b.draad(["AY13", (11.0, -51), (11.0, -25), esp("40")], BL, 33, idx=2, lw=1.6)
    b.draad(["AX21", (20, -50), (20, -42.3), (10.6, -42.3), (10.6, -26), esp("41")], BL, 34, idx=3, lw=1.6)
    b.draad(["AY21", (19.5, -51), (19.5, -41.7), (10.2, -41.7), (10.2, -27), esp("42")], BL, 35, idx=3, lw=1.6)
    # voeding encoders
    b.gat("AF22", OR, "3V3 AF22", dx=0.45)
    b.gat("AF12", ZW, "GND AF12", dx=-0.45, ha="right")
    b.draad(["AZ13", (15.2, -52), (15.2, -33.2), (22, -33.2), "AF22"], OR, 36, idx=2)
    b.draad(["AW13", (12.3, -49), (12.3, -33.2), "AF12"], ZW, 37, idx=2)
    b.draad(["AZ21", "AZ13"], OR, 38)
    b.draad(["AW21", "AW13"], ZW, 39)
    b.onderschrift(
        "Kabel motor L in kolom 13, motor R in kolom 21, rijen AV..BA = M1, GND, C1, C2, VCC, M2 (volg de OPDRUK op het\n"
        "motorprintje; kleuren verschillen per verkoper). Kies je andere gaten: dezelfde verbindingen blijven gelden.\n"
        "28 bruin  motor L M1  AV13 -> AO1 AK31        32 blauw  enc L C1 (A) AX13 -> IO39 X12\n"
        "29 bruin  motor L M2  BA13 -> AO2 AL31        33 blauw  enc L C2 (B) AY13 -> IO40 Y12\n"
        "30 bruin  motor R M1  AV21 -> BO1 AN31        34 blauw  enc R C1 (A) AX21 -> IO41 Z12\n"
        "31 bruin  motor R M2  BA21 -> BO2 AM31        35 blauw  enc R C2 (B) AY21 -> IO42 AA12\n"
        "36 oranje enc L VCC   AZ13 -> 3V3 AF22        38 oranje enc R VCC AZ21 -> AZ13\n"
        "37 zwart  enc L GND   AW13 -> GND AF12        39 zwart  enc R GND AW21 -> AW13\n"
        "Eerst: 100 nF over de motorklemmen (M1-M2) op elk motorprintje.\n"
        "TEST (finale code, wielen in de lucht):  motor l 0.3 500   -> linkerwiel draait VOORUIT, teller links stijgt\n"
        "                                         motor r 0.3 500   -> rechterwiel draait VOORUIT, teller rechts stijgt\n"
        "Fout? Niet hersolderen:  invert motorl | invert motorr (draairichting)   invert encl | invert encr (teller)\n"
        "Verkeerde motor draait? Dan zijn L en R gewisseld: verwissel de stekkers.")
    b.bewaar("stap9_albin_telling.png", ymin=-76)


# =================================================================== stap 10: sensor
def stap10():
    b = Blad("Stap 10: sensor QTR-8A (draden 40-50)")
    PA, OR, ZW = "#8e24aa", "#ef6c00", "#212121"
    namen = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "LEDON", "VCC", "GND"]
    doel = [esp("1"), esp("2"), esp("3"), esp("4"), esp("5"), esp("6"), esp("7"), esp("8"), esp("11"),
            "AE22", "K22"]
    lab = ["IO1", "IO2", "IO3", "IO4", "IO5", "IO6", "IO7", "IO8", "IO11", "3V3", "GND"]
    kl = [PA] * 9 + [OR, ZW]
    b.ax.add_patch(Rectangle((22.5, -8.5), 11, 1, fc="#f3e5f5", ec=PA, lw=1.3, zorder=4))
    b.ax.text(28, -6.2, "kabel van de QTR-8A: rij H, gat 23..33", ha="center", fontsize=7.5, weight="bold", color=PA)
    for i, (n, d, l, k) in enumerate(zip(namen, doel, lab, kl)):
        m = 23 + i
        b.gat(f"H{m}", k)
        b.ax.text(m, -7.2, n, ha="center", va="bottom", fontsize=5.8, weight="bold", rotation=90, zorder=9)
        dx, dy = pt(d)
        if d.endswith("22"):
            b.draad([f"H{m}", (m, dy), d], k, 40 + i, idx=1, lw=1.5)
            b.gat(d, k, f"{l} {d}", dx=-0.45, ha="right", fs=6)
        else:   # S1, S2 naar de linkse pinrij (kolom 12): achter de ESP32 om (rij AG), niet voor de USB-poorten
            lane_y, lane_x = -33.5 + 0.5 * i, 11.0 - 0.5 * i
            b.draad([f"H{m}", (m, lane_y), (lane_x, lane_y), (lane_x, dy), d], k, 40 + i, idx=2, lw=1.5)
            b.gat(d, k, f"{l} {d}", dx=0.45, fs=6)
    b.onderschrift(
        "Eerst: soldeer de jumper '3.3V BYPASS' op de QTR-8A dicht. Sensor op 3 mm van de grond (boortje 3 mm als voeler).\n"
        "11 draadjes van de QTR komen van onderen in rij H (gat 23..33). Sensor 1 = robot LINKS (in de rijrichting).\n"
        "40 S1 H23 -> IO1 AC12     44 S5 H27 -> IO5 AB22     48 LEDON H31 -> IO11 P22\n"
        "41 S2 H24 -> IO2 AB12     45 S6 H28 -> IO6 AA22     49 VCC   H32 -> 3V3  AE22 (oranje)\n"
        "42 S3 H25 -> IO3 T22      46 S7 H29 -> IO7 Z22      50 GND   H33 -> GND  K22  (zwart)\n"
        "43 S4 H26 -> IO4 AC22     47 S8 H30 -> IO8 U22\n"
        "S1 en S2 gaan naar de LINKSE pinrij: leg ze achter de ESP32 om (rij AG), niet voor de USB-poorten langs.\n"
        "Hou de strook voor de USB-poorten vrij (rij A..J, gat 13..21): daar moet de stekker in.\n"
        "TEST (finale code):  sensors   -> 'refl' is hoog op wit en laag op zwart, elke sensor apart (tape eronder schuiven)\n"
        "Reageert de verkeerde kant (tape links, waarde rechts verandert)?  invert sensor   (niet hersolderen)\n"
        "Daarna kalibreren:   cal   -> robot dwars over de lijn schuiven ->   cal stop   (wordt bewaard)")
    b.bewaar("stap10_albin_telling.png", ymin=-74)


# =================================================================== stap 11: knop + power-led
def stap11():
    b = Blad("Stap 11: start/stop-knop (draden 51-52) en power-led")
    GR, ZW, OR = "#00838f", "#212121", "#ef6c00"
    # knop links van de ESP32
    b.ax.add_patch(Rectangle((2.5, -16.5), 3, 3, fc="#fff59d", ec="#f9a825", lw=1.4, zorder=4))
    b.ax.text(4, -12.8, "start/stop-knop", ha="center", fontsize=7.5, weight="bold", color="#f57f17")
    b.gat("N3", GR, "N3", dx=-0.45, ha="right")
    b.gat("P5", ZW, "P5", dx=0.45)
    b.gat(esp("21"), GR, f"IO21 {esp('21')}", dx=0.45)
    b.gat("L12", ZW, "GND L12", dx=0.45)
    b.draad(["N3", (3, -18), (10.5, -18), (10.5, -15), esp("21")], GR, 51, idx=2)
    b.draad(["P5", (9, -16), (9, -12), "L12"], ZW, 52, idx=2)
    # power-led: 3V3 -> R3 -> led -> GND
    b.ax.add_patch(Rectangle((4.6, -41.5), 0.8, 4.0, fc="#d7ccc8", ec="#5d4037", lw=1.2, zorder=4))
    b.ax.text(5.9, -39.5, "R3 330", fontsize=7, weight="bold", color="#5d4037", va="center")
    b.gat("AK5", OR, "AK5", dx=-0.45, ha="right")
    b.gat("AO5", "#5d4037", "AO5", dx=-0.45, ha="right")
    b.ax.add_patch(Rectangle((4.6, -43.4), 1.8, 0.8, fc="#c8e6c9", ec="#2e7d32", lw=1.2, zorder=4))
    b.gat("AQ5", "#2e7d32", "led + (lange poot) AQ5", dx=-0.45, ha="right")
    b.gat("AQ6", ZW, "led - AQ6", dx=0.45)
    b.draad([(6.2, -29.8), (7.6, -29.8), (7.6, -37), "AK5"], OR, "a", idx=2)
    b.draad(["AO5", "AQ5"], "#757575", "b")
    b.draad(["AQ6", (8.4, -43), (8.4, -26.6), (6.2, -26.0)], ZW, "c", idx=2)
    b.onderschrift(
        "KNOP (4 pootjes, schuin tegenover elkaar is altijd geschakeld): pootjes in N3 en P5.\n"
        "51 grijs  knop N3 -> IO21 O12          52 zwart  knop P5 -> GND L12\n"
        "TEST (finale code): druk op de knop -> 'START' in de terminal, led groen; nog een druk -> 'STOP', led rood.\n"
        "\n"
        "POWER-LED (verplicht in de specificaties; overslaan als je hem al geplaatst hebt in stap 5):\n"
        "a oranje  buck OUT+ (3V3) -> R3 in AK5     R3 330 ohm ligt van AK5 naar AO5\n"
        "b brug    R3 AO5 -> led + AQ5 (lange poot)\n"
        "c zwart   led - AQ6 -> buck OUT- (GND)\n"
        "TEST: SW1 aan -> de led brandt; SW1 uit -> de led is uit.\n"
        "De gaten voor de knop en de led zijn een voorstel: liggen er al draden, schuif dan een paar gaten op.")
    b.bewaar("stap11_albin_telling.png", ymin=-72)


if __name__ == "__main__":
    stap9()
    stap10()
    stap11()
