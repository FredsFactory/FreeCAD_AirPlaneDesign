#!/usr/bin/env freecadcmd
#################################################
#
# Cavity void core tests - Aircraft
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
"""Gate test for airPlaneCavity.  Run from the repo root, NO arguments:

    freecadcmd tests/testCavityVoid.py

Plain asserts + printed summary; non-zero exit on failure (freecadcmd 1.1.4
returns 0 on an uncaught exception, so the failure path calls sys.exit(1)
explicitly).

All gates are BOOLEAN-FREE (no common/cut volume checks): OCC booleans against
lofted wing solids are measured garbage; isInside, distToShape and
isValid/isClosed/Volume are the trustworthy operations.
"""
__title__ = "FreeCAD airPlaneCavity tests"
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

import airPlaneCavity

# captured right after importing the module under test, before any other
# workbench import can muddy sys.modules
PURITY_OK = ('PySide' not in sys.modules and 'FreeCADGui' not in sys.modules)

import FreeCAD
import Part
from airPlaneAirFoilNaca import generateNacaCoords

WALL = 20.0          # cavity wall, mm (= the source project's 2 x cover anchor)
NPTS = 41            # resample points per surface = the module default and
                     # the source anchor (build_bwb INNER_POINTS = 41)
T_OVER_C = 0.15      # of the reference section below
# NACA-4 thickness polynomial -> closed-form profile area AREA_K * c * t
YT = (0.2969, -0.1260, -0.3516, 0.2843, -0.1036)
AREA_K = 10.0 * (YT[0] * 2.0 / 3.0 + YT[1] / 2.0 + YT[2] / 3.0
                 + YT[3] / 4.0 + YT[4] / 5.0)

COORDS = generateNacaCoords("0015", 40, False, True,
                            1, 0, 0, 0, 0, 0, 0)
# (y_mm, chord_mm, twist_deg) root -> tip; placement bakes the quarter-chord
# origin, so its Base IS the quarter-chord point of the station
STATIONS = [(0.0, 4000.0, 0.0), (10000.0, 3500.0, -2.0), (20000.0, 3000.0, -4.0),
            (30000.0, 2500.0, -6.0), (40000.0, 2000.0, -8.0)]
SCHEDULE = [(COORDS, chord,
             FreeCAD.Placement(FreeCAD.Vector(0.0, y, 0.0),
                               FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0),
                                                twist)))
            for y, chord, twist in STATIONS]


def outerWire(coords, chord, placement):
    """Reference outer wire: closed polygon through the profile points at the
    quarter-chord origin (same convention as the module's measurement wire).
    Intentionally independent of the library implementation - a test must
    not share code with what it verifies."""
    pts = [placement.multVec(FreeCAD.Vector((p.x - 0.25) * chord, 0.0,
                                            p.z * chord))
           for p in coords]
    if pts[0].sub(pts[-1]).Length < 1e-9:
        pts.pop()
    return Part.makePolygon(pts + [pts[0]])


try:  # freecadcmd 1.1.4 returns 0 on an uncaught exception: every failure
    INNER = [airPlaneCavity.offsetSectionWire(coords, chord, WALL, placement,
                                               NPTS)
             for coords, chord, placement in SCHEDULE]
    OUTER = [outerWire(COORDS, chord, placement)
             for _, chord, placement in SCHEDULE]
    VOID = airPlaneCavity.makeCavityVoid(SCHEDULE, WALL, NPTS)
    OUTER_SOLID = Part.makeLoft(OUTER, True, False)
except Exception:
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)


def gatePurity():
    assert PURITY_OK, "importing airPlaneCavity pulled in the GUI"


def gateWatertight():
    assert VOID.isValid(), "cavity void is not valid"
    assert len(VOID.Solids) == 1, "cavity void is not one solid"
    assert VOID.Shells[0].isClosed(), "cavity void shell is not closed"
    assert VOID.Volume > 0.0, "cavity void volume is not positive"
    # the 3-edge invariant, structurally: a single periodic spline through the
    # nose can loft a plausible-looking closed solid (measured: volume 0.834 x
    # the analytic bound, mid-band) and would pass every volume/inside gate -
    # only the edge count catches it
    assert all(len(w.Edges) == 3 for w in INNER), \
        "an inner station wire is not the 3-edge (upper, lower, blunt TE) " \
        "construction"


def gateInsideOuter():
    # probes: area centroid of every inner wire + consecutive midpoints.
    # Self-checked against the void FIRST: a probe that is not inside the
    # void proves probe generation is broken, and a gate that tests nothing
    # is worse than no gate.
    cents = [Part.Face(w).CenterOfMass for w in INNER]
    probes = cents + [(a + b) * 0.5 for a, b in zip(cents[:-1], cents[1:])]
    for p in probes:
        assert VOID.isInside(p, 1e-6, True), \
            "void probe (%.1f, %.1f, %.1f) not inside the void - probe " \
            "generation broken, the outer gate below would test nothing" \
            % (p.x, p.y, p.z)
    for p in probes:
        assert OUTER_SOLID.isInside(p, 1e-6, True), \
            "cavity probe (%.1f, %.1f, %.1f) pokes out of the outer solid" \
            % (p.x, p.y, p.z)


def gateWall():
    # regression tripwire on the module's INTERNAL gate (offsetSectionWire
    # returns only when its own distToShape >= wall, so this recomputes that
    # quantity - it catches a broken/removed internal loop, not the physics;
    # the pointwise check below is the physical one).  0.98 is NOT from the
    # source cavity gate (build_bwb.py:609 demands 1.0x); the 0.98 in the
    # source is the rib-lane probe-shrink factor (build_ribs.py:313).
    for i, (outer, inner) in enumerate(zip(OUTER, INNER)):
        gap = outer.distToShape(inner)[0]
        assert gap >= 0.98 * WALL, \
            "station %d: wall gap %.2f mm < 0.98 x %.1f mm" % (i, gap, WALL)
    # pointwise at mid-chord: the inner surface crossed by the quarter-chord
    # vertical must sit at ~wall from the outer wire on BOTH surfaces.  Band
    # [-2%, +8%]: the LOWER bound is physics (never thinner than the wall).
    # The UPPER bound is the measured-interpolant allowance - the first-pass
    # nose-crown sagitta (~1 mm at nPts=41) is added back to the wall and
    # lands as wall EXCESS at mid-chord, measured +5.4% at the root here.
    # The source gates only a lower bound (build_bwb.py:609, 1.0x there), so
    # this two-sided band is the test's own invention: its ceiling owes to
    # measured physics, not a ported anchor.
    worst = 0.0
    for i, (coords, chord, placement) in enumerate(SCHEDULE):
        line = Part.makeLine(
            placement.multVec(FreeCAD.Vector(0.0, 0.0, -chord)),
            placement.multVec(FreeCAD.Vector(0.0, 0.0, chord)))
        hits = INNER[i].section(line).Vertexes
        assert len(hits) == 2, \
            "station %d: mid-chord line hits the inner wire %d times, " \
            "expected 2 (upper + lower surface)" % (i, len(hits))
        vAxis = placement.Rotation.multVec(FreeCAD.Vector(0, 0, 1))
        hits.sort(key=lambda vtx: (vtx.Point - placement.Base).dot(vAxis))
        for vtx in hits:
            d = vtx.distToShape(OUTER[i])[0]
            dev = (d - WALL) / WALL
            worst = max(worst, dev)
            assert -0.02 <= dev <= 0.08, \
                "station %d: mid-chord inner surface %.2f mm from the outer " \
                "wire = wall %+.1f%%, outside [-2%%, +8%%]" % (i, d,
                                                               100.0 * dev)
    print("      worst mid-chord deviation %+.2f%% (band [-2%%, +8%%])"
          % (100.0 * worst))


def gateNoseFold():
    # PR #62 report: NACA 2412 panel, root chord 104 mm, wall 3.4 mm died
    # with "wall 3 mm not reached ... gap 2.80 mm (built at 5.13 mm)".
    # Root cause: a wall deeper than the LE radius of curvature
    # (1.1019*(t/c)^2*chord = 1.7 mm for 2412 at 104 mm) folds the offset
    # chains over each other at the nose, the fold sits inside the wall,
    # and the measured loop chases the ever-shrinking gap.  The nose is now
    # trimmed like the TE, so walls build up to the station's inscribed
    # radius (6.2 mm at the root, 2.4 mm at the 39.5 mm tip here).
    sm = generateNacaCoords("2412", 40, False, True,
                            1, 0, 0, 0, 0, 0, 0)
    root, tip = 104.0, 39.5
    ident = FreeCAD.Placement(FreeCAD.Vector(0.0, 0.0, 0.0),
                              FreeCAD.Rotation())
    for wall in (2.5, 3.4, 4.5):  # every one of these failed pre-fix
        wire = airPlaneCavity.offsetSectionWire(sm, root, wall)
        assert len(wire.Edges) == 3 and wire.isValid() and wire.isClosed(), \
            "root wall %.1f mm: the nose trim broke the 3-edge inner wire" \
            % wall
        gap = outerWire(sm, root, ident).distToShape(wire)[0]
        assert wall <= gap <= 1.10 * wall, \
            "root wall %.1f mm measured gap %.2f mm outside [wall, 1.10 x " \
            "wall]" % (wall, gap)
    # the 39.5 mm tip is 4.7 mm thick: a 6.8 mm double wall does not fit
    # anywhere, so 3.4 mm must STILL raise - but the message must name the
    # ceiling, and the ceiling must be the geometry's, not the fold's
    try:
        airPlaneCavity.offsetSectionWire(sm, tip, 3.4)
        assert False, "wall 3.4 mm built on a 4.7 mm thick tip section - " \
                      "the swallow gate is dead"
    except ValueError as err:
        msg = str(err)
        assert "builds is ~" in msg, \
            "error carries no max-wall hint: %s" % msg
        hint = float(msg.split("builds is ~")[1].split(" mm")[0])
        assert 1.8 <= hint <= 2.6, \
            "max-wall hint %.2f mm outside the tip inscribed-radius band " \
            "[1.8, 2.6] - hinting above the ceiling would loop the user" \
            % hint
        print("      fold fix: root builds 2.5-4.5 mm; tip 3.4 mm raises "
              "with hint ~%.2f mm" % hint)
    # the user story: the whole 104 -> 39.5 mm panel at a uniform 2.0 mm
    # wall (pre-fix the tip failed above ~0.8 mm), void structurally sound
    plTip = FreeCAD.Placement(FreeCAD.Vector(0.0, 430.0, 0.0),
                              FreeCAD.Rotation())
    void = airPlaneCavity.makeCavityVoid([(sm, root, ident),
                                          (sm, tip, plTip)], 2.0)
    assert void.isValid() and len(void.Solids) == 1 \
            and void.Shells[0].isClosed() and void.Volume > 0.0, \
        "2.0 mm wall over the 104/39.5 mm panel did not loft a closed void"
    outerSolid = Part.makeLoft([outerWire(sm, root, ident),
                                outerWire(sm, tip, plTip)], True, False)
    assert outerSolid.isInside(void.CenterOfMass, 1e-6, True), \
        "the thin-panel cavity void is not inside its outer loft"


def gateSwallow():
    thin = generateNacaCoords("0012", 40, False, True,
                              1, 0, 0, 0, 0, 0, 0)
    # direct path: at wall 80 mm the offset chains cross everywhere and the
    # pop empties a chain - offsetProfileCoords itself must raise
    try:
        airPlaneCavity.offsetProfileCoords(thin, 1200.0, 80.0)
        assert False, "wall 80 mm on a 1200 mm chord t/c 0.12 section did " \
                      "not raise directly - the swallow tripwire is dead"
    except ValueError:
        pass
    # escalation path: wall 40 mm survives the direct offset (61/61 points),
    # so the void must die in the measured loop - the grown wall reaches the
    # swallow and the ValueError must still surface, never a collapsed void
    try:
        airPlaneCavity.makeCavityVoid([(thin, 1200.0, FreeCAD.Placement())],
                                      40.0, NPTS)
    except ValueError:
        return
    assert False, "wall 40 mm on a 1200 mm chord t/c 0.12 section did not " \
                  "raise through makeCavityVoid - the swallow tripwire " \
                  "is dead"


def gateVolume():
    # analytic bound AREA_K * (c - 2w) * (tc*c - 2w) integrated over the
    # station schedule (trapezoid).  A collapsed void (swallowed section,
    # self-crushed loft) trips the floor; interpolant RINGING toward the wall
    # does not collapse the volume at this scale (measured: a periodic-spline
    # sabotage sits at 0.834, mid-band) - ringing is caught structurally, by
    # the 3-edge assertion in gateWatertight.
    areas = [AREA_K * (chord - 2.0 * WALL) * (T_OVER_C * chord - 2.0 * WALL)
             for _, chord, _ in STATIONS]
    bound = 0.0
    for i in range(len(STATIONS) - 1):
        dy = STATIONS[i + 1][0] - STATIONS[i][0]
        bound += 0.5 * (areas[i] + areas[i + 1]) * dy
    ratio = VOID.Volume / bound
    assert 0.60 <= ratio <= 1.00, \
        "void volume %.3e mm3 is %.3f x the analytic bound %.3e mm3 " \
        "(outside [0.60, 1.00])" % (VOID.Volume, ratio, bound)
    print("      void volume %.1f m3 = %.3f x analytic bound"
          % (VOID.Volume / 1e9, ratio))


def main():
    gates = [
        ("import purity (no PySide / FreeCADGui)", gatePurity),
        ("watertight non-empty void", gateWatertight),
        ("probes inside void (self-check) and outer", gateInsideOuter),
        ("wall thickness (gap + mid-chord pointwise)", gateWall),
        ("LE-fold trim: thick walls on small chords build; hint on impossible",
         gateNoseFold),
        ("swallow tripwire raises ValueError", gateSwallow),
        ("volume vs analytic AREA_K bound", gateVolume),
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


try:  # same reason as the build guard above: never let freecadcmd eat it
    main()
except SystemExit:
    raise
except Exception:
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)
