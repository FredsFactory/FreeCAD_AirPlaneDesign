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

#################################################
# Init Sheet and all parameter (waiting to finalise QT5 HMI
#################################################

def airPlaneDesignInitPlane(filename):
 FreeCAD.newDocument("AirPlane")
 FreeCAD.setActiveDocument("AirPlane") 
 #FreeCAD.ActiveDocument=FreeCAD.getDocument("AirPlane")
 #Gui.ActiveDocument=Gui.getDocument("AirPlane")
 
 FreeCAD.activeDocument().addObject('Spreadsheet::Sheet','AirPlaneData')
 FreeCAD.ActiveDocument.recompute()
 
 FreeCAD.ActiveDocument.AirPlaneData.setForeground('A1:A35', (1.000000,1.000000,1.000000,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setBackground('A1:A35', (0.50193,0.50193,0.50193,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setForeground('B5:F5', (1.000000,1.000000,1.000000,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setBackground('B5:F5', (0.50193,0.50193,0.50193,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setForeground('B10:F10', (1.000000,1.000000,1.000000,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setBackground('B10:F10', (0.50193,0.50193,0.50193,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setForeground('B26:J26', (1.000000,1.000000,1.000000,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setBackground('B26:J26', (0.50193,0.50193,0.50193,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setForeground('A36:A50', (1.000000,1.000000,1.000000,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setBackground('A36:A50', (0.50193,0.50193,0.50193,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setForeground('A43:J43', (1.000000,1.000000,1.000000,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setBackground('A43:J43', (0.50193,0.50193,0.50193,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setForeground('B35:J35', (1.000000,1.000000,1.000000,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setBackground('B35:J35', (0.50193,0.50193,0.50193,1.000000))
 FreeCAD.ActiveDocument.AirPlaneData.setBackground('A59:A4', (0.50193,0.50193,0.50193,1.000000))
 
 FreeCAD.ActiveDocument.AirPlaneData.setStyle('A1:A63', 'italic', 'add')
 FreeCAD.ActiveDocument.AirPlaneData.setStyle('A1:A63', 'bold', 'add')
 FreeCAD.ActiveDocument.AirPlaneData.setStyle('A6:E6', 'italic', 'add')
 FreeCAD.ActiveDocument.AirPlaneData.setStyle('A6:E6', 'bold', 'add')
 FreeCAD.ActiveDocument.AirPlaneData.setColumnWidth('A', 300)

 FreeCAD.ActiveDocument.AirPlaneData.set('A1', 'Name')
 FreeCAD.ActiveDocument.AirPlaneData.set('B1', 'AirPlane')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B3', 'AirPlane')
 FreeCAD.ActiveDocument.AirPlaneData.set('D1', 'Folder')
 FreeCAD.ActiveDocument.AirPlaneData.set('E1',FreeCAD.getUserAppDataDir())

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
 
 FreeCAD.ActiveDocument.AirPlaneData.set('B6',FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil/e207.dat')
 
 FreeCAD.ActiveDocument.AirPlaneData.set('C6',FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil/e205.dat')
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

 FreeCAD.ActiveDocument.AirPlaneData.set('A10', 'link profil/panel')
 FreeCAD.ActiveDocument.AirPlaneData.set('B10', 'Panel 1')
 FreeCAD.ActiveDocument.AirPlaneData.set('C10', 'Panel 2')
 FreeCAD.ActiveDocument.AirPlaneData.set('D10', 'Panel 3')
 FreeCAD.ActiveDocument.AirPlaneData.set('E10', 'Panel 4')

 FreeCAD.ActiveDocument.AirPlaneData.set('A11', 'profilToPanel')
 FreeCAD.ActiveDocument.AirPlaneData.set('B11', '1')
 FreeCAD.ActiveDocument.AirPlaneData.set('C11', '1')
 FreeCAD.ActiveDocument.AirPlaneData.set('D11', '2')
 FreeCAD.ActiveDocument.AirPlaneData.set('E11', '2')

 FreeCAD.ActiveDocument.AirPlaneData.set('A12', 'Profil Name')
 FreeCAD.ActiveDocument.AirPlaneData.set('B12', 'Eppler207')
 FreeCAD.ActiveDocument.AirPlaneData.set('C12', 'Eppler207')
 FreeCAD.ActiveDocument.AirPlaneData.set('D12', 'Eppler205')
 FreeCAD.ActiveDocument.AirPlaneData.set('E12', 'Eppler205')
 
 FreeCAD.ActiveDocument.AirPlaneData.set('A13', 'Aileron')
 FreeCAD.ActiveDocument.AirPlaneData.set('B13', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('C13', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('D13', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('E13', '0')

 FreeCAD.ActiveDocument.AirPlaneData.set('A15', 'longueur_panneau(mm)/panel length')
 FreeCAD.ActiveDocument.AirPlaneData.set('B15', '100')
 FreeCAD.ActiveDocument.AirPlaneData.set('C15', '700')
 FreeCAD.ActiveDocument.AirPlaneData.set('D15', '500')
 FreeCAD.ActiveDocument.AirPlaneData.set('E15', '200')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B15', 'l1')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('C15', 'l2')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('D15', 'l3')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E15', 'l4')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('F15', 'l5')

 # Delta X
 FreeCAD.ActiveDocument.AirPlaneData.set('A16', 'delta')
 FreeCAD.ActiveDocument.AirPlaneData.set('B16', '-10')#premiere nervure=ref=0
 FreeCAD.ActiveDocument.AirPlaneData.set('C16', '70')
 FreeCAD.ActiveDocument.AirPlaneData.set('D16', '120')
 FreeCAD.ActiveDocument.AirPlaneData.set('E16', '150')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B16', 'd1')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('C16', 'd2')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('D16', 'd3')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E16', 'd4')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('F16', 'd5')


 FreeCAD.ActiveDocument.AirPlaneData.set('A17', 'Corde emplature/wing root length')
 FreeCAD.ActiveDocument.AirPlaneData.set('B17', '463')
 FreeCAD.ActiveDocument.AirPlaneData.set('C17', '300')
 FreeCAD.ActiveDocument.AirPlaneData.set('D17', '250')
 FreeCAD.ActiveDocument.AirPlaneData.set('E17', '180')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B17', 'ce1')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('C17', 'ce2')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('D17', 'ce3')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E17', 'ce4')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('F17', 'ce5')
 

 FreeCAD.ActiveDocument.AirPlaneData.set('A18', 'Corde saumon/wingtip length')
 FreeCAD.ActiveDocument.AirPlaneData.set('B18', '300')#
 FreeCAD.ActiveDocument.AirPlaneData.set('C18', '250')
 FreeCAD.ActiveDocument.AirPlaneData.set('D18', '180')
 FreeCAD.ActiveDocument.AirPlaneData.set('E18', '50')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B18', 'cs1')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('C18', 'cs2')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('D18', 'cs3')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E18', 'cs4')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('F18', 'cs5')
 

 FreeCAD.ActiveDocument.AirPlaneData.set('A19', 'Rotation X')
 FreeCAD.ActiveDocument.AirPlaneData.set('B19', '4.5')
 FreeCAD.ActiveDocument.AirPlaneData.set('C19', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('D19', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('E19', '0')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B19', 'rot_e001_x')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('C19', 'rot_e002_x')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('D19', 'rot_e003_x')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E19', 'rot_e004_x')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('F19', 'rot_e005_x')
 
 FreeCAD.ActiveDocument.AirPlaneData.set('A20', 'Rotation Y')
 FreeCAD.ActiveDocument.AirPlaneData.set('B20', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('C20', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('D20', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('E20', '0')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B20', 'rot_e001_y')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('C20', 'rot_e002_y')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('D20', 'rot_e003_y')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E20', 'rot_e004_y')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('F20', 'rot_e005_y')

 FreeCAD.ActiveDocument.AirPlaneData.set('A21', 'Rotation Z')
 FreeCAD.ActiveDocument.AirPlaneData.set('B21', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('C21', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('D21', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('E21', '0')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B21', 'rot_e001_z')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('C21', 'rot_e002_z')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('D21', 'rot_e003_z')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E21', 'rot_e004_z')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('F21', 'rot_e005_z')

 FreeCAD.ActiveDocument.AirPlaneData.set('A22', 'Decalage Hauteur/Height offset')
 FreeCAD.ActiveDocument.AirPlaneData.set('B22', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('C22', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('D22', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('E22', '0')
 
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('B22', 'e001_h')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('C22', 'e002_h')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('D22', 'e003_h')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E22', 'e004_h')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('F22', 'e005_h')
 
 
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
 FreeCAD.ActiveDocument.AirPlaneData.set('B26', 'Yes/No')
 FreeCAD.ActiveDocument.AirPlaneData.set('C26', 'X')
 FreeCAD.ActiveDocument.AirPlaneData.set('D26', 'Y')
 FreeCAD.ActiveDocument.AirPlaneData.set('E26', 'Z')
 FreeCAD.ActiveDocument.AirPlaneData.set('F26', 'Radius')
 FreeCAD.ActiveDocument.AirPlaneData.set('G26', 'Longueur/length')
 FreeCAD.ActiveDocument.AirPlaneData.set('H26', 'AngleX')
 FreeCAD.ActiveDocument.AirPlaneData.set('I26', 'AngleY')
 FreeCAD.ActiveDocument.AirPlaneData.set('J26', 'AngleZ')
 
 FreeCAD.ActiveDocument.AirPlaneData.set('A27', 'cle Aile')
 FreeCAD.ActiveDocument.AirPlaneData.set('B27', 'Yes')
 FreeCAD.ActiveDocument.AirPlaneData.set('C27', '152.91')
 FreeCAD.ActiveDocument.AirPlaneData.set('D27', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('E27', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('F27', '8')
 FreeCAD.ActiveDocument.AirPlaneData.set('G27', '150')
 FreeCAD.ActiveDocument.AirPlaneData.set('H27', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('I27', '0')
 FreeCAD.ActiveDocument.AirPlaneData.set('J27', '0')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('C27', 'wing_key_x')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('D27', 'wing_key_y')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('E27', 'wing_key_z')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('F27', 'wing_key_radius')
 FreeCAD.ActiveDocument.AirPlaneData.setAlias('G27', 'wing_key_length')
 
 FreeCAD.ActiveDocument.AirPlaneData.set('A28', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('B28', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('A29', '-')
 FreeCAD.ActiveDocument.AirPlaneData.set('B29', 'No')
 
 
 
 FreeCAD.ActiveDocument.AirPlaneData.set('A35', 'Peignes')
 FreeCAD.ActiveDocument.AirPlaneData.set('B35', 'Yes/No')
 FreeCAD.ActiveDocument.AirPlaneData.set('C35', 'X')
 FreeCAD.ActiveDocument.AirPlaneData.set('D35', 'Y')
 FreeCAD.ActiveDocument.AirPlaneData.set('E35', 'Z')
 FreeCAD.ActiveDocument.AirPlaneData.set('F35', 'Hauteur')
 FreeCAD.ActiveDocument.AirPlaneData.set('G35', 'Profondeur')
 FreeCAD.ActiveDocument.AirPlaneData.set('A36', 'Peigne #1 : BA')
 FreeCAD.ActiveDocument.AirPlaneData.set('A37', 'Peigne #2 : BF')
 FreeCAD.ActiveDocument.AirPlaneData.set('A38', 'Peigne #3 : ')
 FreeCAD.ActiveDocument.AirPlaneData.set('A39', 'Peigne #4 : ')
 FreeCAD.ActiveDocument.AirPlaneData.set('A40', 'Peigne #5 : ')
 FreeCAD.ActiveDocument.AirPlaneData.set('A41', 'Peigne #6 : ')
 FreeCAD.ActiveDocument.AirPlaneData.set('A42', 'Peigne #7 : ')
 FreeCAD.ActiveDocument.AirPlaneData.set('B36', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('B37', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('B38', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('B39', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('B40', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('B41', 'No')
 FreeCAD.ActiveDocument.AirPlaneData.set('B42', 'No')
 
 FreeCAD.ActiveDocument.AirPlaneData.set('A31', '#1')
 FreeCAD.ActiveDocument.AirPlaneData.set('B31', '')
 FreeCAD.ActiveDocument.AirPlaneData.set('C31', '')
 FreeCAD.ActiveDocument.AirPlaneData.set('D31', '')
 FreeCAD.ActiveDocument.AirPlaneData.set('E31', '3')
 FreeCAD.ActiveDocument.AirPlaneData.set('F31', '30')

 FreeCAD.activeDocument().addObject('Spreadsheet::Sheet','AirPlaneRibs')
 FreeCAD.ActiveDocument.AirPlaneRibs.setColumnWidth('A', 300)
 
 FreeCAD.ActiveDocument.AirPlaneRibs.set('A01', 'Nbre Nerv./Ribs Number')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('B01', '33')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('A02', 'Posit. Nerv./Ribs position')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('A03', 'Epais. Nerv./Ribs length')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('A04', 'Angle Nervure/Ribs angle')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('B02','-3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('B03','5')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('B04','95.5')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('C02','57')#13.07+44.18')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('C03','5')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('C04','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('D02','42.86')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('D03','5')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('D04','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('E02','43.66')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('E03','5')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('E04','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('F2','59.67')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('F3','5')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('F4','90')
 
 FreeCAD.ActiveDocument.AirPlaneRibs.set('G2','58.07')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('G3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('G4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('H2','57.90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('H3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('H4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('I2','58.14')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('I3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('I4','90')
 
 FreeCAD.ActiveDocument.AirPlaneRibs.set('J2','57.39')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('J3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('J4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('K2','57.84')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('K3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('K4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('L2','58.37')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('L3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('L4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('M2','57.47')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('M3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('M4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('N2','57.92')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('N3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('N4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('O2','57.95')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('O3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('O4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('P2','57.84')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('P3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('P4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('Q2','57.38')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('Q3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('Q4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('R2','58.04')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('R3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('R4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('S2','58.28')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('S3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('S4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('T2','57.99')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('T3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('T4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('U2','57.84')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('U3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('U4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('V2','54.80')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('V3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('V4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('W2','65.02')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('W3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('W4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('X2','58.41')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('X3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('X4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('Y2','57.80')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('Y3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('Y4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('Z2','58.33')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('Z3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('Z4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AA2','57.88')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AA3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AA4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AB2','58.59')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AB3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AB4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AC2','58.78')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AC3','3')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AC4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AD2','56.98')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AD3','2')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AD4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AE2','63.74')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AE3','2')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AE4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AF2','52.07')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AF3','2')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AF4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AG2','52.01')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AG3','2')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AG4','90')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AH2','46.30')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AH3','2')
 FreeCAD.ActiveDocument.AirPlaneRibs.set('AH4','90')
 FreeCAD.ActiveDocument.recompute()
 FreeCAD.activeDocument().addObject('Spreadsheet::Sheet','AirPlaneMaterials')
 FreeCAD.ActiveDocument.AirPlaneMaterials.setColumnWidth('A', 300)

 FreeCAD.ActiveDocument.AirPlaneMaterials.set('A01', 'Materiaux/materials')
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('A02', 'Epaisseur CTP/thickness plywood 1 mm')
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('A03', 'Epaisseur CTP/thickness plywood : 2mm')
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('A04', 'Epaisseur CTP/thickness plywood : 3mm')
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('A05', 'Epaisseur CTP/thickness plywood 4mm')
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('A06', 'Epaisseur CTP/thickness plywood 5mm')
 
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('B02', '1')
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('B03', '2.2')
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('B04', '3.3')
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('B05', '4')
 FreeCAD.ActiveDocument.AirPlaneMaterials.set('B06', '5')
 FreeCAD.ActiveDocument.AirPlaneMaterials.setAlias('B02', 'ep_CTP1mm')
 FreeCAD.ActiveDocument.AirPlaneMaterials.setAlias('B03', 'ep_CTP2mm')
 FreeCAD.ActiveDocument.AirPlaneMaterials.setAlias('B04', 'ep_CTP3mmy')
 FreeCAD.ActiveDocument.AirPlaneMaterials.setAlias('B05', 'ep_CTP4mm')
 FreeCAD.ActiveDocument.AirPlaneMaterials.setAlias('B06', 'ep_CTP5mm')
 

 FreeCAD.ActiveDocument.recompute()
 
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
