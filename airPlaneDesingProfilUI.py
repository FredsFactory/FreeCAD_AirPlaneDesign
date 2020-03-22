#################################################
#
# Airfoil creation - Aircraft
# 
# Copyright (c) F. Nivoix - 2018 - V0.3
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
import os
import FreeCAD
import FreeCADGui 
#import Draft
#import Part
import glob
import os.path

from PySide import QtCore, QtGui

from  airPlaneAirFoilNaca import generateNacaCoords
from airPlaneAirFoil import readpointsonfile #,decodeName,process
from FreeCAD import Vector #, Base

FreeCADGui.addLanguagePath(":/translations")

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)



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
        #self.filePath=""
        
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
        self.form.NACANumber.textChanged.connect(self.updateGraphicsNACAViewRib)
        self.form.chord.valueChanged.connect(self.updateGraphicsNACAViewRib)
        self.form.nacaNbrPoint.valueChanged.connect(self.updateGraphicsNACAViewRib)
        self.form.listProfil.clicked.connect(self.on_treeView_clicked)
        self.form.listProfil.clicked.connect(self.updateTableViewDAT)
        return
    

 
    def updateGraphicsViewRib(self,coords):
        #coords=_coords 
        scale=self.form.chord.value()*2
        scene=QtGui.QGraphicsScene()
        self.form.ribView.setScene(scene)
            
        points=[]
        first_v = None
        last_v = None
        for v in coords:
                 if first_v is None:
                     first_v = v
            # End of if first_v is None
            # Line between v and last_v if they're not equal
                 if (last_v != None) and (last_v != v):
                     points.append(QtCore.QPointF(last_v.x*scale,-last_v.y*scale ))
                     points.append(QtCore.QPointF(v.x*scale,-v.y*scale ))
            # End of if (last_v != None) and (last_v != v)
            # The new last_v
                 last_v = v

        # End of for v in upper
        # close the wire if needed
        if last_v != first_v:
                     points.append(QtCore.QPointF(last_v.x*scale,-last_v.y*scale ))
                     points.append(QtCore.QPointF(first_v.x*scale,-first_v.y*scale ))
        item=QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(points))
        item.setPen(QtGui.QPen(QtCore.Qt.blue))
        scene.addItem(item)
        self.form.ribView.setFocus()
        self.form.ribView.show()
                 
        return    

    
    def updateGraphicsNACAViewRib(self):
        coords=[]
        number=self.form.NACANumber.text()
        if len(number)==4:
             #coords=naca4(number, n, finite_TE, half_cosine_spacing)
             coords=generateNacaCoords(number,self.form.nacaNbrPoint.value(),False,0,self.form.chord.value(),0,0,0,0,0,0,coords)
        elif len(number)==5:
             #coords=naca5(number, n, finite_TE, half_cosine_spacing)
             coords=generateNacaCoords(number,self.form.nacaNbrPoint.value(),False,0,self.form.chord.value(),0,0,0,0,0,0,coords)
        else :
             return    
        
        b=coords
        print(b)
        self.eraseTableViewDAT()
     
        row_number=0
        for v in coords :
            print(v.z)
            self.form.profilTable.insertRow(row_number) 
            self.form.profilTable.setItem(row_number,0,QtGui.QTableWidgetItem(str(v.x)))
            self.form.profilTable.setItem(row_number,1,QtGui.QTableWidgetItem(str(v.z)))
            row_number=row_number+1
            #coords.append(Vector(b[row_number].X,b[row_number].Z)) 
        
        
        if (len(number)==4) or (len(number))==5 :
             print(number)
             scale=self.form.chord.value()*2
             scene=QtGui.QGraphicsScene()
             self.form.ribView.setScene(scene)
             #scene.setSceneRect(QtCore.QRectF(-10, -400, 400, 10+self.form.chord.value()))
             points=[]
             first_v = None
             last_v = None
             for v in coords:
                 if first_v is None:
                     first_v = v
            # End of if first_v is None
            # Line between v and last_v if they're not equal
                 if (last_v != None) and (last_v != v):
                     points.append(QtCore.QPointF(last_v.x*scale,last_v.z*scale ))
                     points.append(QtCore.QPointF(v.x*scale,v.z*scale ))
            # End of if (last_v != None) and (last_v != v)
            # The new last_v
                 last_v = v
        # End of for v in upper
        # close the wire if needed
             if last_v != first_v:
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
     
    def eraseTableViewDAT(self):
        for i in range(self.form.profilTable.rowCount()) :
          self.form.profilTable.removeRow(0)
        self.form.profilTable.clearContents()
        self.form.profilTable.clear()
        return
           
    def updateTableViewDAT(self):        
        self.eraseTableViewDAT()
        a,b=readpointsonfile(self.filePath)
        coords=[]
        
        for row_number in range(len(b)-1) :
            print(b[row_number].X)
            self.form.profilTable.insertRow(row_number)
            self.form.profilTable.setItem(row_number,0,QtGui.QTableWidgetItem(str(b[row_number].X)))
            self.form.profilTable.setItem(row_number,1,QtGui.QTableWidgetItem(str(b[row_number].Z)))
            coords.append(Vector(b[row_number].X,b[row_number].Z))   
        self.updateGraphicsViewRib(coords)    
        
        return
