#################################################
#
# Airfoil creation - Aircraft
#
# Copyright (c) F. Nivoix - 2020 - V0.4
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

__title__="FreeCAD Airplane Design"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"



import FreeCAD
import FreeCADGui
import os
from PySide import QtGui
from airPlaneSWPanel import WingSPanel,ViewProviderPanel
from airPlaneRib import WingRib, ViewProviderWingRib
from airPlaneWingUI import WingEditorPanel
import airPlaneCavityDoc

#################################################
#  This module provides a wizard to build a
#  wing panel
#################################################
if open.__module__ in ['__builtin__','io', '_io']:
    pythonopen = open

_wingRibProfilDir = os.path.join(os.path.dirname(__file__), 'wingribprofil')

# last PanelTable column (appended after "Ribs number"), see
# resources/airPlaneDesignWingdialog.ui.  Units: mm, implicit - matches the
# sibling columns, which all omit units.
CAVITY_WALL_COL = 14



class CommandWPanel:
    "the WingPanel command definition"
    def GetResources(self):
        return {'MenuText': "Wing wizard"}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        print("-----------------Wing Wizard-----------------")
        selection = FreeCADGui.Selection.getSelectionEx()
        if selection :
           base = FreeCAD.ActiveDocument.getObject((selection[0].ObjectName))

        PanelTable=[]
        editor = WingEditorPanel()
        editor.setupUi()
        r = editor.form.exec_()

        if r:
          for row_number in range(editor.form.PanelTable.rowCount()):
             rowData=[]
             #create Panel
             for col_number in range(10):#int(editor.form.PanelTable.columnCount())):
                rowData.append(editor.form.PanelTable.item(row_number,col_number).text())
             PanelTable.append(rowData)
        _panelInput=PanelTable


        _ribs=[]
        _position=0
        _PanelLength=[]
        profil=[]
        b=[]
        #for i in range(0,obj.NberOfPanel) :
        for i in range(0,editor.form.PanelTable.rowCount()) :
           _row=_panelInput[i]
           FreeCAD.Console.PrintMessage("Rrow:"+str(_row)+"\n")
           profil.append(_row[2])
           _PanelLength.append(float(_row[4]))

            # Add Rib Root
           _ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibRoot_"+str(i)))
           #WingRibs(obj,_profil,_nacagene,_nacaNbrPoint,_chord,_x,_y,_z,_xrot,_yrot,_zrot,_thickness=0,_useSpline = True,_finite_TE = False,_splitSpline = False):
           #def     (obj,_profil,_nacagene,_nacaNbrPoint,_chord,_x,_y,_z,_xrot,_yrot,_zrot,_rot=0,_thickness=0,_useSpline = True,_finite_TE = False,_splitSpline = False):
           WingRib(_ribs[i*2],_row[2],False,0,float(_row[3]),float(_row[6]),_position,float(_row[8]),0,0,0)
           #FreeCAD.ActiveDocument.recompute()
           ViewProviderWingRib(_ribs[i*2].ViewObject)

           # Add Rib tip
           _position=_position+float(_row[5])
           _ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibTip_"+str(i)))
           WingRib(_ribs[i*2+1],_row[2],False,0,float(_row[4]),float(_row[7]),_position,float(_row[9]),0,0,0)
           #FreeCAD.ActiveDocument.recompute()
           ViewProviderWingRib(_ribs[i*2+1].ViewObject)
           # Add wing panel
           obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","WingPanel")
           #WingPanel(obj, _rootRib ,_tipRib ,_rootChord=200,_tipChord=100,_panelLength=100,_tipTwist=0,_dihedral=0)
           WingSPanel(obj,_ribs[i*2],_ribs[i*2+1],float(_row[3]),float(_row[4]),_position,0,0)
           ViewProviderPanel(obj.ViewObject)
           FreeCAD.ActiveDocument.recompute()
           # Phase C: per-panel cavity from the table's last column
           # ("Cavity wall", mm implicit like every other column).  Empty /
           # N/A / - = SOLID (default); a number > 0 makes THIS panel
           # hollow with that wall thickness.
           # A cavity that starts or stops between panels ends in a FLAT
           # BULKHEAD CAP at the rib plane - physically meaningful, and it
           # comes free from makeCavityVoid's closed solid loft.
           # CAVEAT: HollowShell/CavityVoid/OuterSkin are STATIC
           # Part::Features while WingSPanel.execute rewrites the panel
           # Shape on every recompute - editing a panel's chord/twist/
           # profile afterwards leaves the cavity STALE: delete the three
           # objects and re-run the wizard to recreate it.
           # One bad panel must not abort the build, but the two failure
           # classes differ: invalid cell text is a SOFT skip (console
           # warning, panel left solid); a VALID wall the geometry cannot
           # take (core "wall swallows the section" ValueError) is a
           # refused explicit request and must be VISIBLE in the GUI, not
           # console-only.
           _cavItem = editor.form.PanelTable.item(i, CAVITY_WALL_COL)
           try:
               _wall = airPlaneCavityDoc.parseCavityCell(
                   _cavItem.text() if _cavItem is not None else "")
           except ValueError as _exc:
               FreeCAD.Console.PrintWarning(
                   "Wing wizard: cavity skipped for panel row %d (%s): "
                   "panel left solid\n" % (i + 1, _exc))
               _wall = None
           if _wall is not None:
               try:
                   airPlaneCavityDoc.addCavityToPanel(
                       FreeCAD.ActiveDocument, obj, _wall)
               except Exception as _exc:
                   FreeCAD.Console.PrintWarning(
                       "Wing wizard: cavity FAILED for panel row %d (%s): "
                       "panel left solid\n" % (i + 1, _exc))
                   # inline box, not airPlaneCavityGui.showError: that
                   # module runs addCommand at import time
                   box = QtGui.QMessageBox()
                   box.setIcon(QtGui.QMessageBox.Critical)
                   box.setWindowTitle("Wing wizard: cavity failed")
                   box.setText("Panel row %d could not be hollowed."
                               % (i + 1))
                   box.setInformativeText(str(_exc))
                   box.setStandardButtons(QtGui.QMessageBox.Ok)
                   box.exec_()
           #obj.ViewObject.hide()
           #add to Wing
           if selection : #selection==None :
              if not base.WingPanels :
                 base.WingPanels=obj
              else :
                 b=base.WingPanels
                 b.append(obj)
                 base.WingPanels=b

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignWingWizard',CommandWPanel())
