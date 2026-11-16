"""Tekent het deelschema van elke proof of concept (PNG in de map van de PoC).

  uv run --with schemdraw --with matplotlib python deelschemas.py

De pinnen komen overeen met code/board.h en met het volledige schema
(technische tekeningen/elektronisch/kicad/linefollower.kicad_sch).
"""
import os

import matplotlib
matplotlib.use("Agg")
import schemdraw
import schemdraw.elements as elm

HIER = os.path.dirname(os.path.abspath(__file__))
SP = 0.8   # afstand tussen pinnen
ORANJE, ROOD = "#ef6c00", "#d32f2f"


def ic(naam, links=(), rechts=(), boven=(), onder=(), breedte=4.0):
    pins = [elm.IcPin(name=n, side="left", slot=f"{len(links) - i}/{len(links)}") for i, n in enumerate(links)]
    pins += [elm.IcPin(name=n, side="right", slot=f"{len(rechts) - i}/{len(rechts)}") for i, n in enumerate(rechts)]
    pins += [elm.IcPin(name=n, side="top", slot=f"{i + 1}/{len(boven)}") for i, n in enumerate(boven)]
    pins += [elm.IcPin(name=n, side="bottom", slot=f"{i + 1}/{len(onder)}") for i, n in enumerate(onder)]
    n = max(len(links), len(rechts), 2)
    return elm.Ic(pins=pins, size=(breedte, n * SP + 0.6), pinspacing=SP, edgepadH=0.4, lblsize=10).label(
        naam, "center", fontsize=11)


def voeding(d, punt, tekst, kleur=ROOD, lengte=0.6, loc="top"):
    d += elm.Line().at(punt).length(lengte).up().color(kleur)
    d += elm.Vdd().label(tekst, loc=loc, fontsize=10).color(kleur)


def massa(d, punt):
    d += elm.Line().at(punt).length(0.6).down()
    d += elm.Ground()


def bewaar(d, map_, naam):
    pad = os.path.join(HIER, map_, naam)
    d.save(pad, dpi=140)
    print("->", os.path.relpath(pad, HIER))


def nieuw():
    d = schemdraw.Drawing(show=False)
    d.config(fontsize=10, unit=2.2)
    return d


# ------------------------------------------------------------------ blink
def blink():
    d = nieuw()
    esp = d.add(ic("ESP32-S3\ndevkit", rechts=["IO48"], links=["USB (COM)"], boven=["3V3"], onder=["GND"]))
    d += elm.Line().at(esp.IO48).length(1.0).right()
    d += elm.LED().right().length(1.8).label("ingebouwde RGB-led (WS2812)", loc="top", fontsize=8)
    d += elm.Line().down().length(0.8)
    d += elm.Ground()
    d += elm.Line().at(esp["USB (COM)"]).length(1.5).left()
    d += elm.Label().label("USB-C naar pc\n(voeding + uploaden)", loc="left", fontsize=9)
    massa(d, esp.GND)
    bewaar(d, "blink", "deelschema_blink.png")


# ------------------------------------------------------------------ sensor
def sensor():
    d = nieuw()
    io = [f"IO{i}" for i in range(1, 9)] + ["IO11"]
    uit = [f"OUT{i}" for i in range(1, 9)] + ["LEDON"]
    esp = d.add(ic("ESP32-S3\ndevkit\n(ADC1)", rechts=io, boven=["3V3"], onder=["GND"]))
    qtr = d.add(ic("Pololu QTR-8A\n(3.3V BYPASS\ndichtgesoldeerd)", links=uit, boven=["VCC"], onder=["GND"],
                   breedte=4.6).anchor("OUT1").at((esp.IO1[0] + 4.5, esp.IO1[1])))
    for a, b in zip(io, uit):
        d += elm.Line().at(getattr(esp, a)).to(getattr(qtr, b)).color("#8e24aa")
    voeding(d, esp["3V3"], "3V3 (buck)", kleur=ORANJE)
    voeding(d, qtr.VCC, "3V3", kleur=ORANJE)
    massa(d, esp.GND)
    massa(d, qtr.GND)
    bewaar(d, "sensor", "deelschema_sensor.png")


# ------------------------------------------------------------------ H-brug
def hbridge():
    d = nieuw()
    io = ["IO12", "IO14", "IO13", "IO18", "IO15", "IO16", "IO17"]
    tbl = ["PWMA", "AIN2", "AIN1", "STBY", "BIN1", "BIN2", "PWMB"]
    esp = d.add(ic("ESP32-S3\ndevkit", rechts=io, boven=["3V3"], onder=["GND"]))
    tb = d.add(ic("TB6612FNG\nmodule", links=tbl, rechts=["AO1", "AO2", "BO2", "BO1"], boven=["VCC", "VM"],
                  onder=["GND"], breedte=4.2).anchor("PWMA").at((esp.IO12[0] + 4.5, esp.IO12[1])))
    for a, b in zip(io, tbl):
        d += elm.Line().at(getattr(esp, a)).to(getattr(tb, b)).color("#2e7d32")
    # motoren met ontstoorcondensator over de klemmen
    for p1, p2, naam in (("AO1", "AO2", "motor links (N20 6 V 10:1)"), ("BO2", "BO1", "motor rechts (N20 6 V 10:1)")):
        a, b = getattr(tb, p1), getattr(tb, p2)
        d += elm.Line().at(a).length(1.5).right().color("#795548")
        m = d.add(elm.Motor().down().toy(b[1]))
        d += elm.Line().at(b).tox(m.end[0]).color("#795548")
        d += elm.Line().at(m.start).length(1.8).right()
        d += elm.Capacitor().down().toy(b[1]).label("100 nF", loc="bottom", fontsize=8)
        d += elm.Line().tox(m.end[0])
        d += elm.Label().at((m.start[0] + 2.4, (a[1] + b[1]) / 2)).label(naam, loc="right", fontsize=9)
    voeding(d, tb.VM, "VBAT 6,4-8,4 V (2S LiPo, na SW1)", lengte=2.2, loc="right")
    voeding(d, tb.VCC, "3V3", kleur=ORANJE, loc="left")
    voeding(d, esp["3V3"], "3V3 (buck)", kleur=ORANJE)
    d += elm.Line().at((tb.VM[0], tb.VM[1] + 1.6)).length(2.4).right().color(ROOD)
    d += elm.Capacitor(polar=True).down().length(1.0).label("C1 100 uF", loc="bottom", fontsize=8)
    d += elm.Ground()
    massa(d, esp.GND)
    massa(d, tb.GND)
    bewaar(d, "hbridge", "deelschema_hbridge.png")


# ------------------------------------------------------------------ interrupt
def interrupt():
    d = nieuw()
    esp = d.add(ic("ESP32-S3\ndevkit", rechts=["IO21", "IO48"], boven=["3V3"], onder=["GND"]))
    d += elm.Line().at(esp.IO21).length(4.5).right().color("#00838f")
    d += elm.Button().right().label("start/stop-knop naar GND\n(interne pull-up, interrupt op dalende flank)", fontsize=9)
    d += elm.Line().down().length(2.2)
    d += elm.Ground()
    d += elm.Line().at(esp.IO48).length(0.8).right()
    d += elm.LED().right().length(1.6)
    d += elm.Line().down().length(1.0)
    d += elm.Ground()
    d += elm.Label().at((esp.IO48[0] + 0.6, esp.IO48[1] - 2.3)).label(
        "ingebouwde RGB-led: rood = stop, groen = start", loc="right", fontsize=8)
    voeding(d, esp["3V3"], "3V3 (USB of buck)", kleur=ORANJE)
    massa(d, esp.GND)
    bewaar(d, "interrupt", "deelschema_interrupt.png")


# ------------------------------------------------------------------ wifi
def wifi():
    d = nieuw()
    esp = d.add(ic("ESP32-S3\ndevkit\n(wifi ingebouwd)", rechts=["antenne"], links=["USB (COM)"], boven=["3V3"],
                   onder=["GND"], breedte=4.4))
    d += elm.Line().at(esp.antenne).length(1.2).right()
    d += elm.Antenna().label("access point 'linefollower'\nTCP 192.168.4.1:23", loc="right", fontsize=9)
    d += elm.Line().at(esp["USB (COM)"]).length(1.5).left()
    d += elm.Label().label("USB-C naar pc\n(seriele monitor)", loc="left", fontsize=9)
    voeding(d, esp["3V3"], "3V3 (USB of buck)", kleur=ORANJE)
    massa(d, esp.GND)
    bewaar(d, "wireless communication", "deelschema_wifi.png")


if __name__ == "__main__":
    blink()
    sensor()
    hbridge()
    interrupt()
    wifi()
