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
import FreeCAD, FreeCADGui, Draft, Part,PartDesign,PartDesignGui,Sketcher
import importAirfoilDAT

def generateWing(name):
 list_profil_1mm_ref=[]
 profil_construction_aile=[] 
 panel=[]
 panel_body=[]
 wing_right=[]
 number_of_profils=int(FreeCAD.ActiveDocument.AirPlaneData.number_of_profils)
 number_of_panels=int(FreeCAD.ActiveDocument.AirPlaneData.number_of_panels)
 dat_file=[FreeCAD.ActiveDocument.AirPlaneData.getContents('B6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('C6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('D6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('E6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('F6')]


 cleaile_X=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('B27'))
 cleaile_Y=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('C27'))
 cleaile_Z=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('D27'))
 cleaile_radius=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('E27'))
 cleaile_long=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('F27'))
 cleaile_angleX=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('G27'))
 cleaile_angleY=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('H27'))
 cleaile_angleZ=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('I27'))

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

      obj_nervure_ref.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,0),0)
      FreeCAD.ActiveDocument.removeObject("DWire")
      FreeCAD.Gui.ActiveDocument.ActiveObject.Visibility=False
      profilname= FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + number_profil)+str(7))

      obj_nervure_ref.Label="Prof_ref_1mm_"+profilname#+"_000"#+str(number_profil+1)
      
      list_profil_1mm_ref.append(obj_nervure_ref)
      print "nom : "+obj_nervure_ref.Label

 FreeCAD.ActiveDocument.recompute()

#------------------------------------------------------------------
#Creation des nervures d'emplature et du saumon de chaque paneau
#------------------------------------------------------------------
 position_nervure=0
 position_emplature=0
 posvec=FreeCAD.Vector(0,0,0)
 rotvec=FreeCAD.Vector(1,0,0)#Vector(0,0,0)
 Draft.clone(list_profil_1mm_ref[0])
 for i in range(0,int(FreeCAD.ActiveDocument.AirPlaneData.number_of_panels)):
   corde_emplature=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(13+4)))
   corde_saumon=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(14+4)))
   aa=int(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B')+i)+str(11)))-1 # profil number
   angleX=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(19)))
   angleY=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(20)))
   angleZ=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(21)))
   #nervure emplature
   obj_clone_nervure=Draft.clone(list_profil_1mm_ref[aa]) # creation de la nervure emplature
   obj_clone_nervure.Scale =(corde_emplature,corde_emplature,1) #mise a l echelle
   obj_clone_nervure.Label="Profil_E00"+str(i) #nommage
   #obj_clone_nervure.Placement=FreeCAD.Placement(posvec,rotvec,90-angleX)#positionnement dans lespace
   
   obj_clone_nervure.Placement=FreeCAD.Placement(posvec,FreeCAD.Rotation(angleY,angleZ,90-angleX), FreeCAD.Vector(0,0,0))
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

 delta_emplature=0
 delta_saumon=-float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B'))+str(16)))
 hauteur_bordattaque=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('E'))+str(31)))
 profondeur_bordattaque=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('F'))+str(31)))

 for i in range(0,number_of_panels*2,2):
    panel_=FreeCAD.ActiveDocument.addObject('Part::Loft','Panel_'+str(i/2))    
    FreeCAD.ActiveDocument.ActiveObject.Sections=[profil_construction_aile[i], profil_construction_aile[i+1], ]
    FreeCAD.ActiveDocument.ActiveObject.Solid=True
    FreeCAD.ActiveDocument.ActiveObject.Ruled=False
    FreeCAD.ActiveDocument.ActiveObject.Closed=False
    panel.append(panel_)
    #---------
    # Creation du Body du paneau
    #---------
    a=FreeCAD.activeDocument().addObject('PartDesign::Body','Panel_0'+str(i/2))
    a.BaseFeature = panel_
    col=[(0.2,0.4,0.6)]
    a.ViewObject.DiffuseColor=col
    a.ViewObject.Transparency=70
    panel_body.append(a)
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.Gui.activeView().setActiveObject('pdbody', a)
    FreeCAD.Gui.Selection.clearSelection()
    FreeCAD.Gui.Selection.addSelection(a)
    FreeCAD.ActiveDocument.recompute()
    #---------
    # Creation du bord d'attaque
    #---------
    nbreOfFaces=len(a.Shape.Faces)
    print 'BordAttaque'+str(i/2)+'_0'
    print nbreOfFaces
    FreeCAD.Gui.activeDocument().ActiveView.setActiveObject('pdbody', a)
    b=a.newObject('Sketcher::SketchObject','BordAttaque'+str(i/2)+'_0')
    print a.Label
    print "Face"+str(nbreOfFaces-1)
    #b.Support = (FreeCAD.ActiveDocument.BaseFeature,["Face"+str(nbreOfFaces-1)])
    b.Support = (a,["Face"+str(nbreOfFaces-1)])
    b.MapMode = 'FlatFace'
    
    FreeCAD.ActiveDocument.recompute()
    geoList = []
 
    #hauteur_bordattaque, profondeur_bordattaque, delta_saumon, delta_emplature

    geoList.append(Part.LineSegment(FreeCAD.Vector(delta_emplature,-hauteur_bordattaque/2,0),FreeCAD.Vector(delta_emplature+profondeur_bordattaque,-hauteur_bordattaque/2,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(delta_emplature+profondeur_bordattaque,-hauteur_bordattaque/2,0),FreeCAD.Vector(delta_emplature+profondeur_bordattaque,hauteur_bordattaque/2,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(delta_emplature+profondeur_bordattaque,hauteur_bordattaque/2,0),FreeCAD.Vector(delta_emplature,hauteur_bordattaque/2,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(delta_emplature,hauteur_bordattaque/2,0),FreeCAD.Vector(delta_emplature,-hauteur_bordattaque/2,0)))


    b.addGeometry(geoList,False)
    conList = []
    conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
    conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
    conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
    conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
    conList.append(Sketcher.Constraint('Horizontal',0))
    conList.append(Sketcher.Constraint('Horizontal',2))
    conList.append(Sketcher.Constraint('Vertical',1))
    conList.append(Sketcher.Constraint('Vertical',3))
    b.addConstraint(conList)
    #FreeCAD.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-2))
    print 'BordAttaque'+str(i/2)+'_1'
    print "Face"+str(nbreOfFaces)
    c=a.newObject('Sketcher::SketchObject','BordAttaque'+str(i/2)+'_1')
    #c.Support = (FreeCAD.ActiveDocument.BaseFeature,["Face"+str(nbreOfFaces)])
    c.Support = (a,["Face"+str(nbreOfFaces)])
    c.MapMode = 'FlatFace'
    
    geoList = []
    print "delta saumon:"
    print delta_saumon
    print "delta emplature:"
    print delta_emplature
    geoList.append(Part.LineSegment(FreeCAD.Vector(-delta_saumon,-hauteur_bordattaque/2,0),FreeCAD.Vector(-delta_saumon-profondeur_bordattaque,-hauteur_bordattaque/2,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(-delta_saumon-profondeur_bordattaque,-hauteur_bordattaque/2,0),FreeCAD.Vector(-delta_saumon-profondeur_bordattaque,hauteur_bordattaque/2,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(delta_saumon+profondeur_bordattaque,hauteur_bordattaque/2,0),FreeCAD.Vector(-delta_saumon,hauteur_bordattaque/2,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(-delta_saumon,hauteur_bordattaque/2,0),FreeCAD.Vector(-delta_saumon,-hauteur_bordattaque/2,0)))

    c.addGeometry(geoList,False)
    conList = []
    conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
    conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
    conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
    conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
    conList.append(Sketcher.Constraint('Horizontal',0))
    #conList.append(Sketcher.Constraint('Horizontal',2))
    conList.append(Sketcher.Constraint('Vertical',1))
    conList.append(Sketcher.Constraint('Vertical',3))
    c.addConstraint(conList)


    #---------
    # Suppression du bord d attaque
    #---------
    d=a.newObject("PartDesign::SubtractiveLoft","SubtractiveLoft")
    d.Profile=b#FreeCAD.activeDocument().BordAttaque0

    d.Sections = [c]
    
    FreeCAD.ActiveDocument.recompute()
    #FreeCAD.Gui.activeDocument().hide('BaseFeature'+str(i/2))
    #Gui.getDocument("Aile_v0_3").getObject("BaseFeature").Visibility=False
    
    FreeCAD.Gui.activeDocument().hide('BordAttaque'+str(i/2)+'_0')
    FreeCAD.Gui.activeDocument().hide('BordAttaque'+str(i/2)+'_1')
    FreeCAD.ActiveDocument.recompute()
    
    if i<>number_of_panels*2-2 :
        delta_emplature=delta_saumon
        delta_saumon=-float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i/2+1)+str(16)))
    #delta_emplature=-float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i/2+1)+str(16)))
    else :
        delta_emplature=delta_saumon
        delta_saumon=-float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i/2)+str(16)))

    a.ViewObject.DiffuseColor=col
    a.ViewObject.Transparency=70
    #--------Fin creation du Body
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
 FreeCAD.ActiveDocument.wing_r.ViewObject.Visibility=False

#------------------------------------------------------------------
# Construction de la cle d'aile
#------------------------------------------------------------------
 cleaileobject=FreeCAD.ActiveDocument.addObject("Part::Cylinder","Cylinder")
 FreeCAD.ActiveDocument.ActiveObject.Label = "CleAile"
 FreeCAD.ActiveDocument.ActiveObject.Radius = cleaile_radius
 FreeCAD.ActiveDocument.ActiveObject.Height = cleaile_long
 #cleaileobject.Placement=FreeCAD.Placement(FreeCAD.Vector(cleaile_X,0,0),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-90))
 angleX=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B'))+str(19)))
 angleY=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B'))+str(20)))
 angleZ=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B'))+str(21)))
 #91 et 4.5
 cleaileobject.Placement=FreeCAD.Placement(FreeCAD.Vector(cleaile_X,0,0),FreeCAD.Rotation(4.5,angleZ,90+angleX), FreeCAD.Vector(0,0,0))

#------------------------------------------------------------------
# Construction des longerons
#------------------------------------------------------------------

#longeron01=FreeCAD.ActiveDocument.addObject("Part::Box","Box")
# longeron01.Label = "Longeron01"
# longeron01.Width = '2000 mm'
#longeron01.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,-1),355))

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
        #FreeCAD.ActiveDocument=FreeCAD.getDocument("AirPlane")
        #FreeCAD.Gui.ActiveDocument=FreeCAD.Gui.getDocument("AirPlane")
        #FreeCAD.ActiveDocument=FreeCAD.getDocument("AirPlane")

        generateWing('blabla')
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCAD.Gui.addCommand('generateWing',GenerateWingCommand()) 
