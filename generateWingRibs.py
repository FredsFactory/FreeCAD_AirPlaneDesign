#################################################
#
# Airfoil creation - Aircraft
# 
# Copyright (c) F. Nivoix - 2018 - V0.1
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
import os,FreeCAD,FreeCADGui

from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
import FreeCAD, FreeCADGui, Draft, Part
import importAirfoilDAT

list_profil_1mm_ref=[]
profil_construction_aile=[]
panel=[]
wing_right=[]
couple=[]
distanceinternervure=[-13.07,13.07+44.18,42.86,43.66,59.67,58.07,57.90,58.14,57.39,57.84,58.37,57.47,57.92,57.95,57.84,57.38,58.04,58.28,57.99,57.84,54.80,65.02,58.41,57.80,58.33,57.88,58.59,58.78,56.98,63.74,52.07,52.01,46.30 ]
anglenervureX=[85.5,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90]


#------------------------------------------------------------------
# Construction des plans de decoupe
#------------------------------------------------------------------
def generateWingRibs(name):
 pos=distanceinternervure[0]
 for i in range(0,32,1):
    p1=FreeCAD.Placement()
    p1.Rotation.Q=(0.0,1.0,0.0,0.0)
    p1.Base=FreeCAD.Vector(-300,-100,0.0)
    Plan_coupe = Draft.makeRectangle(length=700.0,height=200.0,placement=p1,face=True,support=None)
    Plan_coupe.Placement=FreeCAD.Placement(FreeCAD.Vector(-200,pos,-100),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),anglenervureX[i]))
    FreeCAD.ActiveDocument.recompute()
    col=[(1.5,0.5,0.5)]
    FreeCAD.ActiveDocument.Rectangle.ViewObject.DiffuseColor=col
    FreeCAD.ActiveDocument.Rectangle.ViewObject.Transparency=90
    Plan_coupe.Label="PlanDeCoupe_"+str(pos)+"mm"
    #Draft.clone(FreeCAD.ActiveDocument.wing_r)
    pos=pos+distanceinternervure[i+1]
    print pos
    print i
 a=FreeCAD.activeDocument().addObject("Part::MultiCommon","Common")
 a.Shapes = [App.activeDocument().Rectangle,App.activeDocument().Clone,]
 a.Label="Nerv"+str(i)
 Gui.activeDocument().Rectangle.Visibility=False
 Gui.activeDocument().Clone.Visibility=False
 Gui.ActiveDocument.Common.ShapeColor=Gui.ActiveDocument.Rectangle.ShapeColor
 Gui.ActiveDocument.Common.DisplayMode=Gui.ActiveDocument.Rectangle.DisplayMode
 App.ActiveDocument.recompute()
 couple.Append(a)
 return

class GenerateWingRibsCommand():

    def GetResources(self):
        return {
                #'Pixmap'  : ':/AirPlaneDesign/icons/importPart_update.svg', 
                #'Accel' : 'Shift+S', # a default shortcut (optional)
                'MenuText': 'Generate Wing Ribs',
                'ToolTip' : 'Generate Wing Ribs What my new command does'
                  }

    def Activated(self):
        generateWingRibs('blabla')
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCAD.Gui.addCommand('generateWingRibs',GenerateWingRibsCommand())
