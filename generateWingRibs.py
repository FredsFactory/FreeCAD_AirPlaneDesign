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
distanceinternervure=[-3,13.07+44.18,42.86,43.66,59.67,58.07,57.90,58.14,57.39,57.84,58.37,57.47,57.92,57.95,57.84,57.38,58.04,58.28,57.99,57.84,54.80,65.02,58.41,57.80,58.33,57.88,58.59,58.78,56.98,63.74,52.07,52.01,46.30 ] #premiere nervure -13.07
anglenervureX=[85.5,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90]


#------------------------------------------------------------------
# Construction des plans de decoupe
#------------------------------------------------------------------
def generateWingRibs(name):
 b=Draft.clone(FreeCAD.ActiveDocument.wing_r)
 xmax=b.Shape.BoundBox.XMax
 xmin=b.Shape.BoundBox.XMin
 zmax=b.Shape.BoundBox.ZMax
 zmin=b.Shape.BoundBox.ZMin
 xlength=b.Shape.BoundBox.XLength
 zlength=b.Shape.BoundBox.ZLength
 
 pos=distanceinternervure[0]
 for i in range(0,25,1):
    p1=FreeCAD.Placement()
    p1.Rotation.Q=(0.0,1.0,0.0,0.0)
    p1.Base=FreeCAD.Vector(xmin,zmin,0.0)
    Plan_coupe = Draft.makeRectangle(xlength,zlength,placement=p1,face=True,support=None)
    Plan_coupe.Placement=FreeCAD.Placement(FreeCAD.Vector(xmin,long(pos),zmin),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),anglenervureX[i]))
    FreeCAD.ActiveDocument.recompute()
    col=[(1.5,0.5,0.5)]
    FreeCAD.ActiveDocument.Rectangle.ViewObject.DiffuseColor=col
    FreeCAD.ActiveDocument.Rectangle.ViewObject.Transparency=90
    Plan_coupe.Label="PlanDeCoupe_"+str(long(pos))+"mm"
    
    f = FreeCAD.activeDocument().addObject('Part::Extrusion', 'Extrude')
    #f = App.getDocument('AirPlane').getObject('Extrude')
    f.Base = Plan_coupe#App.getDocument('AirPlane').getObject('Nerv_021')
    f.DirMode = "Normal"
    f.DirLink = None
    f.LengthFwd = 2.000000000000000
    f.LengthRev = 0.000000000000000
    f.Solid = True
    f.Reversed = False
    f.Symmetric = False
    f.TaperAngle = 0.000000000000000
    f.TaperAngleRev = 0.000000000000000
        #Gui.ActiveDocument.Extrude.ShapeColor=Gui.ActiveDocument.Nerv_021.ShapeColor
        #Gui.ActiveDocument.Extrude.LineColor=Gui.ActiveDocument.Nerv_021.LineColor
        #Gui.ActiveDocument.Extrude.PointColor=Gui.ActiveDocument.Nerv_021.PointColor
    f.Base.ViewObject.hide()
    FreeCAD.ActiveDocument.recompute()

    a=FreeCAD.activeDocument().addObject("Part::MultiCommon","Nerv_")#"Common")
    #a.Shapes = [FreeCAD.activeDocument().Rectangle,b,]#FreeCAD.activeDocument().Clone,]
    a.Shapes = [b,f,]#Plan_coupe,]
    a.Label="Nerv_"+str(pos)+"mm"
    
    pos=pos+distanceinternervure[i+1]
    print pos
    print i
    
    #a.Label="Nerv"+str(i)
    #FreeCAD.ActiveDocument().Rectangle.ViewObject.Visibility=False
    #   FreeCAD.ActiveDocument().Clone.Visibility=False
    #   FreeCAD.ActiveDocument.Common.ShapeColor=Gui.ActiveDocument.Rectangle.ShapeColor
    #   FreeCAD.ActiveDocument.Common.DisplayMode=Gui.ActiveDocument.Rectangle.DisplayMode
    couple.append(a)
    FreeCAD.ActiveDocument.recompute()
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
