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


class WingEditorPanel():
    def __init__(self):
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/airPlaneDesignWingdialog.ui'
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        self.form.airPlaneName.setText("nom")
        #backgroundPicture=QPixmap pix("monImage.png")
        #pixmap=path_to_ui+ 'Mod/AirPlaneDesign/resources/plane.svg'
        #self.form.backGroundPlane.setPixmap(pixmap)
        
        
    def accept(self):
        pass

    def importFile(self):
        print("commande")

    def reject(self):
        FreeCADGui.Control.closeDialog()
        FreeCAD.ActiveDocument.recompute()

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)


    def loadPanelTable(self):
        _wingRibProfilDir=FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil'
        #self.form.NumberOfPanel.setItem=5
        
        ##########################
        # Numéro du panneau, profil, fichier profil, , corde emplature, corde saumon, longueur paneau, X emplature, X saumon, Y emplature, Y saumon, Z emplature, Z saumon, X Rotation, Y Rotation, Z Rotation
        # Panel Number, Profil, Profil file (DAT), Root rib chord, End rib chords, panel length, X position of Root rib ,X position of end rib , Y position of Root rib ,Y position of end rib, Z position of Root rib ,Z position of end rib, X angle of root rib,   Y angle of root rib,  Z angle of root rib,    
     
        initPanelTable = [
             ["1","Eppler207",_wingRibProfilDir+u"/naca/naca2412.dat","250","222","122","0","0","0.0","-54.","0","0","22"],
             ["2","Eppler207",_wingRibProfilDir+u"/naca/naca2412.dat","222","196","35.","0","0","-54","-54","0","54","0"],
             ["3","Eppler205",_wingRibProfilDir+u"/naca/naca2412.dat","196","146","456","0","0","-54","12","0","0","81"],
             ["4","Eppler205",_wingRibProfilDir+u"/naca/naca2412.dat","146","100","10","0","0.","12","12","12","0","0"],
             ["5","Eppler205",_wingRibProfilDir+u"/naca/naca2412.dat","100","100","10","0","0.","12","12","0","0","0"]
                         ]
        #self.form.PanelTable.setRowCount(0)
        for row_number,row_data in enumerate(initPanelTable):
            self.form.PanelTable.insertRow(row_number)
            for col_number, data in enumerate(row_data):
               self.form.PanelTable.setItem(row_number,col_number,QtGui.QTableWidgetItem(str(data)))#,QtGui.QTableWidgetItem(str(data)))

    def accept(self):
        print("OK")
        return

    def setupUi(self):
        # Connect Signals and Slots
        print("setupUI")
        #self.form.testButton.clicked.connect(self.importFile)
        self.loadPanelTable()
        self.updateGraphicsView()
        #self.loadPanelTable()
        #self.updateGraphicsViewWings2()
        #self.form.btnCopyTools.setEnabled(False)
        #self.setFields()
        
    def loadImage(self):
        self._photo.setPixmap(QtGui.QPixmap(FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/plane.svg'))
         
    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()
 
    def updateGraphicsView(self):
        #load picture in Plane Tab
        
        self._scene=QtGui.QGraphicsScene()
        self.form.planeView.setScene(self._scene)
        
        self._photo = QtGui.QGraphicsPixmapItem()
        self._photo.setPixmap(QtGui.QPixmap(FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/plane.png'))
        self._scene.addItem(self._photo)
        self.form.planeView.show()
        
        #self.loadImage()
        
        #self.form.planeView.setScene(selc._scene)
        #self._photo = self.form.planeView()
        #scene.addItem(self.form.planeView()) #self._photo)
        
        #scene.setSceneRect(QtCore.QRectF(-10, -400, 400, 10+self.form.chord.value()))
        #item=QtGui.QGraphicsLineItem(-100,  0, 1000,  0)
        
class CommandWizard():
    def edit(self):
        editor = WingEditorPanel()
        editor.setupUi()
        r = editor.form.exec_()
        if r:
            pass

    def GetResources(self):
     return {'MenuText': "Create a wing",
             'ToolTip':  "Create a wing"
            }

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None #Si pas de document ouvert, le menu est grisé

    def Activated(self):

        self.edit()

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneWingCreate',CommandWizard())
