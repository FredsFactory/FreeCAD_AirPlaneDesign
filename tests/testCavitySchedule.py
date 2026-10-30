#!/usr/bin/env freecadcmd
#################################################
#
# Cavity void schedule tests - Aircraft
#
# Copyright (c) RedxHerring - 2026 - V0.1
#
# For FreeCAD Versions = or > 0.17 Revision xxxx
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (LGPL)
# as published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
# for detail see the LICENCE text file.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
################################################
"""Gate test for airPlaneCavityDoc.  Run from the repo root, NO arguments:

    freecadcmd tests/testCavitySchedule.py

Plain asserts + printed summary; non-zero exit on failure (freecadcmd
1.1.4 returns 0 on an uncaught exception, so the failure path calls
sys.exit(1) explicitly).  Boolean-free doctrine as testCavityVoid.py.
"""
__title__ = "FreeCAD airPlaneCavityDoc schedule tests"
__author__ = "RedxHerring"
__url__ = "https://fredsfactory.fr"

import os
import sys
import traceback

try:  # stream the gate report even when piped - and do not lose it on exit(1)
    sys.stdout.reconfigure(line_buffering=True)
except AttributeError:
    pass

# uninstalled checkout: the workbench root is the parent of tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import airPlaneCavityDoc

# captured right after importing the module under test, before any other
# workbench import can muddy sys.modules
PURITY_OK = ('PySide' not in sys.modules and 'FreeCADGui' not in sys.modules)

import FreeCAD


def gatePurity():
    assert PURITY_OK, "importing airPlaneCavityDoc pulled in the GUI"


def gateGolden():
    # the refactor must reproduce the ORIGINAL hardcoded 3-station schedule
    # (y [0,15000,30000], twist [0,-3,-6], sweep [0,1500,3000]).  ONE
    # deliberate correction: the old hand-picked mid chord was 2400, which
    # is NOT the linear-taper midpoint of 3000 -> 1600 (that is 2300); the
    # panel model is a true trapezoid, so the golden pins 2300.
    sched = airPlaneCavityDoc.buildSchedule("0015", 3000.0, 1600.0 / 3000.0,
                                            30000.0, -6.0, 3000.0)
    assert len(sched) == 3, "schedule is not 3 stations"
    chords = [c for _, c, _ in sched]
    assert [round(c, 6) for c in chords] == [3000.0, 2300.0, 1600.0], \
        "chords %s != [3000, 2300, 1600]" % chords
    ys = [pl.Base.y for _, _, pl in sched]
    assert [round(v, 6) for v in ys] == [0.0, 15000.0, 30000.0], \
        "y stations %s wrong" % ys
    sweeps = [pl.Base.x for _, _, pl in sched]
    assert [round(v, 6) for v in sweeps] == [0.0, 1500.0, 3000.0], \
        "sweep offsets %s wrong" % sweeps
    for twist, (_, _, pl) in zip([0.0, -3.0, -6.0], sched):
        want = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0),
                                twist).multVec(FreeCAD.Vector(1, 0, 0))
        got = pl.Rotation.multVec(FreeCAD.Vector(1, 0, 0))
        assert (want - got).Length < 1e-9, \
            "twist %s deg not baked in the station placement" % twist


def gateDerived():
    # tip chord = lambda*root and AR = span^2/area, hand-checked
    for root, lam, span, tip, area, ar in (
            (3000.0, 1600.0 / 3000.0, 30000.0, 1600.0, 69.0e6,
             900.0e6 / 69.0e6),
            (2000.0, 0.6, 25000.0, 1200.0, 40.0e6, 625.0e6 / 40.0e6)):
        sched = airPlaneCavityDoc.buildSchedule("0015", root, lam, span,
                                                0.0, 0.0)
        assert abs(sched[-1][1] - tip) < 1e-9, \
            "tip chord %.6f != lambda*root %.6f" % (sched[-1][1], tip)
        a = airPlaneCavityDoc.planformAreaMm2(root, lam, span)
        assert abs(a - area) < 1e-6, "area %.1f != %.1f" % (a, area)
        assert abs(span * span / a - ar) < 1e-9, \
            "AR %.6f != hand calc %.6f" % (span * span / a, ar)


def gateFullWingSummary():
    # the panel summary read-out shows FULL-wing values: area x2 and
    # AR = (2*span)^2 / area_full.  Pinned against the 787-9 defaults the
    # GUI panel opens with (the half-wing relations above stay as-is -
    # planformAreaMm2 is the pure half-wing function).
    root, lam, span = 9070.0, 0.31, 30050.0
    areaFull = 2.0 * airPlaneCavityDoc.planformAreaMm2(root, lam, span)
    arFull = (2.0 * span) ** 2 / areaFull
    assert abs(areaFull / 1e6 - 357.0) < 1.0, \
        "full-wing area %.1f m2 not ~357" % (areaFull / 1e6)
    assert abs(arFull - 10.1) < 0.1, "full-wing AR %.2f not ~10.1" % arFull
    print("      full-wing read-out at defaults: %.1f m2, AR %.2f"
          % (areaFull / 1e6, arFull))


def gateShapes():
    # non-default params: the boolean-free trio (valid, one solid, positive
    # volume) - same doctrine as testCavityVoid
    params = {"number": "2412", "rootChord": 2000.0, "span": 25000.0,
              "taper": 0.6, "tipTwist": -4.0, "tipSweep": 2000.0,
              "wall": 15.0, "nPts": 41}
    outer, void, shell = airPlaneCavityDoc.buildCavityShapes(params)
    assert outer.isValid() and shell.isValid(), "outer/shell not valid"
    assert void.isValid() and len(void.Solids) == 1 and void.Volume > 0.0, \
        "void is not one valid positive-volume solid"
    assert void.Shells[0].isClosed(), "void shell not closed"
    print("      2412 non-default: outer %.2f m3, void %.2f m3, shell %.2f m3"
          % (outer.Volume / 1e9, void.Volume / 1e9, shell.Volume / 1e9))


def main():
    gates = [
        ("import purity (no PySide / FreeCADGui)", gatePurity),
        ("golden 3-station schedule reproduction", gateGolden),
        ("derived read-out math (tip chord, area, AR)", gateDerived),
        ("full-wing summary read-out (area x2, AR of the aircraft)",
         gateFullWingSummary),
        ("buildCavityShapes at non-default params", gateShapes),
    ]
    failed = []
    for name, fn in gates:
        try:
            fn()
            print("PASS  %s" % name)
        except AssertionError as err:
            failed.append(name)
            print("FAIL  %s: %s" % (name, err))
    print("%d/%d gates pass" % (len(gates) - len(failed), len(gates)))
    if failed:
        sys.stdout.flush()
        sys.exit(1)


try:  # freecadcmd 1.1.4 returns 0 on an uncaught exception: never let it eat
    main()
except SystemExit:
    raise
except Exception:
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)
