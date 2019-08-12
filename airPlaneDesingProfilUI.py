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
        a=listdirectory(profil_dir)
        print(a)
        for obj in a:
            self.form.listProfil.addItem(obj)
        self.form.listProfil.itemSelectionChanged.connect(self.selectionChanged)
        sel = FreeCADGui.Selection.getSelection()
        if sel:
            selected = sel[0].Label
            print(selected)
        else:
            selected = None

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
        #print filter(lambda obj: obj.Label == label, FreeCAD.ActiveDocument.Objects)[0]
        return
    
    def setupUi(self):
        # Connect Signals and Slots
        #self.form.testButton.clicked.connect(self.importFile)
        return

