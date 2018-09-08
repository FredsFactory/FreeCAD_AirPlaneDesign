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

def generateprofilgenerique(body,x_saumon,y_saumon,x_emplature, y_emplature, hauteur, largeur,i):
    print( "generateprofilgenerique / start")
    nbreOfFaces=len(body.Shape.Faces)
    FreeCAD.Gui.activeDocument().ActiveView.setActiveObject('pdbody', body) #Active le body
    b=body.newObject('Sketcher::SketchObject','BordAttaque'+str(i/2)+'_0')
    FreeCAD.ActiveDocument.recompute()

    print( "Face1")
    b.Support = (FreeCAD.ActiveDocument.getObject("SubWing00"+str(i/2+1)),["Face1"])   #+str(nbreOfFaces)-1)])
    #b.Support = (body.BaseFeature,["Face1"])#+str(nbreOfFaces)-1)])
   
    print (b.Label)
    b.MapMode = 'FlatFace'
    FreeCAD.ActiveDocument.recompute()
    
    geoList = []
    geoList.append(Part.LineSegment(FreeCAD.Vector(-x_emplature,y_emplature-hauteur,0),FreeCAD.Vector(-x_emplature+largeur,y_emplature-hauteur,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(-x_emplature+largeur,y_emplature-hauteur,0),FreeCAD.Vector(-x_emplature+largeur,y_emplature+hauteur,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(-x_emplature+largeur,y_emplature+hauteur,0),FreeCAD.Vector(-x_emplature,y_emplature+hauteur,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(-x_emplature,y_emplature+hauteur,0),FreeCAD.Vector(-x_emplature,y_emplature-hauteur,0)))
    
    b.addGeometry(geoList,False)
    conList = []
    conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
    conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
    conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
    conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
    conList.append(Sketcher.Constraint('Horizontal',0))
    conList.append(Sketcher.Constraint('Vertical',1))
    #conList.setExpression('Constraints[6]', u'AirPlaneData.p001_p + 10')
    b.addConstraint(conList)
    
    FreeCAD.Gui.ActiveDocument.resetEdit()
    
    FreeCAD.ActiveDocument.recompute()
    #FreeCAD.Gui.activeDocument().ActiveView.setActiveObject('pdbody', body) #Active le body
    print ("Face3")
    #print ('BordAttaque'+str(i/2)+'_1, '+"Face"+str(nbreOfFaces))
    c=body.newObject('Sketcher::SketchObject','BordAttaque'+str(i/2)+'_1')
    print( c.Label)
    FreeCAD.ActiveDocument.recompute()
    #c.Support = (FreeCAD.ActiveDocument.BaseFeature,["Face"+str(nbreOfFaces)])
    #c.Support = (body.BaseFeature,["Face3"])#+str(nbreOfFaces)])
    c.Support = (FreeCAD.ActiveDocument.getObject("SubWing00"+str(i/2+1)),["Face3"])#+str(nbreOfFaces)])
    FreeCAD.Gui.ActiveDocument.getObject("SubWing00"+str(i/2+1)).Visibility=False
  

    c.MapMode = 'FlatFace'
    FreeCAD.ActiveDocument.recompute()
    
    geoList = []
    geoList.append(Part.LineSegment(FreeCAD.Vector(-x_saumon,y_saumon-hauteur,0),FreeCAD.Vector(-x_saumon+largeur,y_saumon-hauteur,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(-x_saumon+largeur,y_saumon-hauteur,0),FreeCAD.Vector(-x_saumon+largeur,y_saumon+hauteur,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(-x_saumon+largeur,y_saumon+hauteur,0),FreeCAD.Vector(-x_saumon,y_saumon+hauteur,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(-x_saumon,y_saumon+hauteur,0),FreeCAD.Vector(-x_saumon,y_saumon-hauteur,0)))
    c.addGeometry(geoList,False)
   
    conList = []
    conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
    conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
    conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
    conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
    conList.append(Sketcher.Constraint('Horizontal',0))
    conList.append(Sketcher.Constraint('Vertical',1))
    conList.append(Sketcher.Constraint('Vertical',3))
    c.addConstraint(conList)
    FreeCAD.ActiveDocument.recompute()
    #---------
    # Suppression du bord d attaque
    #---------
    d=body.newObject("PartDesign::SubtractiveLoft","SubtractiveLoft")
    d.Profile=b
    d.Sections = [c]
    FreeCAD.ActiveDocument.recompute()
    #FreeCAD.Gui.activeDocument().hide('BaseFeature'+str(i/2))
    #Gui.getDocument("Aile_v0_3").getObject("BaseFeature").Visibility=False
    FreeCAD.Gui.activeDocument().hide('BordAttaque'+str(i/2)+'_0')
    FreeCAD.Gui.activeDocument().hide('BordAttaque'+str(i/2)+'_1')
    FreeCAD.ActiveDocument.recompute()
    print( "generateprofilgenerique / end fonction")
    
    return

#---------------------------------------------------------
# Creation du bord d'attaque
#---------------------------------------------------------
def generateprofilBA(body,hauteur_bordattaque, profondeur_bordattaque, delta_saumon, delta_emplature,i):
    generateprofilgenerique(body,delta_saumon,0,delta_emplature, 0, hauteur_bordattaque/2, profondeur_bordattaque,i)
    return
#---------------------------------------------------------
# Creation de la clef d aile
#---------------------------------------------------------

def generateprofilWingsKey(body,x, y, long, radius, number_of_panels,sketchcleaile):
    if sketchcleaile==None :
        nbreOfFaces=len(body.Shape.Faces)
        FreeCAD.Gui.activeDocument().ActiveView.setActiveObject('pdbody', body) #Active le body
        b=body.newObject('Sketcher::SketchObject','CleAile')
        sketchcleaile=b
        print( ' Nombre de faces : '+str(nbreOfFaces))
        print( body.Label+', '+"Face2"+str(nbreOfFaces-1))
    
        b.Support = (body.BaseFeature,["Face1"])#+str(nbreOfFaces-1)
        b.MapMode = 'FlatFace'
    
        FreeCAD.ActiveDocument.recompute()
        b.addGeometry(Part.Circle(FreeCAD.Vector(x,y,0),FreeCAD.Vector(0,0,1),11.808961),False)
        
        b.addConstraint(Sketcher.Constraint('Radius',0,radius))
        b.setDatum(0,FreeCAD.Units.Quantity(radius))
        b.addConstraint(Sketcher.Constraint('DistanceX',-2,1,0,3,x))
        b.setDatum(1,FreeCAD.Units.Quantity(x))
        b.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,y))
        b.setDatum(2,FreeCAD.Units.Quantity(y))

        b.setExpression('Constraints[1]', u'AirPlaneData.wing_key_x')
        b.setExpression('Constraints[2]', u'AirPlaneData.wing_key_y')
        b.setExpression('Constraints[0]', u'AirPlaneData.wing_key_radius')
        
        FreeCAD.ActiveDocument.recompute()

        d=body.newObject("PartDesign::Pocket","KeyWing")
        d.Profile = b
        d.Length = 5.0
        d.Length = long
        d.Length2 = long
        d.Type = 0
        d.UpToFace = None
        d.Reversed = 0
        d.Midplane = 0
        d.Offset = 0.000000
        d.Reversed = True
        d.setExpression('Length', u'AirPlaneData.wing_key_length')
    else :
        d=body.newObject("PartDesign::Pocket","KeyWing")
        d.Profile = sketchcleaile
        d.Length = 5.0
        d.Length = long
        d.Length2 = long#100.000000
        d.Type = 0
        d.UpToFace = None
        d.Reversed = 0
        d.Midplane = 0
        d.Offset = 0.000000
        d.Reversed = True
        d.setExpression('Length', u'AirPlaneData.wing_key_length')
    FreeCAD.ActiveDocument.recompute()
    return sketchcleaile

#---------------------------------------------------------
# Creation d un peigne
#---------------------------------------------------------

def generateprofil(body,x, y, long, largeur, hauteur, number_of_panels,sketchcleaile):
    if sketchcleaile==None :
        nbreOfFaces=len(body.Shape.Faces)
        FreeCAD.Gui.activeDocument().ActiveView.setActiveObject('pdbody', body) #Active le body
        b=body.newObject('Sketcher::SketchObject','Peigne00')
        sketchcleaile=b
    
        b.Support = (body.BaseFeature,["Face1"])#+str(nbreOfFaces-1)
        b.MapMode = 'FlatFace'
        FreeCAD.ActiveDocument.recompute()
        geoList = []
        geoList.append(Part.LineSegment(FreeCAD.Vector(-x,y-hauteur,0),FreeCAD.Vector(-x+largeur,y-hauteur,0)))
        geoList.append(Part.LineSegment(FreeCAD.Vector(-x+largeur,y-hauteur,0),FreeCAD.Vector(-x+largeur,y+hauteur,0)))
        geoList.append(Part.LineSegment(FreeCAD.Vector(-x+largeur,y+hauteur,0),FreeCAD.Vector(-x,y+hauteur,0)))
        geoList.append(Part.LineSegment(FreeCAD.Vector(-x,y+hauteur,0),FreeCAD.Vector(-x,y-hauteur,0)))
    
        b.addGeometry(geoList,False)
        conList = []
        conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
        conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
        conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
        conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
        conList.append(Sketcher.Constraint('Horizontal',0))
        conList.append(Sketcher.Constraint('Vertical',1))
        #conList.setExpression('Constraints[6]', u'AirPlaneData.p001_p + 10')
        b.addConstraint(conList)
        
        FreeCAD.ActiveDocument.recompute()

        d=body.newObject("PartDesign::Pocket","Peigne00")
        d.Profile = b
        d.Length = 5.0
        d.Length = long
        d.Length2 = long
        d.Type = 0
        d.UpToFace = None
        d.Reversed = 0
        d.Midplane = 0
        d.Offset = 0.000000
        d.Reversed = True
        d.Length=long
        #d.setExpression('Length', u'AirPlaneData.wing_key_length')
    else :
        d=body.newObject("PartDesign::Pocket","Peigne00")
        d.Profile = sketchcleaile
        d.Length = 5.0
        d.Length = long
        d.Length2 = long#100.000000
        d.Type = 0
        d.UpToFace = None
        d.Reversed = 0
        d.Midplane = 0
        d.Offset = 0.000000
        d.Reversed = True
        d.Length=long
    #d.setExpression('Length', u'AirPlaneData.wing_key_length')
    FreeCAD.ActiveDocument.recompute()
    return sketchcleaile

def generateWing(name):
 list_profil_1mm_ref=[]
 profil_construction_aile_emplature=[]
 profil_construction_aile_saumon=[]
 panel=[] # list of panel
 #panel_body=[]
 wing_right=[]
 number_of_profils=int(FreeCAD.ActiveDocument.AirPlaneData.number_of_profils)
 number_of_panels=int(FreeCAD.ActiveDocument.AirPlaneData.number_of_panels)
 dat_file=[FreeCAD.ActiveDocument.AirPlaneData.getContents('B6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('C6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('D6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('E6'),
          FreeCAD.ActiveDocument.AirPlaneData.getContents('F6')]

 cleaile_X=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('C27'))
 cleaile_Y=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('D27'))
 cleaile_Z=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('E27'))
 cleaile_radius=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('F27'))
 cleaile_long=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('G27'))
 cleaile_angleX=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('H27'))
 cleaile_angleY=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('I27'))
 cleaile_angleZ=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('J27'))
 #------------------------------------------------------------------
 # creation du group permettant de rassembler l ensemble des elements de construction de l aile
 #------------------------------------------------------------------
 group=FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Groupe")
 group.Label='Profils'
 #------------------------------------------------------------------
 # import des profils, utilisation de la macro importAirfoilDAT
 #------------------------------------------------------------------
 if 1 : #FreeCAD.ActiveDocument.AirPlaneData.import_profil=="Yes" :
    print ("import profil, corde 1mm")
    scalefactor=1

 for number_profil in range(0,int(FreeCAD.ActiveDocument.AirPlaneData.number_of_profils)):
      print "profil de ref : "+str(number_profil)+"    Name file :"+dat_file[number_profil]
      importAirfoilDAT.insert(dat_file[number_profil],FreeCAD.ActiveDocument.Name)
      points = FreeCAD.ActiveDocument.ActiveObject.Points
      Draft.makeBSpline(points, closed=True)
      obj_nervure_ref=Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(scalefactor,scalefactor,scalefactor),center=FreeCAD.Vector(0,0,0),legacy=True)

      obj_nervure_ref.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,0),0)
      FreeCAD.ActiveDocument.removeObject("DWire")
      FreeCAD.Gui.ActiveDocument.ActiveObject.Visibility=False
      profilname= FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + number_profil)+str(7))

      obj_nervure_ref.Label="Prof_ref_1mm_"+profilname
      group.addObject(obj_nervure_ref)
      list_profil_1mm_ref.append(obj_nervure_ref)
      print "nom : "+obj_nervure_ref.Label

 FreeCAD.ActiveDocument.recompute()

#------------------------------------------------------------------
# Creation des nervures d'emplature et du saumon de chaque paneau
#  wing_part : part => Label : Wing
#  profil_number : (avant => aa)
#  obj_clone_nervure : Dwire => label : Profil_E00xxx
#  obj_clone_nervure_sketch : sketch => label : Profil_sketch_E00xxx
#------------------------------------------------------------------
#position_nervure=0
#position_emplature=0
#posvec=FreeCAD.Vector(0,0,0)
#rotvec=FreeCAD.Vector(1,0,0)#Vector(0,0,0)
#Draft.clone(list_profil_1mm_ref[0])
# Creation de l aile
 wing_part=FreeCAD.activeDocument().addObject('App::Part','Part')
 wing_part.Label = 'Wing'
 FreeCAD.ActiveDocument.recompute()
 print "nombre de paneau"
 print int(FreeCAD.ActiveDocument.AirPlaneData.number_of_panels)

 for i in range(0,int(FreeCAD.ActiveDocument.AirPlaneData.number_of_panels)):
   corde_emplature=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(13+4)))
   corde_saumon=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(14+4)))
   profil_number=int(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B')+i)+str(11)))-1 # profil number
   
   angleX=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(19)))
   angleY=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(20)))
   angleZ=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(21)))
   #---------------------------------
   # Create panel
   #---------------------------------
   panel_wing=FreeCAD.activeDocument().addObject('PartDesign::Body','Panel00'+str(i+1))#'Body')
   panel_wing.Label='Panel00'+str(i+1)
   FreeCAD.ActiveDocument.recompute()
   wing_part.addObject(panel_wing)
   FreeCAD.ActiveDocument.recompute()
   # nervure emplature
   obj_clone_nervure=Draft.clone(list_profil_1mm_ref[profil_number]) # creation de la nervure emplature
   obj_clone_nervure.Scale =(corde_emplature,corde_emplature,1)          # scale the rib
   obj_clone_nervure.Label="Profil_E00"+str(i)                           # nommage
   FreeCAD.ActiveDocument.recompute()
   FreeCAD.Gui.ActiveDocument.ActiveObject.Visibility=False
   
   obj_clone_nervure_sketch=Draft.makeSketch(obj_clone_nervure,autoconstraints=True)
   obj_clone_nervure_sketch.Label="Profil_sketch_E00"+str(i)             # nommage
   FreeCAD.ActiveDocument.recompute()
   group.addObject(obj_clone_nervure)
   FreeCAD.ActiveDocument.recompute()
   if i==0:
    obj_clone_nervure_sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),4.5))
    obj_clone_nervure_sketch.setExpression('Placement.Rotation.Angle', u'AirPlaneData.rot_e001_z')
    #obj_clone_nervure_sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),u'AirPlaneData.rot_e001_z'))
    #obj_clone_nervure_sketch.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(10,20,30), App.Vector(0,0,0))

    obj_clone_nervure_sketch.setExpression('Placement.Rotation.Angle', u'AirPlaneData.rot_e001_x')
    obj_clone_nervure_sketch.setExpression('Placement.Base.y', u'-AirPlaneData.rot_e001_h')
   else:
    if i==1:
     obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1')
     obj_clone_nervure_sketch.setExpression('Placement.Base.x', u'-AirPlaneData.d1')
     obj_clone_nervure_sketch.setExpression('Placement.Base.y', u'-AirPlaneData.rot_e002_h')
    else :
     if i==2:
      obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1+ AirPlaneData.l2')
      obj_clone_nervure_sketch.setExpression('Placement.Base.x', u'- AirPlaneData.d2')
      obj_clone_nervure_sketch.setExpression('Placement.Base.y', u'-AirPlaneData.rot_e002_h')
     else :
      if i==3:
       obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1+ AirPlaneData.l2 + AirPlaneData.l3')
       obj_clone_nervure_sketch.setExpression('Placement.Base.x', u' - AirPlaneData.d3')
       obj_clone_nervure_sketch.setExpression('Placement.Base.y', u'-AirPlaneData.rot_e003_h')
      else:
       if i==4:
        obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1+ AirPlaneData.l2 + AirPlaneData.l3 +  AirPlaneData.l4')
        obj_clone_nervure_sketch.setExpression('Placement.Base.x', u'- AirPlaneData.d4')
        obj_clone_nervure_sketch.setExpression('Placement.Base.y', u'-AirPlaneData.rot_e004_h')
       else:
        if i==5:
         obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1+ AirPlaneData.l2 + AirPlaneData.l3 + AirPlaneData.l4 + AirPlaneData.l5')
         obj_clone_nervure_sketch.setExpression('Placement.Base.x', u'- AirPlaneData.d5')
         obj_clone_nervure_sketch.setExpression('Placement.Base.y', u'-AirPlaneData.rot_e005_h')

   #association de la nervure au body
   FreeCAD.ActiveDocument.recompute()
   panel_wing.addObject(obj_clone_nervure_sketch)
   FreeCAD.ActiveDocument.recompute()
   profil_construction_aile_emplature.append(obj_clone_nervure_sketch) #sauvegare nervure dans tableau
   #------------------
   # nervure saumon
   #   position_nervure= position_nervure+float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(15)))
   #  position_emplature=-float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i)+str(12+4)))
   #  posvec=FreeCAD.Vector(position_emplature,position_nervure,0)
   #  rotvec=FreeCAD.Vector(1,0,0)
   FreeCAD.ActiveDocument.recompute()
   obj_clone_nervure=Draft.clone(list_profil_1mm_ref[profil_number]) # creation de la nervure saumon
   obj_clone_nervure.Scale =(corde_saumon,corde_saumon,1) # mise a l echelle
   obj_clone_nervure.Label="Profil_S00"+str(i)            # nommage
   group.addObject(obj_clone_nervure)
   FreeCAD.ActiveDocument.recompute()

   FreeCAD.Gui.ActiveDocument.ActiveObject.Visibility=False       # obj_clone_nervure.Visibility=False
   obj_clone_nervure_sketch=Draft.makeSketch(obj_clone_nervure,autoconstraints=True)
   obj_clone_nervure_sketch.Label="Profil_sketch_S00"+str(i)      # nommage
   FreeCAD.ActiveDocument.recompute()
   if i==0:
    obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1')
    obj_clone_nervure_sketch.setExpression('Placement.Base.x', u'-AirPlaneData.d1')
   else :
    if i==1:
     obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1+ AirPlaneData.l2')
     obj_clone_nervure_sketch.setExpression('Placement.Base.x', u' -AirPlaneData.d2')
    else :
     if i==2:
      obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1+ AirPlaneData.l2 + AirPlaneData.l3')
      obj_clone_nervure_sketch.setExpression('Placement.Base.x', u'-AirPlaneData.d3')
     else:
      if i==3:
       obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1+ AirPlaneData.l2 + AirPlaneData.l3 + AirPlaneData.l4')
       obj_clone_nervure_sketch.setExpression('Placement.Base.x', u' -AirPlaneData.d4')
      else:
       if i==4:
        obj_clone_nervure_sketch.setExpression('Placement.Base.z', u'AirPlaneData.l1+ AirPlaneData.l2 + AirPlaneData.l3 + AirPlaneData.l4 + AirPlaneData.l5')
        obj_clone_nervure_sketch.setExpression('Placement.Base.x', u' -AirPlaneData.d5')
   FreeCAD.ActiveDocument.recompute()
   #association de la nervure au body
   panel_wing.addObject(obj_clone_nervure_sketch)
   profil_construction_aile_saumon.append(obj_clone_nervure_sketch)             # sauvegare nervure dans tableau
   FreeCAD.ActiveDocument.recompute()
   a=panel_wing.newObject("PartDesign::AdditiveLoft","SubWing00"+str(i+1))
   FreeCAD.ActiveDocument.recompute()
   a.Profile = profil_construction_aile_emplature[i] #affectation a additiveloft
   a.Sections = [profil_construction_aile_saumon[i]]
   col=[(0.2,0.4,0.6)]
   a.ViewObject.DiffuseColor=col
   a.ViewObject.Transparency=70
   FreeCAD.ActiveDocument.recompute()
   panel.append(panel_wing)
   FreeCAD.ActiveDocument.recompute()
 
 FreeCAD.ActiveDocument.recompute()
 wing_part.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),90))
 FreeCAD.Gui.SendMsgToActiveView("ViewFit")
 FreeCAD.Gui.activeDocument().activeView().viewAxonometric()

 #-------------------------
 # generation du bord d attaque
 #-------------------------
 if FreeCAD.ActiveDocument.AirPlaneData.getContents('B36')=="Yes":
  print( "Generation Bord d attaque")
  delta_emplature=0
  delta_saumon=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B'))+str(16)))
  hauteur_bordattaque=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('F'))+str(36)))
  profondeur_bordattaque=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('G'))+str(36)))
 
  for i in range(0,number_of_panels*2,2):
   generateprofilBA(panel[(i/2)],hauteur_bordattaque, profondeur_bordattaque, delta_saumon-delta_emplature, 0,i)
   col=[(0.2,0.4,0.6)]
   panel[(i/2)].ViewObject.DiffuseColor=col
   panel[(i/2)].ViewObject.Transparency=70
   if i<>number_of_panels*2-2 :
    delta_emplature=delta_saumon
    delta_saumon=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i/2+1)+str(16)))
   else :
    delta_emplature=delta_saumon
    delta_saumon=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i/2)+str(16)))
 else :
  print ("B36 => No, no BA")

#-------------------------
 # generation des peignes sauf BA et BF
 #-------------------------
 for j in range (0,4):
     
  if FreeCAD.ActiveDocument.AirPlaneData.getContents('B'+str(38+j))=="Yes":
    print( "B38 => Yes,")
    print( FreeCAD.ActiveDocument.AirPlaneData.getContents('A'+str(38+j)))   #'A38'))
    x=-float(FreeCAD.ActiveDocument.AirPlaneData.getContents('C'+str(38+j)))      #'C38')
    y=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('D'+str(38+j)))       #'D38')
    long=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('H'+str(38+j)))    #'H38')
    largeur=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('G'+str(38+j))) #'G38')
    hauteur=float(FreeCAD.ActiveDocument.AirPlaneData.getContents('F'+str(38+j))) #'F38')
    col=[(0.2,0.4,0.6)]
    panel[(i/2)].ViewObject.DiffuseColor=col
    panel[(i/2)].ViewObject.Transparency=70
        #if i<>number_of_panels*2-2 :
        #delta_emplature=delta_saumon
        #delta_saumon=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i/2+1)+str(16)))
        #else :
        #delta_emplature=delta_saumon
        #delta_saumon=float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i/2)+str(16)))

    for i in range(0,number_of_panels*2,2):
     if i==0 :
      print(i)
      sketchcleaile=None
       #             generateprofil(body,x, y, long, largeur, hauteur, number_of_panels,sketchcleaile)
       #   "p001_rotx"
       #sketchcleaile=generateprofil(panel[(i/2)],'p001_rotx', 'p001_roty', long, largeur, hauteur, number_of_panels,sketchcleaile)
      sketchcleaile=generateprofil(panel[(i/2)],x, y, long, largeur, hauteur, number_of_panels,sketchcleaile)
   
      print ("creation clef d aile")
     else :
      print ("les autres panels")
      #             generateprofil(body,x, y, long, largeur, hauteur, number_of_panels,sketchcleaile)
      print i
      sketchcleaile=generateprofil(panel[(i/2)],x, y, long, largeur, hauteur, number_of_panels,sketchcleaile)
      col=[(0.2,0.4,0.6)]
      panel[(i/2)].ViewObject.DiffuseColor=col
      panel[(i/2)].ViewObject.Transparency=70
  else:
   print ("B38 => No, no Peigne#1")

#-------------------------
# generation de la clef d aile
#-------------------------
 if FreeCAD.ActiveDocument.AirPlaneData.getContents('B27')=="Yes":
  print ("Integration de la clef d aile")
  for i in range(0,number_of_panels*2,2):
   if i==0 :
    sketchcleaile=None
    sketchcleaile=generateprofilWingsKey(panel[(i/2)],cleaile_X, cleaile_Y, cleaile_long, cleaile_radius, number_of_panels,sketchcleaile)
    print ("creation clef d aile")
   else :
    print ("les autres panels")
    sketchcleaile=generateprofilWingsKey(panel[(i/2)],cleaile_X, cleaile_Y, cleaile_long, cleaile_radius, number_of_panels,sketchcleaile)
   col=[(0.2,0.4,0.6)]
   panel[(i/2)].ViewObject.DiffuseColor=col
   panel[(i/2)].ViewObject.Transparency=70
 else:
  print ("B27 => No, Pas de clef d aile")


#return
#------------------------------------------------------------------
# trash
#------------------------------------------------------------------


def generateWingtmp(name):
    # Passage de cable
    if FreeCAD.ActiveDocument.AirPlaneData.getContents('B28')<>"":
     if i==0:
        sketchcable=None
        sketchcable=generateprofilWingsKey(body,
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('B28')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('C28')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('F28')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('E28')),
                                            number_of_panels,sketchcable)
     else:
        sketchcable=generateprofilWingsKey(body,
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('B28')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('C28')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('F28')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('E28')),
                                            number_of_panels,sketchcable)
    # Teton
    if FreeCAD.ActiveDocument.AirPlaneData.getContents('B29')<>"":
     if i==0:
        sketchcteton=None
        sketchcteton=generateprofilWingsKey(body,
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('B29')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('C29')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('F29')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('E29')),
                                            number_of_panels,sketchcteton)

     else:
        sketchcteton=generateprofilWingsKey(body,
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('B29')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('C29')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('F29')),
                                            float(FreeCAD.ActiveDocument.AirPlaneData.getContents('E29')),
                                            number_of_panels,sketchcteton)

    
    
    if i<>number_of_panels*2-2 :
        delta_emplature=delta_saumon
        delta_saumon=-float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i/2+1)+str(16)))
    else :
        delta_emplature=delta_saumon
        delta_saumon=-float(FreeCAD.ActiveDocument.AirPlaneData.getContents(chr(ord('B') + i/2)+str(16)))

    body.ViewObject.DiffuseColor=col
    body.ViewObject.Transparency=70
    #------------------------------------
    #--------Fin creation du Body
    #------------------------------------
    
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.Gui.SendMsgToActiveView("ViewFit")
    FreeCAD.Gui.activeDocument().activeView().viewAxonometric()
    FreeCAD.ActiveDocument.recompute()


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
