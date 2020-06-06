#################################################
#
# Airfoil creation - Aircraft
# 
# Copyright (c) F. Nivoix - 2019 - V0.1
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
from airPlaneWPanel import WingPanel,ViewProviderPanel
from airPlaneRib import WingRib, ViewProviderWingRib
from airPlaneWingUI import WingEditorPanel

#################################################
#  This module provides tools to build a
#  wing panel
#################################################
if open.__module__ in ['__builtin__','io']:
    pythonopen = open

_wingRibProfilDir=FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil'



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
           profil.append(_row[2])
           _PanelLength.append(float(_row[4]))
           # Add Rib Root
           _ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibRoot_"+str(i)))
           #WingRibs(obj,_profil,_nacagene,_nacaNbrPoint,_chord,_x,_y,_z,_xrot,_yrot,_zrot,_thickness=0,_useSpline = True,_finite_TE = False,_splitSpline = False):
           WingRib(_ribs[i*2],_row[2],False,0,_row[3],_row[6],_position,_row[8],0,0,0)
           #FreeCAD.ActiveDocument.recompute() 
           ViewProviderWingRib(_ribs[i*2].ViewObject)           
           # Add Rib tip
           _position=_position+float(_row[5])
           _ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibTip_"+str(i)))
           WingRib(_ribs[i*2+1],_row[2],False,0,_row[4],_row[7],_position,_row[9],0,0,0)
           #FreeCAD.ActiveDocument.recompute() 
           ViewProviderWingRib(_ribs[i*2+1].ViewObject)
           # Add wing panel
           obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","WingPanel")
           #WingPanel(obj, _rootRib ,_tipRib ,_rootChord=200,_tipChord=100,_panelLength=100,_tipTwist=0,_dihedral=0)
           WingPanel(obj,_ribs[i*2],_ribs[i*2+1],_row[3],_row[4],_position,0,0)
           ViewProviderPanel(obj.ViewObject)
           FreeCAD.ActiveDocument.recompute() 
           obj.ViewObject.hide()
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
