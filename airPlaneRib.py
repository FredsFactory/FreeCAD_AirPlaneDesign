#################################################
#
# Airfoil creation - Aircraft
# 
# Copyright (c) F. Nivoix - 2019 - V0.1
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

__title__="FreeCAD airPlaneRib"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"

#import cv2


import os,FreeCAD,FreeCADGui
from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
from pivy import coin
from FreeCAD import Vector, Base
from Draft import makeWire

import re, FreeCAD, FreeCADGui, Draft, Part, PartDesign,PartDesignGui,Sketcher,cProfile, os, string
from airPlaneAirFoil import process,decodeName
from airPlaneDesingProfilUI import SelectObjectUI
from airPlaneAirFoilNaca import generateNaca



class WingRib:
    def __init__(self, obj,_profil,_nacagene,_nacaNbrPoint,_chord,_x,_y,_z,_xrot,_yrot,_zrot,_useSpline = True):
        '''Rib properties'''
        obj.Proxy = self
        obj.addProperty("App::PropertyFile","RibProfil","Rib","Profil type").RibProfil=_profil
        if _nacagene==True :
            obj.addProperty("App::PropertyString","NacaProfil","NacaProfil","NacaProfil").NacaProfil=_profil
        else :
            obj.addProperty("App::PropertyString","NacaProfil","NacaProfil","NacaProfil").NacaProfil=""
                
        obj.addProperty("App::PropertyInteger","NacaNbrPoint","NacaProfil","NacaNbrPoint").NacaNbrPoint=_nacaNbrPoint
         #obj.addProperty("App::PropertyFloatList","PanelDelta","Rib","Delta").PanelDelta=[0,70.0]
        obj.addProperty("App::PropertyBool","useSpline","Rib","useSpline").useSpline =_useSpline
        obj.addProperty("App::PropertyLength","Chord","Rib","chord").Chord=_chord
        obj.addProperty("App::PropertyLength","xrot","Rib","chord").xrot=_xrot
        obj.addProperty("App::PropertyLength","yrot","Rib","chord").yrot=_yrot
        obj.addProperty("App::PropertyLength","zrot","Rib","chord").zrot=_zrot
        obj.Placement.Base.x=_x
        obj.Placement.Base.y=_y
        obj.Placement.Base.z=_z
    
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
    
    def execute(self, fp):
        #   Do something when doing a recomputation, this method is mandatory
        if fp.NacaProfil =="" :
             FreeCAD.Console.PrintMessage("Create Rib Start\n")
             name=decodeName(fp.RibProfil)
             #fp.addProperty("App::PropertyLink", "Rib", "Panel", "Rib")
             FreeCAD.Console.PrintMessage(name)
             a=process(FreeCAD.ActiveDocument.Name,fp.RibProfil,fp.Chord,fp.Placement.Base.x,fp.Placement.Base.y,fp.Placement.Base.z,fp.xrot,fp.yrot,fp.zrot,fp.useSpline)
        else :
             a=generateNaca(fp.NacaProfil, fp.NacaNbrPoint, False, False,fp.Chord,fp.Placement.Base.x,fp.Placement.Base.y,fp.Placement.Base.z,fp.xrot,fp.yrot,fp.zrot,fp.useSpline)

        
        fp.Shape=a
        FreeCAD.Console.PrintMessage("Create Rib End\n")

class ViewProviderWingRib:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.addProperty("App::PropertyColor","Color","Wing","Color of the wing").Color=(1.0,0.0,0.0)
        obj.Proxy = self
    
    def getDefaultDisplayMode(self):
        '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
        return "Flat Lines"
    
    def getIcon(self):
        '''Return the icon in XPM format which will appear in the tree view. This method is\
            optional and if not defined a default icon is shown.'''
        return """
            /* XPM */
            static const char * ViewProviderBox_xpm[] = {
            "16 16 6 1",
            "   c None",
            ".  c #141010",
            "+  c #615BD2",
            "@  c #C39D55",
            "#  c #000000",
            "$  c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """
    
    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
            Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
            to return a tuple of all serializable objects or None.'''
        return None
    
    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
            Since no data were serialized nothing needs to be done here.'''
        return None

    #def makeWing():
    # FreeCAD.newDocument()
    # a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wpanel")
    #a=FreeCAD.ActiveDocument.addObject("Wing::FeaturePython","Wing")
    #Wing(a)
    #ViewProviderWing(a.ViewObject)
#App.ActiveDocument.recompute()
#makeWing()

class CommandWingRib:
    "the WingPanel command definition"
    def GetResources(self):
        return {'MenuText': "Create a Rib(under dev)"}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):
        editor = SelectObjectUI()
        editor.setupUi()
        r = editor.form.exec_()
        if r:
            #r=1 => OK
            print("corde : /n")
            print (editor.form.NACANumber.text())
            
            if editor.form.NACANumber.text()=="" :
                b=editor.profilSelectedFilePath()#currentItem()
                a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wrib")
                WingRib(a,b,False,0,editor.form.chord.value(),0,0,0,0,0,0,(editor.form.kingOfLines.isChecked() == True))
                ViewProviderWingRib(a.ViewObject)
            else :
                print("Naca : ") 
                print( editor.form.NACANumber)
                b=editor.form.NACANumber
                a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wrib")
                WingRib(a,b.text(),True,int(editor.form.nacaNbrPoint.value()),editor.form.chord.value(),0,0,0,0,0,0,(editor.form.kingOfLines.isChecked() == True))
                ViewProviderWingRib(a.ViewObject)
            FreeCAD.ActiveDocument.recompute()
        else :
            print("Canceled")

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesingWRib',CommandWingRib())
