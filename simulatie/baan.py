"""baan.py - parcours (SVG) -> zwart/wit-raster in mm, voor het sensormodel van de simulatie.

Het parcours van de docent is getekend als gevulde vormen (lijn 15 mm breed) in px op 96 dpi.
We rasteren op RES mm per pixel. Resultaat wordt gecachet in baan_<naam>.npz.
"""
import pathlib
import numpy as np

HIER = pathlib.Path(__file__).parent
PX_PER_MM = 96 / 25.4
RES = 0.5  # mm per pixel


def _polygonen(svg):
    from svgpathtools import Document
    doc = Document(str(svg))
    polys = []
    for pad in doc.paths():
        if len(pad) == 0:
            continue
        for deel in pad.continuous_subpaths():
            n = max(8, int(deel.length() / 2))
            pts = np.array([deel.point(t) for t in np.linspace(0, 1, n)])
            polys.append(np.c_[pts.real, pts.imag] / PX_PER_MM)
    return polys


def laad(naam="parcours3"):
    cache = HIER / f"baan_{naam}.npz"
    if cache.exists():
        d = np.load(cache)
        return d["zwart"], float(d["x0"]), float(d["y0"])
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    polys = _polygonen(HIER.parent / "parcours" / f"{naam}.svg")
    alle = np.vstack(polys)
    x0, y0 = alle.min(0) - 60
    x1, y1 = alle.max(0) + 60
    w, h = int((x1 - x0) / RES), int((y1 - y0) / RES)
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    for p in polys:
        ax.add_patch(Polygon(p, closed=True, fc="k", ec="k", lw=0, antialiased=False))
    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba())[:, :, 0]
    plt.close(fig)
    zwart = (img[::-1] < 128).astype(np.float32)   # rij 0 = y0 (onderaan)
    np.savez_compressed(cache, zwart=zwart, x0=x0, y0=y0)
    return zwart, x0, y0


if __name__ == "__main__":
    z, x0, y0 = laad()
    print("raster", z.shape, "zwart", z.sum() * RES ** 2 / 15 / 1000, "m lijn (oppervlak/15 mm)")
