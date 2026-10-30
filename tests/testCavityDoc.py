#!/usr/bin/env freecadcmd
#################################################
#
# Cavity void selection-layer tests - Aircraft
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
"""Gate test for the Phase B selection layer of airPlaneCavityDoc.
Run from the repo root, NO arguments:

    freecadcmd tests/testCavityDoc.py

Plain asserts + printed summary; non-zero exit on failure (freecadcmd
1.1.4 returns 0 on an uncaught exception, so the failure path calls
sys.exit(1) explicitly).  The fake APD objects are built from raw
addProperty calls mirroring airPlaneRib.py:59-72 / airPlaneSWPanel.py:52-53
/ airPlaneWPanel.py:255 / airPlaneWing.py:60 - the real modules are NOT
imported (they drag in PySide/numpy).
"""
__title__ = "FreeCAD airPlaneCavityDoc selection tests"
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


def makeRib(doc, name, chord, y, twist=0.0, coords=None):
    """Fake WingRib: the property set airPlaneRib.py:59-72 creates (the
    subset the duck-type probes), LE-origin placement."""
    obj = doc.addObject("Part::FeaturePython", name)
    obj.addProperty("App::PropertyFile", "RibProfil", "Rib")
    obj.addProperty("App::PropertyString", "NacaProfil", "NacaProfil")
    obj.addProperty("App::PropertyLength", "Chord", "Rib")
    obj.addProperty("App::PropertyVectorList", "Coordinates", "Rib")
    obj.NacaProfil = "0012"
    obj.Chord = chord
    obj.Coordinates = COORDS if coords is None else coords
    obj.Placement = FreeCAD.Placement(FreeCAD.Vector(0.0, y, 0.0),
                                      FreeCAD.Rotation(FreeCAD.Vector(0, 1,
                                                                      0),
                                                       twist))
    return obj


def makeWizardPanel(doc, name, rootRib, tipRib):
    obj = doc.addObject("Part::FeaturePython", name)
    obj.addProperty("App::PropertyLink", "RootRib", "Rib")
    obj.addProperty("App::PropertyLink", "TipRib", "Rib")
    obj.RootRib = rootRib
    obj.TipRib = tipRib
    return obj


def makeCurvedPanel(doc, name, ribs):
    obj = doc.addObject("Part::FeaturePython", name)
    obj.addProperty("App::PropertyLinkList", "Ribs", "WPRibs")
    obj.Ribs = ribs
    return obj


def makeWing(doc, name, panels):
    obj = doc.addObject("Part::FeaturePython", name)
    obj.addProperty("App::PropertyLinkList", "WingPanels", "Wing")
    obj.WingPanels = panels
    return obj


def gateQuarterChord():
    # THE correctness gate: rib placement origin is the LE, the core wants
    # the quarter-chord: base' = base + rot.multVec(Vector(0.25*chord,0,0))
    doc = FreeCAD.newDocument("tqc")
    try:
        rib = makeRib(doc, "rib", 2000.0, 5000.0, twist=-6.0)
        rib.Placement = FreeCAD.Placement(FreeCAD.Vector(100.0, 5000.0,
                                                         300.0),
                                          rib.Placement.Rotation)
        coords, chord, pl = airPlaneCavityDoc.stationFromRib(rib)
        assert len(coords) == len(COORDS) and chord == 2000.0, \
            "coords/chord not passed through"
        want = rib.Placement.Base + \
            rib.Placement.Rotation.multVec(FreeCAD.Vector(500.0, 0.0, 0.0))
        got = pl.Base
        assert (want - got).Length < 1e-9, \
            "base %s != LE + rot*(0.25*chord,0,0) = %s" % (got, want)
        for v in (FreeCAD.Vector(1, 0, 0), FreeCAD.Vector(0, 0, 1)):
            assert (rib.Placement.Rotation.multVec(v)
                    - pl.Rotation.multVec(v)).Length < 1e-12, \
                "rotation not preserved"
        # and the offset really is along the ROTATED x-axis, not global x
        assert abs(got.x - 100.0) > 1.0, \
            "offset looks un-rotated (global-x shift only)"
    finally:
        FreeCAD.closeDocument(doc.Name)


def gatePanelSchedule():
    doc = FreeCAD.newDocument("tps")
    try:
        root = makeRib(doc, "root", 3000.0, 0.0)
        tip = makeRib(doc, "tip", 1200.0, 12000.0)
        panel = makeWizardPanel(doc, "wiz", root, tip)
        sched = airPlaneCavityDoc.panelSchedule(panel)
        assert [round(c, 6) for _, c, _ in sched] == [3000.0, 1200.0], \
            "wizard panel chords wrong"
        assert [round(pl.Base.y, 6) for _, _, pl in sched] == [0.0,
                                                               12000.0], \
            "wizard panel not root->tip"
        ribs = [makeRib(doc, "r%d" % i, c, y) for i, (c, y) in enumerate(
            [(3000.0, 0.0), (2600.0, 8000.0), (2100.0, 16000.0),
             (1600.0, 24000.0)])]
        curved = makeCurvedPanel(doc, "curv", ribs)
        sched = airPlaneCavityDoc.panelSchedule(curved)
        assert [round(c, 6) for _, c, _ in sched] == [3000.0, 2600.0,
                                                      2100.0, 1600.0], \
            "curved panel not in Ribs-list order"
        try:
            airPlaneCavityDoc.panelSchedule(
                makeCurvedPanel(doc, "bad", ribs[:1]))
            raise AssertionError("1-rib panel did not raise")
        except ValueError:
            pass
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateClassify():
    doc = FreeCAD.newDocument("tcl")
    try:
        root = makeRib(doc, "root", 3000.0, 0.0)
        tip = makeRib(doc, "tip", 1200.0, 12000.0)
        panel = makeWizardPanel(doc, "wiz", root, tip)
        wing = makeWing(doc, "wing", [panel])
        curved = makeCurvedPanel(doc, "curv", [root, tip])
        plain = doc.addObject("Part::Feature", "imported")
        for obj, want in ((wing, "wing"), (panel, "panel"),
                          (curved, "panel"), (root, "rib"),
                          (plain, "other")):
            kind, why = airPlaneCavityDoc.classifySelection(obj)
            assert kind == want, "%s classified %r not %r" % (obj.Label,
                                                              kind, want)
            assert why, "empty why for %s" % obj.Label
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateRefusal():
    doc = FreeCAD.newDocument("trf")
    try:
        plain = doc.addObject("Part::Feature", "importedSTEP")
        kind, why = airPlaneCavityDoc.classifySelection(plain)
        assert kind == "other", "imported solid not classified 'other'"
        assert why and "Part::Feature" in why and "schedule" in why, \
            "refusal text does not name the object/why: %r" % why
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateUnitChordAccepted():
    # the guard must NOT false-trip legitimate unit-chord sections:
    # symmetric, cambered, thin and NACA 5-digit all span x ~[0,1]
    doc = FreeCAD.newDocument("tuc")
    try:
        for number in ("0012", "2412", "0009", "23012"):
            coords = generateNacaCoords(number, 40, False, True,
                                        1, 0, 0, 0, 0, 0, 0)
            rib = makeRib(doc, "r" + number, 2000.0, 0.0, coords=coords)
            _, _, pl = airPlaneCavityDoc.stationFromRib(rib)
            assert pl.Base.y == 0.0  # smoke: conversion ran
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateScaledRejected():
    # THE fix: mm-scaled Coordinates (x in [0,3000], Chord 3000) must raise
    # a named, actionable ValueError - not a silently mis-scaled cavity
    doc = FreeCAD.newDocument("tsr")
    try:
        scaled = [FreeCAD.Vector(p.x * 3000.0, 0.0, p.z * 3000.0)
                  for p in COORDS]
        rib = makeRib(doc, "mmRib", 3000.0, 0.0, coords=scaled)
        rib.Label = "mmScaledRib"
        try:
            airPlaneCavityDoc.stationFromRib(rib)
            raise AssertionError("mm-scaled Coordinates did not raise")
        except ValueError as err:
            msg = str(err)
            assert "mmScaledRib" in msg and "chord-normalised" in msg, \
                "error message not actionable: %s" % msg
            print("      rejection message: %s" % msg)
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateBandEdges():
    # threshold band edges pinned: TE rounding past 1.0 passes, a
    # doubled-extent section raises
    doc = FreeCAD.newDocument("tbe")
    try:
        te = [FreeCAD.Vector(p.x * 1.004, 0.0, p.z) for p in COORDS]
        rib = makeRib(doc, "te", 2000.0, 0.0, coords=te)
        airPlaneCavityDoc.stationFromRib(rib)  # must NOT raise
        wide = [FreeCAD.Vector(p.x * 2.0, 0.0, p.z) for p in COORDS]
        rib = makeRib(doc, "wide", 2000.0, 0.0, coords=wide)
        try:
            airPlaneCavityDoc.stationFromRib(rib)
            raise AssertionError("x-extent 2.0 did not raise")
        except ValueError:
            pass
        # truncated fragment (LE-only, extent << 1) also raises
        frag = [p for p in COORDS if p.x <= 0.3]
        rib = makeRib(doc, "frag", 2000.0, 0.0, coords=frag)
        try:
            airPlaneCavityDoc.stationFromRib(rib)
            raise AssertionError("LE fragment did not raise")
        except ValueError:
            pass
    finally:
        FreeCAD.closeDocument(doc.Name)


def gatePurity():
    assert PURITY_OK, "importing airPlaneCavityDoc pulled in the GUI"


def loftedWizardPanel(doc, name, rootChord, tipChord, y, twist):
    """Fake wizard panel WITH a real lofted shape (rib wires in the LE
    frame, exactly how airPlaneSWPanel.execute builds it)."""
    root = makeRib(doc, name + "_root", rootChord, 0.0)
    tip = makeRib(doc, name + "_tip", tipChord, y, twist=twist)
    panel = makeWizardPanel(doc, name, root, tip)
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


def gateEndToEnd():
    # the full addCavityToPanel doc-object path on a wizard-shaped fake
    doc = FreeCAD.newDocument("te2e")
    try:
        panel = loftedWizardPanel(doc, "wiz", 3000.0, 1500.0, 15000.0, -4.0)
        created = airPlaneCavityDoc.addCavityToPanel(doc, panel, 20.0)
        labels = [o.Label for o in created]
        assert labels == ["HollowShell (wiz)", "CavityVoid (wiz)",
                          "OuterSkin (wiz)"], "wrong objects: %s" % labels
        shell, void, outer = created
        assert shell.Visibility and not void.Visibility \
            and not outer.Visibility, "visibility defaults wrong"
        assert void.Shape.isValid() and void.Shape.Volume > 0.0 \
            and void.Shape.Shells[0].isClosed(), "void not a closed solid"
        assert shell.Shape.isValid() and shell.Shape.Volume > 0.0 \
            and shell.Shape.Volume < outer.Shape.Volume, \
            "shell not a valid sub-volume of the panel"
        assert panel.Shape.Volume == outer.Shape.Volume, \
            "OuterSkin does not match the panel shape"
        print("      e2e: panel %.2f m3, void %.2f m3, shell %.2f m3"
              % (outer.Shape.Volume / 1e9, void.Shape.Volume / 1e9,
                 shell.Shape.Volume / 1e9))
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateSurfacePanelRefused():
    # curved WingPanel lofts a FACE: addCavityToPanel must REFUSE with an
    # actionable message, not silently produce a 0-solid negative-volume
    # "HollowShell" (PR #61's example panel made this path reachable)
    doc = FreeCAD.newDocument("tsurf")
    try:
        panel = loftedWizardPanel(doc, "surf", 3000.0, 1500.0, 8000.0, 0.0)
        # rebuild the same loft as a FACE (solid=False), like
        # WingPanel.wingpshape's makeSurfaceSolid(..., False)
        pts = [[rib.Placement.multVec(FreeCAD.Vector(
                    p.x * float(rib.Chord), 0.0, p.z * float(rib.Chord)))
                for p in COORDS] for rib in (panel.RootRib, panel.TipRib)]
        for pl in pts:
            if pl[0].sub(pl[-1]).Length < 1e-9:
                pl.pop()
        wires = [Part.makePolygon(pl + [pl[0]]) for pl in pts]
        panel.Shape = Part.makeLoft(wires, False, False)
        assert not panel.Shape.Solids, "test fixture is not a face"
        try:
            airPlaneCavityDoc.addCavityToPanel(doc, panel, 20.0)
            raise AssertionError("face panel did not raise")
        except ValueError as err:
            msg = str(err)
            assert "surf" in msg and "surface" in msg and "solid" in msg, \
                "refusal not actionable: %s" % msg
            assert not [o for o in doc.Objects
                        if o.Name.startswith("HollowShell")], \
                "objects created despite refusal"
            print("      face-panel refusal: %s" % msg)
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateMultiPanelLabels():
    # N4: a multi-panel wing must not produce four identical "HollowShell"
    # labels - addCavityToPanel qualifies each with the panel's Label
    doc = FreeCAD.newDocument("tmpl")
    try:
        a = loftedWizardPanel(doc, "PanelA", 3000.0, 2200.0, 8000.0, -2.0)
        b = loftedWizardPanel(doc, "PanelB", 2200.0, 1400.0, 7000.0, -2.0)
        created = (airPlaneCavityDoc.addCavityToPanel(doc, a, 20.0)
                   + airPlaneCavityDoc.addCavityToPanel(doc, b, 20.0))
        labels = [o.Label for o in created]
        assert len(set(labels)) == 6, "labels not distinct: %s" % labels
        assert "HollowShell (PanelA)" in labels \
            and "HollowShell (PanelB)" in labels, \
            "panel qualification missing: %s" % labels
        print("      multi-panel labels: %s" % ", ".join(labels))
    finally:
        FreeCAD.closeDocument(doc.Name)


def main():
    gates = [
        ("quarter-chord LE conversion (stationFromRib)", gateQuarterChord),
        ("panelSchedule: wizard 2-station + curved N-station",
         gatePanelSchedule),
        ("classifySelection matrix", gateClassify),
        ("refusal path names object and why", gateRefusal),
        ("unit-chord guard accepts legit sections (camber/thin/5-digit)",
         gateUnitChordAccepted),
        ("unit-chord guard rejects mm-scaled Coordinates",
         gateScaledRejected),
        ("unit-chord guard band edges (1.004 ok, 2.0 and fragment raise)",
         gateBandEdges),
        ("import purity (no PySide / FreeCADGui)", gatePurity),
        ("addCavityToPanel end-to-end on a fake wizard panel",
         gateEndToEnd),
        ("face (surface-only) panel refused with actionable message",
         gateSurfacePanelRefused),
        ("multi-panel objects get distinct panel-qualified labels",
         gateMultiPanelLabels),
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
