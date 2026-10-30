#!/usr/bin/env freecadcmd
#################################################
#
# WingPanel restore tests - Aircraft
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
"""Restore-path gates for the WingPanel proxy.  Run from the repo root:

    freecadcmd tests/testWPanelRestore.py

Restored documents rebuild FeaturePython proxies WITHOUT running __init__;
these gates pin the save -> reopen -> touch -> recompute path (see
__getstate__/__setstate__/_adopt in airPlaneWPanel.py) and the OLD-FORMAT
path: docs saved before those hooks existed reopen with a bare proxy and
__setstate__ never called at all.
Plain asserts + printed summary; failure path calls sys.exit(1) because
freecadcmd 1.1.4 returns 0 on an uncaught exception.
"""
__title__ = "FreeCAD WPanel restore tests"
__author__ = "RedxHerring"
__url__ = "https://fredsfactory.fr"

import os
import sys
import tempfile

import wp_fixture as fx

# measured before any workbench import (airPlaneWPanel pulls PySide/
# FreeCADGui by design)
PURITY_OK = ('PySide' not in sys.modules and 'FreeCADGui' not in sys.modules)

import FreeCAD

import airPlaneWPanel as wp


def gateImportPurity():
    assert PURITY_OK, "loading the test alone pulled in the GUI"


def gateSetstateResetsTransientState():
    # the unpickle path: __setstate__ alone must leave the proxy usable
    proxy = wp.WingPanel.__new__(wp.WingPanel)   # like a restore: no __init__
    proxy.__setstate__({'extract': False})
    assert proxy.obj is None, "obj not reset to None"
    assert proxy.doScaleXYZ == [] and proxy.doScaleXYZsum == [False] * 3, \
        "transient scale state not reset"
    doc = FreeCAD.newDocument("tss")
    try:
        obj = doc.addObject("App::FeaturePython", "panel")
        # a restored feature carries its saved properties; add them all
        # BEFORE attaching the proxy so no onChanged rebuild fires.  Empty
        # Hullcurves makes execute() fall through before makeRibs.
        for p, t in (("Ribs", "App::PropertyLinkList"),
                     ("Base", "App::PropertyLink"),
                     ("Axis", "App::PropertyVector"),
                     ("Hullcurves", "App::PropertyLinkList"),
                     ("Items", "App::PropertyFloat")):
            obj.addProperty(t, p, "RestoreGate")
        obj.Axis = FreeCAD.Vector(0.0, 1.0, 0.0)
        obj.Proxy = proxy                        # restore does this too
        fresh = wp.WingPanel.__new__(wp.WingPanel)
        fresh.__setstate__({'extract': False})
        fresh.execute(obj)
        assert fresh.obj is obj, "execute did not re-adopt the feature"
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateOnChangedAdoptsBeforeDelete():
    # onChanged wipes ribs BEFORE execute; it only survives a restored proxy
    # if it adopts self.obj first
    proxy = wp.WingPanel.__new__(wp.WingPanel)
    proxy.__setstate__({'extract': False})
    doc = FreeCAD.newDocument("toc")
    try:
        obj = doc.addObject("App::FeaturePython", "panel")
        obj.Proxy = proxy
        # no Base: onChanged's proplist guard returns early anyway; adoption
        # must have happened regardless
        proxy.onChanged(obj, "Twist")
        assert proxy.obj is obj, "onChanged did not re-adopt the feature"
    finally:
        FreeCAD.closeDocument(doc.Name)


def gateSaveReopenTouchRecompute():
    # the user story: reopen a saved doc, touch a tracked property,
    # recompute - ribs and skin survive
    tmp = os.path.join(tempfile.gettempdir(), "wp_restore_gate.FCStd")
    if os.path.exists(tmp):
        os.remove(tmp)
    doc, panel = fx.make_panel_doc("wpre", 400.0)
    ribs0 = len(panel.Ribs)
    doc.saveAs(tmp)
    FreeCAD.closeDocument(doc.Name)
    doc = FreeCAD.openDocument(tmp)
    try:
        panel = doc.getObject("Panel")
        assert panel is not None, "panel missing after reopen"
        proxy = panel.Proxy
        assert getattr(proxy, "obj", None) is panel or \
            hasattr(proxy, "doScaleXYZ"), \
            "restored proxy did not run __setstate__"
        doc.recompute()                          # open-recompute path
        panel.TipTwist = 3.0                     # tracked property
        doc.recompute()
        assert len(panel.Ribs) >= 2, \
            "ribs wiped by reopen+touch (%d left)" % len(panel.Ribs)
        assert not panel.Shape.isNull(), "skin lost after reopen+touch"
        print("      reopen+touch kept %d ribs (built %d), skin %.0f mm2"
              % (len(panel.Ribs), ribs0, panel.Shape.Area))
    finally:
        FreeCAD.closeDocument(doc.Name)
        os.remove(tmp)


def gateRestoreWithoutSetstate():
    # THE GUI REGRESSION: pre-hook docs stored an EMPTY proxy state (its obj
    # link broke the JSON dump), so on open FreeCAD allocates via __new__ and
    # skips __setstate__ outright - the proxy has no attributes at all and
    # `self.obj` raises AttributeError in _adopt, wedging every rebuild
    # (panel Touched/Invalid, TipTwist inert).  getattr is the load-bearing fix.
    #
    # part 1: bare __new__, no __setstate__ call, empty __dict__
    proxy = wp.WingPanel.__new__(wp.WingPanel)
    assert 'obj' not in proxy.__dict__, "bare __new__ must have no obj"
    doc = FreeCAD.newDocument("noset")
    try:
        obj = doc.addObject("App::FeaturePython", "panel")
        for p, t in (("Ribs", "App::PropertyLinkList"),
                     ("Base", "App::PropertyLink"),
                     ("Axis", "App::PropertyVector"),
                     ("Hullcurves", "App::PropertyLinkList"),
                     ("Items", "App::PropertyFloat")):
            obj.addProperty(t, p, "RestoreGate")
        obj.Axis = FreeCAD.Vector(0.0, 1.0, 0.0)
        obj.Proxy = proxy
        proxy.onChanged(obj, "TipTwist")         # must not raise
        proxy.execute(obj)                       # must not raise
        assert proxy.obj is obj, "empty-dict proxy did not re-adopt"
    finally:
        FreeCAD.closeDocument(doc.Name)

    # part 2: end-to-end - save WITHOUT the hooks (old class behaviour),
    # reopen WITH them, touch TipTwist, rebuild must survive
    tmp = os.path.join(tempfile.gettempdir(), "wp_oldfmt_gate.FCStd")
    if os.path.exists(tmp):
        os.remove(tmp)
    doc, panel = fx.make_panel_doc("wpold", 400.0)
    gs, ss = wp.WingPanel.__getstate__, wp.WingPanel.__setstate__
    try:
        del wp.WingPanel.__getstate__
        del wp.WingPanel.__setstate__            # dump __dict__, like HEAD did
        doc.saveAs(tmp)
    finally:
        wp.WingPanel.__getstate__ = gs
        wp.WingPanel.__setstate__ = ss
    FreeCAD.closeDocument(doc.Name)
    doc = FreeCAD.openDocument(tmp)
    try:
        panel = doc.getObject("Panel")
        proxy = panel.Proxy
        # prove this really is the empty-state path, not a silent upgrade:
        # 'extract' can only arrive via __setstate__ (obj may already be
        # re-adopted by an onChanged that fired during the open itself)
        assert 'extract' not in proxy.__dict__, \
            "old-format reopen unexpectedly applied __setstate__: %r" \
            % (sorted(proxy.__dict__),)
        panel.TipTwist = -3.0                    # fired onChanged -> crash before
        doc.recompute()
        assert len(panel.Ribs) >= 2, \
            "old-format reopen+TipTwist wiped ribs (%d left)" % len(panel.Ribs)
        assert not panel.Shape.isNull(), "skin lost after old-format reopen"
        print("      old-format reopen rebuilt %d ribs, skin %.0f mm2"
              % (len(panel.Ribs), panel.Shape.Area))
    finally:
        FreeCAD.closeDocument(doc.Name)
        os.remove(tmp)


fx.run_gates([
    ("module imports stay headless-safe to load under freecadcmd",
     gateImportPurity),
    ("__setstate__ resets transient state; execute re-adopts",
     gateSetstateResetsTransientState),
    ("onChanged adopts self.obj before its rib wipe",
     gateOnChangedAdoptsBeforeDelete),
    ("save -> reopen -> touch -> recompute keeps ribs + skin",
     gateSaveReopenTouchRecompute),
    ("old-format restore without __setstate__ rebuilds (GUI regression)",
     gateRestoreWithoutSetstate),
])
