#!/usr/bin/env freecadcmd
#################################################
#
# Cavity void example - Aircraft
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

"""Runnable showcase for airPlaneCavity.  Run from the workbench root,
NO arguments:

    freecadcmd examples/cavity-void-example.py

Story: build a NACA 0015 section, loft a tapered + twisted + swept outer
wing, cut a cavity void with a fixed wall thickness, and write
cavity-void-example.FCStd / .step into the CURRENT WORKING DIRECTORY (the
repo tree is never dirtied by running the example).  Headless - no Qt, no
workbench command needed.
"""
__title__ = "FreeCAD airPlaneCavity example"
__author__ = "RedxHerring"
__url__ = "https://fredsfactory.fr"

import os
import sys

try:  # keep the narration in order against STEP export's own stdout
    sys.stdout.reconfigure(line_buffering=True)
except AttributeError:
    pass

# uninstalled checkout: the workbench root is the parent of examples/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import FreeCAD
import Part
from airPlaneAirFoilNaca import generateNacaCoords
import airPlaneCavity

NACA = "0015"
WALL = 20.0  # cavity wall, mm (the normal offset applied all round)
# (y_mm, chord_mm, twist_deg, sweep_mm) root -> tip; sweep shifts the
# quarter-chord point aft, twist washes the tip out
STATIONS = [(0.0, 3000.0, 0.0, 0.0),
            (15000.0, 2400.0, -3.0, 1500.0),
            (30000.0, 1600.0, -6.0, 3000.0)]

print("== cavity-void example: NACA %s, wall %.0f mm ==" % (NACA, WALL))
coords = generateNacaCoords(NACA, 40, False, True, 1, 0, 0, 0, 0, 0, 0)
print("1. section: generateNacaCoords('%s', 40 points)" % NACA)

schedule = []
for y, chord, twist, sweep in STATIONS:
    print("   station y=%6.0f mm  chord %5.0f mm  twist %+4.1f deg  "
          "sweep %5.0f mm" % (y, chord, twist, sweep))
    # the placement IS the quarter-chord point of the station: the module
    # builds sections around that origin
    schedule.append((coords, chord,
                     FreeCAD.Placement(FreeCAD.Vector(sweep, y, 0.0),
                                       FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0),
                                                        twist))))

print("2. outer skin: loft of the %d station profiles" % len(STATIONS))


def outerWire(coords, chord, placement):
    """Reference skin wire: polygon through the profile points at the
    quarter-chord origin (same convention the module measures against)."""
    pts = [placement.multVec(FreeCAD.Vector((p.x - 0.25) * chord, 0.0,
                                            p.z * chord))
           for p in coords]
    if pts[0].sub(pts[-1]).Length < 1e-9:
        pts.pop()
    return Part.makePolygon(pts + [pts[0]])


outer = Part.makeLoft([outerWire(*s) for s in schedule], True, False)
print("   outer wing solid: %.2f m3 (valid: %s)"
      % (outer.Volume / 1e9, outer.isValid()))

print("3. cavity void: airPlaneCavity.makeCavityVoid(schedule, %.0f)" % WALL)
void = airPlaneCavity.makeCavityVoid(schedule, WALL)
print("   void: %.2f m3 = %.1f%% of the wing, watertight: %s"
      % (void.Volume / 1e9, 100.0 * void.Volume / outer.Volume,
         void.Shells[0].isClosed()))
inside = all(outer.isInside(v.Point, 1e-6, True) for v in void.Vertexes)
print("   every void vertex sits >= wall inside the skin: %s (%d probed)"
      % (inside, len(void.Vertexes)))

print("4. hollow shell: outer.cut(void)")
shell = outer.cut(void)
print("   shell: %.2f m3 (outer - void = %.2f m3, boolean agrees within %.2f%%)"
      % (shell.Volume / 1e9, (outer.Volume - void.Volume) / 1e9,
         100.0 * abs(shell.Volume - (outer.Volume - void.Volume))
         / outer.Volume))

print("5. artifacts -> current working directory")
doc = FreeCAD.newDocument("cavity-void-example")
for name, label, shape in (("Skin", "OuterSkin", outer),
                           ("CavityVoid", "CavityVoid", void),
                           ("Shell", "HollowShell", shell)):
    obj = doc.addObject("Part::Feature", name)
    obj.Label = label
    obj.Shape = shape
doc.recompute()
if FreeCAD.GuiUp:  # display state is stored inside the saved FCStd; headless skips this
    _disp = {"Skin": ((0.80, 0.80, 0.80), False),
             "CavityVoid": ((1.00, 0.20, 0.20), False),
             "Shell": ((0.20, 0.50, 0.90), True)}
    for _o in doc.Objects:
        _c, _v = _disp[_o.Name]
        _o.ViewObject.ShapeColor = _c
        _o.ViewObject.Visibility = _v
fcstd = "cavity-void-example.FCStd"
step = "cavity-void-example.step"
doc.saveAs(fcstd)
Part.export(doc.Objects, step)
print("   wrote %s (%d bytes)" % (os.path.abspath(fcstd),
                                  os.path.getsize(fcstd)))
print("   wrote %s (%d bytes)" % (os.path.abspath(step),
                                  os.path.getsize(step)))
# colors need a ViewObject, which freecadcmd does not have - the GuiUp
# block above sets them when this runs inside the FreeCAD GUI
FreeCAD.closeDocument(doc.Name)
print("done - open cavity-void-example.FCStd in FreeCAD (HollowShell is "
      "shown; switch on OuterSkin / CavityVoid in the tree to see them)")
