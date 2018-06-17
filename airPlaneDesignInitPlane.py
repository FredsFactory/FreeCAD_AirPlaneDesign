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
################################################import os,FreeCAD,FreeCADGui
from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
import FreeCAD, FreeCADGui, Draft, Part
import importAirfoilDAT

def airPlaneDesignInitPlane(filename):
 FreeCAD.newDocument("AirPlane")
 FreeCAD.setActiveDocument("AirPlane") 
 #FreeCAD.ActiveDocument=FreeCAD.getDocument("AirPlane")
 #Gui.ActiveDocument=Gui.getDocument("AirPlane")
#################################################
# Init Sheet
#################################################

 FreeCAD.activeDocument().addObject('Spreadsheet::Sheet','AirPlaneData')

 FreeCAD.ActiveDocument.AirPlaneData.setStyle('A1:A20', 'italic', 'add')
 FreeCAD.ActiveDocument.AirPlaneData.setStyle('A1:A20', 'bold', 'add')
 FreeCAD.ActiveDocument.AirPlaneData.setStyle('A6:E6', 'italic', 'add')
 FreeCAD.ActiveDocument.AirPlaneData.setStyle('A6:E6', 'bold', 'add')
 FreeCAD.ActiveDocument.AirPlaneData.setColumnWidth('A', 200)

 FreeCAD.ActiveDocument.AirPlaneData.set('A1', 'Name')
 FreeCAD.ActiveDocument.AirPlaneData.set('B1', 'AirPlane')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B3', 'AirPlane')
 FreeCAD.ActiveDocument.AirPlaneData.set('D1', 'Folder')
 FreeCAD.ActiveDocument.AirPlaneData.set('E1', '/Users/fredericnivoix/Documents/888-Aeromodelisme/MesAvions/ASK13/montage/montageV0.2/aile/')
 #FreeCAD.ActiveDocument.AirPlaneData.set('E1', 'D:\users\PuyDeSancy\BureauFrederic\MesAvions\ASK13\montage\montageV0.2\aile\e207.dat')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E3', 'Folder')

 FreeCAD.ActiveDocument.AirPlaneData.set('A3', 'number_of_panels')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B3', 'number_of_panels')
 FreeCAD.ActiveDocument.AirPlaneData.set('B3','4')
 FreeCAD.ActiveDocument.AirPlaneData.set('A4', 'number_of_profils')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B4', 'number_of_profils')
 FreeCAD.ActiveDocument.AirPlaneData.set('B4', '2')

 FreeCAD.ActiveDocument.AirPlaneData.set('A5', 'Import Profil')
 FreeCAD.ActiveDocument.AirPlaneData.set('B5', 'Profil 1')
 FreeCAD.ActiveDocument.AirPlaneData.set('C5', 'Profil 2')
 FreeCAD.ActiveDocument.AirPlaneData.set('D5', 'Profil 3')
 FreeCAD.ActiveDocument.AirPlaneData.set('E5', 'Profil 4')
 FreeCAD.ActiveDocument.AirPlaneData.set('F5', 'Profil 5')
 
 #A10-E10
 FreeCAD.ActiveDocument.AirPlaneData.set('A6','file_name')
 FreeCAD.ActiveDocument.AirPlaneData.set('B6','/Users/fredericnivoix/Documents/888-Aeromodelisme/MesAvions/ASK13/montage/montageV0.2/aile/e207.dat')
 #FreeCAD.ActiveDocument.AirPlaneData.set('B6','D:\users\PuyDeSancy\BureauFrederic\MesAvions\ASK13\montage\montageV0.2\aile\e207.dat')
 FreeCAD.ActiveDocument.AirPlaneData.set('C6', '/Users/fredericnivoix/Documents/888-Aeromodelisme/MesAvions/ASK13/montage/montageV0.2/aile/e205.dat')
 #FreeCAD.ActiveDocument.AirPlaneData.set('C6', 'D:/users/PuyDeSancy/BureauFrederic/MesAvions/ASK13/montage/montageV0.2/aile/e205.dat')
 FreeCAD.ActiveDocument.AirPlaneData.set('D6', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('E6', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('F6', '-')

 FreeCAD.ActiveDocument.AirPlaneData.set('A7', 'Profil Name')
 FreeCAD.ActiveDocument.AirPlaneData.set('B7', 'Eppler207')
 FreeCAD.ActiveDocument.AirPlaneData.set('C7', 'Eppler205')
 FreeCAD.ActiveDocument.AirPlaneData.set('D7', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('E7', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('F7', '-')

 FreeCAD.ActiveDocument.AirPlaneData.set('A8', 'Import Profil?')
 FreeCAD.ActiveDocument.AirPlaneData.set('B8', 'Yes')
 FreeCAD.ActiveDocument.AirPlaneData.set('C8', 'Yes')
 FreeCAD.ActiveDocument.AirPlaneData.set('D8', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('E8', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('F8', '-')



 #A6-E7
 FreeCAD.ActiveDocument.AirPlaneData.set('A10', 'Affectation profil/paneau')
 FreeCAD.ActiveDocument.AirPlaneData.set('B10', 'Panel 1')
 FreeCAD.ActiveDocument.AirPlaneData.set('C10', 'Panel 2')
 FreeCAD.ActiveDocument.AirPlaneData.set('D10', 'Panel 3')
 FreeCAD.ActiveDocument.AirPlaneData.set('E10', 'Panel 4')

 #A7-E7
 FreeCAD.ActiveDocument.AirPlaneData.set('A11', 'profilToPanel')
 FreeCAD.ActiveDocument.AirPlaneData.set('B11', '1')
 FreeCAD.ActiveDocument.AirPlaneData.set('C11', '1')
 FreeCAD.ActiveDocument.AirPlaneData.set('D11', '2')
 FreeCAD.ActiveDocument.AirPlaneData.set('E11', '2')
 #A8-E8
 FreeCAD.ActiveDocument.AirPlaneData.set('A12', 'Profil Name')
 FreeCAD.ActiveDocument.AirPlaneData.set('B12', 'Eppler207')
 FreeCAD.ActiveDocument.AirPlaneData.set('C12', 'Eppler207')
 FreeCAD.ActiveDocument.AirPlaneData.set('D12', 'Eppler205')
 FreeCAD.ActiveDocument.AirPlaneData.set('E12', 'Eppler205')




 #A11-E11
 FreeCAD.ActiveDocument.AirPlaneData.set('A15', 'longueur_panneau(mm)')
 FreeCAD.ActiveDocument.AirPlaneData.set('B15', '100')
 FreeCAD.ActiveDocument.AirPlaneData.set('C15', '700')
 FreeCAD.ActiveDocument.AirPlaneData.set('D15', '500')
 FreeCAD.ActiveDocument.AirPlaneData.set('E15', '200')

 # Delta X
 FreeCAD.ActiveDocument.AirPlaneData.set('A16', 'delta')
 FreeCAD.ActiveDocument.AirPlaneData.set('B16', '-10')#premiere nervure=ref=0
 FreeCAD.ActiveDocument.AirPlaneData.set('C16', '70')
 FreeCAD.ActiveDocument.AirPlaneData.set('D16', '120')
 FreeCAD.ActiveDocument.AirPlaneData.set('E16', '150')

 FreeCAD.ActiveDocument.AirPlaneData.set('A17', 'Corde emplature')
 FreeCAD.ActiveDocument.AirPlaneData.set('B17', '463')#380.78')#+82
 FreeCAD.ActiveDocument.AirPlaneData.set('C17', '300') #'341.43')
 FreeCAD.ActiveDocument.AirPlaneData.set('D17', '250')#263.84')
 FreeCAD.ActiveDocument.AirPlaneData.set('E17', '180')#176.24')

 FreeCAD.ActiveDocument.AirPlaneData.set('A18', 'Corde saumon')
 FreeCAD.ActiveDocument.AirPlaneData.set('B18', '300')#
 FreeCAD.ActiveDocument.AirPlaneData.set('C18', '250')
 FreeCAD.ActiveDocument.AirPlaneData.set('D18', '180')
 FreeCAD.ActiveDocument.AirPlaneData.set('E18', '50')

 FreeCAD.ActiveDocument.AirPlaneData.set('A19', 'Rotation X')
 FreeCAD.ActiveDocument.AirPlaneData.set('B19', '4.5')
 FreeCAD.ActiveDocument.AirPlaneData.set('C19', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('D19', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('E19', '0')
 
 FreeCAD.ActiveDocument.AirPlaneData.set('A20', 'Rotation Y')
 FreeCAD.ActiveDocument.AirPlaneData.set('B20', '')
 FreeCAD.ActiveDocument.AirPlaneData.set('C20', '')
 FreeCAD.ActiveDocument.AirPlaneData.set('D20', '')
 FreeCAD.ActiveDocument.AirPlaneData.set('E20', '')

 FreeCAD.ActiveDocument.AirPlaneData.set('A21', 'Rotation Z')
 FreeCAD.ActiveDocument.AirPlaneData.set('B21', '')
 FreeCAD.ActiveDocument.AirPlaneData.set('C21', '')
 FreeCAD.ActiveDocument.AirPlaneData.set('D21', '')
 FreeCAD.ActiveDocument.AirPlaneData.set('E21', '')

 FreeCAD.ActiveDocument.AirPlaneData.set('A22', 'Flap')
 FreeCAD.ActiveDocument.AirPlaneData.set('B22', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('C22', 'Yes')
 FreeCAD.ActiveDocument.AirPlaneData.set('D22', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('E22', 'No')

 FreeCAD.ActiveDocument.AirPlaneData.set('A23', 'Flap#')
 FreeCAD.ActiveDocument.AirPlaneData.set('B23', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('C23', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('D23', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('E23', '-')



 FreeCAD.ActiveDocument.AirPlaneData.set('A25', 'Aerofrein')
 FreeCAD.ActiveDocument.AirPlaneData.set('B25', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('C25', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('D25', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('E25', 'No')

 FreeCAD.ActiveDocument.AirPlaneData.set('A26', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('B26', 'Radius')
 FreeCAD.ActiveDocument.AirPlaneData.set('C26', 'X')
 FreeCAD.ActiveDocument.AirPlaneData.set('D26', 'Y')
 FreeCAD.ActiveDocument.AirPlaneData.set('E26', 'Longueur')
 
 FreeCAD.ActiveDocument.AirPlaneData.set('A27', 'cle Aile')
 FreeCAD.ActiveDocument.AirPlaneData.set('B27', '8')
 FreeCAD.ActiveDocument.AirPlaneData.set('C27', '152.91')
 FreeCAD.ActiveDocument.AirPlaneData.set('D27', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('E27', '150')

 FreeCAD.ActiveDocument.recompute()
 #################################################
 # Init Sheet
 #################################################
 
 return
 
class AirPlaneDesignInitPlaneCommand():
    def GetResources(self):
        return {
                #'Pixmap'  : ':/AirPlaneDesign/icons/importPart_update.svg', 
                #'Accel' : 'Shift+S', # a default shortcut (optional)
                'MenuText': 'Init new plane',
                'ToolTip' : 'Init new plane'
                  }

    def Activated(self):
        airPlaneDesignInitPlane('blabla')
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('airPlaneDesignInitPlane',AirPlaneDesignInitPlaneCommand())