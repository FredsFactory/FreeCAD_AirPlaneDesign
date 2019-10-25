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
from  airPlaneAirFoilNaca import generateNacaChoords
import FreeCAD, FreeCADGui, Draft, Part
import glob, os.path


def listdirectory(path):
    fichier=[]
    l = glob.glob(path+'/*')
    for i in l:
        if os.path.isdir(i): fichier.extend(listdirectory(i))
        else: fichier.append(i)
    return fichier

class SelectObjectUI():
    def __init__(self):
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/selectRibProfil.ui'
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        profil_dir=FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil' 
        self.filePath=""
        
        #QTreeView.__init__(self)
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath( profil_dir)
        tree =  self.form.listProfil
        tree.setModel(self.model)
        tree.hideColumn(1)
        tree.hideColumn(2)
        tree.hideColumn(3)
        tree.hideColumn(4)        
        tree.resizeColumnToContents(0)
        tree.setRootIndex(self.model.index(profil_dir))
              
    def on_treeView_clicked(self,index):
        self.filePath = self.model.filePath(index)
        return 
        
    def profilSelectedFilePath(self):
        return self.filePath
        
    def accept(self):
        #_profil=sel[0].Label
        print(_profil)
        #_chord=self.form.chord.value()
        print(_chord)
        return
    
    def reject(self):
        FreeCADGui.Control.closeDialog()
        FreeCAD.ActiveDocument.recompute()
        return
    
    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)
    
    def selectionChanged(self):
        a=self.form.listProfil.currentItem()
        item=a.text()
        print("Selected items: ",item)
        
        return
    
    def setupUi(self):
        # Connect Signals and Slots
        #self.form.testButton.clicked.connect(self.importFile)
        self.form.NACANumber.textChanged.connect(self.updateGraphicsViewRib)
        self.form.choord.valueChanged.connect(self.updateGraphicsViewRib)
        self.form.nacaNbrPoint.valueChanged.connect(self.updateGraphicsViewRib)
        self.form.listProfil.clicked.connect(self.on_treeView_clicked)
        return
        
    def updateGraphicsViewRib(self):
        choords=[]
        number=self.form.NACANumber.text()
        if len(number)==4:
             #choords=naca4(number, n, finite_TE, half_cosine_spacing)
             choords=generateNacaChoords(number,self.form.nacaNbrPoint.value(),False,0,self.form.choord.value(),0,0,0,0,0,0)
        elif len(number)==5:
             #choords=naca5(number, n, finite_TE, half_cosine_spacing)
             choords=generateNacaChoords(number,self.form.nacaNbrPoint.value(),False,0,self.form.choord.value(),0,0,0,0,0,0)
        else :
             return    
        
        if (len(number)==4) or (len(number))==5 :
             print(number)
             scale=self.form.choord.value()
             scene=QtGui.QGraphicsScene()
             self.form.ribView.setScene(scene)
             #scene.setSceneRect(QtCore.QRectF(-10, -400, 400, 10+self.form.choord.value()))
             #item=QtGui.QGraphicsLineItem(-100,  0, 1000,  0)
             #scene.addItem(item)
             points=[]
             first_v = None
             last_v = None
             for v in choords:
                 if first_v == None:
                     first_v = v
            # End of if first_v == None
            # Line between v and last_v if they're not equal
                 if (last_v != None) and (last_v != v):
                     points.append(QtCore.QPointF(last_v.x*scale,last_v.z*scale ))
                     points.append(QtCore.QPointF(v.x*scale,v.z*scale ))
            # End of if (last_v != None) and (last_v != v)
            # The new last_v
                 last_v = v
                 print("last_v:")
                 print(last_v.x)
                 print("/n")

        # End of for v in upper
        # close the wire if needed
             if last_v != first_v:
                     print("last_v:")
                     print(last_v.x)
                     print("/n")
                     points.append(QtCore.QPointF(last_v.x*scale,last_v.z*scale ))
                     points.append(QtCore.QPointF(first_v.x*scale,first_v.z*scale ))
             item=QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(points))
             item.setPen(QtGui.QPen(QtCore.Qt.blue))
             scene.addItem(item)
             self.form.ribView.setFocus()
             self.form.ribView.show()
        #else:
             #raise Exception            
        return
                
