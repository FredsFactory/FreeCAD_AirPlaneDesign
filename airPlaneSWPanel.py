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
from PySide import QtCore
import math

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

class WingSPanel:
    def __init__(self, obj, _rootRib ,_tipRib ,_rootChord=200,_tipChord=100,_panelLength=100,_tipTwist=0,_dihedral=0):
         # _parent,_NberOfPanel,_panelInput,_rootChord,_tipChord,_panelLength,_tipTwist,_dihedral):
        '''Add some custom properties to our box feature'''
        self.obj = obj
        obj.Proxy = self
        #obj.addProperty("App::PropertyLink","Base","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Rib of the panel")).Base=_rootRib#
        obj.addProperty("App::PropertyLink","RootRib","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Root Rib of the panel")).RootRib=_rootRib#.rootRib-_rootRib
        obj.addProperty("App::PropertyLink","TipRib","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Rib of the panel")).TipRib=_tipRib#.tipRib-_tipRib


        # leadingEdge : bord d'attaque
        obj.addProperty("App::PropertyLink","LeadingEdge","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Select the leading edge of the panal, line or Spline"))
        # trailing edge : bord de fuite
        obj.addProperty("App::PropertyLink","TrailingEdge","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Select the trailing edge of the panel, line or Spline"))

        obj.addProperty("App::PropertyLength","TipChord","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Chord")).TipChord=_tipChord
        obj.addProperty("App::PropertyLength","RootChord","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Root Chord")).RootChord=_rootChord

        obj.addProperty("App::PropertyLength","PanelLength","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Panel Length")).PanelLength=_panelLength
        obj.addProperty("App::PropertyAngle","TipTwist","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Twist")).TipTwist=_tipTwist
        obj.addProperty("App::PropertyAngle","Dihedral","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Dihedral")).Dihedral=_dihedral
        #obj.addProperty("App::PropertyLinkList","Ribs","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","list of ribs")).Ribs=[]

        obj.addProperty("App::PropertyBool","Solid","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Solid")).Solid=True #
        obj.addProperty("App::PropertyBool","Surface","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Surface")).Surface=False
        obj.addProperty("App::PropertyBool","Structure","Design",QtCore.QT_TRANSLATE_NOOP("App::Property","Surface")).Structure=False

        #ribs=[]
        #ribs.append(obj.RootRib)
        #ribs.append(obj.TipRib)
        #FreeCAD.ActiveDocument.recompute()


    def onChanged(self, obj, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, obj):
        '''Do something when doing a recomputation, this method is mandatory'''
        if not obj.Structure :
           if obj.RootRib :

           #obj.RootRib.Placement.Rotation.Axis.x=1
           #obj.RootRib.Placement.Rotation.Axis.y=0
           #obj.RootRib.Placement.Rotation.Axis.z=0
           #obj.RootRib.Placement.Rotation.Angle=obj.Dihedral

           #obj.TipRib.Placement.Rotation.Axis.x=1
           #obj.TipRib.Placement.Rotation.Axis.y=0
           #obj.TipRib.Placement.Rotation.Axis.z=0
           #obj.TipRib.Placement.Rotation.Angle=obj.Dihedral

              obj.TipRib.Placement.Base.y= obj.PanelLength
              #obj.TipRib.Placement.Base.z= obj.PanelLength*math.tan(obj.Dihedral)

              ribsWires=[]
              ribsWires.append(obj.RootRib.Shape.OuterWire)
              ribsWires.append(obj.TipRib.Shape.OuterWire)
              obj.RootRib.ViewObject.hide()
              obj.TipRib.ViewObject.hide()
              obj.Shape=Part.makeLoft(ribsWires,obj.Solid,False)
           else :
              print("Wing Panel : structure, not implemented yet")
        #FreeCAD.ActiveDocument.recompute()
        FreeCAD.Console.PrintMessage("Recompute Python Wing feature\n")

class ViewProviderPanel:
    def __init__(self, vobj):
        vobj.Proxy = self
        self.Object = vobj.Object

    def getIcon(self):
        return os.path.join(smWB_icons_path,'panel.xpm')

    def attach(self, vobj):
        self.Object = vobj.Object
        self.onChanged(vobj,"Base")

    def claimChildren(self):
        return [self.Object.TipRib] + [self.Object.RootRib]

    def onDelete(self, feature, subelements):
        return True

    def onChanged(self, fp, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def dumps(self):
        return None

    def loads(self, state):
        return None

class CommandWPanel:
    "the WingPanel command definition"
    def GetResources(self):
        iconpath = os.path.join(smWB_icons_path,'panel.png')
        return {'Pixmap': iconpath, 'MenuText': QtCore.QT_TRANSLATE_NOOP("Create_a_wing_Panel","Create/Add a wing panel, select a panl and clic")}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        print("---------------------------------------")
        print("-----------------Panel-----------------")
        print("---------------------------------------")

        selection = FreeCADGui.Selection.getSelectionEx()
        if selection :
           base = FreeCAD.ActiveDocument.getObject((selection[0].ObjectName))

        #---------------------création des nervures temporaires
        _rootRib=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibRoot_")
        WingRib(_rootRib,"/Users/fredericnivoix/Library/Preferences/FreeCAD/Mod/AirPlaneDesign/wingribprofil/naca/naca2412.dat",False,0,200,0,0,0,0,0,0)
        ViewProviderWingRib(_rootRib.ViewObject)


        _tipRib=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibTip_")
        WingRib(_tipRib,"/Users/fredericnivoix/Library/Preferences/FreeCAD/Mod/AirPlaneDesign/wingribprofil/naca/naca2412.dat",False,0,200,0,500,0,0,0,0)
        ViewProviderWingRib(_tipRib.ViewObject)
        FreeCAD.ActiveDocument.recompute()
        #----------
        #obj=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","WingPanel")

        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","WingPanel")
        WingPanel(obj,_rootRib,_tipRib,200,100,100,0,0)
        ViewProviderPanel(obj.ViewObject)
        b=[]
        if selection : #selection==None :
           if not base.WingPanels :
              base.WingPanels=obj
           else :
              b=base.WingPanels
              b.append(obj)
              base.WingPanels=b

        #if selection :  #selection ==None:
        #   if not base.Group :
        #      base.Group=obj
        #   else :
        #      b=base.Group
        #      b.append(obj)
        #      base.Group=b

        FreeCAD.ActiveDocument.recompute()
        FreeCAD.Gui.activeDocument().activeView().viewAxonometric()
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")


if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignSWingPanel',CommandWPanel())
