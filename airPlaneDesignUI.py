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
from PySide import QtCore, QtGui



class EditorPanel():
    def __init__(self):
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/dialog.ui'
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        self.form.airPlaneName.setText("nom")

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
        #initPanelTable =[["Eppler207","100","-10","463","300","4.5","0","-","-","-"],
        #                ["Eppler207","700","70","300","250","0","0","-","-","-"],
        #               ["Eppler205","100","-10","463","300","0","0","-","-","-"],
        #               ["Eppler205","100","-10","463","300","0","0","-","-","-"],
        #               ["Eppler205","100","-10","463","300","0","0","-","-","-"],]
       self.form.NumberOfPanel.setText(FreeCAD.ActiveDocument.AirPlaneData.getContents("B3"))
       initPanelTable =[["1",FreeCAD.ActiveDocument.AirPlaneData.getContents("B12"),FreeCAD.ActiveDocument.AirPlaneData.getContents("B15"),FreeCAD.ActiveDocument.AirPlaneData.getContents("B16"),FreeCAD.ActiveDocument.AirPlaneData.getContents("B17"),FreeCAD.ActiveDocument.AirPlaneData.getContents("B18"),FreeCAD.ActiveDocument.AirPlaneData.getContents("B19"),FreeCAD.ActiveDocument.AirPlaneData.getContents("B20"),FreeCAD.ActiveDocument.AirPlaneData.getContents("B21")],
       ["2",FreeCAD.ActiveDocument.AirPlaneData.getContents("C12"),FreeCAD.ActiveDocument.AirPlaneData.getContents("C15"),FreeCAD.ActiveDocument.AirPlaneData.getContents("C16"),FreeCAD.ActiveDocument.AirPlaneData.getContents("C17"),FreeCAD.ActiveDocument.AirPlaneData.getContents("C18"),FreeCAD.ActiveDocument.AirPlaneData.getContents("C19"),FreeCAD.ActiveDocument.AirPlaneData.getContents("C20"),FreeCAD.ActiveDocument.AirPlaneData.getContents("C21")],
                        
       ["3",FreeCAD.ActiveDocument.AirPlaneData.getContents("D12"),FreeCAD.ActiveDocument.AirPlaneData.getContents("D15"),FreeCAD.ActiveDocument.AirPlaneData.getContents("D16"),FreeCAD.ActiveDocument.AirPlaneData.getContents("D17"),FreeCAD.ActiveDocument.AirPlaneData.getContents("D18"),FreeCAD.ActiveDocument.AirPlaneData.getContents("D19"),FreeCAD.ActiveDocument.AirPlaneData.getContents("D20"),FreeCAD.ActiveDocument.AirPlaneData.getContents("D21")],
            
       ["4",FreeCAD.ActiveDocument.AirPlaneData.getContents("E12"),FreeCAD.ActiveDocument.AirPlaneData.getContents("E15"),FreeCAD.ActiveDocument.AirPlaneData.getContents("E16"),FreeCAD.ActiveDocument.AirPlaneData.getContents("E17"),FreeCAD.ActiveDocument.AirPlaneData.getContents("E18"),FreeCAD.ActiveDocument.AirPlaneData.getContents("E19"),FreeCAD.ActiveDocument.AirPlaneData.getContents("E20"),FreeCAD.ActiveDocument.AirPlaneData.getContents("E21")],]
       initPanelTable=[]
       line=[]

       
       for j in range(0,int(str(FreeCAD.ActiveDocument.AirPlaneData.getContents("B3")))):
         line.append(str(j+1))
         for i in range(9):
           line.append(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + j)+str(12+i)))
         initPanelTable.append(line)
         line=[]
                      
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
                                                          QtCore.QPointF( 100+700,  300),
                                                          QtCore.QPointF( 100+700,  0)
                                                          ]  ),)
        item = QtGui.QGraphicsEllipseItem(-60, -40, 60, 40)
        scene.addItem(item)
        
    def updateGraphicsViewWings2(self):
        scene=QtGui.QGraphicsScene()
        self.form.WingView.setScene(scene)
        
        scene.setSceneRect(QtCore.QRectF(-100, -1500, 3000, 3000))
        self.setpen = QtGui.QPen(QtCore.Qt.red)
        item=QtGui.QGraphicsLineItem(-50,  0, 50,  0)
        item.setPen(QtGui.QPen(QtCore.Qt.red))
        scene.addItem(item)
        item=QtGui.QGraphicsLineItem(0,-50,0,50)
        item.setPen(QtGui.QPen(QtCore.Qt.red))
        scene.addItem(item)
        #self.pen = QtGui.QPen(QtCore.Qt.black)
        line=[]
        initPanelTable=[]
        for j in range(0,int(str(FreeCAD.ActiveDocument.AirPlaneData.getContents("B3")))):
          line.append(str(j+1))
          for i in range(9):
            line.append(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + j)+str(12+i)))
          initPanelTable.append(line)
          line=[]
        
        
        item=QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(
            [ QtCore.QPointF( 0,  0),
              QtCore.QPointF(0, float(initPanelTable[0][6])),
              QtCore.QPointF( float(initPanelTable[0][4]), float(initPanelTable[0][7])-float(initPanelTable[0][5])),
             QtCore.QPointF( float(initPanelTable[0][4]), -float(initPanelTable[0][5])),
              QtCore.QPointF( 0, 0)
            ] ),)
        #item.setPen(QtGui.QPen(QtCore.Qt.blue)) # Pyth3 compatibilite
        print (float(initPanelTable[0][5]))
        scene.addItem(item)
        xref=float(initPanelTable[0][4])
        yref=-float(initPanelTable[0][5])
        for j in range(1,int(str(FreeCAD.ActiveDocument.AirPlaneData.getContents("B3")))):
            item=QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(
              [ QtCore.QPointF( 0+xref,  0+yref),
                QtCore.QPointF(0+xref, yref+float(initPanelTable[j][6])),
                QtCore.QPointF( xref+float(initPanelTable[j][4]), yref+float(initPanelTable[j][7])-float(initPanelTable[j][5])),
                QtCore.QPointF( xref+float(initPanelTable[j][4]), yref-float(initPanelTable[j][5])),
                QtCore.QPointF( xref, yref)
              ] ),)
            xref=xref+float(initPanelTable[j][4])
            yref=yref-float(initPanelTable[j][5])
            item.setPen(QtGui.QPen(QtCore.Qt.blue))
            scene.addItem(item)
        self.form.WingView.setFocus()
        self.form.WingView.show()
            
    

    def setupUi(self):
                # Connect Signals and Slots
        self.form.testButton.clicked.connect(self.importFile)
        self.loadTable()
        self.loadPanelTable()
        self.updateGraphicsViewWings2()

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
     return {'MenuText': "Wizard(under dev)"}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None #Si pas de document ouvert, le menu est grisé

    def Activated(self):

        self.edit()

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignEdit',CommandWizard())


