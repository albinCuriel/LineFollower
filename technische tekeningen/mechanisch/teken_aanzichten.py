"""Technische tekening linefollower: 4 aanzichten + maten + stuklijst.

Leest de STL-bestanden uit 3d/ (gemaakt door model_linefollower.py) en tekent met matplotlib.
Gebruik:  py -3 teken_aanzichten.py   -> tekening_linefollower.pdf / .png
Assen: X = rijrichting (vooruit), Y = links, Z = omhoog. Oorsprong: wielas op de grond.
"""
import struct, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import PolyCollection

HIER = pathlib.Path(__file__).parent
STL = HIER / "3d"

# naam -> (kleur, stuklijstnr, omschrijving)
ONDERDELEN = {
    "gaatjesprint":           ("#2e7d32", 1,  "Gaatjesprint 120x90 mm (chassis, ingekort)"),
    "ESP32-S3_devkit":        ("#283593", 2,  "ESP32-S3 devkit N8R2 (dual USB-C)"),
    "QTR-8A":                 ("#c62828", 3,  "Pololu QTR-8A sensorarray"),
    "M2_bevestiging_sensor":  ("#9e9e9e", 4,  "M2x25 + moeren (sensorhoogte 3 mm)"),
    "TB6612FNG":              ("#e53935", 5,  "TB6612FNG-module"),
    "buck_CN3903_3V3":        ("#1565c0", 6,  "CN3903 buck 3,3 V"),
    "LiPo_2S_450mAh":         ("#424242", 7,  "DOGCOM LiPo 2S 450 mAh"),
    "XT30":                   ("#f9a825", 8,  "XT30 male pigtail"),
    "motor_links":            ("#b0bec5", 9,  "GA12-N20 6V 10:1 + encoder (L)"),
    "motor_rechts":           ("#b0bec5", 9,  "GA12-N20 6V 10:1 + encoder (R)"),
    "beugel_links":           ("#212121", 10, "Pololu micro motorbeugel"),
    "beugel_rechts":          ("#212121", 10, "Pololu micro motorbeugel"),
    "wiel_links":             ("#f5f5f5", 11, "Pololu wiel 32x7 mm"),
    "wiel_rechts":            ("#f5f5f5", 11, "Pololu wiel 32x7 mm"),
    "ball_caster":            ("#616161", 12, "Pololu ball caster 3/8\""),
    "caster_afstandsstukken": ("#9e9e9e", 13, "Afstandsstukken caster (12,4 mm)"),
    "aan_uit_schakelaar":     ("#1e88e5", 14, "Aan/uit-schakelaar SS12D00"),
    "start_stop_knop":        ("#fdd835", 15, "Start/stop-drukknop 6x6"),
    "elco_100uF":             ("#3949ab", 16, "Elco 100 uF (2x)"),
    "spoiler":                ("#ff6f00", 17, "Spoiler (afgezaagd stuk print)"),
    "spoiler_bouten":         ("#9e9e9e", 18, "2x M3x30 + moeren (spoiler)"),
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


def teken(ax, R, titel):
    """R: 3x3 rotatie; na rotatie kijken we langs -Z' (x',y' op papier, z' = diepte)."""
    diepte, vlakken, kleuren = [], [], []
    for n, tri in mesh.items():
        basis = np.array(matplotlib.colors.to_rgb(ONDERDELEN[n][0]))
        t = tri @ R.T
        nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12)
        f = 0.55 + 0.45 * np.abs(nrm @ LICHT)                     # schaduw, alles in een keer
        diepte.append(t[:, :, 2].mean(1)); vlakken.append(t[:, :, :2])
        kleuren.append(np.clip(basis[None, :] * f[:, None], 0, 1))
    volgorde = np.argsort(np.concatenate(diepte))                 # schildersalgoritme: ver -> dichtbij
    vl, kl = np.concatenate(vlakken)[volgorde], np.concatenate(kleuren)[volgorde]
    # 1 collectie i.p.v. 1 patch per driehoek (veel sneller); gerasterd zodat de PDF klein blijft
    ax.add_collection(PolyCollection(vl, facecolors=kl, edgecolors=kl, linewidths=0.3, rasterized=True))
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

# ---------------------------------------------------------------- massa en zwaartepunt
# Massa per onderdeel (g): datasheet/winkel, of geschat uit afmetingen (FR4 1,85 g/cm3, -20 % gaten).
MASSA_G = {
    "gaatjesprint": 25.6, "ESP32-S3_devkit": 9.0, "QTR-8A": 3.1, "M2_bevestiging_sensor": 1.5,
    "TB6612FNG": 2.0, "buck_CN3903_3V3": 2.0, "LiPo_2S_450mAh": 28.0, "XT30": 3.0,
    "motor_links": 11.0, "motor_rechts": 11.0, "beugel_links": 1.2, "beugel_rechts": 1.2,
    "wiel_links": 1.8, "wiel_rechts": 1.8, "ball_caster": 1.1, "caster_afstandsstukken": 1.5,
    "aan_uit_schakelaar": 0.5, "start_stop_knop": 0.5, "elco_100uF": 2.0, "spoiler": 6.0, "spoiler_bouten": 3.0,
}
DRAAD_TIN_G = 6.0          # draadjes + soldeer, verdeeld over de print
zw = {n: mesh[n].reshape(-1, 3).mean(0) for n in ONDERDELEN}
m_tot = sum(MASSA_G.values()) + DRAAD_TIN_G
cg = (sum(MASSA_G[n] * zw[n] for n in ONDERDELEN) + DRAAD_TIN_G * zw["gaatjesprint"]) / m_tot
X_CASTER = 84.0
aandeel_wielen = 1 - cg[0] / X_CASTER          # momentenevenwicht rond de wielas
a_steiger = 9.81 * cg[0] / cg[2]               # boven deze versnelling komt de neus (caster) los
with open(HIER / "massa_zwaartepunt.txt", "w", encoding="utf-8") as f:
    f.write(f"massa_g={m_tot:.1f}\ncg_x_mm={cg[0]:.1f}\ncg_z_mm={cg[2]:.1f}\naandeel_wielen={aandeel_wielen:.3f}\n"
            f"a_steiger={a_steiger:.2f}\n")

# ---------------------------------------------------------------- blad A3, aanzichten op schaal 1:1
MMP = 1 / 25.4
fig = plt.figure(figsize=(420 * MMP, 297 * MMP))
fig.patch.set_facecolor("white")
fig.add_artist(Rectangle((5 / 420, 5 / 297), 410 / 420, 287 / 297, fill=False, lw=1.2, transform=fig.transFigure))
fig.text(12 / 420, 280 / 297, "LINEFOLLOWER - SAMENSTELLINGSTEKENING (plan B, gaatjesprint)", fontsize=15, fontweight="bold")


def as_mm(x, y, xlim, ylim):
    """As waarvan 1 data-mm exact 1 mm papier is (schaal 1:1). x, y = linkeronderhoek op het blad (mm)."""
    w, h = xlim[1] - xlim[0], ylim[1] - ylim[0]
    a = fig.add_axes([x / 420, y / 297, w / 420, h / 297])
    return a


def aanzicht(x, y, xlim, ylim, titel, R):
    ax = as_mm(x, y, xlim, ylim)
    teken(ax, R, "")
    ax.set_aspect("auto"); ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.text(0, 1.0, titel, transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")
    return ax


ZP = dict(marker="$\\odot$", ms=11, color="#d50000")

# BOVENAANZICHT (1:1)
ax = aanzicht(14, 142, (-28, 140), (-62, 66), "BOVENAANZICHT  1:1", BOVEN)
maat(ax, (mn[0], mn[1]), (mx[0], mn[1]), f"{mx[0]-mn[0]:.0f}", off=(0, -6))
maat(ax, (mx[0], mn[1]), (mx[0], mx[1]), f"{mx[1]-mn[1]:.0f}", off=(9, 0))
maat(ax, (0, -2), (98.7, -2), "98,7", kleur="#b71c1c")
maat(ax, (0, 12), (84, 12), "84 (caster)", kleur="#b71c1c")
maat(ax, (98.7, -37.45), (98.7, 37.45), "74,9 (QTR)", off=(-6, 0), kleur="#b71c1c")
maat(ax, (0, -49.5), (0, 49.5), "99", off=(-14, 0), kleur="#b71c1c")
ax.plot(0, 0, "+", color="k", ms=10); ax.text(1.5, 2, "wielas", fontsize=6.5)
ax.plot(cg[0], cg[1], **ZP)

# ZIJAANZICHT (1:1), onder het bovenaanzicht en even breed
ax = aanzicht(14, 62, (-28, 140), (-14, 62), "ZIJAANZICHT (links)  1:1", ZIJ)
ax.axhline(0, color="#795548", lw=1.0); ax.text(-26, -4, "grond", fontsize=6.5, color="#795548")
maat(ax, (mn[0], 0), (mx[0], 0), f"{mx[0]-mn[0]:.0f}", off=(0, -9))
maat(ax, (mx[0], 0), (mx[0], mx[2]), f"{mx[2]:.0f}", off=(9, 0))
maat(ax, (60, 0), (60, 22.5), "22,5", kleur="#b71c1c")
maat(ax, (112, 0), (112, 3), "3", kleur="#b71c1c")
maat(ax, (-22, 24.1), (-22, 44.1), "20", kleur="#b71c1c")
ax.plot(cg[0], cg[2], **ZP)
ax.annotate(f"zwaartepunt ({cg[0]:.0f}; {cg[2]:.0f})", xy=(cg[0], cg[2]), xytext=(cg[0] - 10, 56), fontsize=6.5,
            color="#d50000", fontweight="bold", arrowprops=dict(arrowstyle="-", color="#d50000", lw=0.6))

# VOORAANZICHT (1:1)
ax = aanzicht(196, 62, (-72, 72), (-14, 62), "VOORAANZICHT  1:1", VOOR)
ax.axhline(0, color="#795548", lw=1.0)
maat(ax, (-mx[1], 0), (-mn[1], 0), f"{mx[1]-mn[1]:.0f} (max. 110)", off=(0, -9))
maat(ax, (56, 0), (56, 32), "Ø32", off=(6, 0))
ax.add_patch(Rectangle((-60, 0), 120, 120, fill=False, ls="--", ec="#9e9e9e", lw=0.8))
ax.text(-58, 55, "chronobrug 120 x 120", fontsize=6, color="#757575")

# ISOMETRIE met positienummers (niet op schaal)
ax = fig.add_axes([182 / 420, 150 / 297, 140 / 420, 122 / 297])
teken(ax, ISO, "")
ax.text(0, 1.0, "ISOMETRIE (niet op schaal)", transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")
proj = {n: zw[n] @ ISO.T for n in ONDERDELEN}
gezien_nr = {}
for n, (kl, nr, oms) in ONDERDELEN.items():
    gezien_nr.setdefault(nr, n)
x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
midden = np.array([(x0 + x1) / 2, (y0 + y1) / 2])
rx, ry = 0.62 * (x1 - x0), 0.62 * (y1 - y0)
items = sorted(gezien_nr.items(), key=lambda kv: np.arctan2(proj[kv[1]][1] - midden[1], proj[kv[1]][0] - midden[0]))
hoek0 = np.arctan2(proj[items[0][1]][1] - midden[1], proj[items[0][1]][0] - midden[0])
r_bal = 0.035 * (x1 - x0)
for k, (nr, n) in enumerate(items):
    hoek = hoek0 + 2 * np.pi * k / len(items)
    lx, ly = midden[0] + rx * np.cos(hoek), midden[1] + ry * np.sin(hoek)
    px, py = proj[n][:2]
    ax.plot([px, lx], [py, ly], color="#424242", lw=0.5, zorder=9)
    ax.plot(px, py, "o", ms=2, color="#424242", zorder=9)
    ax.add_patch(Circle((lx, ly), r_bal, fc="white", ec="#212121", lw=0.8, zorder=10))
    ax.text(lx, ly, str(nr), ha="center", va="center", fontsize=6.5, fontweight="bold", zorder=11)
ax.set_xlim(midden[0] - rx - 2 * r_bal, midden[0] + rx + 2 * r_bal)
ax.set_ylim(midden[1] - ry - 2 * r_bal, midden[1] + ry + 2 * r_bal)
ax.set_aspect("equal")

# STUKLIJST met massa
ax = fig.add_axes([330 / 420, 12 / 297, 82 / 420, 262 / 297]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.text(0, 0.99, "STUKLIJST", fontsize=10, fontweight="bold", va="top")
ax.text(0.97, 0.99, "g", fontsize=8, fontweight="bold", va="top", ha="right")
massa_per_nr = {}
for n, (kl, nr, oms) in ONDERDELEN.items():
    massa_per_nr[nr] = massa_per_nr.get(nr, 0) + MASSA_G[n]
y = 0.955
for nr, n in sorted(gezien_nr.items()):
    kl, _, oms = ONDERDELEN[n]
    ax.add_patch(Rectangle((0, y - 0.009), 0.05, 0.018, fc=kl, ec="k", lw=0.4))
    ax.text(0.07, y, f"{nr:>2} {oms}", fontsize=6.4, va="center")
    ax.text(0.99, y, f"{massa_per_nr[nr]:.1f}", fontsize=6.4, va="center", ha="right")
    y -= 0.026
ax.text(0.07, y, "    draad + soldeer", fontsize=6.4, va="center")
ax.text(0.99, y, f"{DRAAD_TIN_G:.1f}", fontsize=6.4, va="center", ha="right")
y -= 0.03
ax.plot([0, 1], [y + 0.013, y + 0.013], color="k", lw=0.6)
ax.text(0.07, y, "TOTAAL (schatting)", fontsize=7.2, fontweight="bold", va="center")
ax.text(0.99, y, f"{m_tot:.0f}", fontsize=7.2, fontweight="bold", va="center", ha="right")
y -= 0.05
for regel in [
    "KERNMATEN",
    f"L x B x H  {mx[0]-mn[0]:.0f} x {mx[1]-mn[1]:.0f} x {mx[2]:.0f} mm",
    "spoor 99 mm, wiel Ø32 x 7",
    "sensor 98,7 voor de as, 3 boven grond",
    "print 22,5 boven grond, caster op 84",
    "",
    "ZWAARTEPUNT Z (berekend)",
    f"{cg[0]:.1f} mm voor de as, {cg[2]:.1f} mm hoog",
    f"{aandeel_wielen * 100:.0f} % gewicht op de aandrijfwielen",
    f"neus komt los boven {a_steiger:.1f} m/s2",
]:
    vet = regel in ("KERNMATEN", "ZWAARTEPUNT Z (berekend)")
    ax.text(0, y, regel, fontsize=6.8, fontweight="bold" if vet else "normal", va="center")
    y -= 0.023
ax.add_patch(Rectangle((0, 0.0), 1, 0.11, fill=False, lw=1))
ax.text(0.03, 0.088, "HOGENT - Elektromechanica", fontsize=7.5, fontweight="bold")
ax.text(0.03, 0.062, "Linefollower - samenstelling plan B", fontsize=7.5)
ax.text(0.03, 0.036, "Maten in mm | schaal 1:1 (A3) | ISO E", fontsize=7)
ax.text(0.03, 0.011, "Getekend: Albin | rev 1.2 | 2026-10-19", fontsize=7)
for ext in ("pdf", "png"):
    fig.savefig(HIER / f"tekening_linefollower.{ext}", dpi=170)
print(f"massa {m_tot:.0f} g, zwaartepunt x={cg[0]:.1f} z={cg[2]:.1f} mm, "
      f"{aandeel_wielen * 100:.0f} % op de wielen, neus los boven {a_steiger:.1f} m/s2")

# losse 3D-renders vanuit 4 hoeken
for naam, R in {"iso_voor_links": ISO, "iso_achter_rechts": Rx(np.radians(-60)) @ Rz(np.radians(45)),
                "iso_onder": Rx(np.radians(-120)) @ Rz(np.radians(-135))}.items():
    f2 = plt.figure(figsize=(9, 6)); a2 = f2.add_subplot(111); teken(a2, R, "")
    f2.savefig(HIER / f"3d_{naam}.png", dpi=160, bbox_inches="tight"); plt.close(f2)
print("klaar:", mx - mn)
