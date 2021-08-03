#################################################
#
# Airfoil creation - Airplane Nacelle
#
# Copyright (c) C. Guth - 2021 - V0.4
#
# For FreeCAD Versions = or > 0.19 Revision xxxx
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

__title__="FreeCAD airPlane Nacelle"
__author__ = "C. Guth"
__url__ = "https://fredsfactory.fr"


import os, math
import FreeCAD, FreeCADGui, Part 
import libAeroShapes

from PySide import QtCore, QtGui, QtUiTools


# debug messages handling
debug= True;
def debugMsg(msg, always= False):
    if debug or always:
        FreeCAD.Console.PrintMessage(msg)     

# resources path, files
apWB_resources_path= os.path.join(os.path.dirname(__file__), 'resources')
apWB_icons_path= os.path.join(apWB_resources_path, 'icons')
apWB_icon_png= os.path.join(apWB_icons_path,'nacelle.png')
apWB_icon_xpm= os.path.join(apWB_icons_path,'nacelle.xpm')
apWB_ui_file= os.path.join( os.path.dirname(__file__), 'resources', 'nacelleTaskPanel.ui')
FreeCADGui.addLanguagePath(":/translations")


class Nacelle:
    def __init__(self, obj, _length, _diameter, _nType, _XMaxRel, _nbPoints, _useSpline = True):
        '''Nacelle properties'''
        obj.Proxy = self
        obj.addProperty("App::PropertyLength", "nacelleLength", "nacelle", QtCore.QT_TRANSLATE_NOOP("App::Property", "Length")).nacelleLength = _length
        obj.addProperty("App::PropertyLength", "nacelleDiameter", "nacelle", QtCore.QT_TRANSLATE_NOOP("App::Property", "Diameter")).nacelleDiameter = _diameter
        obj.addProperty("App::PropertyFloat", "nacelleXMaxRel", "nacelle", QtCore.QT_TRANSLATE_NOOP("App::Property", "Diameter")).nacelleXMaxRel = _XMaxRel
        obj.addProperty("App::PropertyString", "nacelleType", "nacelle", QtCore.QT_TRANSLATE_NOOP("App::Property", "Type")).nacelleType =  _nType
        obj.addProperty("App::PropertyBool","useSpline","nacelle",QtCore.QT_TRANSLATE_NOOP("App::Property","use Spline")).useSpline = _useSpline
        obj.addProperty("App::PropertyInteger","nbPoints","nacelle",QtCore.QT_TRANSLATE_NOOP("App::Property","Number of Points")).nbPoints = _nbPoints
 
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        debugMsg("Nacelle: change property  " + str(prop) + "\n")
        #self.execute(fp)

    def execute(self, fp):
        #   Do something when doing a recomputation, this method is mandatory
        debugMsg("Nacelle : execute process l= " + str(fp.nacelleLength) + "\n")

        # get coords
        if fp.nacelleType == "Lyon":
            coords= libAeroShapes.getLyonCoords(fp.nacelleLength, fp.nacelleDiameter, fp.nbPoints)
        else:
            if fp.nacelleType == "EllipseCos":
                coords= libAeroShapes.getHoernerCoords(fp.nacelleLength, fp.nacelleDiameter, fp.nacelleXMaxRel, fp.nbPoints)
            else:
                if fp.nacelleType == "Duhamel":
                    coords= libAeroShapes.getDuhamelCoords(fp.nacelleLength, fp.nacelleDiameter, fp.nbPoints)
                else:       #  fp.nacelleType = "NACA"
                    coords= libAeroShapes.getNACACoords(fp.nacelleLength, fp.nacelleDiameter, fp.nbPoints)
                   
        if fp.useSpline:
            spline = Part.BSplineCurve()
            spline.interpolate(coords)
            wire = Part.Wire([spline.toShape(), Part.makeLine(coords[0], coords[-1])])
        else:
            wire = Part.Wire([coords.toShape(), Part.makeLine(coords[0], coords[-1])])
        
        face = Part.Face(wire)
        fp.Shape = face
 		#fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(fp.Placement.Rotation.Axis.x,fp.Placement.Rotation.Axis.y,fp.Placement.Rotation.Axis.z),fp.Placement.Rotation.Angle))


class NacelleTaskPanel:
    '''A TaskPanel for the Nacelle'''
    def __init__(self, vobj):
        print("init NacelleTaskPanel")
        self.obj = vobj
        self.form = FreeCADGui.PySideUic.loadUi(apWB_ui_file)
        self.update(vobj)

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)

    def update(self, vobj):
        'fills the dialog with nacelle properties'
        print('update')
        self.form.sbLength.setValue(vobj.Object.nacelleLength)
        self.form.sDiameter.setValue(vobj.Object.nacelleDiameter)
        if vobj.Object.nacelleType == "Lyon":
            self.form.rbLyon.setChecked(True)
        else:
            if vobj.Object.nacelleType == "EllipseCos":
                self.form.rbLyon.setChecked(True)
            else:
                if vobj.Object.nacelleType == "Duhamel":
                    self.form.rbLyon.setChecked(True)
                else:       #  vobj.Object.nacelleType = "NACA"
                    self.form.rbLyon.setChecked(True)
        self.form.sbXMaxRel.setValue(vobj.Object.nacelleXMaxRel)
        #self.form.sbAngle.setValue(vobj.Object.nacelleLength)
        self.form.sbNbPoints.setValue(vobj.Object.nbPoints)
        self.form.cbSpline.setChecked(vobj.Object.useSpline)
 
    def accept(self):
        '''Update properties of nacelle'''
        print("accept")
        fp=self.obj.Object

        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def retranslateUi(self, TaskPanel):
        self.addButton.setText(QtGui.QApplication.translate("draft", "Update", None))
        print("")


class ViewProviderskNacelle:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.addProperty("App::PropertyColor","Color","nacelle","Color of the nacelle sketch").Color=(1.0,0.0,0.0)
        obj.Proxy = self

    def getDefaultDisplayMode(self):
        '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
        return "Flat Lines"

    def getIcon(self):
        '''Return the icon in XPM format which will appear in the tree view. This method is\
            optional and if not defined a default icon is shown.'''
        return apWB_icon_xpm

    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
            Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
            to return a tuple of all serializable objects or None.'''
        return None

    def __setstate__(self, state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
            Since no data were serialized nothing needs to be done here.'''
        return None

    def setEdit(self, vobj, mode):
         #nacelleTaskPanel.ui
        taskd = NacelleTaskPanel(vobj)
        FreeCADGui.Control.showDialog(taskd)
        return True

    def doubleClicked(self, vobj):
        taskd = NacelleTaskPanel(vobj)
        FreeCADGui.Control.showDialog(taskd)
        return(True)


class CommandNacelle:
    "the Nacelle command definition"

    def GetResources(self):
        return {'Pixmap': apWB_icon_png, 'MenuText': QtCore.QT_TRANSLATE_NOOP("Create_a_Nacelle","Create a nacelle")}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        loader=QtUiTools.QUiLoader()
        self.form=loader.load(apWB_ui_file)
        if not self.form.exec_():
            quit()
        
        doc= FreeCAD.ActiveDocument
        sk= doc.addObject("Part::FeaturePython","skNacelle")    # sketch
        nacelle= doc.addObject("Part::Revolution","Nacelle")    # volume
        nacelle.Source= sk
        nacelle.Axis = (1, 0, 0)
        nacelle.Base = (0, 0,  0)
        nacelle.Angle = self.form.sbAngle.value()
        nacelle.Solid = False
        nacelle.AxisLink = None
        nacelle.Symmetric = False

        XMaxRel= 0
        if self.form.rbLyon.isChecked():
            nType= "Lyon"
        else:
            if self.form.rbHoerner.isChecked():
                nType= "EllipseCos"
                XMaxRel= self.form.sbXMaxRel.value()
            else:
                if self.form.rbDuhamel.isChecked():
                    nType= "Duhamel"
                else:
                    nType= "NACA"
            
        Nacelle(sk, self.form.sbLength.value(), self.form.sbDiameter.value(), nType, XMaxRel, self.form.sbNbPoints.value(), self.form.cbSpline.isChecked())
        
        # display
        ViewProviderskNacelle(sk.ViewObject)
        sk.Visibility = False
        FreeCAD.ActiveDocument.recompute()


if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignNacelle', CommandNacelle())
