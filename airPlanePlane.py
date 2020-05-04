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


import FreeCAD,FreeCADGui

from PySide import QtCore
from PySide import QtGui

FreeCADGui.addLanguagePath(":/translations")

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)


class Plane:
    def __init__(self, obj,_profil,_nacagene,_nacaNbrPoint,_chord,_x,_y,_z,_xrot,_yrot,_zrot,_thickness=0,_useSpline = True,_finite_TE = False):
        '''Rib properties'''
        obj.Proxy = self
        obj.addProperty("App::PropertyFile","RibProfil","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Profil type")).RibProfil=_profil
        if _nacagene==True :
            obj.addProperty("App::PropertyString","NacaProfil","NacaProfil",QtCore.QT_TRANSLATE_NOOP("App::Property","Naca Profil")).NacaProfil=_profil
        else :
            obj.addProperty("App::PropertyString","NacaProfil","NacaProfil",QtCore.QT_TRANSLATE_NOOP("App::Property","Naca Profil")).NacaProfil=""

        obj.addProperty("App::PropertyInteger","NacaNbrPoint","NacaProfil",QtCore.QT_TRANSLATE_NOOP("App::Property","Naca Number of Points")).NacaNbrPoint=_nacaNbrPoint
        obj.addProperty("App::PropertyBool","finite_TE","NacaProfil",QtCore.QT_TRANSLATE_NOOP("App::Property","Use a finite thickness at TE")).finite_TE=_finite_TE
        obj.addProperty("App::PropertyBool","useSpline","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","use Spline")).useSpline =_useSpline
        obj.addProperty("App::PropertyLength","Chord","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Chord")).Chord=_chord
        obj.addProperty("App::PropertyLength","Thickness","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Thickness")).Thickness=_thickness
        obj.addProperty("App::PropertyLength","xrot","Rib","chord").xrot=_xrot
        obj.addProperty("App::PropertyLength","yrot","Rib","chord").yrot=_yrot
        obj.addProperty("App::PropertyLength","zrot","Rib","chord").zrot=_zrot
        obj.Placement.Base.x=_x
        obj.Placement.Base.y=_y
        obj.Placement.Base.z=_z
        # List Geomtry to edit list of points
        obj.addProperty("App::PropertyVectorList","Coordinates","Rib","Vector list that defines the airfoil's geometry").Coordinates=[]
        #obj.setEditorMode("MyPropertyName", mode) #2 -- hidden

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        #FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        #   Do something when doing a recomputation, this method is mandatory


        FreeCAD.Console.PrintMessage("execute process\n")


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
        'fills the dialog with rib properties'
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

    def setEdit(self,vobj,mode):
        taskd = PlaneTaskPanel(vobj)
        FreeCADGui.Control.showDialog(taskd)
        
        # airPlaneDesignPlanedialog.ui
        
        
        return True


class CommandPlane:
    "the WingPanel command definition"
    def GetResources(self):
        return {'MenuText': "Create a Plane"}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","plane")
        ViewProviderPlane(a.ViewObject)
        
        

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignPlane',CommandPlane())
