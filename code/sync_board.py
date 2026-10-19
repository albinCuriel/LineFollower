"""Kopieer code/board.h naar elke plaats waar Arduino een eigen kopie nodig heeft.
Pas pinnen ENKEL aan in code/board.h en draai daarna:  py -3 sync_board.py"""
import pathlib, shutil
hier = pathlib.Path(__file__).parent
bron = hier / "board.h"
doelen = [hier / "lib" / "lf_esp32" / "src" / "board.h"] + [p for p in hier.rglob("board.h") if p != bron]
for d in sorted(set(doelen)):
    shutil.copyfile(bron, d)
    print("bijgewerkt:", d.relative_to(hier))
