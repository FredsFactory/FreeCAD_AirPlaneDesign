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
#------------------------------------------------------
#AirPlaneDesign 
#------------------------------------------------------

import path_locator
from PySide import QtCore


# Qt tanslation handling
#from DraftGui import translate
#from DraftGui import utf8_decode
FreeCADGui.addLanguagePath(":/translations")


smWBpath = os.path.dirname(path_locator.__file__)
smWB_icons_path =  os.path.join( smWBpath, 'resources', 'icons')
global main_smWB_Icon # lgtm[py/redundant-global-declaration]
main_smWB_Icon = os.path.join( smWB_icons_path , 'appicon.svg')

#def QT_TRANSLATE_NOOP(scope, text):
#    return text

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)


class AirPlaneDesignWorkbench(Workbench):
    def __init__(self):
        self.__class__.Icon = main_smWB_Icon
        self.__class__.MenuText = "AirPlaneDesign"
        self.__class__.ToolTip = "A description of my workbench"

    def Initialize(self):
        def QT_TRANSLATE_NOOP(scope, text):
          return text
        #"This function is executed when FreeCAD starts"
        import airPlanePanel
        import airPlaneRib
        import airPlanePlane
        import airPlaneWPanel
        import airPlaneWing
        import airPlaneWingWizard
        self.comList= ['airPlaneDesignPlane','airPlaneDesignWing','airPlaneDesignWingPanel','airPlaneDesignWRib','airPlaneDesignWingWizard','airPlaneDesignWPanel']
        # creates a new toolbar with your commands
        self.appendToolbar(QT_TRANSLATE_NOOP("AirPlaneDesign", "Air Plane Design"), self.comList)
        # creates a new menu
        self.appendMenu([QT_TRANSLATE_NOOP("AirPlaneDesign","Air Plane Design")],self.comList)

    def Activated(self):
        #This function is executed when the workbench is activated
        return

    def Deactivated(self):
        #This function is executed when the workbench is deactivated
        return

    def ContextMenu(self, recipient):
        # This is executed whenever the user right-clicks on screen
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("AirPlaneDesignInitPlane",self.list) # add commands to the context menu

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(AirPlaneDesignWorkbench())

