"""Bouwt linefollower_planA.kicad_pcb uit het schema (netlijst) met KiCad's pcbnew-API.

Gebruik (KiCad 10):
  kicad-cli sch export netlist --format kicadxml -o planA.xml linefollower_planA.kicad_sch
  "<KiCad>/bin/python.exe" bouw_pcb.py planA.xml
Daarna routeren met Freerouting (zie readme.md).

Coordinaten in mm. y = 0 is de VOORKANT van de robot (sensoren), x = 0 is links.
"""
import os
import sys
import xml.etree.ElementTree as ET

import pcbnew

HIER = os.path.dirname(os.path.abspath(__file__))
FPDIR = os.environ.get("KICAD_FP_DIR",
                       r"C:\Users\Albin\AppData\Local\Programs\KiCad\10.0\share\kicad\footprints")
BREED, LANG = 100.0, 130.0

# ---- plaatsing: ref -> (x, y, rotatie, onderkant?)
PLAATS = {
    # sensoren: onderkant, 9,5 mm steek (zoals de QTR-8A), lichtrichting naar de vloer
    **{f"Q{i+1}": (50 + (i - 3.5) * 9.5, 5.0, 0, True) for i in range(8)},
    **{f"R{10+i}": (50 + (i - 3.5) * 9.5 - 2.4, 13.0, 90, False) for i in range(8)},
    **{f"R{22+i}": (50 + (i - 3.5) * 9.5 + 2.4, 13.0, 90, False) for i in range(8)},
    "Q9": (50, 21, 0, False), "R6": (44, 21, 0, False), "R7": (56, 21, 0, False),
    # ESP32-S3-module: antenne naar de linkerrand (rot 90)
    "U1": (14.0, 55.0, 90, False),
    "C6": (31, 44, 0, False), "C7": (31, 48, 0, False),
    "R4": (10, 74, 0, False), "C8": (10, 78, 0, False), "SW4": (20, 76, 0, False),
    "R5": (10, 84, 0, False), "SW3": (20, 85, 0, False),
    "J5": (40, 70, 90, False),
    "D3": (40, 32, 0, False), "C9": (47, 32, 0, False),
    "SW2": (90, 48, 0, False),
    # motorsturing
    "U3": (74, 86, 0, False),
    "C10": (64, 80, 90, False), "C11": (64, 86, 90, False), "C12": (84, 80, 90, False),
    "J2": (8, 104, 90, False), "J3": (92, 104, 270, False),
    # voeding
    "U2": (45, 104, 0, False), "C1": (37, 104, 90, False), "C2": (45, 98, 0, False),
    "L1": (54, 104, 0, False), "C3": (61, 101, 90, False), "C4": (61, 107, 90, False),
    "R1": (28, 92, 0, False), "R2": (28, 96, 0, False), "C5": (34, 96, 90, False),
    "R3": (18, 94, 0, False), "D2": (18, 98, 0, False),
    "J1": (50, 122, 180, False), "SW1": (28, 125, 0, False),
    "J4": (76, 124, 180, False), "D1": (70, 114, 0, False),
    "R20": (82, 114, 90, False), "R21": (86, 114, 90, False),
}
GATEN = [(30, 26), (95, 30), (5, 118), (95, 118)]  # M2-bevestiging (H1 buiten de antennezone)


def mm(v):
    return pcbnew.FromMM(v)


def lees_netlijst(pad):
    root = ET.parse(pad).getroot()
    comps = {}
    for c in root.iter("comp"):
        ref = c.get("ref")
        fp = c.findtext("footprint") or ""
        comps[ref] = (fp, c.findtext("value") or "")
    nets = {}
    for n in root.iter("net"):
        naam = n.get("name").lstrip("/")
        for node in n.iter("node"):
            nets[(node.get("ref"), node.get("pin"))] = naam
    return comps, nets


def main(xml):
    comps, padnet = lees_netlijst(xml)
    board = pcbnew.BOARD()
    netinfo = {}

    def net(naam):
        if naam not in netinfo:
            ni = pcbnew.NETINFO_ITEM(board, naam)
            board.Add(ni)
            netinfo[naam] = ni
        return netinfo[naam]

    # ontwerpregels: 0,2 mm spoor/afstand (JLCPCB-standaard), via 0,6/0,3
    ds = board.GetDesignSettings()
    ds.m_TrackMinWidth = mm(0.2)
    ds.m_MinClearance = mm(0.2)
    ds.m_ViasMinSize = mm(0.6)
    ds.m_MinThroughDrill = mm(0.2)   # thermische vias onder de ESP32-module
    ds.m_HoleClearance = mm(0.15)    # USB-C-footprint heeft gaten dicht bij de pads
    nc = ds.m_NetSettings.GetDefaultNetclass()
    nc.SetTrackWidth(mm(0.25))
    nc.SetClearance(mm(0.2))
    nc.SetViaDiameter(mm(0.6))
    nc.SetViaDrill(mm(0.3))

    for ref, (fpnaam, waarde) in sorted(comps.items()):
        if ref.startswith("#") or not fpnaam:
            continue
        lib, naam = fpnaam.split(":")
        fp = pcbnew.FootprintLoad(os.path.join(FPDIR, lib + ".pretty"), naam)
        if fp is None:
            raise SystemExit(f"footprint niet gevonden: {fpnaam}")
        fp.SetReference(ref)
        fp.SetValue(waarde)
        board.Add(fp)
        x, y, rot, onder = PLAATS.get(ref, (110, 10, 0, False))
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(rot)
        if onder:
            fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
        for pad in fp.Pads():
            nm = padnet.get((ref, pad.GetNumber()))
            if nm:
                pad.SetNet(net(nm))

    for gx, gy in GATEN:
        g = pcbnew.FootprintLoad(os.path.join(FPDIR, "MountingHole.pretty"), "MountingHole_2.2mm_M2")
        g.SetReference(f"H{GATEN.index((gx, gy)) + 1}")
        g.SetPosition(pcbnew.VECTOR2I(mm(gx), mm(gy)))
        board.Add(g)

    # omtrek met afgeronde hoeken
    r = 3.0
    pts = [(r, 0), (BREED - r, 0), (BREED, r), (BREED, LANG - r), (BREED - r, LANG), (r, LANG), (0, LANG - r), (0, r)]
    for i in range(0, 8, 2):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(mm(pts[i][0]), mm(pts[i][1])))
        s.SetEnd(pcbnew.VECTOR2I(mm(pts[i + 1][0]), mm(pts[i + 1][1])))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(mm(0.1))
        board.Add(s)
    k = r * (1 - 0.7071)  # middelpunt van de boog, naar de hoek toe
    hoeken = [((r, 0), (k, k), (0, r)), ((BREED, r), (BREED - k, k), (BREED - r, 0)),
              ((BREED - r, LANG), (BREED - k, LANG - k), (BREED, LANG - r)), ((0, LANG - r), (k, LANG - k), (r, LANG))]
    for a, mid, b in hoeken:
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_ARC)
        s.SetArcGeometry(pcbnew.VECTOR2I(mm(a[0]), mm(a[1])), pcbnew.VECTOR2I(mm(mid[0]), mm(mid[1])),
                         pcbnew.VECTOR2I(mm(b[0]), mm(b[1])))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(mm(0.1))
        board.Add(s)

    # tekst op de print
    t = pcbnew.PCB_TEXT(board)
    t.SetText("LINEFOLLOWER plan A - Albin Curiel - HOGENT 2026")
    t.SetPosition(pcbnew.VECTOR2I(mm(62), mm(60)))
    t.SetLayer(pcbnew.F_SilkS)
    t.SetTextSize(pcbnew.VECTOR2I(mm(1.5), mm(1.5)))
    board.Add(t)

    # GND-vlak op beide lagen, behalve onder de antenne van de ESP32 (links, x < 8)
    for laag in (pcbnew.F_Cu, pcbnew.B_Cu):
        z = pcbnew.ZONE(board)
        z.SetLayer(laag)
        z.SetNet(net("GND"))
        z.SetLocalClearance(mm(0.3))
        z.SetMinThickness(mm(0.25))
        ol = z.Outline()
        ol.NewOutline()
        for px, py in [(0.5, 0.5), (99.5, 0.5), (99.5, 129.5), (0.5, 129.5), (0.5, 66), (9, 66), (9, 44), (0.5, 44)]:
            ol.Append(mm(px), mm(py))
        board.Add(z)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())

    uit = os.path.join(HIER, "linefollower_planA.kicad_pcb")
    board.Save(uit)
    print("opgeslagen:", uit, "footprints:", len(board.GetFootprints()), "netten:", len(netinfo))


if __name__ == "__main__":
    main(sys.argv[1])
