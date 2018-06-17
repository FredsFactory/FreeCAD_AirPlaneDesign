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

def generateWing(name):
 list_profil_1mm_ref=[]
 profil_construction_aile=[] 
 panel=[]
 wing_right=[]
 number_of_profils=int(FreeCAD.ActiveDocument.AirPlaneData.number_of_profils)
 number_of_panels=int(FreeCAD.ActiveDocument.AirPlaneData.number_of_panels)
 dat_file=[FreeCAD.ActiveDocument.AirPlaneData.getContents('B6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('C6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('D6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('E6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('F6')]

 cleaile_radius=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('B27'))
 cleaile_X=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('C27'))
 cleaile_Y=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('D27'))
 cleaile_long=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('E27'))

 #FreeCAD.ActiveDocument.AirPlaneData.getContents('B10')

 #import des profils
 if 1 : #FreeCAD.ActiveDocument.AirPlaneData.import_profil=="Yes" :
    print ("import profil, corde 1mm")
    scalefactor=1

 for number_profil in range(0,int(FreeCAD.ActiveDocument.AirPlaneData.number_of_profils)):
      print "profil de ref : "+str(number_profil)+"    Name file :"+dat_file[number_profil]
      importAirfoilDAT.insert(dat_file[number_profil],FreeCAD.ActiveDocument.Name)#'AirPlane1')
      points = FreeCAD.ActiveDocument.ActiveObject.Points
      Draft.makeBSpline(points, closed=True)
      obj_nervure_ref=Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(scalefactor,scalefactor,scalefactor),center=FreeCAD.Vector(0,0,0),legacy=True)
      #obj_nervure_ref.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(-1,0,0),270))
      obj_nervure_ref.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,0),0)
      FreeCAD.ActiveDocument.removeObject("DWire")
      FreeCAD.Gui.ActiveDocument.ActiveObject.Visibility=False
      profilname= FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + number_profil)+str(7))

      obj_nervure_ref.Label="Prof_ref_1mm_"+profilname#+"_000"#+str(number_profil+1)
             

      list_profil_1mm_ref.append(obj_nervure_ref)

      print "nom : "+obj_nervure_ref.Label
      #Position de l'origine du profil a 25% du profil 
      #obj_nervure_ref.Placement=FreeCAD.Placement(FreeCAD.Vector(-0.25,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,0),0))      print 'fin'
      #FreeCAD.Gui.getDocument("AirPlane").getObject("BSpline").Visibility=False
 FreeCAD.ActiveDocument.recompute()

#------------------------------------------------------------------
#Creation des nervures d'emplature et du saumon de chaque paneau
#------------------------------------------------------------------
 position_nervure=0
 position_emplature=0
 posvec=FreeCAD.Vector(0,0,0)
 rotvec=FreeCAD.Vector(1,0,0)#Vector(0,0,0)

 for i in range(0,int(FreeCAD.ActiveDocument.AirPlaneData.number_of_panels)):
   corde_emplature=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(13+4)))
   corde_saumon=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(14+4)))
   aa=int(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B')+i)+str(11)))-1 # profil number
   angle=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(19)))
   #nervure emplature
   obj_clone_nervure=Draft.clone(list_profil_1mm_ref[aa]) # creation de la nervure emplature
   obj_clone_nervure.Scale =(corde_emplature,corde_emplature,1) #mise a l echelle
   obj_clone_nervure.Label="Profil_E00"+str(i) #nommage
   obj_clone_nervure.Placement=FreeCAD.Placement(posvec,rotvec,90-angle)#positionnement dans lespace
   FreeCAD.Gui.ActiveDocument.ActiveObject.Visibility=False#obj_clone_nervure.Visibility=False
   profil_construction_aile.append(obj_clone_nervure) #sauvegare nervure dans tableau
   #nervure saumon
   position_nervure= position_nervure+float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(15)))
   position_emplature=-float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(12+4)))

   posvec=FreeCAD.Vector(position_emplature,position_nervure,0)
   rotvec=FreeCAD.Vector(1,0,0)

   obj_clone_nervure=Draft.clone(list_profil_1mm_ref[aa]) # creation de la nervure saumon
   obj_clone_nervure.Scale =(corde_saumon,corde_saumon,1) #mise a l echelle
   obj_clone_nervure.Label="Profil_S00"+str(i) #nommage
 
   obj_clone_nervure.Placement=FreeCAD.Placement(posvec,rotvec,90)#positionnement dans lespace
   FreeCAD.Gui.ActiveDocument.ActiveObject.Visibility=False#obj_clone_nervure.Visibility=False
   profil_construction_aile.append(obj_clone_nervure) #sauvegare nervure dans tableau

   posvec=FreeCAD.Vector(position_emplature,position_nervure+0.01,0)
   print "corde_emplature :" +str(corde_emplature)+", corde_saumon:"+str(corde_saumon)+", position_emplature:"+str(position_emplature)

#------------------------------------------------------------------
# Construction des paneaux et de l aile
#------------------------------------------------------------------

 for i in range(0,number_of_panels*2,2):
    panel_=FreeCAD.ActiveDocument.addObject('Part::Loft','Panel_'+str(i/2))    
    FreeCAD.ActiveDocument.ActiveObject.Sections=[profil_construction_aile[i], profil_construction_aile[i+1], ]
    FreeCAD.ActiveDocument.ActiveObject.Solid=True
    FreeCAD.ActiveDocument.ActiveObject.Ruled=False
    FreeCAD.ActiveDocument.ActiveObject.Closed=False
    #panel_.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(-1,0,0),270))    
    panel.append(panel_)  
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
 FreeCAD.Gui.activeDocument().activeView().viewAxonometric()

#------------------------------------------------------------------
# Fusion des paneaux et de l aile
#------------------------------------------------------------------

 a=FreeCAD.activeDocument().addObject("Part::MultiFuse","wing_r")
 a.Shapes=panel
 a.Label='wing_r'
 wing_right.append(a)
 FreeCAD.ActiveDocument.recompute()
 col=[(0.2,0.4,0.6)]
 FreeCAD.ActiveDocument.wing_r.ViewObject.DiffuseColor=col
 FreeCAD.ActiveDocument.wing_r.ViewObject.Transparency=70



#------------------------------------------------------------------
# Construction de la cle d'aile
#------------------------------------------------------------------
 cleaileobject=FreeCAD.ActiveDocument.addObject("Part::Cylinder","Cylinder")
 FreeCAD.ActiveDocument.ActiveObject.Label = "CleAile"
 FreeCAD.ActiveDocument.ActiveObject.Radius = cleaile_radius
 FreeCAD.ActiveDocument.ActiveObject.Height = cleaile_long
 cleaileobject.Placement=FreeCAD.Placement(FreeCAD.Vector(cleaile_X,0,0),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-90))


 longeron01=FreeCAD.ActiveDocument.addObject("Part::Box","Box")
 longeron01.Label = "Longeron01"
 longeron01.Width = '2000 mm'
 longeron01.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,-1),355))

 return


class GenerateWingCommand():

    def GetResources(self):
        return {
                #'Pixmap'  : ':/AirPlaneDesign/icons/importPart_update.svg', 
                #'Accel' : 'Shift+S', # a default shortcut (optional)
                'MenuText': 'Generate Wing',
                'ToolTip' : 'Generate Wing  What my new command does'
                  }

    def Activated(self):
        generateWing('blabla')
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCAD.Gui.addCommand('generateWing',GenerateWingCommand()) 