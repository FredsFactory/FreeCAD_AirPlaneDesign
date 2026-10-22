#!/usr/bin/env freecadcmd
#################################################
#
# Cavity void wizard tests - Aircraft
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
"""Gate test for the Phase C wizard cavity column.  Run from the repo
root, NO arguments:

    freecadcmd tests/testCavityWizard.py

The Qt wizard dialog cannot be driven headlessly, so the cell-text
decision is pinned on airPlaneCavityDoc.parseCavityCell (the single
implementation the wizard calls) and the build-time call is pinned as an
integration gate on a wizard-shaped fake WingSPanel.  Same freecadcmd
assert style as testCavityDoc.py; failure path calls sys.exit(1) because
freecadcmd 1.1.4 returns 0 on an uncaught exception.
"""
__title__ = "FreeCAD cavity wizard tests"
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
import Part
from airPlaneAirFoilNaca import generateNacaCoords

COORDS = generateNacaCoords("0012", 40, False, True, 1, 0, 0, 0, 0, 0, 0)


def makeRib(doc, name, chord, y, twist=0.0):
    obj = doc.addObject("Part::FeaturePython", name)
    obj.addProperty("App::PropertyString", "NacaProfil", "NacaProfil")
    obj.addProperty("App::PropertyLength", "Chord", "Rib")
    obj.addProperty("App::PropertyVectorList", "Coordinates", "Rib")
    obj.NacaProfil = "0012"
    obj.Chord = chord
    obj.Coordinates = COORDS
    obj.Placement = FreeCAD.Placement(FreeCAD.Vector(0.0, y, 0.0),
                                      FreeCAD.Rotation(FreeCAD.Vector(0, 1,
                                                                      0),
                                                       twist))
    return obj


def gateSolidTokens():
    for txt in ("", " ", "N/A", "n/a", "-", "na", "NA", "none", "None",
                None):
        assert airPlaneCavityDoc.parseCavityCell(txt) is None, \
            "%r must parse as solid (None)" % txt


def gateWalls():
    assert airPlaneCavityDoc.parseCavityCell("20") == 20.0
    assert airPlaneCavityDoc.parseCavityCell(" 15.5 ") == 15.5
    assert airPlaneCavityDoc.parseCavityCell("0.5") == 0.5


def gateInvalid():
    # policy: invalid text raises so the wizard warns and leaves the panel
    # solid - never a silent cavity, never a build abort
    for txt in ("abc", "-5", "0", "0.0", "20mm"):
        try:
            airPlaneCavityDoc.parseCavityCell(txt)
            raise AssertionError("%r did not raise" % txt)
        except ValueError as err:
            assert str(err), "empty error for %r" % txt


def buildWizardPanel(doc, rootChord, tipChord, length, name="WingPanel"):
    """Wizard-shaped fake WingSPanel: RootRib/TipRib links + lofted Shape
    in the LE frame, exactly as airPlaneSWPanel.execute builds it."""
    root = makeRib(doc, name + "_root", rootChord, 0.0)
    tip = makeRib(doc, name + "_tip", tipChord, length, twist=-3.0)
    panel = doc.addObject("Part::FeaturePython", name)
    panel.addProperty("App::PropertyLink", "RootRib", "Rib")
    panel.addProperty("App::PropertyLink", "TipRib", "Rib")
    panel.RootRib = root
    panel.TipRib = tip
    wires = []
    for rib in (root, tip):
        pts = [rib.Placement.multVec(
            FreeCAD.Vector(p.x * float(rib.Chord), 0.0,
                           p.z * float(rib.Chord))) for p in COORDS]
        if pts[0].sub(pts[-1]).Length < 1e-9:
            pts.pop()
        wires.append(Part.makePolygon(pts + [pts[0]]))
    panel.Shape = Part.makeLoft(wires, True, False)
    return panel


def gateWizardPanelIntegration():
    # the exact call the wizard makes after creating + recomputing a
    # WingSPanel row, on a wizard-shaped fake
    doc = FreeCAD.newDocument("twiz")
    try:
        panel = buildWizardPanel(doc, 2500.0, 1600.0, 10000.0)
        created = airPlaneCavityDoc.addCavityToPanel(doc, panel, 20.0)
        assert [o.Label for o in created] == ["HollowShell (WingPanel)",
                                              "CavityVoid (WingPanel)",
                                              "OuterSkin (WingPanel)"], \
            "wrong objects: %s" % [o.Label for o in created]
        shell, void, outer = created
        assert shell.Visibility and not void.Visibility \
            and not outer.Visibility, "visibility defaults wrong"
        assert void.Shape.isValid() and void.Shape.Volume > 0.0 \
            and void.Shape.Shells[0].isClosed(), "void not a closed solid"
        assert shell.Shape.isValid() and 0.0 < shell.Shape.Volume \
            < outer.Shape.Volume, "shell not a valid sub-volume"
        print("      wizard-shaped panel: void %.3f m3, shell %.3f m3"
              % (void.Shape.Volume / 1e9, shell.Shape.Volume / 1e9))
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateSwallowRaises():
    # the LOUD path is reachable: a VALID wall too thick for the section
    # must propagate out of addCavityToPanel as a ValueError (the wizard
    # then shows its dialog); addCavityToPanel has no internal catch
    doc = FreeCAD.newDocument("tsw")
    try:
        panel = buildWizardPanel(doc, 800.0, 600.0, 3000.0, "TinyPanel")
        try:
            airPlaneCavityDoc.addCavityToPanel(doc, panel, 500.0)
            raise AssertionError("500 mm wall on an 800 mm chord did not "
                                 "raise - the wizard could not surface it")
        except ValueError as err:
            assert "wall" in str(err).lower(), \
                "error does not name the wall: %s" % err
            print("      swallow error: %s" % err)
    finally:
        FreeCAD.closeDocument(doc.Name)


def gatePurity():
    assert PURITY_OK, "importing airPlaneCavityDoc pulled in the GUI"


def main():
    gates = [
        ("parseCavityCell: solid tokens -> None", gateSolidTokens),
        ("parseCavityCell: numbers -> wall", gateWalls),
        ("parseCavityCell: invalid -> ValueError (warn+solid)", gateInvalid),
        ("addCavityToPanel on a wizard-shaped panel",
         gateWizardPanelIntegration),
        ("too-thick wall propagates ValueError (loud path reachable)",
         gateSwallowRaises),
        ("import purity (no PySide / FreeCADGui)", gatePurity),
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
