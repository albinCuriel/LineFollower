"""Mechanische maattekening van de plan A-print (omtrek, uitsparingen, boorgaten, sensorlijn, wielas).

  uv run --with matplotlib python maattekening.py      -> ../../mechanisch/tekening_planA.pdf en .png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

import planA_maten as M

HIER = os.path.dirname(os.path.abspath(__file__))
UIT = os.path.join(HIER, "..", "..", "mechanisch")
BL, RD = "#0d47a1", "#b71c1c"

fig, ax = plt.subplots(figsize=(11.69, 16.54))   # A3 staand
ax.set_aspect("equal")
ax.invert_yaxis()                                 # y = 0 (voorkant) bovenaan

ax.add_patch(Polygon(M.omtrek(), closed=True, fc="#e8f5e9", ec="k", lw=1.8))
# onderdelen aan de onderkant (streeplijn)
d = M.WIEL_UIT["diepte"]
for s in (1, -1):
    xw = 2 if s > 0 else M.BREED - 9
    ax.add_patch(Rectangle((xw, M.AS_Y - 16), 7, 32, fc="#bdbdbd", ec="k", lw=0.8))            # wiel 32 x 7
    xm = 12 if s > 0 else M.BREED - 12 - 34
    ax.add_patch(Rectangle((xm, M.AS_Y - 6), 34, 12, fc="none", ec="#616161", ls="--", lw=1))   # motor + encoder
ax.text(29, M.AS_Y, "motor L\n(onderkant)", ha="center", va="center", fontsize=8, color="#616161")
ax.text(71, M.AS_Y, "motor R\n(onderkant)", ha="center", va="center", fontsize=8, color="#616161")
ax.add_patch(Rectangle((50 - 9.55, 30 - 6.05), 19.1, 12.1, fc="none", ec="#616161", ls="--", lw=1))
ax.text(50, 39, "ball caster (onderkant)", ha="center", fontsize=8, color="#616161")
for i in range(8):
    x = 50 + (i - 3.5) * M.SENSOR_STEEK
    ax.add_patch(Rectangle((x - 1.8, M.SENSOR_Y - 1.45), 3.6, 2.9, fc="#ef9a9a", ec=RD, lw=0.8))
ax.text(50, M.SENSOR_Y + 5, "8x QRE1113 (onderkant), steek 9,5", ha="center", fontsize=8, color=RD)
ax.add_patch(Rectangle((1.2, 46), 25.5, 18, fc="#c5cae9", ec="#283593", lw=1))
ax.text(14, 55, "ESP32-S3-WROOM-1\nantenne over de rand", ha="center", va="center", fontsize=7.5, color="#283593")
ax.add_patch(Rectangle((44.5, 118), 11, 12.5, fc="#fff59d", ec="#f57f17", lw=1))
ax.text(50, 124.5, "XT30", ha="center", va="center", fontsize=7.5)
ax.add_patch(Rectangle((71.5, 121), 9, 9.5, fc="#cfd8dc", ec="#455a64", lw=1))
ax.text(76, 126, "USB-C", ha="center", va="center", fontsize=7.5)
ax.add_patch(Rectangle((0, 124), M.BREED, 6, fc="#ffe0b2", ec="#ef6c00", ls=":", lw=1, alpha=0.6))
ax.text(50, 133.5, "spoiler 100 x 25 mm op 2x M3x30, 20 mm boven de print", ha="center", fontsize=8, color="#ef6c00")

# boorgaten
for x, y, dia, wat in M.GATEN:
    ax.add_patch(Circle((x, y), dia / 2, fc="white", ec="k", lw=1.2))
    ax.plot([x - 2, x + 2], [y, y], color="k", lw=0.4)
    ax.plot([x, x], [y - 2, y + 2], color="k", lw=0.4)
ax.plot([-4, M.BREED + 4], [M.AS_Y, M.AS_Y], color=RD, lw=0.8, ls="-.")
ax.text(M.BREED + 5, M.AS_Y, "wielas", color=RD, fontsize=8, va="center")
ax.plot([10, 90], [M.SENSOR_Y, M.SENSOR_Y], color=RD, lw=0.6, ls="-.")


def maat_h(x0, x1, y, tekst, kleur=BL, boven=True):
    ax.annotate("", xy=(x0, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", color=kleur, lw=1))
    ax.text((x0 + x1) / 2, y - 1.0 if boven else y + 3.0, tekst, ha="center", fontsize=9, color=kleur)


def maat_v(x, y0, y1, tekst, kleur=BL, links=True):
    ax.annotate("", xy=(x, y0), xytext=(x, y1), arrowprops=dict(arrowstyle="<->", color=kleur, lw=1))
    ax.text(x - 1.2 if links else x + 1.2, (y0 + y1) / 2, tekst, ha="right" if links else "left", va="center",
            fontsize=9, color=kleur, rotation=90)


maat_h(0, M.BREED, -8, f"{M.BREED:.0f}")
maat_v(-14, 0, M.LANG, f"{M.LANG:.0f}")
maat_v(-8, M.SENSOR_Y, M.AS_Y, f"{M.AS_Y - M.SENSOR_Y:.0f} (sensor - wielas)", kleur=RD)
maat_v(M.BREED + 12, M.WIEL_UIT['y0'], M.WIEL_UIT['y1'], f"{M.WIEL_UIT['y1'] - M.WIEL_UIT['y0']:.0f}", links=False)
maat_h(M.BREED - d, M.BREED, M.WIEL_UIT['y0'] - 3, f"{d:.0f}")
maat_h(16.5, 83.5, M.AS_Y - 9, "67", boven=True)
maat_v(22, M.AS_Y - 9, M.AS_Y + 9, "18", links=False)
maat_h(50 - 6.75, 50 + 6.75, 26, "13,5")
maat_v(64, 0, 30, "30", links=False)
maat_h(6, 94, 126, "88", boven=False)
maat_v(M.BREED + 20, M.AS_Y, M.LANG, f"{M.LANG - M.AS_Y:.0f}", links=False)

ax.text(-18, -20, "LINEFOLLOWER plan A - MAATTEKENING PRINT (bovenaanzicht, schaal 1:1 op A3)", fontsize=14,
        weight="bold")
ax.text(-18, 148,
        "Print FR4 1,6 mm, 2 lagen, 100 x 130 mm, hoeken R3. De print is het chassis.\n"
        "Boorgaten: 4x 2,2 mm motorbeugels (Pololu #989, 18 mm uit elkaar), 2x 2,2 mm ball caster (Pololu #950, 13,5 mm),\n"
        "2x 3,2 mm spoiler. Wieluitsparingen 11 x 36 mm: de wielen (32 x 7 mm) vallen binnen de printbreedte,\n"
        "zodat de robot 100 mm breed is (chronobrug 120 mm). Sensorlijn 99 mm voor de wielas, sensoren 3 mm boven de grond\n"
        "(wiel 32 mm: as op 16 mm; motor 10 mm hoog onder de print -> onderkant print op 22,5 mm; caster + afstandsringen 12,4 mm).\n"
        "HOGENT Elektromechanica - Albin Curiel - 2026-11-16 - maten in mm",
        fontsize=9, va="top")
ax.set_xlim(-22, 128)
ax.set_ylim(170, -26)
ax.axis("off")
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(UIT, f"tekening_planA.{ext}"), dpi=110, bbox_inches="tight")
print("-> tekening_planA.pdf / .png")
