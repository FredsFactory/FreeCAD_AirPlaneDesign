#!/usr/bin/env freecadcmd
#################################################
#
# WingPanel twist tests - Aircraft
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
"""Twist gates for the WingPanel (WPanel) command.  Run from the repo root:

    freecadcmd tests/testWPanelTwist.py

Twist/TipTwist used to be dead properties (accepted in the GUI, never read).
Convention pinned here (see airPlaneWPanel.WingPanel.__init__):
twist = Twist + TipTwist * f (f: 0 root -> 1 tip), a rotation about the rib
normal (+Y; section plane is the local XZ plane) - the airPlaneCavity
station axis, so negative TipTwist = washout, hinged at the rib origin (LE).
Twist rides on Placement only; Coordinates keeps the untwisted unit chord.
Plain asserts + printed summary; failure path calls sys.exit(1) because
freecadcmd 1.1.4 returns 0 on an uncaught exception.
"""
__title__ = "FreeCAD WPanel twist tests"
__author__ = "RedxHerring"
__url__ = "https://fredsfactory.fr"

import math
import os
import tempfile

import wp_fixture as fx

import FreeCAD
from airPlaneAirFoilNaca import generateNacaCoords


def _ang(rib):
    """Signed twist about the section normal: the straight-path alignment
    rotation is identity here, so the Placement rotation IS the twist."""
    rot = rib.Placement.Rotation
    return math.degrees(rot.Angle) if rot.Axis == FreeCAD.Vector(0, 1, 0) \
        else -math.degrees(rot.Angle)


def gateTipWashoutLinear():
    # TipTwist=20, Twist=0: root stays flat, tip reaches 20 deg, linear
    # between; the LE hinge must not move.
    doc, panel = fx.make_panel_doc("wptw", 450.0)
    try:
        f0 = [_ang(r) for r in panel.Ribs]
        assert all(abs(a) < 1e-9 for a in f0), "build is not flat: %s" % f0
        panel.TipTwist = 20.0                     # the user's GUI action
        doc.recompute()
        f1 = [_ang(r) for r in panel.Ribs]
        n = len(f1)
        assert abs(f1[0]) < 1e-6, "root twisted to %.2f (Twist=0)" % f1[0]
        assert abs(f1[-1] - 20.0) < 0.05, "tip %.2f deg, expected 20" % f1[-1]
        for i, a in enumerate(f1):
            want = 20.0 * i / (n - 1)
            assert abs(a - want) < 0.05, "rib %d: %.2f deg, want %.2f" % (
                i, a, want)
        for r in panel.Ribs:
            assert abs(r.Placement.Base.x) < 1e-6 and \
                abs(r.Placement.Base.z) < 1e-6, \
                "LE hinge moved: %s at %s" % (r.Label, r.Placement.Base)
        print("      station angles %s (linear 0->20 deg about +Y)" % (
            ["%.1f" % a for a in f1]))
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateRootTwistOffset():
    # Twist is the ROOT incidence: Twist=10, TipTwist=20 -> root 10, tip 30.
    doc, panel = fx.make_panel_doc("wptw", 450.0)
    try:
        panel.TipTwist = 20.0
        panel.Twist = 10.0                        # GUI order: both set, then recompute
        doc.recompute()
        f = [_ang(r) for r in panel.Ribs]
        assert abs(f[0] - 10.0) < 0.05, "root %.2f, want Twist=10" % f[0]
        assert abs(f[-1] - 30.0) < 0.05, "tip %.2f, want 10+20" % f[-1]
        print("      Twist=10 TipTwist=20 -> root %.1f tip %.1f" % (f[0], f[-1]))
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateAxisChordWashoutSign():
    # axis is the rib normal (perpendicular to the chord): with the cavity
    # sign, negative TipTwist must raise the tip TE and tilt the chord up.
    doc, panel = fx.make_panel_doc("wptw", 450.0)
    try:
        z0 = panel.Ribs[-1].Shape.BoundBox.ZMax
        panel.TipTwist = -10.0                    # washout, cavity convention
        doc.recompute()
        tip = panel.Ribs[-1]
        bb = tip.Shape.BoundBox
        # tip chord 100 mm hinged at the LE: TE rises to ~sin(10)*100,
        # dominating the twisted section's ZMax
        assert bb.ZMax > math.sin(math.radians(10)) * 90.0, \
            "washout did not raise the TE (ZMax %.2f -> %.2f)" % (z0, bb.ZMax)
        chord = tip.Placement.Rotation.multVec(FreeCAD.Vector(1, 0, 0))
        ang = _ang(tip)
        assert abs(chord.z + math.sin(math.radians(ang))) < 1e-9, \
            "chord tilt wrong: z=%.6f, ang=%.2f" % (chord.z, ang)
        assert abs(chord.dot(FreeCAD.Vector(0, 1, 0))) < 1e-9, \
            "chord left the rib plane (rotation not about the normal)"
        print("      TipTwist=-10: TE ZMax %.1f -> %.1f, chord z-component %.3f"
              % (z0, bb.ZMax, chord.z))
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateCoordinatesStayUnitChord():
    # Twist lives on Placement ONLY: Coordinates keeps the untwisted
    # unit-chord frame, the invariant airPlaneCavity's schedule reads.
    doc, panel = fx.make_panel_doc("wptw", 450.0)
    try:
        panel.Twist = 5.0
        panel.TipTwist = 20.0
        doc.recompute()
        ref = generateNacaCoords("2412", 40, False, True, 1,
                                 0, 0, 0, 0, 0, 0)
        for r in panel.Ribs:
            c = r.Coordinates
            assert len(c) == len(ref), "%s: coords length changed" % r.Label
            assert max(abs(p.y) for p in c) < 1e-12, \
                "%s: coords left the section plane" % r.Label
            assert max(abs(p.x) for p in c) <= 1.0 + 1e-9 and \
                min(p.x for p in c) > -1e-9, \
                "%s: coords are not unit chord (x range %f..%f)" % (
                    r.Label, min(p.x for p in c), max(p.x for p in c))
            for p, q in zip(c, ref):
                assert (p - q).Length < 1e-9, \
                    "%s: coords rotated by the twist" % r.Label
        print("      all %d twisted ribs keep the base rib's unit-chord coords"
              % len(panel.Ribs))
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateSkinRebuiltAndRibRecomputeSurvives():
    # the skin must be re-lofted over the twisted ribs, and a plain
    # touch+recompute of a twisted rib must keep its placement and shape.
    doc, panel = fx.make_panel_doc("wptw", 450.0)
    try:
        z0 = panel.Shape.BoundBox.ZLength
        area0 = panel.Shape.Area
        panel.Twist = 0.0
        panel.TipTwist = 20.0
        doc.recompute()
        assert panel.Shape.isValid(), "twisted skin is invalid"
        assert panel.Shape.BoundBox.ZLength > 1.5 * z0, \
            "skin not re-lofted over twisted ribs (zext %.1f vs %.1f)" % (
                panel.Shape.BoundBox.ZLength, z0)
        tip = panel.Ribs[-1]
        ang, pos = _ang(tip), tuple(tip.Placement.Base)
        zmax = tip.Shape.BoundBox.ZMax
        tip.touch()
        doc.recompute()
        assert abs(_ang(tip) - ang) < 1e-6, \
            "rib recompute wiped the twist (%.2f -> %.2f)" % (ang, _ang(tip))
        assert tuple(tip.Placement.Base) == pos, "rib recompute moved it"
        assert abs(tip.Shape.BoundBox.ZMax - zmax) < 1e-6, \
            "rib shape lost the twist on recompute"
        print("      skin %.0f -> %.0f mm2 (zext %.1f -> %.1f), touch kept "
              "ang %.1f deg" % (area0, panel.Shape.Area, z0,
                                panel.Shape.BoundBox.ZLength, ang))
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateSaveReopenRetwist():
    # save a twisted panel, reopen, change TipTwist: ribs survive, re-twist
    tmp = os.path.join(tempfile.gettempdir(), "wp_twist_gate.FCStd")
    if os.path.exists(tmp):
        os.remove(tmp)
    doc, panel = fx.make_panel_doc("wptw", 450.0)
    panel.Twist = 5.0
    panel.TipTwist = 15.0
    doc.recompute()
    ribs0 = len(panel.Ribs)
    doc.saveAs(tmp)
    FreeCAD.closeDocument(doc.Name)
    doc = FreeCAD.openDocument(tmp)
    try:
        panel = doc.getObject("Panel")
        assert panel is not None, "panel missing after reopen"
        doc.recompute()
        panel.TipTwist = 20.0                     # tracked: must rebuild
        doc.recompute()
        assert len(panel.Ribs) >= 2, "ribs wiped by reopen+retwist"
        assert not panel.Shape.isNull(), "skin lost after reopen+retwist"
        f = [_ang(r) for r in panel.Ribs]
        assert abs(f[0] - 5.0) < 0.05 and abs(f[-1] - 25.0) < 0.05, \
            "twist after reopen+retwist wrong: %s" % f
        print("      reopen -> TipTwist 15->20: %d ribs, root %.1f tip %.1f"
              % (ribs0, f[0], f[-1]))
    finally:
        FreeCAD.closeDocument(doc.Name)
        os.remove(tmp)


fx.run_gates([
    ("TipTwist=20 twists tip 20 deg about the rib normal, linearly",
     gateTipWashoutLinear),
    ("Twist is the root incidence (Twist=10, TipTwist=20 -> 10..30)",
     gateRootTwistOffset),
    ("axis is the section normal; negative TipTwist = washout (cavity sign)",
     gateAxisChordWashoutSign),
    ("twisted ribs keep untwisted unit-chord Coordinates (cavity contract)",
     gateCoordinatesStayUnitChord),
    ("skin re-lofted; rib touch+recompute keeps placement and shape",
     gateSkinRebuiltAndRibRecomputeSurvives),
    ("save -> reopen -> TipTwist change -> rebuild keeps the twist",
     gateSaveReopenRetwist),
])
