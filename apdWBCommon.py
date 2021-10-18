#***************************************************************************
#*                                                                         *
#*   AirPlaneDesign workbench                                              *
#*     For more details see InitGui.py and the LICENCE text file.          *
#*                                                                         *
#*   Module : apdWBCommon.py                                               *
#*   Common resources for the AirPlaneDesign workbench                     *
#*     - path to resources...                                              *
#*     - translation for python modules                                    *
#*     - messages : debug, console                                         *
#*                                                                         *
#*   History :                                                             *
#*     2021-10-09 : Initial release Claude GUTH                            *
#*                                                                         *
#***************************************************************************

__title__="FreeCAD airPlane Plane"
__author__ = "Claude GUTH "
__url__ = "https://fredsfactory.fr"

import os
import FreeCAD, FreeCADGui 
from PySide import QtCore

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)

# resources path, files
base_path= os.path.dirname(__file__)
resources_path= os.path.join(base_path, 'resources')
icons_path= os.path.join(resources_path, 'icons')

# debug messages handling
debug= False;        # global debug         
def debugMsg(msg, always= True):
    if debug or always:
        FreeCAD.Console.PrintMessage(translate("Debug", msg))     

def consoleMsg(msg, type=None):
    if type:
        if type=='W':
            FreeCAD.Console.PrintWarning(translate("App", msg))
            exit()
        if type=='E':
            FreeCAD.Console.PrintError(translate("App", msg))
            exit()
        FreeCAD.Console.PrintMessage(translate("App", msg))
    else:
        FreeCAD.Console.PrintMessage(translate("App", msg))
