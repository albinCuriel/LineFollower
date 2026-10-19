"""3D-model linefollower (plan B, gaatjesprint) met de maten van de BESTELDE onderdelen.

Alle maten staan in de tabel MATEN hieronder, met de bron per maat:
  "Pololu" = officiele maattekening van de fabrikant (exact)
  "typisch" = typische maat van dit AliExpress-type -> NAMETEN bij levering (zie readme.md)
Maat aanpassen = getal wijzigen en opnieuw draaien:

  C:\\Users\\Albin\\AppData\\Roaming\\uv\\tools\\build123d-mcp\\Scripts\\python.exe model_linefollower.py
  py -3 teken_aanzichten.py

Assen: X = rijrichting (vooruit), Y = links, Z = omhoog. Oorsprong: midden wielas, op de grond.
Uitvoer: 3d/<onderdeel>.stl + 3d/linefollower_assembly.step
"""
import pathlib
from build123d import (Box, Cylinder, Sphere, Pos, Rot, Compound, Align, export_stl, export_step)

UIT = pathlib.Path(__file__).parent / "3d"
UIT.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------- maten (mm)
MATEN = {
    # onderdeel: (waarden, bron)
    "print":      (dict(L=120.0, B=90.0, t=1.6), "bestelling 9x15 cm, ingekort tot 120 mm (zie bouwplan)"),
    "wiel":       (dict(D=32.0, b=7.0), "Pololu #1087"),
    "n20":        (dict(b=12.0, h=10.0, tandwiel=9.0, motor=15.0, encoder=7.0, as_d=3.0, as_l=10.0), "typisch GA12-N20 + Hall-encoder"),
    "beugel":     (dict(L=22.0, b=9.0, t=1.3, gat_afst=18.0), "Pololu #989 (gatafstand typisch)"),
    "caster":     (dict(L=19.1, B=12.1, flens=1.5, H=10.1, kogel=9.53, gat_afst=13.5, afstandsstuk=12.4), "Pololu #950 tekening"),
    "qtr":        (dict(L=74.9, B=12.7, t=1.57, comp=1.5, pitch=9.525, gat_afst=69.9, gat_rand=2.5, hoogte=3.0), "Pololu #960 tekening"),
    "esp32":      (dict(L=63.5, B=28.0, t=1.6, header=2.5, rij_afst=25.4, mod_L=25.5, mod_B=18.0, mod_h=3.1), "typisch dual USB-C devkit"),
    "tb6612":     (dict(L=20.3, B=20.3, t=1.6, header=2.5), "typisch TB6612-module"),
    "buck":       (dict(L=22.0, B=17.0, t=1.6, h=4.0), "typisch CN3903-module"),
    "lipo":       (dict(L=60.0, B=17.0, H=15.0), "typisch 2S 450 mAh"),
    "xt30":       (dict(L=16.0, B=8.0, H=5.2), "typisch XT30"),
    "ss12d00":    (dict(L=8.6, B=3.6, H=3.5, hendel=4.0), "typisch SS12D00"),
    "knop":       (dict(L=6.0, B=6.0, H=5.0), "6x6 mm drukknop"),
    "elco":       (dict(D=6.3, H=11.0), "100 uF 16 V"),
    "spoiler":    (dict(L=86.0, B=25.0, hoogte=20.0, bout="M3x30"), "afgezaagd stuk gaatjesprint"),
}
M = {k: v[0] for k, v in MATEN.items()}

# ----------------------------------------------------------------------------- afgeleide posities
R_WIEL = M["wiel"]["D"] / 2                       # wielas op 16 mm
P_ACHTER = -15.0                                  # achterrand print (x)
P_VOOR = P_ACHTER + M["print"]["L"]               # voorrand print
Z_ONDER = R_WIEL + M["n20"]["h"] / 2 + M["beugel"]["t"] + 0.2   # onderkant print
Z_BOVEN = Z_ONDER + M["print"]["t"]
Y_RAND = M["print"]["B"] / 2
Y_WIEL_IN = Y_RAND + 1.0                          # 1 mm speling print <-> wiel
Y_TANDWIEL = Y_WIEL_IN - 3.0                      # as steekt 3 mm vrij voor de naaf
X_SENSOR = P_VOOR - M["qtr"]["B"] / 2             # sensorlijn = midden QTR
X_CASTER = 34.0                                   # net achter de ESP32 (bouten niet onder de devkit)


def box(lx, ly, lz, x, y, z):
    """Balk met hoek-minimum op (x, y, z)."""
    return Pos(x, y, z) * Box(lx, ly, lz, align=(Align.MIN, Align.MIN, Align.MIN))


def cyl_y(r, l, x, y0, z):
    """Cilinder langs Y van y0 tot y0+l."""
    return Pos(x, y0, z) * Rot(-90, 0, 0) * Cylinder(r, l, align=(Align.CENTER, Align.CENTER, Align.MIN))


def cyl_z(r, l, x, y, z0):
    return Pos(x, y, z0) * Cylinder(r, l, align=(Align.CENTER, Align.CENTER, Align.MIN))


onderdelen = {}

# print (chassis)
p = M["print"]
onderdelen["gaatjesprint"] = box(p["L"], p["B"], p["t"], P_ACHTER, -Y_RAND, Z_ONDER)

# motoren + beugels + wielen (links = +Y, rechts = gespiegeld)
n, bg, w = M["n20"], M["beugel"], M["wiel"]
for kant, s in (("links", 1), ("rechts", -1)):
    def ys(a, b):  # interval in |y| -> echte y-min en lengte
        return (a if s > 0 else -b), b - a
    y_tw = Y_TANDWIEL
    y_mot = y_tw - n["tandwiel"]
    y_enc = y_mot - n["motor"]
    y0, l = ys(y_tw - n["tandwiel"], y_tw)
    delen = [box(n["b"], l, n["h"], -n["b"] / 2, y0, R_WIEL - n["h"] / 2)]
    y0, l = ys(y_enc, y_mot)
    delen.append(box(n["b"], l, n["h"], -n["b"] / 2, y0, R_WIEL - n["h"] / 2))
    y0, l = ys(y_enc - n["encoder"], y_enc)
    delen.append(box(n["b"] + 2, l, n["h"] + 4, -n["b"] / 2 - 1, y0, R_WIEL - n["h"] / 2 - 2))   # encoderprintje
    y0, l = ys(y_tw, y_tw + n["as_l"])
    delen.append(cyl_y(n["as_d"] / 2, l, 0, y0, R_WIEL))
    onderdelen[f"motor_{kant}"] = Compound(children=delen)

    # beugel: plaat tegen de onderkant van de print + 2 zijwangen rond de tandwielkast
    y0, l = ys(y_tw - bg["b"], y_tw)
    plaat = box(bg["L"], l, bg["t"], -bg["L"] / 2, y0, Z_ONDER - bg["t"])
    wang1 = box(bg["t"], l, n["h"], -n["b"] / 2 - bg["t"], y0, R_WIEL - n["h"] / 2)
    wang2 = box(bg["t"], l, n["h"], n["b"] / 2, y0, R_WIEL - n["h"] / 2)
    onderdelen[f"beugel_{kant}"] = Compound(children=[plaat, wang1, wang2])

    y0, l = ys(Y_WIEL_IN, Y_WIEL_IN + w["b"])
    band = cyl_y(R_WIEL, l, 0, y0, R_WIEL) - cyl_y(R_WIEL - 3, l, 0, y0, R_WIEL)
    velg = cyl_y(R_WIEL - 3, l, 0, y0, R_WIEL) - cyl_y(4, l, 0, y0, R_WIEL)
    naaf = cyl_y(4, l, 0, y0, R_WIEL) - cyl_y(n["as_d"] / 2, l, 0, y0, R_WIEL)
    onderdelen[f"wiel_{kant}"] = Compound(children=[band, velg, naaf])

# ball caster (kop naar beneden) + afstandsstukken tot tegen de print
c = M["caster"]
flens_z = c["H"] - c["flens"]
kogel = Pos(X_CASTER, 0, c["kogel"] / 2) * Sphere(c["kogel"] / 2)
huis = cyl_z(c["kogel"] / 2 + 1.2, flens_z - c["kogel"] / 2, X_CASTER, 0, c["kogel"] / 2)
flens = box(c["B"], c["L"] - 2 * 2.8, c["flens"], X_CASTER - c["B"] / 2, -c["L"] / 2 + 2.8, flens_z) \
    + cyl_z(2.8, c["flens"], X_CASTER, -c["gat_afst"] / 2, flens_z) \
    + cyl_z(2.8, c["flens"], X_CASTER, c["gat_afst"] / 2, flens_z)       # gaten dwars (langs Y)
onderdelen["ball_caster"] = Compound(children=[kogel, huis, flens])
onderdelen["caster_afstandsstukken"] = Compound(children=[
    cyl_z(2.0, Z_ONDER - c["H"], X_CASTER, dy, c["H"]) for dy in (-c["gat_afst"] / 2, c["gat_afst"] / 2)])

# QTR-8A onder de voorrand, sensoren naar beneden op 3 mm
q = M["qtr"]
z_pcb = q["hoogte"] + q["comp"]
qtr = [box(q["B"], q["L"], q["t"], X_SENSOR - q["B"] / 2, -q["L"] / 2, z_pcb)]
for i in range(8):
    y = (i - 3.5) * q["pitch"]
    qtr.append(box(2.9, 3.6, q["comp"], X_SENSOR - 1.45, y - 1.8, q["hoogte"]))
onderdelen["QTR-8A"] = Compound(children=qtr)
x_gat = X_SENSOR - q["B"] / 2 + q["gat_rand"]
onderdelen["M2_bevestiging_sensor"] = Compound(children=[
    cyl_z(1.0, Z_BOVEN + 1.5 - z_pcb, x_gat, y, z_pcb) for y in (-q["gat_afst"] / 2, q["gat_afst"] / 2)]
    + [cyl_z(1.9, 1.5, x_gat, y, Z_BOVEN) for y in (-q["gat_afst"] / 2, q["gat_afst"] / 2)])

# bovenzijde: batterij boven de as, elektronica ervoor
lp = M["lipo"]
onderdelen["LiPo_2S_450mAh"] = box(lp["B"], lp["L"], lp["H"], P_ACHTER + 1, -lp["L"] / 2, Z_BOVEN)
x30 = M["xt30"]
onderdelen["XT30"] = box(x30["L"], x30["B"], x30["H"], P_ACHTER + 1 + lp["B"] + 5, 27, Z_BOVEN)

e = M["esp32"]
x_esp = P_VOOR - 2 - e["L"]
z_esp = Z_BOVEN + e["header"]
onderdelen["ESP32-S3_devkit"] = Compound(children=[
    box(e["L"], e["B"], e["t"], x_esp, -e["B"] / 2, z_esp),
    box(e["mod_L"], e["mod_B"], e["mod_h"], x_esp + 4, -e["mod_B"] / 2, z_esp + e["t"]),
    box(7.5, 9.0, 3.2, x_esp + e["L"] - 6.5, 2.5, z_esp + e["t"]),     # USB-C 1
    box(7.5, 9.0, 3.2, x_esp + e["L"] - 6.5, -11.5, z_esp + e["t"]),   # USB-C 2
] + [box(2.5, 2.5, e["header"], x_esp + 1.3 + 2.54 * i, y - 1.25, Z_BOVEN)
     for i in range(22) for y in (-e["rij_afst"] / 2, e["rij_afst"] / 2)])

tb = M["tb6612"]
x_elek = P_ACHTER + 1 + lp["B"] + 5     # vrije strook x 3..8 voor de motorkabels
onderdelen["TB6612FNG"] = box(tb["L"], tb["B"], tb["t"], x_elek, -4 - tb["B"], Z_BOVEN + tb["header"])   # rechts, naast ESP32-rij J1
bk = M["buck"]
onderdelen["buck_CN3903_3V3"] = box(bk["L"], bk["B"], bk["h"], x_elek, 4, Z_BOVEN)                              # links

sw = M["ss12d00"]
onderdelen["aan_uit_schakelaar"] = Compound(children=[
    box(sw["L"], sw["B"], sw["H"], x_elek + 2, Y_RAND - sw["B"], Z_BOVEN),
    box(1.5, sw["hendel"], 1.5, x_elek + 2 + sw["L"] / 2 - 0.75, Y_RAND, Z_BOVEN + 1)])
kn = M["knop"]
onderdelen["start_stop_knop"] = Compound(children=[
    box(kn["L"], kn["B"], 3.5, x_esp + 20, Y_RAND - kn["B"] - 1, Z_BOVEN),
    cyl_z(1.75, kn["H"] - 3.5, x_esp + 23, Y_RAND - kn["B"] / 2 - 1, Z_BOVEN + 3.5)])
el = M["elco"]
onderdelen["elco_100uF"] = Compound(children=[
    cyl_z(el["D"] / 2, el["H"], x_elek + tb["L"] + 5, -30, Z_BOVEN),     # C1 bij VM van de TB6612
    cyl_z(el["D"] / 2, el["H"], x_esp - 2.5, -19, Z_BOVEN)])             # C2 bij 3V3 van de ESP32

# spoiler (specs): het afgezaagde stuk gaatjesprint (30 x 90) op 2 M3-bouten achteraan
sp = M["spoiler"]
SPOILER_B, SPOILER_L, SPOILER_Z = sp["B"], sp["L"], Z_BOVEN + sp["hoogte"]
onderdelen["spoiler"] = box(SPOILER_B, SPOILER_L, p["t"], P_ACHTER, -SPOILER_L / 2, SPOILER_Z)
onderdelen["spoiler_bouten"] = Compound(children=[
    cyl_z(1.5, SPOILER_Z + p["t"] + 2 - (Z_ONDER - 2), P_ACHTER + 3, y, Z_ONDER - 2) for y in (-34.0, 34.0)])   # naast batterij, vrij van de beugelbouten

# ----------------------------------------------------------------------------- export
for naam, deel in onderdelen.items():
    export_stl(deel, str(UIT / f"{naam}.stl"))
export_step(Compound(children=list(onderdelen.values())), str(UIT / "linefollower_assembly.step"))

alles = Compound(children=list(onderdelen.values())).bounding_box()
print(f"L x B x H = {alles.size.X:.1f} x {alles.size.Y:.1f} x {alles.size.Z:.1f} mm")
print(f"sensorlijn {X_SENSOR:.1f} mm voor de as | print onderkant {Z_ONDER:.1f} mm | caster x={X_CASTER:.1f}")
print(f"x_elek={x_elek:.1f} x_esp={x_esp:.1f}")
print(f"spoorbreedte (wielmidden) {2 * (Y_WIEL_IN + M['wiel']['b'] / 2):.1f} mm")
