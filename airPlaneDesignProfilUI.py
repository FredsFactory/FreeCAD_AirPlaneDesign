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
import FreeCAD, FreeCADGui, os
from PySide import QtCore, QtGui, QtUiTools
from airPlaneAirFoilNaca import generateNacaCoords
from airPlaneAirFoil import readpointsonfile

FreeCADGui.addLanguagePath(":/translations")

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)


class zoomableGraphic(QtGui.QGraphicsView):
    def __init__(self, parent):
        super(zoomableGraphic, self).__init__(parent)

    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)


class SelectObjectUI():
    def __init__(self):
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/selectRibProfil.ui'
        loader=QtUiTools.QUiLoader()
        loader.registerCustomWidget(zoomableGraphic)
        self.form=loader.load(path_to_ui)
        #self.form.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint) # compatibility with Freecad V0.18
        profil_dir=FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil'
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(profil_dir)
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
        if os.path.isfile(self.filePath):
            self.updateRibDAT()
        else:
            self.form.profilTable.setRowCount(0)
            self.form.ribView.setScene(QtGui.QGraphicsScene())
        return 
        
    def accept(self):
        return
    
    def reject(self):
        FreeCADGui.Control.closeDialog()
        FreeCAD.ActiveDocument.recompute()
        return
    
    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)
    
    def setupUi(self):
        # Connect Signals and Slots
        self.form.NACANumber.editingFinished.connect(self.updateRibNACA)
        self.form.NACANumber.editingFinished.connect(self.form.listProfil.clearSelection)
        self.form.nacaNbrPoint.editingFinished.connect(self.updateRibNACA)
        self.form.listProfil.clicked.connect(self.form.NACANumber.clear)
        self.form.listProfil.clicked.connect(self.on_treeView_clicked)
        self.form.finite_TE.clicked.connect(self.updateRibNACA)
        return
    

 
    def updateGraphicsRibView(self,coords):
        scene=QtGui.QGraphicsScene()
        self.form.ribView.setScene(scene)
        scale=self.form.ribView.width()-2*self.form.ribView.frameWidth()
            
        points=[]
        first_v = None
        last_v = None
        for v in coords:
            if first_v is None:
                first_v = v
            # End of if first_v is None
            # Line between v and last_v if they're not equal
            if (last_v != None) and (last_v != v):
                points.append(QtCore.QPointF(last_v.x*scale,-last_v.z*scale ))
                points.append(QtCore.QPointF(v.x*scale,-v.z*scale ))
            # End of if (last_v != None) and (last_v != v)
            # The new last_v
            last_v = v
        # End of for v in coords
        # close the wire if needed
        if last_v != first_v:
                     points.append(QtCore.QPointF(last_v.x*scale,-last_v.z*scale ))
                     points.append(QtCore.QPointF(first_v.x*scale,-first_v.z*scale ))
        item=QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(points))
        item.setPen(QtGui.QPen(QtCore.Qt.blue))
        scene.addItem(item)

        return


    def updateRibNACA(self):
        number=self.form.NACANumber.text()
        self.form.profilTable.setRowCount(0)
        try:
            coords=generateNacaCoords(number,self.form.nacaNbrPoint.value(),self.form.finite_TE.isChecked(),True,self.form.chord.value(),0,0,0,0,0,0)
        except ValueError:
            self.form.ribView.setScene(QtGui.QGraphicsScene())
            return

        row_number=0
        for v in coords :
            self.form.profilTable.insertRow(row_number)
            self.form.profilTable.setItem(row_number,0,QtGui.QTableWidgetItem(str(v.x)))
            self.form.profilTable.setItem(row_number,1,QtGui.QTableWidgetItem(str(v.z)))
            row_number=row_number+1

        self.form.profilTable.resizeColumnsToContents()
        self.updateGraphicsRibView(coords)

        return


    def updateRibDAT(self):
        self.form.profilTable.setRowCount(0)
        coords=readpointsonfile(self.filePath)

        row_number=0
        for v in coords :
            self.form.profilTable.insertRow(row_number)
            self.form.profilTable.setItem(row_number,0,QtGui.QTableWidgetItem(str(v.x)))
            self.form.profilTable.setItem(row_number,1,QtGui.QTableWidgetItem(str(v.z)))
            row_number=row_number+1

        self.form.profilTable.resizeColumnsToContents()
        self.updateGraphicsRibView(coords)

        return
