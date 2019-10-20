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

#import path_locator

smWBpath = os.path.dirname(path_locator.__file__)
smWB_icons_path =  os.path.join( smWBpath, 'resources', 'icons')
global main_smWB_Icon
main_smWB_Icon = os.path.join( smWB_icons_path , 'appicon.svg')

class AirPlaneDesignWorkbench(Workbench):
    def __init__(self):
     self.__class__.Icon = main_smWB_Icon# ':/AirPlaneDesign/resources/icons/favicon.svg'
     self.__class__.MenuText = "AirPlaneDesign"
     self.__class__.ToolTip = "A description of my workbench"
     #Icon = """paste here the contents of a 16x16 xpm icon"""

    def Initialize(self):
        #"This function is executed when FreeCAD starts"
        import airPlaneDesignInitPlane,airPlanePanel,generateWing,airPlaneDesignUI,generateWingRibs,airPlaneWingUI
        import airPlaneRib
       #self.list 
        commandslistV0= ['airPlaneDesignEdit','airPlaneDesignInitPlane','generateWing','generateWingRibs']
        commandslistV1= ['airPlaneDesingWRib','airPlaneDesingWPanel']
        self.appendToolbar("Air Plane Design",commandslistV1) # creates a new toolbar with your commands
        
        #self.appendMenu('Air Plane Design V0',commandslistV0+["Separator"] )#self.list) # creates a new menu
        self.appendMenu('Air Plane Design',["Separator"] +commandslistV1+["Separator"])

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

