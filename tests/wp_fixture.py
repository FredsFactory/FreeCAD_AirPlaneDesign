#!/usr/bin/env freecadcmd
#################################################
#
# WingPanel shared test fixture - Aircraft
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
"""Shared fixture for the headless WPanel gates (run under freecadcmd).

Importing this sets up stdout buffering and sys.path only - no workbench
module is imported at module level, so tests can measure import purity
before it (airPlaneWPanel pulls in PySide/FreeCADGui by design).
"""
__title__ = "FreeCAD WPanel test fixture"
__author__ = "RedxHerring"
__url__ = "https://fredsfactory.fr"

import os
import sys
import traceback

try:
    sys.stdout.reconfigure(line_buffering=True)
except AttributeError:
    pass

# uninstalled checkout: the workbench root is the parent of tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import FreeCAD
import Part


def line(doc, name, p0, p1):
    ln = doc.addObject("Part::Feature", name)
    ln.Shape = Part.makeLine(p0, p1)
    return ln


def make_panel_doc(doc_name, panel_length):
    """Recomputed wizard-free WingPanel doc: straight LE/TE/path lines along
    +Y (workbench frame: X chord aft, Y span, Z up) + a NACA 2412 base rib.
    LE 0->450, TE tapered 300->100 mm, so the rib window is [0,450] and the
    i-th of Items=5 ribs sits at f = i/4.  Asserts a real skin was built."""
    # deferred: keep purity measurement possible before this import (see the
    # module docstring); the tests import airPlaneWPanel after measuring too
    import airPlaneWPanel as wp
    from airPlaneRib import WingRib
    doc = FreeCAD.newDocument(doc_name)
    try:
        le = line(doc, "LE", FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 450, 0))
        te = line(doc, "TE", FreeCAD.Vector(300, 0, 0), FreeCAD.Vector(100, 450, 0))
        path = line(doc, "Path", FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 450, 0))
        base = doc.addObject("Part::FeaturePython", "BaseRib")
        # headless: no ViewObject; createRib only needs the data props + Shape
        WingRib(base, "2412", True, 40, 300.0, 0, 0, 0, 0, 0, 0)
        panel = doc.addObject("Part::FeaturePython", "Panel")
        wp.WingPanel(panel, base, path, te, le, te,
                     _rootChord=300.0, _tipChord=100.0, _panelLength=panel_length)
        doc.recompute()
        assert len(panel.Ribs) >= 2, "fixture built %d ribs" % len(panel.Ribs)
        assert not panel.Shape.isNull(), "fixture skin is null"
        return doc, panel
    except Exception:
        FreeCAD.closeDocument(doc.Name)
        raise


def run_gates(gates):
    failed = []
    for name, fn in gates:
        try:
            fn()
            print("PASS  %s" % name)
        except Exception as exc:
            traceback.print_exc()
            print("FAIL  %s: %s" % (name, exc))
            failed.append(name)
    print("%d/%d gates pass" % (len(gates) - len(failed), len(gates)))
    if failed:
        sys.exit(1)
