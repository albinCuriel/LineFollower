"""Technische tekening linefollower: 4 aanzichten + maten + stuklijst.

Leest de STL-bestanden uit 3d/ (export uit build123d) en tekent met matplotlib.
Gebruik:  py -3 teken_aanzichten.py   -> tekening_linefollower.pdf / .png
Assen: X = rijrichting (vooruit), Y = links, Z = omhoog. Oorsprong: wielas op de grond.
"""
import struct, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

HIER = pathlib.Path(__file__).parent
STL = HIER / "3d"

# naam -> (kleur, stuklijstnr, omschrijving)
ONDERDELEN = {
    "gaatjesprint":          ("#2e7d32", 1,  "Gaatjesprint 150x90 mm (chassis)"),
    "ESP32-S3_devkit":       ("#283593", 2,  "ESP32-S3-DevKitC-1 N8R2"),
    "vrouwelijke_headers":   ("#151515", 3,  "Vrouwelijke headers 2x22 (8,5 mm)"),
    "QTR-8A":                ("#c62828", 4,  "Pololu QTR-8A sensorarray"),
    "M2_bevestiging_sensor": ("#9e9e9e", 5,  "M2-bouten + moeren (sensorhoogte 3 mm)"),
    "TB6612FNG":             ("#e53935", 6,  "TB6612FNG H-brug"),
    "buck_CN3903_3V3":       ("#1565c0", 7,  "CN3903 buck 3,3 V"),
    "LiPo_2S_450mAh":        ("#424242", 8,  "LiPo 2S 450 mAh (28 g)"),
    "XT30":                  ("#f9a825", 9,  "XT30-connector"),
    "motor_links":           ("#b0bec5", 10, "N20 6V 10:1 + encoder (L)"),
    "motor_rechts":          ("#b0bec5", 10, "N20 6V 10:1 + encoder (R)"),
    "beugel_links":          ("#212121", 11, "Pololu motorbeugel"),
    "beugel_rechts":         ("#212121", 11, "Pololu motorbeugel"),
    "wiel_links":            ("#f5f5f5", 12, "Pololu wiel 32x7 mm (siliconen)"),
    "wiel_rechts":           ("#f5f5f5", 12, "Pololu wiel 32x7 mm (siliconen)"),
    "ball_caster":           ("#616161", 13, "Pololu ball caster 3/8\""),
    "WS2812_8leds":          ("#eceff1", 14, "WS2812B 8 leds (sensorweergave)"),
    "aan_uit_schakelaar":    ("#1e88e5", 15, "Aan/uit-schakelaar SS12D00"),
    "start_stop_knop":       ("#fdd835", 16, "Start/stop-drukknop 6x6"),
    "elco_100uF":            ("#3949ab", 17, "Elco 100 uF (2x)"),
    "spoiler":               ("#ff6f00", 18, "Spoiler (op 2 M3-boutjes)"),
}


def lees_stl(pad):
    data = pad.read_bytes()
    if data[:5] == b"solid" and b"facet" in data[:400]:
        v = [list(map(float, l.split()[1:4])) for l in data.decode(errors="ignore").splitlines()
             if l.strip().startswith("vertex")]
        return np.array(v).reshape(-1, 3, 3)
    n = struct.unpack("<I", data[80:84])[0]
    arr = np.frombuffer(data[84:84 + n * 50], dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]))
    return arr["v"].reshape(-1, 3, 3).astype(float)


def verfijn(tri, max_rib=4.0):
    """Splits grote driehoeken in 4 tot elke rib < max_rib mm (correcte tekenvolgorde)."""
    uit, todo = [], list(tri)
    while todo:
        a, b, c = todo.pop()
        if max(np.linalg.norm(a - b), np.linalg.norm(b - c), np.linalg.norm(c - a)) <= max_rib:
            uit.append((a, b, c)); continue
        ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
        todo += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
    return np.array(uit)


mesh = {n: verfijn(lees_stl(STL / f"{n}.stl")) for n in ONDERDELEN}
alle = np.concatenate(list(mesh.values()))
mn, mx = alle.reshape(-1, 3).min(0), alle.reshape(-1, 3).max(0)
LICHT = np.array([-0.4, 0.5, 0.75]); LICHT /= np.linalg.norm(LICHT)


def kleur_schaduw(hexkleur, normaal):
    c = np.array(matplotlib.colors.to_rgb(hexkleur))
    f = 0.55 + 0.45 * abs(float(normaal @ LICHT))
    return np.clip(c * f, 0, 1)


def teken(ax, R, titel):
    """R: 3x3 rotatie; na rotatie kijken we langs -Z' (x',y' op papier, z' = diepte)."""
    polys = []
    for n, tri in mesh.items():
        kl = ONDERDELEN[n][0]
        t = tri @ R.T
        nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12)
        for k in range(len(t)):
            polys.append((t[k, :, 2].mean(), t[k, :, :2], kleur_schaduw(kl, nrm[k])))
    polys.sort(key=lambda p: p[0])
    for _, p, c in polys:
        ax.add_patch(Polygon(p, closed=True, facecolor=c, edgecolor=c, linewidth=0.3))
    ax.set_aspect("equal"); ax.autoscale_view(); ax.axis("off")
    ax.set_title(titel, fontsize=11, fontweight="bold", loc="left")


def maat(ax, p1, p2, tekst, off=(0, 0), kleur="#0d47a1"):
    (x1, y1), (x2, y2) = p1, p2
    ox, oy = off
    ax.annotate("", xy=(x1 + ox, y1 + oy), xytext=(x2 + ox, y2 + oy),
                arrowprops=dict(arrowstyle="<|-|>", color=kleur, lw=0.9, shrinkA=0, shrinkB=0))
    for (x, y) in (p1, p2):
        ax.plot([x, x + ox], [y, y + oy], color=kleur, lw=0.5, ls=":")
    ax.text((x1 + x2) / 2 + ox, (y1 + y2) / 2 + oy, tekst, color=kleur, fontsize=8,
            ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.6))


Rx = lambda a: np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
Rz = lambda a: np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
BOVEN = np.eye(3)                                            # papier: x vooruit -> rechts, y links -> boven
VOOR = np.array([[0, -1, 0], [0, 0, 1], [1, 0, 0]], float)   # kijk tegen de rijrichting in: y -> links
ZIJ = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)    # linkerzijde: x -> rechts, z -> boven
ISO = Rx(np.radians(-60)) @ Rz(np.radians(-135))

fig = plt.figure(figsize=(16.54, 11.69))  # A3 liggend
fig.patch.set_facecolor("white")
gs = fig.add_gridspec(2, 3, width_ratios=[1.25, 1.0, 0.75], height_ratios=[1, 1],
                      left=0.03, right=0.98, top=0.93, bottom=0.05, wspace=0.12, hspace=0.18)
fig.suptitle("LINEFOLLOWER - SAMENSTELLINGSTEKENING (plan B, gaatjesprint)", fontsize=16, fontweight="bold", x=0.03, ha="left")

ax = fig.add_subplot(gs[0, 0]); teken(ax, BOVEN, "BOVENAANZICHT")
maat(ax, (mn[0], mn[1]), (mx[0], mn[1]), f"{mx[0]-mn[0]:.0f}", off=(0, -10))
maat(ax, (mx[0], mn[1]), (mx[0], mx[1]), f"{mx[1]-mn[1]:.0f}", off=(10, 0))
maat(ax, (0, 0), (95, 0), "95 (as -> sensor)", off=(0, 0), kleur="#b71c1c")
maat(ax, (-25, 45), (125, 45), "150 (print)", off=(0, 18))
ax.plot(0, 0, "+", color="k", ms=12); ax.text(2, 3, "wielas", fontsize=7)
ax.set_xlim(mn[0] - 15, mx[0] + 22); ax.set_ylim(mn[1] - 20, mx[1] + 28)

ax = fig.add_subplot(gs[0, 1]); teken(ax, ZIJ, "ZIJAANZICHT (links)")
maat(ax, (mn[0], 0), (mx[0], 0), f"{mx[0]-mn[0]:.0f}", off=(0, -8))
maat(ax, (mx[0], 0), (mx[0], mx[2]), f"{mx[2]:.0f}", off=(9, 0))
maat(ax, (60, 0), (60, 22.5), "22,5", off=(0, 0), kleur="#b71c1c")
maat(ax, (95, 0), (95, 3), "3", off=(-8, 0), kleur="#b71c1c")
ax.axhline(0, color="#795548", lw=1.2); ax.text(mn[0], -3.5, "grond / parcours", fontsize=7, color="#795548")
ax.set_xlim(mn[0] - 8, mx[0] + 18); ax.set_ylim(-16, mx[2] + 8)

ax = fig.add_subplot(gs[1, 1]); teken(ax, VOOR, "VOORAANZICHT")
maat(ax, (-mx[1], 0), (-mn[1], 0), f"{mx[1]-mn[1]:.0f}  (chronobrug: max. 120)", off=(0, -8))
maat(ax, (54, 0), (54, 32), "Ø32", off=(8, 0))
maat(ax, (-mx[1], 0), (-mx[1], mx[2]), f"{mx[2]:.0f}", off=(-9, 0))
ax.axhline(0, color="#795548", lw=1.2)
ax.add_patch(Rectangle((-60, 0), 120, 120, fill=False, ls="--", ec="#9e9e9e", lw=0.8))
ax.text(-58, 116, "binnenmaat chronobrug 120 x 120", fontsize=7, color="#757575")
ax.set_xlim(-75, 75); ax.set_ylim(-16, 125)

ax = fig.add_subplot(gs[1, 0]); teken(ax, ISO, "ISOMETRISCH AANZICHT")

# stuklijst + titelblok
ax = fig.add_subplot(gs[:, 2]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.text(0, 0.985, "STUKLIJST", fontsize=11, fontweight="bold")
gezien = {}
for n, (kl, nr, oms) in ONDERDELEN.items():
    gezien.setdefault(nr, (kl, oms))
y = 0.95
for nr in sorted(gezien):
    kl, oms = gezien[nr]
    ax.add_patch(Rectangle((0, y - 0.012), 0.05, 0.024, fc=kl, ec="k", lw=0.4))
    ax.text(0.07, y, f"{nr:>2}  {oms}", fontsize=8.5, va="center")
    y -= 0.034
y -= 0.02
for regel in [
    "KERNMATEN",
    f"Totaal L x B x H: {mx[0]-mn[0]:.0f} x {mx[1]-mn[1]:.0f} x {mx[2]:.0f} mm",
    "Spoorbreedte (wielmidden): 101 mm",
    "Sensor 95 mm voor de wielas, 3 mm boven grond",
    "Bodemvrijheid print: 22,5 mm",
    "Wielas 16 mm boven grond (wiel Ø32)",
    "Zwaartepunt: batterij net achter/boven de as",
]:
    ax.text(0, y, regel, fontsize=8.5, fontweight="bold" if regel == "KERNMATEN" else "normal"); y -= 0.028
ax.add_patch(Rectangle((0, 0.0), 1, 0.13, fill=False, lw=1))
ax.text(0.02, 0.105, "HOGENT - Elektromechanica", fontsize=9, fontweight="bold")
ax.text(0.02, 0.075, "Linefollower - samenstelling plan B", fontsize=9)
ax.text(0.02, 0.045, "Maten in mm  |  schaal: n.v.t. (gerenderd)", fontsize=8)
ax.text(0.02, 0.015, "Getekend: Albin  |  rev 1.0  |  2026-10-08", fontsize=8)

for ext in ("pdf", "png"):
    fig.savefig(HIER / f"tekening_linefollower.{ext}", dpi=170)

# losse 3D-renders vanuit 4 hoeken
for naam, R in {"iso_voor_links": ISO, "iso_achter_rechts": Rx(np.radians(-60)) @ Rz(np.radians(45)),
                "iso_onder": Rx(np.radians(-120)) @ Rz(np.radians(-135))}.items():
    f2 = plt.figure(figsize=(9, 6)); a2 = f2.add_subplot(111); teken(a2, R, "")
    f2.savefig(HIER / f"3d_{naam}.png", dpi=160, bbox_inches="tight"); plt.close(f2)
print("klaar:", mx - mn)
