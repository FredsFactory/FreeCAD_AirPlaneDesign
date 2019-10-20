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
distanceinternervure=[]
#[-3,13.07+44.18,42.86,43.66,59.67,58.07,57.90,58.14,57.39,57.84,58.37,57.47,57.92,57.95,57.84,57.38,58.04,58.28,57.99,57.84,54.80,65.02,58.41,57.80,58.33,57.88,58.59,58.78,56.98,63.74,52.07,52.01,46.30 ] #premiere nervure -13.07
epaisseurnervure=[]
#[5,5,5,5,5,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2 ]
anglenervureX=[]
#[95.5,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90]


#------------------------------------------------------------------
# Construction des plans de decoupe
#------------------------------------------------------------------
def generateWingRibs(name):
 obj=Draft.clone(FreeCAD.ActiveDocument.getObjectsByLabel(name))
 
 xmax=obj.Shape.BoundBox.XMax
 xmin=obj.Shape.BoundBox.XMin
 ymax=obj.Shape.BoundBox.YMax
 ymin=obj.Shape.BoundBox.YMin
 zmax=obj.Shape.BoundBox.ZMax
 zmin=obj.Shape.BoundBox.ZMin
 xlength=obj.Shape.BoundBox.XLength
 zlength=obj.Shape.BoundBox.ZLength
 print(xmax)
 print(xmin)
 
 print(ymax)
 print(ymin)
 
 print(xlength)
 print(zlength)
 xmax=200
 xmin=-200
 ymax=200
 ymin=-200
 zmax=200
 zmin=-200
 xlength=1000
 zlength=1000
 
 
 aaa=chr(ord('B')+1)+str(2)
 aaaa=float(FreeCAD.ActiveDocument.AirPlaneRibs.getContents(aaa))
 
 
 print("lecture tableau")
 print(aaa)
 print(aaaa)
 ribsnumber=int(FreeCAD.ActiveDocument.AirPlaneRibs.getContents('B1'))
 # init ribs position
 print("ribsnumber:"+str(ribsnumber))
 for i in range(0,ribsnumber,1):
    print("nombre:"+str(i))
    if i<25 :
      distanceinternervure.append(float(FreeCAD.ActiveDocument.AirPlaneRibs.getContents(chr(ord('B')+i)+str(2))))
      epaisseurnervure.append(float(FreeCAD.ActiveDocument.AirPlaneRibs.getContents(chr(ord('B')+i)+str(3))))
      anglenervureX.append(float(FreeCAD.ActiveDocument.AirPlaneRibs.getContents(chr(ord('B')+i)+str(4))))
    else :
      distanceinternervure.append(float(FreeCAD.ActiveDocument.AirPlaneRibs.getContents('A'+chr(ord('A')+i-25)+str(2))))
      epaisseurnervure.append(float(FreeCAD.ActiveDocument.AirPlaneRibs.getContents('A'+chr(ord('A')+i-25)+str(3))))
      anglenervureX.append(float(FreeCAD.ActiveDocument.AirPlaneRibs.getContents('A'+chr(ord('A')+i-25)+str(4))))
 #produce ribs
 pos=-distanceinternervure[0]
 print(ribsnumber)
 for i in range(0,ribsnumber,1):#
    print("Creation nervure")
    print(i)
    p1=FreeCAD.Placement()
    p1.Rotation.Q=(0.0,1.0,0.0,0.0)
    p1.Base=FreeCAD.Vector(xmin,zmin,0.0)
    Plan_coupe = Draft.makeRectangle(xlength,zlength,placement=p1,face=True,support=None)
    Plan_coupe.Placement=FreeCAD.Placement(FreeCAD.Vector(xmin,pos,zmin),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),anglenervureX[i]))
    FreeCAD.ActiveDocument.recompute()
    col=[(1.5,0.5,0.5)]
    FreeCAD.ActiveDocument.Rectangle.ViewObject.DiffuseColor=col
    FreeCAD.ActiveDocument.Rectangle.ViewObject.Transparency=90
    Plan_coupe.Label="PlanDeCoupe_"+str(-round(pos,2))+"mm"
    
    f = FreeCAD.activeDocument().addObject('Part::Extrusion', 'Extrude')
    #f = App.getDocument('AirPlane').getObject('Extrude')
    f.Base = Plan_coupe#App.getDocument('AirPlane').getObject('Nerv_021')
    f.DirMode = "Normal"
    f.DirLink = None
    f.LengthFwd = epaisseurnervure[i]#2.000000000000000
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

    a=FreeCAD.activeDocument().addObject("Part::MultiCommon","Nerv_")
    #a.Shapes = [FreeCAD.activeDocument().Rectangle,b,]#FreeCAD.activeDocument().Clone,]
    a.Shapes = [obj,f,]
    a.Label="Nerv_"+str(-round(pos,2))+"mm"
    if i<ribsnumber-1 :
       pos=pos-distanceinternervure[i+1]
    
    couple.append(a)
    FreeCAD.ActiveDocument.recompute()
 return

class SelectObjectUI():
    def __init__(self):
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/selectobject.ui'
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        for obj in FreeCAD.ActiveDocument.Objects:
            self.form.listWidget.addItem(obj.Label)
        self.form.listWidget.itemSelectionChanged.connect(self.selectionChanged)
        sel = FreeCADGui.Selection.getSelection()
        if sel:
            selected = sel[0].Label
        else:
            selected = None

    def accept(self):
        return
    
    def reject(self):
        FreeCADGui.Control.closeDialog()
        FreeCAD.ActiveDocument.recompute()
        return
    
    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)
    
    def loadTable(self):
        return
    
    def selectionChanged(self):
        a=self.form.listWidget.currentItem()
        item=a.text()
        #print("Selected items: ",item)
        #print filter(lambda obj: obj.Label == label, FreeCAD.ActiveDocument.Objects)[0]
        return
    
    def setupUi(self):
        # Connect Signals and Slots
        #self.form.testButton.clicked.connect(self.importFile)
        #self.loadTable()
        #self.loadPanelTable()
        #self.updateGraphicsViewWings()
        return

class GenerateWingRibsCommand():

    def GetResources(self):
        return {
                #'Pixmap'  : ':/AirPlaneDesign/icons/importPart_update.svg', 
                #'Accel' : 'Shift+S', # a default shortcut (optional)
                'MenuText': 'Generate Wing Ribs',
                'ToolTip' : 'Create a Rib based on DAT file or Generate NACA profil'
                  }

    def Activated(self):
        editor = SelectObjectUI()
        editor.setupUi()
        r = editor.form.exec_()
        if r:
           #r=1 => OK
           a=editor.form.listWidget.currentItem()
           print(a.text())
           generateWingRibs(a.text())
           FreeCAD.Gui.activeDocument().activeView().viewAxonometric()
           FreeCAD.Gui.SendMsgToActiveView("ViewFit")
           pass
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCAD.Gui.addCommand('generateWingRibs',GenerateWingRibsCommand())
