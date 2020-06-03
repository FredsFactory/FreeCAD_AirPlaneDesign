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

__title__="FreeCAD Airplane Design"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"


import FreeCAD, FreeCADGui, Part, os
from airPlaneRib import WingRib, ViewProviderWingRib
from airPlaneWingUI import WingEditorPanel
from PySide import QtCore
from FreeCAD import Vector
import Part, Draft 
from importlib import reload
import math
from airPlaneWPanel import WingPanel 

smWB_icons_path =  os.path.join( os.path.dirname(__file__), 'resources', 'icons')

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)

#################################################
#  This module provides tools to build a
#  wing panel
#################################################
if open.__module__ in ['__builtin__','io']:
    pythonopen = open

_wingRibProfilDir=FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil'

class Wing:
    def __init__(self, obj, _wPanels):
         # _parent,_NberOfPanel,_panelInput,_rootChord,_tipChord,_panelLength,_tipTwist,_dihedral):
        '''Add some custom properties to our box feature'''
        self.obj = obj
        obj.Proxy = self
        
        obj.addProperty("App::PropertyLinkList","WingPanels","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","panel")).WingPanels=_wPanels
        
        obj.addProperty("App::PropertyBool","Solid","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","Solid")).Solid=True # 
        obj.addProperty("App::PropertyBool","Surface","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","Surface")).Surface=False 
        
        
    
        FreeCAD.ActiveDocument.recompute()


    def onChanged(self, obj, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        
    def execute(self, obj):
        '''Do something when doing a recomputation, this method is mandatory'''
        panelShape=[]
        for panel in obj.WingPanels :
            panelShape.append(panel.Shape)
        if obj.WingPanels :
         obj.Shape=Part.makeCompound(panelShape)

        FreeCAD.Console.PrintMessage("Recompute Python Wing feature\n")

class ViewProviderWing:
    def __init__(self, vobj):
        vobj.Proxy = self
        self.Object = vobj.Object
        
    def getIcon(self):    
        return os.path.join(smWB_icons_path,'panel.xpm')

    def attach(self, vobj):
        self.Object = vobj.Object
        self.onChanged(vobj,"Base")

    def claimChildren(self):
        return self.Object.WingPanels
        
    def onDelete(self, feature, subelements):
        return True
    
    def onChanged(self, fp, prop):
        pass
        
    def __getstate__(self):
        return None
 
    def __setstate__(self,state):
        return None

class CommandWing:
    "the Wing command definition"
    def GetResources(self):
        iconpath = os.path.join(smWB_icons_path,'panel.png')
        return {'Pixmap': iconpath, 'MenuText': QtCore.QT_TRANSLATE_NOOP("Create_a_wing","Create/Add a wing to plane, select a plane and clic")}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):

        print("-----------------Wing-----------------")
       
        selection = FreeCADGui.Selection.getSelectionEx()
        if selection :
           base = FreeCAD.ActiveDocument.getObject((selection[0].ObjectName))

        _wPanels=[]
          
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Wing")
        Wing(obj,_wPanels)
        ViewProviderWing(obj.ViewObject)
        b=[]
        if selection : #selection==None :
           if not base.Wings :
              base.Wings=obj
           else : 
              b=base.Wings
              b.append(obj)
              base.Wings=b
              
        if selection :  #selection ==None:   
           if not base.Group :
              base.Group=obj
           else : 
              b=base.Group
              b.append(obj)
              base.Group=b
           
        FreeCAD.ActiveDocument.recompute()      
        FreeCAD.Gui.activeDocument().activeView().viewAxonometric()
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")

 
if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignWing',CommandWing())
