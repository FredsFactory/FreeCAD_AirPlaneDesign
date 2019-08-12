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

__title__="FreeCAD Arch Stairs"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"


import os,FreeCAD,FreeCADGui,airPlaneRib
from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
from pivy import coin
from FreeCAD import Vector, Base
from Draft import makeWire

import re, FreeCAD, FreeCADGui, Draft, Part, PartDesign,PartDesignGui,Sketcher
import cProfile, os, string

from airPlaneRib import WingRib, ViewProviderWingRib

#################################################
#  This module provides tools to build a
#  wing panel
#################################################
if open.__module__ in ['__builtin__','io']:
    pythonopen = open

_wingRibProfilDir=FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil'

class WPanel:
    def __init__(self, obj):
        '''Add some custom properties to our box feature'''
        
        obj.Proxy = self
        #obj.addProperty("App::PropertyFile","PanelProfil","WingPanel","Profil type").PanelProfil=u"/Users/fredericnivoix/Library/Preferences/FreeCAD/Mod/AirPlaneDesign/wingribprofil/e207.dat"
        obj.addProperty("App::PropertyFile","PanelProfil","WingPanel","Profil type").PanelProfil=_wingRibProfilDir+u"/e207.dat"
        obj.addProperty("App::PropertyInteger","NberOfPanel","WingPanel","Number of Panel").NberOfPanel=5
        
        obj.addProperty("App::PropertyFile","PanelProfil","WingPanel","Profil type").PanelProfil=_wingRibProfilDir+u"/e207.dat"
    #, _wingRibProfilDir+u"/e207.dat",_wingRibProfilDir+u"/e207.dat",_wingRibProfilDir+u"/e207.dat",_wingRibProfilDir+u"/e207.dat"]
        
        obj.addProperty("App::PropertyFloatList","PanelLength","WingPanel","Length of the Wing").PanelLength=[100.0,100.0,100,70,50]
        obj.addProperty("App::PropertyFloatList","PanelDelta","WingPanel","Delta").PanelDelta=[0.0,70.0]
        obj.addProperty("App::PropertyLinkList", "RibRoot", "Ribs", "Root Ribs")
        obj.addProperty("App::PropertyLinkList", "RibTip", "Ribs", "Tip Ribs")
        
        _ribs=[]
        _panel=[]
        _position=0

        for i in range(0,obj.NberOfPanel) :
           FreeCAD.Console.PrintMessage("Panel creation : ")
           FreeCAD.Console.PrintMessage(i)
           FreeCAD.Console.PrintMessage("\n")
           
           # Add Rib Root
           FreeCAD.Console.PrintMessage("Add Rib Root")
           _ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibRoot_"+str(i)))
           WingRib(_ribs[i*2],obj.PanelProfil,100,0,_position,0)
           ViewProviderWingRib(_ribs[i*2].ViewObject)
           obj.RibRoot.append(_ribs[i*2])
        
           # Add Rib tip
           FreeCAD.Console.PrintMessage("Add Rib tip")
           FreeCAD.Console.PrintMessage(i+1)
           _position=_position+obj.PanelLength[i]
           
           _ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibTip_"+str(i)))
           WingRib(_ribs[i*2+1],obj.PanelProfil,100,0,_position,0)
           ViewProviderWingRib(_ribs[i*2+1].ViewObject)
           obj.RibTip.append(_ribs[i*2+1])
       
        
        #_ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibRoot"))
        #WingRib(_ribs[0],obj.PanelProfil,100,0,0,0)
        #ViewProviderWingRib(_ribs[0].ViewObject)
        #obj.RibRoot.append(_ribs[0])

        # Add Rib Root
        
        #_ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibTip"))
        #WingRib(_ribs[1],obj.PanelProfil,100,0,obj.PanelLength[0],0)
        #ViewProviderWingRib(_ribs[1].ViewObject)
        #obj.RibTip.append(_ribs[1])


           FreeCAD.Console.PrintMessage("create the panel")
           _panel.append(FreeCAD.ActiveDocument.addObject('Part::Loft','panel'))
           _panel[i].Sections=[_ribs[i*2],_ribs[i*2+1]]
           _panel[i].Solid=True
           _panel[i].Ruled=False
           FreeCAD.ActiveDocument.recompute()
        
        obj.Group=_panel

        #obj.addProperty("App::PropertyLink", "Operations", "Base", "Operations ")
        # Ordonner les champs
        #obj.OrderOutputBy = ['NumberOfPanel','Length', 'Width', 'Height','Delta']

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
     
        FreeCAD.Console.PrintMessage("Recompute Python Wing feature\n")

    def addOperation(self, op, before = None):
        group = self.obj.Operations.Group
        if op not in group:
            if before:
                try:
                    group.insert(group.index(before), op)
                except Exception as e:
                    PathLog.error(e)
                    group.append(op)
            else:
                group.append(op)
            self.obj.Operations.Group = group
            op.Path.Center = self.obj.Operations.Path.Center


class ViewProviderPanel:
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

class CommandWPanel:
    "the WingPanel command definition"
    def GetResources(self):
        return {'MenuText': "Create a Panel(under dev)"}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):
        a=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","Wing")#Path::FeaturePython","wpanel") #"Part::FeaturePython","wpanel")
        WPanel(a)
        ViewProviderPanel(a.ViewObject)
        #FreeCADGui.addModule("AirPlaneDesign")
        #FreeCAD.ActiveDocument.commitTransaction()
        FreeCAD.ActiveDocument.recompute()

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesingWPanel',CommandWPanel())
