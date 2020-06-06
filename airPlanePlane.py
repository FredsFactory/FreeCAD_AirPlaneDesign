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

__title__="FreeCAD airPlane Plane"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"


import FreeCAD,FreeCADGui, os

from PySide import QtCore
from PySide import QtGui

FreeCADGui.addLanguagePath(":/translations")

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)

smWB_icons_path =  os.path.join( os.path.dirname(__file__), 'resources', 'icons')


class Plane:
    def __init__(self, obj):
        '''Rib properties'''
        obj.Proxy = self
         
        obj.addProperty("App::PropertyLinkList", "Wings", "Base", QtCore.QT_TRANSLATE_NOOP("App::Property", "List of wings"))
        

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Wing: Change property  " + str(prop) + "\n")

    def execute(self, fp):
        #   Do something when doing a recomputation, this method is mandatory
        FreeCAD.Console.PrintMessage("Wing : execute process\n")

    def addWing(self, op, before=None, removeBefore=False):
        group = self.obj.Wings.Group
        if op not in group:
            if before:
                try:
                    group.insert(group.index(before), op)
                    if removeBefore:
                        group.remove(before)
                except Exception as e:  # pylint: disable=broad-except
                    PathLog.error(e)
                    group.append(op)
            else:
                group.append(op)
            self.obj.Wings.Group = group
            op.Path.Center = self.obj.Operations.Path.Center


class PlaneTaskPanel: 
    '''A TaskPanel for the Rib'''
    def __init__(self,vobj): 
        print("init RibTaskPanel")
        self.obj = vobj
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/airPlaneDesignEdit.ui'  
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        self.update(vobj)

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)


    def update(self,vobj):
        'fills the dialog with plane properties'
        print('update')
        #self.form.thickness.setValue(vobj.Object.Thickness)
        #self.form.chord.setValue(vobj.Object.Chord)
        #self.form.kingOfLines.setChecked(vobj.Object.useSpline) 
        #self.form.fileName.setText(vobj.Object.RibProfil) 
        #self.form.NACANumber.setText(vobj.Object.NacaProfil)
        #self.form.nacaNbrPoint.setValue(vobj.Object.NacaNbrPoint)
        #self.form.finite_TE.setChecked(vobj.Object.finite_TE)
    
    def accept(self):
        '''Update properties of Rib'''
        print("accept")
        #fp=self.obj.Object
        #fp.Thickness=self.form.thickness.value()
        #fp.Chord=self.form.chord.value()
        #fp.useSpline=self.form.kingOfLines.isChecked()
        
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def retranslateUi(self, TaskPanel):
        #TaskPanel.setWindowTitle(QtGui.QApplication.translate("draft", "Faces", None))
        self.addButton.setText(QtGui.QApplication.translate("draft", "Update", None))
        print("")


class ViewProviderPlane:
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
        return os.path.join(smWB_icons_path,'plane.xpm')
    
    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
            Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
            to return a tuple of all serializable objects or None.'''
        return None
    
    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
            Since no data were serialized nothing needs to be done here.'''
        return None

    def setEdit(self,vobj,mode):
         #airPlaneDesignPlanedialog.ui
        taskd = PlaneTaskPanel(vobj)
        FreeCADGui.Control.showDialog(taskd)
        return True
    

class CommandPlane:
    "the WingPanel command definition"
 
    def GetResources(self):
        iconpath = os.path.join(smWB_icons_path,'plane.png')
        return {'Pixmap': iconpath, 'MenuText': QtCore.QT_TRANSLATE_NOOP("Create_a_Plane","Create a Plane")}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):
        #a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","plane")
        a=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython","plane")
        a.Group=[]
        Plane(a)
        ViewProviderPlane(a.ViewObject)
        FreeCAD.ActiveDocument.recompute()
            

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignPlane',CommandPlane())
