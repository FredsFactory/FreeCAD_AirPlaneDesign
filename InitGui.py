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
class AirPlaneDesignWorkbench(Workbench):
    MenuText = "AirPlaneDesign"
    ToolTip = "A description of my workbench"
    #Icon = """paste here the contents of a 16x16 xpm icon"""

    def Initialize(self):
        #"This function is executed when FreeCAD starts"
        import airPlaneDesignInitPlane, generateWing 
       #self.list 
        commandslist= [
            'airPlaneDesignInitPlane',
            'generateWing'
            ] 
                    
        #self.appendToolbar("My Commands",commandslist)#self.list) # creates a new toolbar with your commands
        
        self.appendMenu('Air Plane Design',commandslist)#self.list) # creates a new menu
        
        #self.appendMenu("Air PlaneDesign",commandslist)#self.list) # appends a submenu to an existing menu

    def Activated(self):
        "This function is executed when the workbench is activated"
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return

    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("AirPlaneDesignInitPlane",self.list) # add commands to the context menu

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(AirPlaneDesignWorkbench())

