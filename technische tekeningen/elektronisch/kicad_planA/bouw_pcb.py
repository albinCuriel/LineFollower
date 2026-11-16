"""Bouwt linefollower_planA.kicad_pcb uit het schema (netlijst) met KiCad's pcbnew-API.

Gebruik (KiCad 10):
  kicad-cli sch export netlist --format kicadxml -o planA_netlijst.xml linefollower_planA.kicad_sch
  "<KiCad>/bin/python.exe" bouw_pcb.py planA_netlijst.xml
Daarna routeren met route_pcb.py (zie readme.md).

Coordinaten in mm: x = 0 links, y = 0 is de VOORKANT van de robot (sensoren). Maten: planA_maten.py.
"""
import os
import sys
import xml.etree.ElementTree as ET   # invoer = eigen netlijst uit kicad-cli

import pcbnew

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import planA_maten as M   # noqa: E402

HIER = os.path.dirname(os.path.abspath(__file__))
FPDIR = os.environ.get("KICAD_FP_DIR",
                       r"C:\Users\Albin\AppData\Local\Programs\KiCad\10.0\share\kicad\footprints")
SX = [50 + (i - 3.5) * M.SENSOR_STEEK for i in range(8)]

# ---- plaatsing: ref -> (x, y, rotatie, onderkant?)
PLAATS = {
    # sensoren: onderkant, vooraan, loodrecht op de rijrichting
    **{f"Q{i + 1}": (SX[i], M.SENSOR_Y, 0, True) for i in range(8)},
    **{f"R{10 + i}": (SX[i] - 2.4, 13.0, 90, False) for i in range(8)},
    **{f"R{22 + i}": (SX[i] + 2.4, 13.0, 90, False) for i in range(8)},
    "Q9": (50, 21, 0, False), "R6": (44, 21, 0, False), "R7": (56, 21, 0, False),
    # microcontroller: antenne over de linkerrand, ontkoppeling er vlak naast
    "U1": (14.0, 55.0, 90, False),
    "C6": (31, 44, 0, False), "C7": (31, 48, 0, False),
    "R4": (10, 72, 0, False), "C8": (10, 76, 0, False), "SW4": (20, 74, 0, False),
    "R5": (10, 80, 0, False), "SW3": (20, 81.5, 0, False),
    "J5": (40, 70, 90, False),
    "D3": (30, 33, 0, False), "C9": (37, 33, 0, False),
    "SW2": (90, 48, 0, False),
    # motorsturing: tussen de motoren, korte banen naar de motorstekkers
    "U3": (50, 87, 0, False),
    "C10": (41, 82, 90, False), "C11": (41, 88, 90, False), "C12": (59, 84, 90, False),
    "J2": (27, 92, 0, False), "J3": (63, 92, 0, False),
    # voeding: achteraan, vlak bij de batterijstekker
    "U2": (45, 104, 0, False), "C1": (37, 104, 90, False), "C2": (45, 98, 0, False),
    "L1": (54, 104, 0, False), "C3": (61, 101, 90, False), "C4": (61, 107, 90, False),
    "R1": (30, 100, 0, False), "R2": (30, 104, 0, False), "C5": (30, 108, 0, False),
    "R3": (24, 116, 0, False), "D2": (30, 116, 0, False),
    "J1": (50, 122, 180, False), "Q10": (39, 117, 0, False), "R8": (39, 112.5, 0, False),
    "SW1": (22, 125, 0, False),
    # usb: op de achterrand, kabel van de print weg
    "J4": (76, 124, 180, False), "D1": (68, 114, 0, False),
    "R20": (63, 118.5, 0, False), "R21": (63, 122.5, 0, False),
}


def mm(v):
    return pcbnew.FromMM(v)


def pt(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


def lees_netlijst(pad):
    root = ET.parse(pad).getroot()
    comps = {c.get("ref"): (c.findtext("footprint") or "", c.findtext("value") or "") for c in root.iter("comp")}
    nets = {}
    for n in root.iter("net"):
        naam = n.get("name").lstrip("/")
        for node in n.iter("node"):
            nets[(node.get("ref"), node.get("pin"))] = naam
    return comps, nets


def lijn(board, a, b):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pt(*a))
    s.SetEnd(pt(*b))
    s.SetLayer(pcbnew.Edge_Cuts)
    s.SetWidth(mm(0.1))
    board.Add(s)


def boog(board, a, mid, b):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_ARC)
    s.SetArcGeometry(pt(*a), pt(*mid), pt(*b))
    s.SetLayer(pcbnew.Edge_Cuts)
    s.SetWidth(mm(0.1))
    board.Add(s)


def teken_omtrek(board):
    """Omtrek met wieluitsparingen; enkel de 4 buitenhoeken zijn afgerond."""
    B, L, r = M.BREED, M.LANG, M.HOEK_R
    k = r * (1 - 0.7071)
    hoeken = {(0, 0): ((0, r), (k, k), (r, 0)), (B, 0): ((B - r, 0), (B - k, k), (B, r)),
              (B, L): ((B, L - r), (B - k, L - k), (B - r, L)), (0, L): ((r, L), (k, L - k), (0, L - r))}
    p = M.omtrek()
    n = len(p)
    for i in range(n):
        a, b = p[i], p[(i + 1) % n]
        a2 = hoeken[a][2] if a in hoeken else a       # vertrek na de afronding
        b2 = hoeken[b][0] if b in hoeken else b       # aankomst voor de afronding
        lijn(board, a2, b2)
    for a, mid, b in hoeken.values():
        boog(board, a, mid, b)


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

    # ontwerpregels (2 lagen, standaard bij JLCPCB/PCBWay)
    ds = board.GetDesignSettings()
    ds.m_TrackMinWidth = mm(0.2)
    ds.m_MinClearance = mm(0.2)
    ds.m_ViasMinSize = mm(0.6)
    ds.m_MinThroughDrill = mm(0.2)   # thermische vias onder de ESP32-module
    ds.m_HoleClearance = mm(0.15)    # USB-C-footprint heeft gaten dicht bij de pads
    nc = ds.m_NetSettings.GetDefaultNetclass()
    nc.SetTrackWidth(mm(0.3))        # signalen: breedte van de smalste IC-pinnen
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
        if ref not in PLAATS:
            raise SystemExit(f"geen plaats voor {ref}")
        fp.SetReference(ref)
        fp.SetValue(waarde)
        board.Add(fp)
        x, y, rot, onder = PLAATS[ref]
        fp.SetPosition(pt(x, y))
        fp.SetOrientationDegrees(rot)
        if onder:
            fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
        for pad in fp.Pads():
            nm = padnet.get((ref, pad.GetNumber()))
            if nm:
                pad.SetNet(net(nm))

    for i, (gx, gy, dia, waarvoor) in enumerate(M.GATEN, 1):
        naam = "MountingHole_2.2mm_M2" if dia < 3 else "MountingHole_3.2mm_M3"
        g = pcbnew.FootprintLoad(os.path.join(FPDIR, "MountingHole.pretty"), naam)
        g.SetReference(f"H{i}")
        g.SetValue(waarvoor)
        g.SetPosition(pt(gx, gy))
        g.Reference().SetVisible(False)
        board.Add(g)

    teken_omtrek(board)

    def tekst(t, x, y, grootte=1.2, laag=pcbnew.F_SilkS, rot=0):
        e = pcbnew.PCB_TEXT(board)
        e.SetText(t)
        e.SetPosition(pt(x, y))
        e.SetLayer(laag)
        e.SetTextSize(pcbnew.VECTOR2I(mm(grootte), mm(grootte)))
        e.SetTextThickness(mm(grootte * 0.15))
        e.SetTextAngleDegrees(rot)
        if laag == pcbnew.B_SilkS:
            e.SetMirrored(True)
        board.Add(e)

    tekst("LINEFOLLOWER plan A - Albin Curiel - HOGENT 2026", 62, 60, 1.5)
    tekst("VOOR", 50, 25.5, 1.5)
    tekst("motor L", 31, 96.5, 1.0)
    tekst("motor R", 67, 96.5, 1.0)
    tekst("START/STOP", 90, 53, 1.0)
    tekst("RESET", 28, 74, 0.9)
    tekst("BOOT", 28, 81.5, 0.9)
    tekst("AAN/UIT", 31, 125, 0.9)
    tekst("2S LiPo  - +", 50, 115.5, 1.0)
    tekst("3V3 TX RX GND", 40, 66.5, 0.9)

    # GND-vlak op beide lagen, behalve onder de antenne van de ESP32 (links)
    for laag in (pcbnew.F_Cu, pcbnew.B_Cu):
        z = pcbnew.ZONE(board)
        z.SetLayer(laag)
        z.SetNet(net("GND"))
        z.SetLocalClearance(mm(0.3))
        z.SetMinThickness(mm(0.25))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)            # volle verbinding: geen halve thermals
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)  # geen losse koper-eilanden
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
