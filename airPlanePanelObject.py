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

__title__="FreeCAD Air Plane Panel"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"

import FreeCAD,FreeCADGui
from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
from pivy import coin
from FreeCAD import Vector, Base
from Draft import makeWire

import re, FreeCAD, FreeCADGui, Draft, Part, PartDesign,PartDesignGui,Sketcher,cProfile, os, string
import importAirfoilDAT




class _WPanel:
    def __init__(self, obj):
        '''Add some custom properties to our box feature'''
        obj.addProperty("App::PropertyLength","Length","WingPanel","Length of the wing").Length=1.0
        obj.addProperty("App::PropertyLength","Width","WingPanel","Width of the wing").Width=1.0
        obj.addProperty("App::PropertyLength","Height","WingPanel", "Height of the wing").Height=1.0
        obj.addProperty("App::PropertyStringList","PanelProfil","WingPanel","Profil type").PanelProfil=[u"Mod/AirPlaneDesign/wingribprofil/e207.dat"]
        obj.addProperty("App::PropertyLength","PanelLength","WingPanel","Length of the Wing").PanelLength=100.0
        obj.addProperty("App::PropertyFloatList","PanelDelta","WingPanel","Delta").PanelDelta=[0,70.0]
        obj.addProperty("App::PropertyLength","PanelWidth","WingPanel","Width of the panel").PanelWidth=300.0
        #cordre a l'emplature
        obj.addProperty("App::PropertyLength","PanelRootLength","WingPanel"," root length").PanelRootLength=300.0
        #corde au saumon
        obj.addProperty("App::PropertyLength","PanelTipLength","WingPanel"," wingtip length").PanelTipLength=200.0
        #--------------------------
        # Ordonner les champs
        #obj.OrderOutputBy = ['NumberOfPanel','Length', 'Width', 'Height','Delta']
        #ops = FreeCAD.ActiveDocument.addObject("Ribs::FeatureCompoundPython", "Ribs")
        #if ops.ViewObject:
        #    ops.ViewObject.Proxy = 0
        #    ops.ViewObject.Visibility = False

        #obj.Operations = ops

        obj.Proxy = self
    
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
    

    def setupRib(self, fp,number,pos,length,models=None):
        name=decodeName(fp.PanelProfil[number])
        fp.addProperty("App::PropertyLink", "Rib", "Panel", "Rib")
        print("input in setup rib")
        fp.Shape=process(FreeCAD.ActiveDocument.Name,name,
                         length,
                         pos,0,0,
                         0,0,0,
                         0,False,[])
        
        
    
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage(fp.PanelProfil[0])
        panelRootFace=FreeCAD.ActiveDocument.addObject("Part::Feature","PanelRootFace")
        #     def process(doc,filename,scale,
        #                posX,posY,posZ,
        #                rotX,rotY,rotZ,
        #                thickness,
        #                useSpline = True,coords=[]):
        
        # process(doc,filename,
        #         scale,
        #         posX,posY,posZ,
        #         rotX,rotY,rotZ,
        #         thickness,useSpline = False,coords=[]):
        print("input in execute process")
        panelRootFace.Shape=process(FreeCAD.ActiveDocument.Name,fp.PanelProfil[0],
                                    fp.PanelRootLength,
                                    fp.PanelDelta[0],0,0,
                                    0,0,0,
                                    0,False,[])
        
        panelTipFace=FreeCAD.ActiveDocument.addObject("Part::Feature","PanelTipFace")
        panelTipFace.Shape=process(FreeCAD.ActiveDocument.Name,fp.PanelProfil[0],
                                   fp.PanelTipLength,
                                   fp.PanelDelta[1],fp.PanelLength,0,
                                   0,0,0,
                                   0,False,[])
        #panelTipFace.translate(Base.Vector(fp.PanelLength,0,0))
             
        #fp=panelRootFace
        a=FreeCAD.ActiveDocument.addObject('Part::Loft','Loft') #addObject
        a.Sections=[panelRootFace, panelTipFace]
        fp=a#panelRootFace
        FreeCAD.Console.PrintMessage("Recompute Python Wing feature\n")

class ViewProviderWing:
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

 

class _CommandWPanel:
    "the WingPanel command definition"
    def GetResources(self):
        return {'MenuText': "Create a Panel(under dev)"}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wpanel")
        _WPanel(a)
        ViewProviderWing(a.ViewObject)
        #FreeCADGui.addModule("AirPlaneDesign")
        #FreeCAD.ActiveDocument.commitTransaction()
        FreeCAD.ActiveDocument.recompute()

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesingWPanel',_CommandWPanel())
