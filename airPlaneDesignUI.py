# -*- coding: utf-8 -*-
#################################################
#
# ASK13 - Airfoil creation - Aircraft
#
# F. Nivoix - 2018 - V0.1
# For FreeCAD Versions = or > 0.17 Revision xxxx
#
# Works best with OCC/OCE = or > 6.7
#
#
################################################
import FreeCAD
import FreeCADGui
import Path
import PathScripts
import PathScripts.PathLog as PathLog
import PathScripts.PathUtil as PathUtil
import PathScripts.PathUtils as PathUtils
from PySide import QtCore, QtGui


LOG_MODULE = 'airPlaneDesingUI'
PathLog.setLevel(PathLog.Level.INFO, LOG_MODULE)

class EditorPanel():
    def __init__(self):
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/ressources/dialog.ui'
        #Mod/AirPlaneDesign/ressources/
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)

    def accept(self):
        pass

    def importFile(self):
        print("commande")

    def reject(self):
        FreeCADGui.Control.closeDialog()
        FreeCAD.ActiveDocument.recompute()

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)

    def loadTable(self):
        tooldata =[["1","Ep001","Eppler","c:lkjdsq"],["1","Ep001","Eppler","c:lkjdsq"]]
        headers = ["","Profil Num.","Name","File"]
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        
        model.setRowCount(10);
        model.setColumnCount(3);
        #self.form.tableWidget.setHorizontalHeaderLabels(QtGui.QTableWidgetItem("colonne1"))
        #model.appendRow(tooldata)
        self.form.tableWidget.setRowCount(0)
        for row_number,row_data in enumerate(tooldata):
            self.form.tableWidget.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.form.tableWidget.setItem(row_number,col_number,QtGui.QTableWidgetItem(str(data)))

    def loadPanelTable(self):
        #longueur paneau, delta, corde emplature, corde saumon, angle
       initPanelTable =[["Eppler207","100","-10","463","300","4.5","0","-","-","-"],
                        ["Eppler207","700","70","300","250","0","0","-","-","-"],
                        ["Eppler205","100","-10","463","300","0","0","-","-","-"],
                        ["Eppler205","100","-10","463","300","0","0","-","-","-"],
                        ["Eppler205","100","-10","463","300","0","0","-","-","-"],]
       self.form.PanelTable.setRowCount(0)
       for row_number,row_data in enumerate(initPanelTable):
            self.form.PanelTable.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.form.PanelTable.setItem(row_number,col_number,QtGui.QTableWidgetItem(str(data)))

    def updateGraphicsViewWings(self):

        scene=QtGui.QGraphicsScene()
        self.form.WingView.setScene(scene)
        scene.setSceneRect(QtCore.QRectF(-100, -400, 400, 1400))
        item=QtGui.QGraphicsLineItem(-100,  0, 1000,  0)#,#(QtCore.QPointF( -50,  0),QtCore.QPointF( 1000,  0))#,
            #item.QtCore.Qpen(QtCore.Qt.red))
        scene.addItem(item)
        item=QtGui.QGraphicsLineItem(0,-300,0,300)#(QtCore.QPointF( 0,  -300),QtCore.QPointF( 0,  300))
        scene.addItem(item)
        item=QtGui.QGraphicsPolygonItem(QtGui.QPolygonF( [
                                                    QtCore.QPointF( 0,  0),
                                                    QtCore.QPointF( 0,  463),
                                                    QtCore.QPointF(    100,  300),
                                                    QtCore.QPointF(    100,  0)
                                                    ]  ),)
                                                    
                                                  
    
        scene.addItem(item)
        item=QtGui.QGraphicsPolygonItem(QtGui.QPolygonF( [
                                                          QtCore.QPointF( 100,  300),
                                                          QtCore.QPointF( 100,  300),
                                                          QtCore.QPointF(    100+700,  300),
                                                          QtCore.QPointF(    100+700,  0)
                                                          ]  ),)
        item = QtGui.QGraphicsEllipseItem(-60, -40, 60, 40)
       
        scene.addItem(item)


    def setupUi(self):
                # Connect Signals and Slots
        self.form.testButton.clicked.connect(self.importFile)
        self.loadTable()
        self.loadPanelTable()
        self.updateGraphicsViewWings()

        #self.form.btnCopyTools.setEnabled(False)

#self.setFields()

class CommandWizard():
    def edit(self):
        editor = EditorPanel()
        editor.setupUi()
        r = editor.form.exec_()
        if r:
            pass

    def GetResources(self):
     return {'MenuText': "Wizard"}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None #Si pas de document ouvert, le menu est grisé

    def Activated(self):

        self.edit()

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignEdit',CommandWizard())


