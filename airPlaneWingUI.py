# -*- coding: utf-8 -*-
#################################################
#
# ASK13 - Airfoil creation - Aircraft
#
# F. Nivoix - 2018 - V0.3
# For FreeCAD Versions = or > 0.17 Revision xxxx
#
# Works best with OCC/OCE = or > 6.7
#
#
################################################
import FreeCAD
import FreeCADGui
from PySide import QtCore
from PySide import QtGui

FreeCADGui.addLanguagePath(":/translations")
# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)



class WingEditorPanel():
    def __init__(self):
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/airPlaneDesignWingdialog.ui'
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        self.form.airPlaneName.setText("nom")


    def importFile(self):
        print("commande")

    def reject(self):
        FreeCADGui.Control.closeDialog()
        FreeCAD.ActiveDocument.recompute()

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)

    def loadPanelTable(self):
        _wingRibProfilDir=FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil'

        ##########################
        # Numéro du panneau, profil, fichier profil, , corde emplature, corde saumon, longueur paneau, X emplature, X saumon, Y emplature, Y saumon, Z emplature, Z saumon, X Rotation, Y Rotation, Z Rotation
        # Panel Number, Profil, Profil file (DAT), Root rib chord, End rib chords, panel length, X position of Root rib ,X position of end rib , Y position of Root rib ,Y position of end rib, Z position of Root rib ,Z position of end rib, X angle of root rib,   Y angle of root rib,  Z angle of root rib,

        initPanelTable = [
             ["1","Eppler207",_wingRibProfilDir+u"/naca/naca2412.dat","250","222","122","0.0","0.0","0.0","-54.","0.0","0.0","22"],
             ["2","Eppler207",_wingRibProfilDir+u"/naca/naca2412.dat","222","196","35.","0.0","0.0","-54","-54","0.0","54","0.0"],
             ["3","Eppler205",_wingRibProfilDir+u"/naca/naca2412.dat","196","146","456","0.0","0.0","-54","12","0.0","0.0","81"],
             ["4","Eppler205",_wingRibProfilDir+u"/naca/naca2412.dat","146","100","10","0.0","0.0","12","12","12","0.0","0.0"],
             ["5","Eppler205",_wingRibProfilDir+u"/naca/naca2412.dat","100","100","10","0.0","0.0","12","12","0.0","0.0","0.0"]
                         ]
        #self.form.PanelTable.setRowCount(0)
        for row_number,row_data in enumerate(initPanelTable):
            self.form.PanelTable.insertRow(row_number)
            for col_number, data in enumerate(row_data):
               self.form.PanelTable.setItem(row_number,col_number,QtGui.QTableWidgetItem(str(data)))#,QtGui.QTableWidgetItem(str(data)))

    def addLine(self):
        initPanelTable = [
             ["-","-","","100","100","100","0","0","0.0","0","0","0","22"],
                         ]
        #self.form.PanelTable.setRowCount(0)
        for row_number,row_data in enumerate(initPanelTable):
            self.form.PanelTable.insertRow(row_number)
            for col_number, data in enumerate(row_data):
               self.form.PanelTable.setItem(row_number,col_number,QtGui.QTableWidgetItem(str(data)))#,QtGui.QTableWidgetItem(str(data)))

    def delLine(self):
        self.form.PanelTable.removeRow(self.form.PanelTable.currentRow())


    def accept(self):
        #print("OK")
        return

    def setupUi(self):
        # Connect Signals and Slots
        self.form.filSheet.clicked.connect(self.loadPanelTable) # fil sheet with an example, #self.loadPanelTable()
        self.form.addline.clicked.connect(self.addLine)
        self.form.delline.clicked.connect(self.delLine)
