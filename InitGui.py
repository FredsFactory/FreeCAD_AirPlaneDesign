#***************************************************************************
#*                                                                         *
#*   AirPlaneDesign workbench                                              *
#*                                                                         *
#*   Created by F. Nivoix  Copyright (c) 2018                              *
#*   Contributors : see source files                                       *
#*   For FreeCAD Versions = or > 0.17 tested on 0.19                       *
#*                                                                         *
#*   History :                                                             *
#*     v 0.5 :                                                             *
#*     v 0.4 : New Object : Plane, Wing and WingPanel. New Wing generator. *
#*     v 0.3 : NACA Rib generator, Nacelle generator by Claude             *
#*     v 0.2 : New release with parametric objects based on a dedicated UI *
#*     v 0.1 : 2018-07-11 : Initial release based on sheet deprecated!     *
#*                                                                         *
#* This program is free software; you can redistribute it and/or modify    *  
#* it under the terms of the GNU Lesser General Public License (LGPL)      *  
#* as published by the Free Software Foundation; either version 2 of       * 
#* the License, or (at your option) any later version.                     *
#* This program is distributed in the hope that it will be useful,         *
#* but WITHOUT ANY WARRANTY; without even the implied warranty of          *
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                    *
#* For more details see the LICENCE text file.                             *       
#*                                                                         *
#***************************************************************************

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore
import os


# resources ui, icon
import apdWBCommon as wb
global apdWB_Icon # lgtm[py/redundant-global-declaration]  
apdWB_Icon = os.path.join(wb.icons_path, 'apdIcon.svg')

# Qt tanslation handling
FreeCADGui.addLanguagePath(os.path.join(wb.base_path, 'translations'))

class AirPlaneDesignWorkbench(Workbench):
    def __init__(self):
        def QT_TRANSLATE_NOOP(context, text):
            return text
        self.__class__.Icon = apdWB_Icon
        self.__class__.MenuText = "AirPlaneDesign"
        self.__class__.ToolTip = "Tools to design an airplane"

    def Initialize(self):
        #"This function is executed when FreeCAD starts"
        def QT_TRANSLATE_NOOP(context, text):
            return text
        import apdPlane                     # Create a plane wizard
        import apdWing                      # Create/add a wing
        import apdNacelle                   # Create/add a nacelle
        import apdRib                       # Create/add a rib
        # airPlaneDesign WB commands
        self.comList= ['apdPlane', \
                       'apdWing', \
                       'apdNacelle', \
                       'apdRib']                

        # creates a new toolbar with your commands
        self.appendToolbar(QT_TRANSLATE_NOOP("apdGeneral", "Airplane Design"), self.comList)
        # creates a new menu
        self.appendMenu([QT_TRANSLATE_NOOP("apdGeneral","Airplane Design")], self.comList)

    def Activated(self):
        #This function is executed when the workbench is activated
        return

    def Deactivated(self):
        #This function is executed when the workbench is deactivated
        return

    def ContextMenu(self, recipient):
        # This is executed whenever the user right-clicks on screen
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu(QT_TRANSLATE_NOOP("apdGeneral", self.comlist)) # add commands to the context menu


    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(AirPlaneDesignWorkbench())

