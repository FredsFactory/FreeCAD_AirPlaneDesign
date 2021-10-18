#***************************************************************************
#*                                                                         *
#*   AirPlaneDesign workbench                                              *
#*     For more details see InitGui.py and the LICENCE text file.          *
#*                                                                         *
#*   Module : apdPlane.py                                                  *
#*   Generate a plane.                                                     *
#*                                                                         *
#*   History :                                                             *
#*     2019 : Initial release Copyright (c) F. Nivoix - 2019 - V0.4        *
#*                                                                         *
#***************************************************************************


__title__="FreeCAD airPlane Plane"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"


import FreeCAD,FreeCADGui, os

from PySide import QtCore
from PySide import QtGui

debugWingUI= False

# resources ui, icon
import apdWBCommon as wb
ui_file= os.path.join(wb.resources_path, 'apdPlane.ui')
icon_xpm= os.path.join(wb.icons_path, 'apdPlane.xpm')


class Plane:
    def __init__(self, obj):
        '''Rib properties'''
        obj.Proxy = self
        obj.addProperty("App::PropertyLength", "fuselageLength", "fuselage", QtCore.QT_TRANSLATE_NOOP("App::Property", "Fuselage Length"))
        obj.addProperty("App::PropertyLength", "fuselageHeigth", "fuselage", QtCore.QT_TRANSLATE_NOOP("App::Property", "Fuselage Heigth"))
        obj.addProperty("App::PropertyLength", "fuselageWidth", "fuselage", QtCore.QT_TRANSLATE_NOOP("App::Property", "Fuselage Width"))


        obj.addProperty("App::PropertyFile", "_3viewsFile", "fuselage", QtCore.QT_TRANSLATE_NOOP("App::Property", "3 Views file"))

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
        wb.debugMsg("init RibTaskPanel", debugWingUI)
        self.obj = vobj
        self.form = FreeCADGui.PySideUic.loadUi(ui_file)
        self.update(vobj)

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)


    def update(self,vobj):
        'fills the dialog with plane properties'
        wb.debugMsg('update', debugWingUI)
        self.form.fuselageLength.setValue(vobj.Object.fuselageLength)
        self.form.fuselageHeigth.setValue(vobj.Object.fuselageHeigth)
        self.form.fuselageWidth.setValue(vobj.Object.fuselageWidth)
        #self.form.fileName.setText(vobj.Object.RibProfil)
        #self.form.NACANumber.setText(vobj.Object.NacaProfil)
        #self.form.nacaNbrPoint.setValue(vobj.Object.NacaNbrPoint)
        #self.form.finite_TE.setChecked(vobj.Object.finite_TE)

    def accept(self):
        '''Update properties of Rib'''
        wb.debugMsg("accept", debugWingUI)
        fp=self.obj.Object
        fp.fuselageLength=self.form.fuselageLength.value()
        fp.fuselageHeigth=self.form.fuselageHeigth.value()
        fp.fuselageWidth=self.form.fuselageWidth.value()

        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def retranslateUi(self, TaskPanel):
        self.addButton.setText(wb.translate("draft", "Update", None))
        wb.debugMsg("retranslate", debugWingUI)


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
        return icon_xpm

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

    def doubleClicked(self,vobj):
        taskd = PlaneTaskPanel(vobj)
        FreeCADGui.Control.showDialog(taskd)
        return(True)


class CommandPlane:
    "the WingPanel command definition"

    def GetResources(self):
        return {'Pixmap': icon_xpm, 'MenuText': wb.translate("Plane","Create a plane")}

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
    FreeCADGui.addCommand('apdPlane', CommandPlane())
