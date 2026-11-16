"""Routeert linefollower_planA.kicad_pcb met Freerouting en legt GND-vlakken op beide lagen.

  "<KiCad>/bin/python.exe" route_pcb.py [pad/naar/freerouting.jar]
Freerouting 1.9.0 werkt met Java 17: https://github.com/freerouting/freerouting/releases
"""
import os
import subprocess
import sys

import pcbnew

HIER = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.join(HIER, "linefollower_planA.kicad_pcb")
JAR = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.kicad-mcp/freerouting.jar")
DSN, SES = os.path.join(HIER, "planA.dsn"), os.path.join(HIER, "planA.ses")


def mm(v):
    return pcbnew.FromMM(v)


board = pcbnew.LoadBoard(PCB)

# netklassen: signalen 0,3 mm (standaard), USB 0,25 mm, voeding 0,5 mm, vermogen 0,6 mm, batterij 1,0 mm
ds = board.GetDesignSettings()
ns = ds.m_NetSettings
KLASSEN = {
    "Batterij": (1.0, ["BATT+"]),
    "Vermogen": (0.6, ["VBAT", "SW_BUCK", "MOT_L1", "MOT_L2", "MOT_R1", "MOT_R2"]),
    "Voeding": (0.5, ["+3V3"]),
    "USB": (0.25, ["USB_DP", "USB_DN", "CC1", "CC2", "VBUS"]),   # USB-C: pads 0,3 mm op 0,5 mm steek
}
for naam, (breedte, netten) in KLASSEN.items():
    k = pcbnew.NETCLASS(naam)
    k.SetTrackWidth(mm(breedte))
    k.SetClearance(mm(0.2))
    k.SetViaDiameter(mm(0.8))
    k.SetViaDrill(mm(0.4))
    ns.SetNetclass(naam, k)
    for net in netten:
        ns.SetNetclassPatternAssignment(net, naam)
board.SynchronizeNetsAndNetClasses(True)

# GND-vlakken (uit bouw_pcb.py) tijdelijk weg: Freerouting trekt dan ook GND als sporen,
# zodat geen enkele GND-pad op een los eiland in het vlak afhangt
zones = list(board.Zones())
for z in zones:
    board.Remove(z)
pcbnew.ExportSpecctraDSN(board, DSN)
print("DSN ->", DSN)
r = subprocess.run(["java", "-jar", JAR, "-de", DSN, "-do", SES, "-mp", "60", "-mt", "1"],
                   capture_output=True, text=True, timeout=1800)
print(r.stdout[-1500:], r.stderr[-1500:])
if not os.path.exists(SES):
    raise SystemExit("Freerouting gaf geen SES-bestand")
pcbnew.ImportSpecctraSES(board, SES)
for z in zones:
    board.Add(z)

filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
board.Save(PCB)
print("gerouteerd en opgeslagen:", PCB, "sporen:", len(board.GetTracks()))
