#***************************************************************************
#*                                                                         *
#*   AirPlaneDesign workbench                                              *
#*     For more details see InitGui.py and the LICENCE text file.          *       
#*                                                                         *
#*   Module : apdNacelle.py                                                *
#*   Generate a nacelle volume.                                            *
#*     - optinal shapes : Hoerner, Lyon, Duhamel, NACA.                    *
#*     - 0° to 360° volume.                                                *
#*                                                                         *
#*   Dependencies :                                                        *
#*     - apdNacelle.py : GUI.                                              *
#*     - apdLibShapes : profils coordinates generation                     *
#*                                                                         *
#*   History :                                                             *
#*     2021-10-11 : correction Naca                                        *
#*     2021-07-11 : Initial release for v 0.5 tested on FreeCAD 0.19       *
#*                                                                         *
#***************************************************************************
''' @package apdNacelle
    Produces a nacelle volume.
 
    Optional shapes : Hoerner, Lyon, Duhamel, NACA.
'''
__title__="FreeCAD airPlaneDesign Nacelle"
__author__ = "Claude GUTH"
__url__ = "https://github.com/FredsFactory/FreeCAD_AirPlaneDesign"


import FreeCAD, FreeCADGui, Part 
import os, math
from PySide import QtCore, QtGui, QtUiTools
import apdLibShapes

debugNacelle= False

# resources ui, icon
import apdWBCommon as wb
ui_file=  os.path.join(wb.resources_path, 'apdNacelle.ui')
icon_xpm= os.path.join(wb.icons_path,     'apdNacelle.xpm')


class Nacelle:
    ''' Nacelle class'''
    def __init__(self, obj, _length, _diameter, _nType, _XMaxRel, _nbPoints, _useSpline = True):
        '''Nacelle properties'''
        obj.Proxy = self
        obj.addProperty("App::PropertyLength", "nacelleLength", "nacelle", QtCore.QT_TRANSLATE_NOOP("App::Property", "Length")).nacelleLength = _length
        obj.addProperty("App::PropertyLength", "nacelleDiameter", "nacelle", QtCore.QT_TRANSLATE_NOOP("App::Property", "Diameter")).nacelleDiameter = _diameter
        obj.addProperty("App::PropertyFloat", "nacelleXMaxRel", "nacelle", QtCore.QT_TRANSLATE_NOOP("App::Property", "X_max relative")).nacelleXMaxRel = _XMaxRel
        obj.addProperty("App::PropertyString", "nacelleNacaNb", "nacelle", QtCore.QT_TRANSLATE_NOOP("App::Property", "NACA nb")).nacelleNacaNb = '00'+format(int(100*_diameter/_length), '02')
        obj.addProperty("App::PropertyString", "nacelleType", "nacelle", QtCore.QT_TRANSLATE_NOOP("App::Property", "Type")).nacelleType =  _nType
        obj.addProperty("App::PropertyBool","useSpline","nacelle",QtCore.QT_TRANSLATE_NOOP("App::Property","Use spline")).useSpline = _useSpline
        obj.addProperty("App::PropertyInteger","nbPoints","nacelle",QtCore.QT_TRANSLATE_NOOP("App::Property","Number of points")).nbPoints = _nbPoints
 
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        wb.debugMsg("Nacelle: change property  " + str(prop) + "\n", debugNacelle)
        #self.execute(fp)

    def execute(self, fp):
        #   Do something when doing a recomputation, this method is mandatory
        wb.debugMsg("Nacelle : execute process l= " + str(fp.nacelleLength) + "\n", debugNacelle)

        # get coords
        if fp.nacelleType == "Lyon":
            coords= apdLibShapes.getLyonCoords(fp.nacelleLength, fp.nacelleDiameter, fp.nbPoints)
        else:
            if fp.nacelleType == "EllipseCos":
                coords= apdLibShapes.getHoernerCoords(fp.nacelleLength, fp.nacelleDiameter, fp.nacelleXMaxRel, fp.nbPoints)
            else:
                if fp.nacelleType == "Duhamel":
                    coords= apdLibShapes.getDuhamelCoords(fp.nacelleLength, fp.nacelleDiameter, fp.nbPoints)
                else:       #  fp.nacelleType = "NACA"
                    coords= apdLibShapes.getNACACoords(fp.nacelleLength, fp.nacelleDiameter, fp.nbPoints)
                   
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
        wb.debugMsg("init Nacelle task panel", debugNacelle)
        self.obj = vobj
        self.form = FreeCADGui.PySideUic.loadUi(ui_file)
        self.update(vobj)

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)

    def update(self, vobj):
        'fills the dialog with nacelle properties'
        wb.debugMsg('update', debugNacelle)
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
        wb.debugMsg("accept", debugNacelle)
        fp=self.obj.Object

        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def retranslateUi(self, TaskPanel):
        self.addButton.setText(wb.translate("draft", "Update", None))


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
        return icon_xpm

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
        return {'Pixmap': icon_xpm, 'MenuText': wb.translate("Create_a_Nacelle","Create a nacelle")}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        loader=QtUiTools.QUiLoader()
        self.form=loader.load(ui_file)
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
    FreeCADGui.addCommand('apdNacelle', CommandNacelle())
