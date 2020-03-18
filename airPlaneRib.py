#################################################
#
# Airfoil creation - Aircraft
# 
# Copyright (c) F. Nivoix - 2019 - V0.3
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


import FreeCAD,FreeCADGui
#import re
#import Draft
#import Part
#import PartDesign
#import PartDesignGui
#import Sketcher
#import cProfile
#import string

from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
from pivy import coin
from FreeCAD import Vector, Base
from Draft import makeWire
from airPlaneAirFoil import process,decodeName
from airPlaneDesingProfilUI import SelectObjectUI
from airPlaneAirFoilNaca import generateNaca

FreeCADGui.addLanguagePath(":/translations")

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)


class WingRib:
    def __init__(self, obj,_profil,_nacagene,_nacaNbrPoint,_chord,_x,_y,_z,_xrot,_yrot,_zrot,_thickness=0,_useSpline = True):
        '''Rib properties'''
        obj.Proxy = self
        obj.addProperty("App::PropertyFile","RibProfil","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Profil type")).RibProfil=_profil        
        if _nacagene==True :
            obj.addProperty("App::PropertyString","NacaProfil","NacaProfil",QtCore.QT_TRANSLATE_NOOP("App::Property","Naca Profil")).NacaProfil=_profil
        else :
            obj.addProperty("App::PropertyString","NacaProfil","NacaProfil",QtCore.QT_TRANSLATE_NOOP("App::Property","Naca Profil")).NacaProfil=""
                
        #obj.addProperty("App::PropertyInteger","NacaNbrPoint","NacaProfil","NacaNbrPoint").NacaNbrPoint=_nacaNbrPoint
        obj.addProperty("App::PropertyInteger","NacaNbrPoint","NacaProfil",QtCore.QT_TRANSLATE_NOOP("App::Property","Naca Number of Points")).NacaNbrPoint=_nacaNbrPoint
        #obj.addProperty("App::PropertyBool","useSpline","Rib","useSpline").useSpline =_useSpline
        obj.addProperty("App::PropertyBool","useSpline","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","use Spline")).useSpline =_useSpline
        #obj.addProperty("App::PropertyLength","Chord","Rib","chord").Chord=_chord
        obj.addProperty("App::PropertyLength","Chord","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Chord")).Chord=_chord
        obj.addProperty("App::PropertyLength","Thickness","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Thickness")).Thickness=_thickness
        obj.addProperty("App::PropertyLength","xrot","Rib","chord").xrot=_xrot
        obj.addProperty("App::PropertyLength","yrot","Rib","chord").yrot=_yrot
        obj.addProperty("App::PropertyLength","zrot","Rib","chord").zrot=_zrot
        obj.Placement.Base.x=_x
        obj.Placement.Base.y=_y
        obj.Placement.Base.z=_z
        # List Geomtry to edit list of points
        obj.addProperty("Part::PropertyGeometryList","Geometry","Rib","Geometry").Geometry=[]
        #obj.setEditorMode("MyPropertyName", mode) #2 -- hidden
    
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        #FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
    
    def execute(self, fp):
        #   Do something when doing a recomputation, this method is mandatory
        if fp.NacaProfil =="" :
             FreeCAD.Console.PrintMessage("Create Rib Start\n")
             name=decodeName(fp.RibProfil)
             FreeCAD.Console.PrintMessage(name)
              # process(doc,filename,
              #         scale,
              #         posX,posY,posZ,
              #         rotX,rotY,rotZ,
              #         thickness,
              #         useSpline = False,coords=[]):
             a,fp.Geometry=process(FreeCAD.ActiveDocument.Name,fp.RibProfil,
                                   fp.Chord,
                                   fp.Placement.Base.x,fp.Placement.Base.y,fp.Placement.Base.z,
                                   fp.xrot,fp.yrot,fp.zrot,
                                   0,
                                   fp.useSpline,fp.Geometry)
        else :
             a,fp.Geometry=generateNaca(fp.NacaProfil, fp.NacaNbrPoint, False, False,fp.Chord,fp.Placement.Base.x,fp.Placement.Base.y,fp.Placement.Base.z,fp.xrot,fp.yrot,fp.zrot,fp.useSpline,fp.Geometry)

        
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

class CommandWingRib:
    "the WingPanel command definition"
    def GetResources(self):
        return {'MenuText': "Create a Rib"}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):
        editor = SelectObjectUI()
        editor.setupUi()
        r = editor.form.exec_()
        if r:
            #r=1 => OK
            #print("corde : /n")
            #print (editor.form.NACANumber.text())
            
            if editor.form.NACANumber.text()=="" :
                b=editor.profilSelectedFilePath()
                a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wrib")
                WingRib(a,b,False,0,editor.form.chord.value(),0,0,0,0,0,0,editor.form.thickness.value(),(editor.form.kingOfLines.isChecked() == True))
                ViewProviderWingRib(a.ViewObject)
            else :
                print("Naca : ") 
                print( editor.form.NACANumber)
                b=editor.form.NACANumber
                a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wrib")
                WingRib(a,b.text(),True,int(editor.form.nacaNbrPoint.value()),editor.form.chord.value(),0,0,0,0,0,0,editor.form.thickness.value(),(editor.form.kingOfLines.isChecked() == True))
                ViewProviderWingRib(a.ViewObject)
            FreeCAD.ActiveDocument.recompute()
        else :
            print("Canceled")

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesingWRib',CommandWingRib())
