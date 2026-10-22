#################################################
#
# Cavity void creation - Aircraft (GUI command)
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

__title__ = "FreeCAD airPlaneCavity GUI"
__author__ = "RedxHerring"
__url__ = "https://fredsfactory.fr"

import os

import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui

import airPlaneCavityDoc
from airPlaneAirFoilNaca import generateNacaCoords

apWB_icons_path = os.path.join(os.path.dirname(__file__), 'resources', 'icons')

# SCOPE: airPlaneCavity.makeCavityVoid() needs a per-station SECTION SCHEDULE
# (coords, chord, placement).  Reconstructing that schedule from an arbitrary
# selected solid is not reliable, so this command is a GENERATOR, not a
# general solid-sheller.  Layering: panel -> params dict ->
# airPlaneCavityDoc.buildCavityShapes(params) -> shapes -> object loop (the
# loop takes shapes, never params).  Geometry lives in airPlaneCavityDoc.py
# (Qt-free); ALL Qt imports stay in this file.


def showError(exc):
    box = QtGui.QMessageBox()
    box.setIcon(QtGui.QMessageBox.Critical)
    box.setWindowTitle("Cavity void error")
    box.setText("The cavity void could not be created.")
    box.setInformativeText(str(exc))
    box.setStandardButtons(QtGui.QMessageBox.Ok)
    box.exec_()


class CavityTaskPanel(QtGui.QDialog):
    """Modal parameter panel (APD create-command idiom: nacelle/rib/wizard
    are all modal QDialogs).  OK validates the NACA designation and keeps
    the panel open on a bad one; Cancel closes without a params read."""

    def __init__(self, parent=None):
        super(CavityTaskPanel, self).__init__(parent)
        self.setWindowTitle("Cavity Void")
        form = QtGui.QFormLayout(self)
        # Defaults approximate a Boeing 787-9 planform under this model's
        # trapezoid math: semi-span 30050 (full span 60.1 m - the span field
        # IS the root->tip semi-span), taper 0.31, root chord 9070 chosen so
        # full area = span*root*(1+lambda) = 357 m2 and full AR = (2*span)^2/
        # area = 10.1.  Tip sweep 19500 mm puts the LINE THROUGH THE STATION
        # LEADING EDGES at ~35 deg (tan 35 * 30050 - 0.25*(root-tip) LE
        # offset; the quarter-chord line lands ~33 deg) - a linear tip LE
        # offset model, NOT a true 35 deg swept LE curve.  NACA 0015 is an
        # honest stand-in for the real supercritical section (4-digit NACA
        # cannot represent it).  Washout -4 deg mid-range; wall and nPts are
        # NOT 787-derived (20 mm anchor, 41 measured anchor).
        self.number = QtGui.QLineEdit("0015")
        self.rootChord = self._spin(9070.0, 100.0, 99999.0, 1.0, " mm")
        self.span = self._spin(30050.0, 500.0, 999999.0, 1.0, " mm")
        # span is the ROOT->TIP distance of this half-wing model (stations
        # at y = 0, span/2, span); the summary read-out shows FULL-wing
        # values (area x2, AR of the symmetric aircraft)
        self.span.setToolTip("root->tip distance (half-wing model, "
                             "stations at y = 0, span/2, span)")
        self.taper = self._spin(0.31, 0.05, 1.00, 0.01, "")
        self.taper.setToolTip("tip chord / root chord")
        self.washout = self._spin(-4.0, -30.0, 15.0, 0.5, u"\u00b0")
        self.washout.setToolTip("twist at the tip, linear from root (0) to "
                                "tip; negative = washout")
        self.sweep = self._spin(19500.0, -30000.0, 30000.0, 50.0, " mm")
        self.sweep.setToolTip("leading-edge offset of the tip, negative = "
                              "forward sweep, linear from root")
        self.wall = self._spin(20.0, 1.0, 200.0, 0.5, " mm")
        self.nPts = QtGui.QSpinBox()
        self.nPts.setRange(11, 121)
        self.nPts.setValue(41)
        self.nPts.setToolTip("cavity resample points per surface "
                             "(core default 41)")
        form.addRow("NACA designation", self.number)
        form.addRow("Root chord", self.rootChord)
        form.addRow("Span (root->tip)", self.span)
        form.addRow("Taper ratio", self.taper)
        form.addRow("Washout at tip", self.washout)
        form.addRow("Tip sweep (LE)", self.sweep)
        form.addRow("Wall thickness", self.wall)
        form.addRow("Cavity points/surface", self.nPts)
        self.summary = QtGui.QLabel()
        self.summary.setWordWrap(True)
        form.addRow(self.summary)
        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok
                                        | QtGui.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._onOk)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)
        for w in (self.rootChord, self.span, self.taper):
            w.valueChanged.connect(self._updateSummary)
        self._updateSummary()

    @staticmethod
    def _spin(value, lo, hi, step, suffix):
        sb = QtGui.QDoubleSpinBox()
        sb.setRange(lo, hi)
        sb.setSingleStep(step)
        sb.setSuffix(suffix)
        sb.setValue(value)
        return sb

    def _updateSummary(self):
        # derived read-out (aspect ratio is shown, never typed); FULL-wing
        # values so they match published aircraft figures: the model is a
        # half-wing, so area x2 and AR = (2*span)^2 / area_full
        root = self.rootChord.value()
        lam = self.taper.value()
        span = self.span.value()
        areaFull = 2.0 * airPlaneCavityDoc.planformAreaMm2(root, lam, span)
        self.summary.setText(
            "tip chord %.0f mm   planform %.2f m2   AR %.2f"
            % (lam * root, areaFull / 1e6, (2.0 * span) ** 2 / areaFull))

    def _onOk(self):
        try:  # validate BEFORE the document is ever touched; stay open
            generateNacaCoords(self.params()["number"], 40, False, True,
                               1, 0, 0, 0, 0, 0, 0)
        except ValueError as exc:
            showError(exc)
            return
        self.accept()

    def params(self):
        return {"number": str(self.number.text()).strip(),
                "rootChord": self.rootChord.value(),
                "span": self.span.value(),
                "taper": self.taper.value(),
                "tipTwist": self.washout.value(),
                "tipSweep": self.sweep.value(),
                "wall": self.wall.value(),
                "nPts": self.nPts.value()}


class CommandCavityVoid:
    "Build a wing from a chosen NACA section and cut a cavity void"

    def GetResources(self):
        return {'Pixmap': os.path.join(apWB_icons_path, 'cavity_void.png'),
                'MenuText': QtCore.QT_TRANSLATE_NOOP(
                    "Create_a_Cavity_Void", "Create cavity void"),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP(
                    "Create_a_Cavity_Void",
                    "Build a tapered, twisted and swept wing from the "
                    "chosen NACA section and cut a cavity void at the "
                    "chosen wall thickness (HollowShell / CavityVoid / "
                    "OuterSkin)")}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        # Phase B: a selection means "cavity THIS APD wing/panel" - only the
        # wall thickness is prompted, the geometry comes FROM the object.
        # No selection keeps the full demo task panel below.
        doc = FreeCAD.ActiveDocument
        sel = FreeCADGui.Selection.getSelectionEx()
        if sel:
            self._cavityFromSelection(doc, sel[0].Object)
            return
        panel = CavityTaskPanel(FreeCADGui.getMainWindow())
        if panel.exec_() != QtGui.QDialog.Accepted:
            return  # Cancel: nothing touched (never copy nacelle's quit())
        params = panel.params()
        doc.openTransaction("Create cavity void")
        try:
            outer, void, shell = airPlaneCavityDoc.buildCavityShapes(params)
            # lifecycle defaults live in airPlaneCavityDoc.addCavityObjects
            # (HollowShell visible / CavityVoid hidden / OuterSkin x-ray)
            airPlaneCavityDoc.addCavityObjects(doc, outer, void, shell)
            doc.recompute()
            doc.commitTransaction()
        except Exception as exc:
            # e.g. wall too thick for the tip section: the core raises a
            # plain ValueError ("wall swallows the section") - show it,
            # and let the transaction roll the document back
            doc.abortTransaction()
            showError(exc)

    def _cavityFromSelection(self, doc, obj):
        """Selection path: classify -> (wall prompt) -> addCavityToPanel.
        The dialog never touches the document; only this method does,
        inside one transaction."""
        kind, why = airPlaneCavityDoc.classifySelection(obj)
        if kind not in ("wing", "panel"):
            box = QtGui.QMessageBox()
            box.setIcon(QtGui.QMessageBox.Warning)
            box.setWindowTitle("Cavity void")
            box.setText("'%s' (%s) cannot be cavitated."
                        % (obj.Label, obj.TypeId))
            box.setInformativeText(
                why + ".\n\nSupported: APD Wing (WingPanels), wizard "
                "WingSPanel (RootRib/TipRib), curved WingPanel (Ribs "
                "list).")
            box.exec_()
            return
        wall, ok = QtGui.QInputDialog.getDouble(
            FreeCADGui.getMainWindow(), "Cavity wall thickness",
            "Wall thickness (mm) for '%s':\n\nThe cavity objects are "
            "static - after editing the panel geometry later, delete them "
            "and re-run this command." % obj.Label, 20.0, 1.0, 200.0, 1)
        if not ok:
            return  # Cancel: nothing touched
        targets = list(obj.WingPanels) if kind == "wing" else [obj]
        if not targets:
            showError(ValueError("wing '%s' has no WingPanels to cavity"
                                 % obj.Label))
            return
        doc.openTransaction("Create cavity void")
        try:
            for p in targets:
                airPlaneCavityDoc.addCavityToPanel(doc, p, wall)
            doc.recompute()
            doc.commitTransaction()
        except Exception as exc:
            doc.abortTransaction()
            showError(exc)


if FreeCAD.GuiUp:
    # register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignCavity', CommandCavityVoid())
