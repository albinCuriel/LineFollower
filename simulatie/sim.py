"""sim.py - simulatie van de linefollower op parcours 3, met de ECHTE firmwareregelaar (code/lib/lf_core).

Gebruik (vanuit deze map):
  uv run --no-project --with numpy,scipy,matplotlib,svgpathtools,ziglang python sim.py          -> 1 ronde met de standaardparameters
  uv run --no-project --with numpy,scipy,matplotlib,svgpathtools,ziglang python sim.py tune     -> parameters zoeken
  ... python sim.py set kp=0.02 kd=0.0006 vrecht=1.8                                             -> 1 ronde met eigen waarden

Software-in-the-loop: lf_core wordt met zig/clang gecompileerd tot lf_sim.dll en via ctypes aangeroepen.
Wat de simulatie oplevert, kan je 1-op-1 als parameters op de robot zetten ("set kp 0.02").

Model (eenheden SI, posities in mm voor het raster):
- sensoren: 8 x QRE1113, 9,525 mm uit elkaar, 98,7 mm voor de wielas, meetvlek r = 2 mm
- motoren: GA12-N20 10:1, 2,51 m/s onbelast @ 6 V, trekkracht 0,8 N @ 6 V (blokkeerkoppel 0,013 Nm / r 16 mm)
- grip: mu = 0,9 (siliconen), gewichtsverdeling uit de tekening (massa_zwaartepunt.txt), zijdelings mu*g
- encoders: 280 tellen per wieltoer, snelheid gemeten over 10 ms (zoals in de firmware)
"""
import ctypes
import math
import pathlib
import subprocess
import sys

import numpy as np
from scipy import ndimage

import baan

HIER = pathlib.Path(__file__).parent
CORE = HIER.parent / "code" / "lib" / "lf_core" / "src"
DLL = HIER / "lf_sim.dll"

# ------------------------------------------------------------------ robot (maten uit het 3D-model)
SENSOR_AFSTAND = 98.7      # mm voor de wielas
PITCH = 9.525              # mm
SPOOR = 0.099              # m
# massa en gewichtsverdeling: berekend door mechanisch/teken_aanzichten.py uit het 3D-model
_MZ = dict(l.split("=") for l in (HIER.parent / "technische tekeningen" / "mechanisch" / "massa_zwaartepunt.txt")
           .read_text().split())
MASSA = float(_MZ["massa_g"]) / 1000          # kg
AANDEEL_WIELEN = float(_MZ["aandeel_wielen"])  # deel van het gewicht op de aangedreven wielen
J = MASSA * 0.040 ** 2     # kg m^2
MU = 0.9
G = 9.81
V_NL_6V = 2.51             # m/s onbelast bij 6 V
F_STALL_6V = 0.8           # N per wiel bij 6 V
F_WRIJVING = 0.04          # N per wiel
VBAT = 7.6
CYCLUS = 0.001             # s (firmware cyclus_us = 1000)
SUBSTAP = 4
TELLEN = 280
WIEL_OMTREK = math.pi * 0.032


def bouw_dll():
    bronnen = list(CORE.glob("*.h")) + [HIER / "lf_sim_api.cpp"]
    if DLL.exists() and DLL.stat().st_mtime > max(b.stat().st_mtime for b in bronnen):
        return
    print("lf_core compileren -> lf_sim.dll")
    subprocess.check_call([sys.executable, "-m", "ziglang", "c++", "-shared", "-O2", "-std=c++17",
                           "-o", str(DLL), str(HIER / "lf_sim_api.cpp"), "-I", str(CORE)])


class Firmware:
    def __init__(self):
        if not DLL.exists():   # (her)bouwen gebeurt enkel in het hoofdproces, zie __main__
            bouw_dll()
        self.lib = lib = ctypes.CDLL(str(DLL))
        lib.lf_nieuw.restype = ctypes.c_void_p
        lib.lf_zet.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_float]
        lib.lf_lees.argtypes = [ctypes.c_void_p, ctypes.c_char_p]; lib.lf_lees.restype = ctypes.c_float
        lib.lf_kalibreer.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
        lib.lf_start.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.lf_stap.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.c_float, ctypes.c_float,
                                ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float)]
        lib.lf_weg.argtypes = [ctypes.c_void_p]
        self.h = lib.lf_nieuw()
        self.refl = (ctypes.c_float * 8)()
        self.uit = (ctypes.c_float * 6)()

    def zet(self, **kw):
        for k, v in kw.items():
            if not self.lib.lf_zet(self.h, k.encode(), float(v)):
                raise KeyError(k)

    def lees(self, k):
        return self.lib.lf_lees(self.h, k.encode())

    def kalibreer(self, wit, zwart):
        self.lib.lf_kalibreer(self.h, (ctypes.c_float * 8)(*wit), (ctypes.c_float * 8)(*zwart))

    def start(self, aan=True):
        self.lib.lf_start(self.h, int(aan))

    def stap(self, refl, dt, vbat, vl, vr):
        for i in range(8):
            self.refl[i] = refl[i]
        self.lib.lf_stap(self.h, self.refl, dt, vbat, vl, vr, self.uit)
        return list(self.uit)

    def __del__(self):
        try:
            self.lib.lf_weg(self.h)
        except Exception:
            pass


class Baan:
    def __init__(self, naam="parcours3"):
        z, self.x0, self.y0 = baan.laad(naam)
        r = int(round(2.0 / baan.RES))
        yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
        disc = (xx ** 2 + yy ** 2 <= r * r).astype(np.float32)
        self.dekking = ndimage.convolve(z, disc / disc.sum(), mode="constant")   # zwart-fractie onder elke sensor
        self.afst_buiten = ndimage.distance_transform_edt(z < 0.5) * baan.RES    # mm tot de lijn
        self.zwart = z

    def _idx(self, x, y):
        c = np.clip(((np.asarray(x) - self.x0) / baan.RES).astype(int), 0, self.zwart.shape[1] - 1)
        r = np.clip(((np.asarray(y) - self.y0) / baan.RES).astype(int), 0, self.zwart.shape[0] - 1)
        return r, c

    def dekking_op(self, x, y):
        r, c = self._idx(x, y)
        return self.dekking[r, c]

    def afstand_tot_lijn(self, x, y):
        r, c = self._idx(x, y)
        return self.afst_buiten[r, c]


START = (300.0, 57.0, 0.0)   # mm, mm, rad: onderste rechte stuk, naar rechts (zie baan_parcours3)


def rij(params=None, seed=0, mismatch=0.0, max_t=25.0, log=False, baan_obj=None):
    """Een ronde rijden. mismatch = relatief verschil tussen de motoren links/rechts (bv. 0.08)."""
    rng = np.random.default_rng(seed)
    b = baan_obj or Baan()
    fw = Firmware()
    if params:
        fw.zet(**params)
    # sensoren: elk een eigen gevoeligheid (zoals echte QRE1113's)
    wit = 2700 + rng.normal(0, 150, 8)
    zwart = 250 + rng.normal(0, 40, 8)
    fw.kalibreer(wit * (1 + rng.normal(0, 0.03, 8)), zwart * (1 + rng.normal(0, 0.05, 8)))
    sens_y = (3.5 - np.arange(8)) * PITCH          # sensor 1 = links (+y)
    mot = np.array([1 - mismatch / 2, 1 + mismatch / 2])
    x, y, th = START
    v = w = 0.0
    afst = [0.0, 0.0]; tellen_hist = [[0.0] * 11, [0.0] * 11]
    t = 0.0; afgelegd = 0.0; buiten = 0.0
    fw.start(True)
    L = {"t": [], "x": [], "y": [], "v": [], "pos": [], "fout": [], "vdoel": [], "sx": [], "sy": []} if log else None
    start_s = (x + SENSOR_AFSTAND * math.cos(th), y + SENSOR_AFSTAND * math.sin(th))
    vorig_s = start_s; lijn_afgelegd = 0.0
    max_fout = 0.0
    kwijt = 0.0   # s dat de sensoren de lijn niet zagen
    rand = 0.0    # s dat de lijn aan de rand van de sensorbalk lag
    while t < max_t:
        # --- sensoren
        c, s = math.cos(th), math.sin(th)
        sx = x + SENSOR_AFSTAND * c - sens_y * s
        sy = y + SENSOR_AFSTAND * s + sens_y * c
        dek = b.dekking_op(sx, sy)
        refl = wit - (wit - zwart) * dek + rng.normal(0, 25, 8)
        # --- encoders: tellen over 10 ms venster
        vmeet = []
        for i in range(2):
            tellen = math.floor(afst[i] / (WIEL_OMTREK / TELLEN))
            tellen_hist[i] = tellen_hist[i][1:] + [tellen]
            vmeet.append((tellen_hist[i][-1] - tellen_hist[i][0]) * (WIEL_OMTREK / TELLEN) / 0.010)
        dl, dr, pos, vdoel, dv, lijn = fw.stap(refl, CYCLUS, VBAT, vmeet[0], vmeet[1])
        # --- fysica
        h = CYCLUS / SUBSTAP
        for _ in range(SUBSTAP):
            vl, vr = v - w * SPOOR / 2, v + w * SPOOR / 2
            F = []
            for i, (duty, vw) in enumerate(((dl, vl), (dr, vr))):
                f = F_STALL_6V * mot[i] * (duty * VBAT / 6.0 - vw / (V_NL_6V * mot[i]))
                f -= F_WRIJVING * math.copysign(1, vw) if abs(vw) > 1e-3 else 0
                fmax = MU * AANDEEL_WIELEN * MASSA * G / 2
                F.append(max(-fmax, min(fmax, f)))
                afst[i] += abs(vw) * h
            v += (F[0] + F[1]) / MASSA * h
            w += (F[1] - F[0]) * SPOOR / 2 / J * h
            w_eff = w
            if abs(v * w) > MU * G:                 # zijdelings slippen: minder draaien dan gevraagd
                w_eff = math.copysign(MU * G / max(abs(v), 1e-3), w)
            th += w_eff * h
            x += v * math.cos(th) * h * 1000
            y += v * math.sin(th) * h * 1000
            afgelegd += abs(v) * h
        t += CYCLUS
        # --- ligt de robot nog op de baan?
        mid_x, mid_y = x + SENSOR_AFSTAND * math.cos(th), y + SENSOR_AFSTAND * math.sin(th)
        fout = float(b.afstand_tot_lijn(mid_x, mid_y))
        lijn_afgelegd += math.hypot(mid_x - vorig_s[0], mid_y - vorig_s[1]) / 1000
        vorig_s = (mid_x, mid_y)
        max_fout = max(max_fout, fout)
        buiten = buiten + CYCLUS if fout > 40 else 0
        kwijt += CYCLUS if lijn < 0.5 else 0
        rand += CYCLUS if abs(pos) > 26 else 0      # lijn onder de buitenste sensor = geen marge meer
        if L is not None:
            for k, val in zip(L, (t, x, y, v, pos, fout, vdoel, mid_x, mid_y)):
                L[k].append(val)
        if buiten > 0.15:
            return dict(ok=False, t=t, afgelegd=lijn_afgelegd, max_fout=max_fout, kwijt=kwijt, rand=rand, log=L, reden="van de baan")
        if lijn_afgelegd > 6.0 and math.hypot(mid_x - start_s[0], mid_y - start_s[1]) < 25:
            return dict(ok=True, t=t, afgelegd=lijn_afgelegd, max_fout=max_fout, kwijt=kwijt, rand=rand, log=L, reden="ronde")
    return dict(ok=False, t=t, afgelegd=lijn_afgelegd, max_fout=max_fout, kwijt=kwijt, rand=rand, log=L, reden="tijd op")


def plot(res, b, titel, bestand):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    L = res["log"]
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_axes([0.03, 0.08, 0.55, 0.84])
    ext = [b.x0, b.x0 + b.zwart.shape[1] * baan.RES, b.y0, b.y0 + b.zwart.shape[0] * baan.RES]
    ax.imshow(b.zwart, origin="lower", cmap="Greys", extent=ext, alpha=0.35)
    ax.plot(L["x"], L["y"], color="#9e9e9e", lw=0.6, ls="--", label="wielas")
    sc = ax.scatter(L["sx"][::4], L["sy"][::4], c=L["v"][::4], cmap="turbo", s=3, vmin=0, vmax=max(2.0, max(L["v"])),
                    label="midden sensorbalk")
    ax.legend(loc="upper right", fontsize=8)
    fig.colorbar(sc, ax=ax, label="snelheid (m/s)", shrink=0.7)
    ax.plot(*START[:2], "g^", ms=12)
    ax.set_aspect("equal"); ax.set_title(titel, loc="left", fontweight="bold")
    ax.set_xlabel("mm"); ax.set_ylabel("mm")
    a2 = fig.add_axes([0.64, 0.56, 0.34, 0.36])
    a2.plot(L["t"], L["v"], label="snelheid robot"); a2.plot(L["t"], L["vdoel"], "--", label="doel (profiel)")
    a2.set_ylabel("m/s"); a2.legend(fontsize=8); a2.grid(alpha=0.3)
    a3 = fig.add_axes([0.64, 0.08, 0.34, 0.38])
    a3.plot(L["t"], L["pos"], lw=0.7, label="lijnpositie volgens sensoren (mm)")
    a3.plot(L["t"], L["fout"], lw=0.7, label="echte afstand tot lijn (mm)")
    a3.set_xlabel("tijd (s)"); a3.legend(fontsize=8); a3.grid(alpha=0.3)
    fig.savefig(bestand, dpi=110)
    plt.close(fig)


ZOEKRUIMTE = {  # parameter: (min, max), log-schaal voor kp/kd
    "kp": (0.01, 0.12), "ki": (0.001, 3.0), "kd": (0.0001, 0.008), "vbocht": (0.6, 1.6), "vrecht": (1.0, 3.0),
    "erecht": (2.0, 15.0), "ebocht": (5.0, 35.0), "drem": (100, 2000), "aboost": (2.0, 12.0),
}
SEEDS = (1, 2, 3)
_BAAN = None


def _init():
    global _BAAN
    _BAAN = Baan()


def score(params, b=None, seeds=SEEDS):
    """Robuust en vloeiend: gemiddelde rondetijd over runs met ruis en motorverschil (-6 %, 0, +6 %),
    + 4 s straf per mislukte run (minder als hij al ver kwam), + kleine straf voor grote afwijking."""
    b = b or _BAAN
    tot, mislukt = 0.0, 0
    for s in seeds:
        r = rij(params, seed=s, mismatch=0.06 * (s - 2), baan_obj=b, max_t=15)
        if r["ok"]:
            tot += r["t"] + 0.03 * r["max_fout"] + 8 * r["kwijt"] + 4 * r["rand"]
        else:
            mislukt += 1
            tot += 15 + 4 * (1 - min(r["afgelegd"] / 7.0, 1))
    return tot / len(seeds), mislukt


def _eval(params):
    sc, m = score(params)
    return sc, m, params


def tune(n_willekeurig=700, n_verfijn=8):
    from concurrent.futures import ProcessPoolExecutor
    import os
    rng = np.random.default_rng(42)

    def trek():
        p = {}
        for k, (lo, hi) in ZOEKRUIMTE.items():
            p[k] = float(np.exp(rng.uniform(np.log(lo), np.log(hi))) if k in ("kp", "ki", "kd", "drem") else rng.uniform(lo, hi))
        p["vrecht"] = max(p["vrecht"], p["vbocht"])
        return p

    with ProcessPoolExecutor(max_workers=max(2, (os.cpu_count() or 4) - 1), initializer=_init) as ex:
        kand = [dict(kp=0.02, ki=0.01, kd=0.0006, vbocht=0.9, vrecht=1.6, erecht=4, ebocht=9, drem=400, aboost=6)]
        kand += [trek() for _ in range(n_willekeurig)]
        res = sorted(ex.map(_eval, kand), key=lambda r: r[0])
        print("willekeurig zoeken: beste", [round(r[0], 3) for r in res[:5]])
        best_s, _, best = res[0]
        # verfijnen rond de beste: telkens 3*cpu kandidaten met steeds kleinere stappen
        schaal = 0.15
        for ronde in range(n_verfijn):
            buren = []
            for _ in range(3 * (os.cpu_count() or 4)):
                p = {k: v * float(np.exp(rng.normal(0, schaal))) for k, v in best.items()}
                p["vrecht"] = max(p["vrecht"], p["vbocht"])
                buren.append(p)
            for sc, m, p in ex.map(_eval, buren):
                if sc < best_s:
                    best_s, best = sc, p
            print(f"verfijnen ronde {ronde + 1}: {best_s:.3f}")
            schaal *= 0.6
    return best, best_s


if __name__ == "__main__":
    bouw_dll()
    b = Baan()
    if len(sys.argv) > 1 and sys.argv[1] == "tune":
        best, s = tune()
        veilig = dict(best, vbocht=best["vbocht"] * 0.9, vrecht=best["vrecht"] * 0.9)
        r = rij(veilig, seed=7, mismatch=0.05, log=True, baan_obj=b)
        plot(r, b, f"Getunede parameters (90 % van de max. snelheid): ronde {r['t']:.2f} s", HIER / "resultaat_tune.png")
        regels = ["# Simulatie: getunede parameters", "",
                  f"Beste score: **{s:.2f} s** (gemiddelde over 3 runs met sensorruis en -6/0/+6 % motorverschil).",
                  f"Met 90 % van die snelheden (startwaarden voor de echte robot): **{r['t']:.2f} s**, "
                  f"gemiddeld {r['afgelegd'] / r['t']:.2f} m/s.", "",
                  "Op de robot zetten (wifi-terminal of seriële monitor):", "```"]
        regels += [f"set {k} {v:.4g}" for k, v in veilig.items()] + ["save", "```", "",
                   "![resultaat](resultaat_tune.png)"]
        (HIER / "resultaat_tune.md").write_text("\n".join(regels), encoding="utf-8")
        print("\n".join(regels))
    else:
        params = {}
        if len(sys.argv) > 2 and sys.argv[1] == "set":
            params = {k: float(v) for k, v in (a.split("=") for a in sys.argv[2:])}
        r = rij(params, seed=7, log=True, baan_obj=b)
        print(f"{r['reden']}: {r['t']:.2f} s, {r['afgelegd']:.2f} m, gem. {r['afgelegd'] / r['t']:.2f} m/s, "
              f"max. afwijking {r['max_fout']:.1f} mm, lijn kwijt {r['kwijt']:.2f} s, aan de rand {r['rand']:.2f} s")
        plot(r, b, f"{r['reden']}: {r['t']:.2f} s  ({r['afgelegd'] / r['t']:.2f} m/s gemiddeld)", HIER / "resultaat.png")
