"""perfplan.py - duidelijk bekabelingsplan voor een gaatjesprint (perfboard), stap per stap.

Herbruikbaar: alle projectgegevens zitten in een config-module (zie voorbeeld_config.py).
Uitvoer:
  <prefix>.pdf                 alle pagina's (A3 liggend): plaatsing, 1 pagina per bouwstap, overzicht
  <prefix>_p<NN>_<naam>.png    elke pagina apart (voor readme / instructable)
  <prefix>_boormal_1op1.pdf    bovenaanzicht op ware grootte (A4, afdrukken op 100 %)
  <prefix>_draadlijst.md       afvinklijst per stap met gatcoordinaten en lengtes

Gebruik:
  py -3 perfplan.py <config.py> [uitvoermap]

Conventies
- Gat = rij (letter, A = bovenrand in BOVENaanzicht) + kolom (nummer, 1 = linkerrand in bovenaanzicht).
  Voorbeeld "F22". Rijen na Z: AA, AB, ...
- Bovenaanzicht = componentenkant. Onderaanzicht = soldeerkant, gespiegeld rond de lange as
  (kolom 1 blijft links, rij A ligt nu ONDERAAN). Letters/nummers staan op alle randen.
- Draden lopen aan de soldeerkant langs de gatenrijen. Een router (A*) zoekt per draad een pad door
  vrije gaten: niet door pinnen van andere onderdelen, niet door verboden zones (onderdelen aan de
  onderkant), met strafpunten voor bochten en voor kruisen met eerdere draden.
"""
import heapq
import importlib.util
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import matplotlib.patheffects as pe

MM = 1 / 25.4


# ------------------------------------------------------------------ hulpfuncties
def rij_letter(r):
    return chr(65 + r) if r < 26 else "A" + chr(65 + r - 26)


def gat(rc):
    r, c = rc
    return f"{rij_letter(int(r))}{int(c) + 1}"


def laad_config(pad):
    spec = importlib.util.spec_from_file_location("perfplan_config", pad)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Plan:
    def __init__(self, cfg):
        self.cfg = cfg
        self.R, self.C = cfg.BOARD["rijen"], cfg.BOARD["kolommen"]
        self.parts = {p["naam"]: p for p in cfg.PARTS}
        self.pin_eigenaar = {}
        for p in cfg.PARTS:
            for pin, rc in p["pins"].items():
                self.pin_eigenaar[tuple(rc)] = (p["naam"], pin)
        self.routes = {}
        self.banen = {}  # stukje gatenrij -> draden die erover lopen
        self._route_alles()

    # ---------------------------------------------------------- adressen
    def punt(self, ref):
        """'ESP.J1-1' -> (r, c); of direct een gat 'F22' / tuple."""
        if isinstance(ref, tuple):
            return ref
        deel, pin = ref.split(".", 1)
        return tuple(self.parts[deel]["pins"][pin])

    def naam(self, ref):
        deel, pin = ref.split(".", 1)
        p = self.parts[deel]
        lab = p.get("pinlabels", {}).get(pin)
        return f"{p.get('kort', deel)} {pin}" + (f" ({lab})" if lab and lab != pin else "")

    # ---------------------------------------------------------- routing
    def _geblokkeerd(self):
        blok = set(self.pin_eigenaar)
        for (r0, c0, r1, c1, *_rest) in self.cfg.KEEPOUTS:
            for r in range(self.R):
                for c in range(self.C):
                    if r0 <= r <= r1 and c0 <= c <= c1:
                        blok.add((r, c))
        for (rb, cb, d_mm, _l) in self.cfg.BOORGATEN:   # rond een boorgat/bout/moer: geen draad
            straal = d_mm / self.cfg.BOARD["pitch"] / 2 + 0.9
            for r in range(self.R):
                for c in range(self.C):
                    if (r - rb) ** 2 + (c - cb) ** 2 <= straal ** 2:
                        blok.add((r, c))
        return blok

    def _route_alles(self):
        blok = self._geblokkeerd()
        bezet = {}  # gat -> {"h": n, "v": n}: hoeveel draden er horizontaal / verticaal door lopen
        for d in self.cfg.WIRES:
            nr, stap, a, b, soort = d[:5]
            pa, pb = self.punt(a), self.punt(b)
            if soort == "BRUG":
                pad = [pa, pb]
            else:
                pad = self._astar(pa, pb, blok - {pa, pb}, bezet)
            self.routes[nr] = pad
            for p, q in zip(pad, pad[1:]):
                self.banen.setdefault(tuple(sorted((p, q))), []).append(nr)
            for i in range(1, len(pad) - 1):
                for buur in (pad[i - 1], pad[i + 1]):
                    o = "h" if buur[0] == pad[i][0] else "v"
                    bezet.setdefault(pad[i], {"h": 0, "v": 0})[o] += 1

    def _astar(self, a, b, blok, bezet):
        # Geisoleerde draden mogen kruisen (goedkoop), maar niet samen door dezelfde gatenrij lopen (duur).
        BOCHT, KRUIS, PARALLEL = 3.0, 1.0, 0.8
        h = lambda p: abs(p[0] - b[0]) + abs(p[1] - b[1])
        start = (a, None)
        best = {start: 0.0}
        q = [(h(a), 0.0, a, None, None)]
        vorig = {}
        while q:
            f, g, p, rich, _ = heapq.heappop(q)
            if p == b:
                pad = [p]; s = (p, rich)
                while s in vorig:
                    s = vorig[s]; pad.append(s[0])
                return pad[::-1]
            if g > best.get((p, rich), 1e9):
                continue
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (p[0] + dr, p[1] + dc)
                if not (0 <= n[0] < self.R and 0 <= n[1] < self.C) or (n in blok and n != b):
                    continue
                o = "h" if dr == 0 else "v"
                b_n = bezet.get(n, {"h": 0, "v": 0})
                kost = (1.0 + (BOCHT if rich and rich != (dr, dc) else 0)
                        + PARALLEL * b_n[o] + KRUIS * b_n["v" if o == "h" else "h"])
                s = (n, (dr, dc))
                if g + kost < best.get(s, 1e9):
                    best[s] = g + kost
                    vorig[s] = (p, rich)
                    heapq.heappush(q, (g + kost + h(n), g + kost, n, (dr, dc), None))
        print(f"WAARSCHUWING: geen pad {gat(a)} -> {gat(b)}, rechte lijn getekend")
        return [a, b]

    def lengte(self, nr):
        pad = self.routes[nr]
        stappen = sum(abs(p[0] - q[0]) + abs(p[1] - q[1]) for p, q in zip(pad, pad[1:]))
        return stappen * self.cfg.BOARD["pitch"] + (0 if self._soort(nr) == "BRUG" else 10)

    def _soort(self, nr):
        return next(d[4] for d in self.cfg.WIRES if d[0] == nr)

    # ---------------------------------------------------------- tekenen
    def _xy(self, rc, onder):
        r, c = rc
        return (c, r)  # y-as wordt per aanzicht omgekeerd of niet

    def teken_print(self, ax, onder, stap=None, alles=False):
        cfg, R, C = self.cfg, self.R, self.C
        ax.set_aspect("equal")
        ax.set_xlim(-3.2, C + 2.2)
        if onder:
            ax.set_ylim(-3.2, R + 2.2)       # rij A onderaan
        else:
            ax.set_ylim(R + 2.2, -3.2)       # rij A bovenaan
        ax.axis("off")
        # print
        ax.add_patch(FancyBboxPatch((-0.9, -0.9), C - 0.2, R - 0.2, boxstyle="round,pad=0.1,rounding_size=0.6",
                                    fc="#eef6ee", ec="#2e7d32", lw=1.6, zorder=0))
        # raster
        xs = [c for r in range(R) for c in range(C)]
        ys = [r for r in range(R) for c in range(C)]
        ax.scatter(xs, ys, s=7, facecolors="white", edgecolors="#9ccc9c", linewidths=0.5, zorder=1)
        for c in range(C):  # kolomnummers
            vet = (c + 1) % 5 == 0
            for y in (-1.9, R + 0.9):
                ax.text(c, y, str(c + 1), ha="center", va="center", fontsize=5.2 if not vet else 6,
                        fontweight="bold" if vet else "normal", color="#1b5e20" if vet else "#558b2f")
        for r in range(R):  # rijletters
            vet = (r + 1) % 5 == 0
            for x in (-1.9, C + 0.9):
                ax.text(x, r, rij_letter(r), ha="center", va="center", fontsize=5.2 if not vet else 6,
                        fontweight="bold" if vet else "normal", color="#1b5e20" if vet else "#558b2f")
        # verboden zones (onderdelen aan de onderkant)
        for (r0, c0, r1, c1, label, *_rest) in cfg.KEEPOUTS:
            ax.add_patch(Rectangle((c0 - 0.45, r0 - 0.45), c1 - c0 + 0.9, r1 - r0 + 0.9, fc="#cfd8dc",
                                   ec="#78909c", lw=0.8, ls="--", alpha=0.55 if onder else 0.25, zorder=1.5,
                                   hatch="////" if onder else None))
            ax.text((c0 + c1) / 2, (r0 + r1) / 2, label, ha="center", va="center", fontsize=6,
                    color="#455a64", zorder=1.6, rotation=90 if (r1 - r0) > 2.5 * (c1 - c0) else 0)
        # boorgaten
        for (r, c, d_mm, label) in cfg.BOORGATEN:
            ax.add_patch(Circle((c, r), d_mm / cfg.BOARD["pitch"] / 2 + 0.15, fc="white", ec="#e65100", lw=1.3, zorder=6))
            ax.plot([c - 0.35, c + 0.35], [r, r], color="#e65100", lw=0.7, zorder=6)
            ax.plot([c, c], [r - 0.35, r + 0.35], color="#e65100", lw=0.7, zorder=6)
        # onderdelen
        for p in cfg.PARTS:
            geplaatst = stap is None or alles or p["stap"] <= stap
            nieuw = stap is not None and p["stap"] == stap and not alles
            r0, c0, r1, c1 = p["omtrek"]
            zelfde_kant = (p.get("kant", "boven") == "onder") == onder
            if not geplaatst:
                stijl = dict(fc="none", ec="#bdbdbd", lw=0.6, ls=":")
            elif zelfde_kant:
                stijl = dict(fc=p["kleur"], ec=p["kleur"], lw=1.4 if nieuw else 1.0, alpha=0.35 if onder else 0.55)
            else:  # doorkijk: onderdeel aan de andere kant
                stijl = dict(fc=p["kleur"], ec=p["kleur"], lw=1.2 if nieuw else 0.9, ls="--", alpha=0.18)
            ax.add_patch(FancyBboxPatch((c0 - 0.45, r0 - 0.45), c1 - c0 + 0.9, r1 - r0 + 0.9,
                                        boxstyle="round,pad=0,rounding_size=0.4", zorder=2, **stijl))
            if nieuw:
                ax.add_patch(FancyBboxPatch((c0 - 0.65, r0 - 0.65), c1 - c0 + 1.3, r1 - r0 + 1.3,
                                            boxstyle="round,pad=0,rounding_size=0.5", fc="none", ec="#d50000",
                                            lw=1.8, zorder=7))
            lx, ly = p.get("labelpos", ((c0 + c1) / 2, (r0 + r1) / 2))
            ax.text(lx, ly, p["label"], ha="center", va="center", fontsize=7.5 if geplaatst else 6,
                    fontweight="bold", color="#212121" if geplaatst else "#bdbdbd", zorder=8,
                    rotation=p.get("labelrot", 0),
                    path_effects=[pe.withStroke(linewidth=2.5, foreground="white")] if geplaatst else None)
            if geplaatst:
                for pin, (r, c) in p["pins"].items():
                    ax.add_patch(Rectangle((c - 0.3, r - 0.3), 0.6, 0.6, fc="#ffca28", ec="#3e2723", lw=0.6, zorder=9))
                    lab = p.get("pinlabels", {}).get(pin, pin)
                    dx, dy = p.get("pinlabel_offsets", {}).get(pin, p.get("pinlabel_offset", (0, -0.75)))
                    if onder:
                        dy = -dy
                    ax.text(c + dx, r + dy, lab, ha="center", va="center", fontsize=4.6, zorder=9.5,
                            rotation=p.get("pinlabel_rot", 0), color="#3e2723",
                            path_effects=[pe.withStroke(linewidth=1.6, foreground="white")])
                if "pin1" in p:
                    r, c = p["pins"][p["pin1"]]
                    ax.add_patch(Circle((c, r), 0.55, fc="none", ec="#d50000", lw=1.2, zorder=9.6))
        # draden
        if onder:
            self._teken_draden(ax, stap, alles)
        # oriëntatie
        voor = cfg.BOARD.get("voorkant", "rechts")
        ax.annotate("", xy=(C + 1.6, R / 2), xytext=(C - 0.2, R / 2),
                    arrowprops=dict(arrowstyle="-|>", lw=2, color="#0d47a1"), zorder=10) if voor == "rechts" else None
        ax.text(C + 1.0, R / 2 - 1.3, "voor", fontsize=7, color="#0d47a1", ha="center", fontweight="bold")

    def _lijn(self, nr):
        """Punten om te tekenen. Draden die hetzelfde stukje gatenrij delen, worden naast elkaar
        verschoven (zoals een bundeltje), zodat elke draad apart te volgen blijft."""
        pad = self.routes[nr]
        if len(pad) == 2 and abs(pad[0][0] - pad[1][0]) + abs(pad[0][1] - pad[1][1]) != 1:
            return [p[1] for p in pad], [p[0] for p in pad]
        xs, ys = [], []
        for p, q in zip(pad, pad[1:]):
            lst = self.banen[tuple(sorted((p, q)))]
            off = (lst.index(nr) - (len(lst) - 1) / 2) * min(0.24, 0.8 / len(lst))
            dr, dc = (off, 0) if p[0] == q[0] else (0, off)
            xs += [p[1] + dc, q[1] + dc]; ys += [p[0] + dr, q[0] + dr]
        return xs, ys

    def _teken_draden(self, ax, stap, alles):
        cfg = self.cfg
        geplaatst = []
        for d in cfg.WIRES:
            nr, st, a, b, soort = d[:5]
            if stap is not None and st > stap and not alles:
                continue
            pad = self.routes[nr]
            xs, ys = self._lijn(nr)
            huidig = alles or stap is None or st == stap
            kl = cfg.KLEUREN[soort][0]
            if not huidig:
                ax.plot(xs, ys, color="#9e9e9e", lw=1.0, alpha=0.55, zorder=3, solid_capstyle="round")
                continue
            lw = 3.2 if soort == "BRUG" else 2.0
            ax.plot(xs, ys, color=kl, lw=lw, zorder=4, solid_capstyle="round", solid_joinstyle="round",
                    path_effects=[pe.Stroke(linewidth=lw + 1.8, foreground="white"), pe.Normal()])
            for (r, c) in (pad[0], pad[-1]):
                ax.add_patch(Circle((c, r), 0.32, fc=kl, ec="white", lw=0.8, zorder=5))
            if soort != "BRUG":
                # nummer op het punt van de draad dat het verst van andere nummers en pinnen ligt
                kand = [(ys[i], xs[i]) for i in range(len(xs))] or [pad[0]]
                def vrij(p):
                    d1 = min((abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in geplaatst), default=99)
                    d2 = min(abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in self.pin_eigenaar)
                    return min(d1, 2.5) * 3 + min(d2, 1.0) - 0.02 * abs(kand.index(p) - len(kand) / 2)
                m = max(kand, key=vrij)
                geplaatst.append(m)
                ax.add_patch(Circle((m[1], m[0]), 0.62, fc="white", ec=kl, lw=1.4, zorder=11))
                ax.text(m[1], m[0], str(nr), ha="center", va="center", fontsize=5.8, fontweight="bold",
                        color="#212121", zorder=12)


# ------------------------------------------------------------------ pagina's
def pagina(plan, titel, sub, onder, stap=None, alles=False, tabel=None, notities=None):
    fig = plt.figure(figsize=(420 * MM, 297 * MM))
    fig.text(0.02, 0.965, titel, fontsize=16, fontweight="bold")
    fig.text(0.02, 0.935, sub, fontsize=9, color="#424242")
    ax = fig.add_axes([0.01, 0.07, 0.69, 0.85])
    plan.teken_print(ax, onder, stap, alles)
    zij = "ONDERZIJDE = soldeerkant (gespiegeld: rij A onderaan)" if onder else "BOVENZIJDE = componentenkant"
    fig.text(0.02, 0.905, zij, fontsize=10, fontweight="bold", color="#b71c1c" if onder else "#1b5e20")
    rechts = fig.add_axes([0.71, 0.07, 0.28, 0.85]); rechts.axis("off")
    y = 1.0
    if tabel:
        kop, rijen, kleuren = tabel
        rechts.text(0, y, kop, fontsize=10, fontweight="bold", va="top"); y -= 0.035
        for i, rij in enumerate(rijen):
            kl = kleuren[i] if kleuren else None
            if kl:
                rechts.add_patch(Rectangle((0, y - 0.024), 0.02, 0.022, fc=kl, ec="k", lw=0.4, transform=rechts.transAxes))
            rechts.text(0.03 if kl else 0, y, rij, fontsize=7.2, va="top", family="DejaVu Sans Mono" if kl else None,
                        transform=rechts.transAxes)
            y -= 0.03 if rij.count("\n") == 0 else 0.03 + 0.021 * rij.count("\n")
    if notities:
        y -= 0.02
        rechts.text(0, y, "Let op", fontsize=10, fontweight="bold", va="top"); y -= 0.033
        for n in notities:
            rechts.text(0, y, "• " + n, fontsize=7.6, va="top", wrap=True); y -= 0.028 + 0.02 * n.count("\n")
    # legende
    leg = [plt.Line2D([], [], color=k, lw=3, label=f"{s.lower()} ({naam})") for s, (k, naam) in plan.cfg.KLEUREN.items()]
    fig.legend(handles=leg, loc="lower left", ncol=6, fontsize=7.5, frameon=False, bbox_to_anchor=(0.02, 0.005))
    fig.text(0.99, 0.01, plan.cfg.BOARD.get("voettekst", ""), fontsize=7, ha="right", color="#757575")
    return fig


def maak_alles(cfg_pad, uit=None):
    cfg = laad_config(cfg_pad)
    uit = pathlib.Path(uit or pathlib.Path(cfg_pad).parent)
    prefix = uit / cfg.BOARD.get("prefix", "bekabelingsplan")
    plan = Plan(cfg)
    pngs = []
    kleurnaam = {s: n for s, (k, n) in cfg.KLEUREN.items()}

    def kort(ref):
        return plan.naam(ref) if not isinstance(ref, tuple) else gat(ref)

    with PdfPages(f"{prefix}.pdf") as pdf:
        def bewaar(fig, naam):
            pdf.savefig(fig)
            png = f"{prefix}_p{len(pngs):02d}_{naam}.png"
            fig.savefig(png, dpi=130)
            plt.close(fig)
            pngs.append(pathlib.Path(png).name)

        # 0. plaatsing
        rijen, kleuren = [], []
        for p in sorted(cfg.PARTS, key=lambda p: p["stap"]):
            ref = p.get("pin1", next(iter(p["pins"])))
            rijen.append(f"stap {p['stap']:>2}  {p['label'].replace(chr(10), ' ')[:22]:<22} {ref} -> {gat(p['pins'][ref])}")
            kleuren.append(p["kleur"])
        bewaar(pagina(plan, cfg.BOARD["titel"] + " - plaatsing", cfg.BOARD.get("plaatsing_uitleg", ""),
                      onder=False, tabel=("Onderdeel  ·  referentiepin -> gat", rijen, kleuren),
                      notities=cfg.BOARD.get("plaatsing_notities")), "plaatsing")
        # 1..n per stap
        for stap, (titel, uitleg, notities) in cfg.STAPPEN.items():
            draden = [d for d in cfg.WIRES if d[1] == stap]
            if not draden and not any(p["stap"] == stap for p in cfg.PARTS):
                continue
            rijen, kleuren = [], []
            for d in draden:
                nr, _, a, b, soort = d[:5]
                opm = d[5] if len(d) > 5 else ""
                rij = (f"{nr:>2} {gat(plan.punt(a)):>4} {kort(a)[:18]:<18}\n"
                       f"   {gat(plan.punt(b)):>4} {kort(b)[:18]:<18} {plan.lengte(nr):>3.0f}mm")
                if opm:
                    rij += f"\n   {opm[:40]}"
                rijen.append(rij); kleuren.append(cfg.KLEUREN[soort][0])
            bewaar(pagina(plan, f"Stap {stap} - {titel}", uitleg, onder=True, stap=stap,
                          tabel=(f"Draden stap {stap}  (nr  gat  pin / gat  pin  lengte)", rijen, kleuren),
                          notities=notities), f"stap{stap:02d}")
        # overzicht
        bewaar(pagina(plan, cfg.BOARD["titel"] + " - alle draden", "Controleblad: alle draden samen.", onder=True,
                      alles=True), "alles")

    # boormal 1:1 (A4 liggend)
    fig = plt.figure(figsize=(297 * MM, 210 * MM))
    P = cfg.BOARD["pitch"]
    w, h = (plan.C + 5.4) * P, (plan.R + 5.4) * P
    ax = fig.add_axes([(297 - w) / 2 / 297, (210 - h) / 2 / 210, w / 297, h / 210])
    plan.teken_print(ax, onder=False)
    ax.set_aspect("auto")
    fig.text(0.03, 0.95, cfg.BOARD["titel"] + " - BOORMAL 1:1 (afdrukken op 100 %, bovenzijde)", fontsize=11, fontweight="bold")
    fig.text(0.03, 0.92, f"Controle: 10 gaten = {10 * P:.1f} mm. Oranje kruis = boren, rode cirkel = pin 1.", fontsize=8)
    fig.savefig(f"{prefix}_boormal_1op1.pdf"); fig.savefig(f"{prefix}_boormal_1op1.png", dpi=150); plt.close(fig)

    # draadlijst markdown
    md = [f"# Draadlijst - {cfg.BOARD['titel']}", "",
          f"Automatisch gemaakt door `perfplan.py`. Plaatjes per stap: zie hieronder. Volledige PDF: [{prefix.name}.pdf]({prefix.name}.pdf).",
          "Gat = rij (letter) + kolom (nummer), zoals op de randen van de tekening. Lengte = afgeknipte draad incl. 2× 5 mm strippen.", ""]
    for stap, (titel, uitleg, notities) in cfg.STAPPEN.items():
        draden = [d for d in cfg.WIRES if d[1] == stap]
        nieuw = [p["label"].replace("\n", " ") for p in cfg.PARTS if p["stap"] == stap]
        png = next((p for p in pngs if f"stap{stap:02d}" in p), None)
        if not draden and not nieuw:
            continue
        md += [f"## Stap {stap} - {titel}", "", uitleg, ""]
        if nieuw:
            md += ["Plaatsen: " + ", ".join(nieuw), ""]
        if png:
            md += [f"![stap {stap}]({png})", ""]
        if draden:
            md += ["| ✓ | nr | van | gat | naar | gat | kleur | lengte | opmerking |", "|---|---|---|---|---|---|---|---|---|"]
            for d in draden:
                nr, _, a, b, soort = d[:5]
                opm = d[5] if len(d) > 5 else ""
                md.append(f"| ☐ | {nr} | {kort(a)} | **{gat(plan.punt(a))}** | {kort(b)} | **{gat(plan.punt(b))}** | "
                          f"{kleurnaam[soort]} | {plan.lengte(nr):.0f} mm | {opm} |")
            md.append("")
        if notities:
            md += ["Let op:"] + [f"- {n}" for n in notities] + [""]
    pathlib.Path(f"{prefix}_draadlijst.md").write_text("\n".join(md), encoding="utf-8")
    print(f"klaar: {len(pngs)} pagina's, {len(cfg.WIRES)} draden ->", prefix)
    return pngs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    maak_alles(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
