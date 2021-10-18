#***************************************************************************
#*                                                                         *
#*   AirPlaneDesign workbench                                              *
#*     For more details see InitGui.py and the LICENCE text file.          *
#*                                                                         *
#*   Module : apdWing.py                                                   *
#*   Generate a wing panel.                                                *
#*                                                                         *
#*   Dependencies :                                                        *
#*     - apdWingUI.py : handles the GUI.                                   *
#*     - apdRib.py : to generate rib.                                      *
#*                                                                         *
#*   History :                                                             *
#*     2021-10-11 : wing hierarchy Copyright (c) C. Guth - V0.4 refactor   *
#*     2020 : Initial release Copyright (c) F. Nivoix - 2020 - V0.4        *
#*                                                                         *
#***************************************************************************

__title__="FreeCAD Airplane Design"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"



import FreeCAD
import FreeCADGui
import Part
from PySide import QtCore
import math
import os
from apdRib import WingRib, ViewProviderWingRib
from apdWingUI import WingEditorPanel

debugWing= False

if open.__module__ in ['__builtin__','io']:
    pythonopen = open

# resources ui, icon
import apdWBCommon as wb
ui_file=  os.path.join(wb.resources_path, 'apdWing.ui')
icon_xpm= os.path.join(wb.icons_path,     'apdWing.xpm')

class ViewProviderWing:
    def __init__(self, vobj):
        vobj.Proxy = self

    def getIcon(self):
        return icon_xpm

    def attach(self, vobj):
        self.Object = vobj.Object

    def claimChildren(self):
        if self.Object:
            return self.Object.Panels

    def onDelete(self, feature, subelements):
        return True

    def onChanged(self, fp, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

class ViewProviderWingPanel:
    def __init__(self, vobj):
        vobj.Proxy = self
        self.Object = vobj.Object

    def getIcon(self):
        return os.path.join(wb.icons_path, 'apdWingPanel.xpm')

    def attach(self, vobj):
        self.Object = vobj.Object
        self.onChanged(vobj,"Base")

    def claimChildren(self):
        if self.Object:
            return [self.Object.TipRib] + [self.Object.RootRib]

    def onDelete(self, feature, subelements):
        return True

    def onChanged(self, fp, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

class WingSections:
    def __init__(self, obj, _rootRib ,_tipRib ,_rootChord=200,_tipChord=100,_panelLength=100,_tipTwist=0,_dihedral=0):
         # _parent,_NberOfPanel,_panelInput,_rootChord,_tipChord,_panelLength,_tipTwist,_dihedral):
        '''Add some custom properties to our box feature'''
        self.obj = obj
        obj.Proxy = self
        obj.addProperty("App::PropertyLink","RootRib","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Root Rib of the panel")).RootRib=_rootRib
        obj.addProperty("App::PropertyLink","TipRib","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Rib of the panel")).TipRib=_tipRib


        # leadingEdge : bord d'attaque
        obj.addProperty("App::PropertyLink","LeadingEdge","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Select the leading edge of the panal, line or Spline"))
        # trailing edge : bord de fuite
        obj.addProperty("App::PropertyLink","TrailingEdge","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Select the trailing edge of the panel, line or Spline"))

        obj.addProperty("App::PropertyLength","TipChord","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Chord")).TipChord=_tipChord
        obj.addProperty("App::PropertyLength","RootChord","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Root Chord")).RootChord=_rootChord

        obj.addProperty("App::PropertyLength","PanelLength","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Panel Length")).PanelLength=_panelLength
        obj.addProperty("App::PropertyAngle","TipTwist","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Twist")).TipTwist=_tipTwist
        obj.addProperty("App::PropertyAngle","Dihedral","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Dihedral")).Dihedral=_dihedral
        #obj.addProperty("App::PropertyLinkList","Ribs","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","list of ribs")).Ribs=[]

        obj.addProperty("App::PropertyBool","Solid","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Solid")).Solid=True #
        obj.addProperty("App::PropertyBool","Surface","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Surface")).Surface=False
        obj.addProperty("App::PropertyBool","Structure","Design",QtCore.QT_TRANSLATE_NOOP("App::Property","Surface")).Structure=False

        #ribs=[]
        #ribs.append(obj.RootRib)
        #ribs.append(obj.TipRib)
        #FreeCAD.ActiveDocument.recompute()


    def onChanged(self, obj, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, obj):
        '''Do something when doing a recomputation, this method is mandatory'''
        if not obj.Structure :
           if obj.RootRib :

           #obj.RootRib.Placement.Rotation.Axis.x=1
           #obj.RootRib.Placement.Rotation.Axis.y=0
           #obj.RootRib.Placement.Rotation.Axis.z=0
           #obj.RootRib.Placement.Rotation.Angle=obj.Dihedral

           #obj.TipRib.Placement.Rotation.Axis.x=1
           #obj.TipRib.Placement.Rotation.Axis.y=0
           #obj.TipRib.Placement.Rotation.Axis.z=0
           #obj.TipRib.Placement.Rotation.Angle=obj.Dihedral

              obj.TipRib.Placement.Base.y= obj.PanelLength
              #obj.TipRib.Placement.Base.z= obj.PanelLength*math.tan(obj.Dihedral)

              ribsWires=[]
              ribsWires.append(obj.RootRib.Shape.OuterWire)
              ribsWires.append(obj.TipRib.Shape.OuterWire)
              obj.RootRib.ViewObject.hide()
              obj.TipRib.ViewObject.hide()
              obj.Shape=Part.makeLoft(ribsWires,obj.Solid,False)
           else :
              wb.debugMsg("Wing Panel : strucutre, not implemented yet")
        #FreeCAD.ActiveDocument.recompute()
        FreeCAD.Console.PrintMessage("Recompute Python Wing feature\n")

class CommandWing:
    "the WingPanel command definition"
    def GetResources(self):
         return {'Pixmap': icon_xpm, 'MenuText': wb.translate("apdWing", "Create a wing")}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        wb.debugMsg("-----------------Wing Wizard-----------------", debugWing)

        editor = WingEditorPanel()
        editor.setupUi()
        if not editor.form.exec_():
            exit()

        wing = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", "Wing")
        wing.addProperty("App::PropertyLinkList","Panels","Panels",QtCore.QT_TRANSLATE_NOOP("App::Property","Panels of the wing")).Panels= []
        ViewProviderWing(wing.ViewObject)

        panelTable= editor.form.PanelTable
        _ribs=[]
        _position=0
        for i in range(panelTable.rowCount()) :
            profil=panelTable.item(i, 2).text()
            chord_root= float(panelTable.item(i, 3).text())
            chord_tip= float(panelTable.item(i, 4).text())
            panelLength=float(panelTable.item(i, 5).text())
            x_root=float(panelTable.item(i, 6).text())
            x_tip=float(panelTable.item(i, 7).text())
            z_root=float(panelTable.item(i, 8).text())
            z_tip=float(panelTable.item(i, 9).text())

            # Add Rib Root
            _ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibRoot_"+str(i)))
            WingRib(_ribs[i*2], profil, False,0, chord_root, x_root, _position, z_root)
            ViewProviderWingRib(_ribs[i*2].ViewObject)

            # Add Rib tip
            _position=_position+panelLength
            _ribs.append(FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibTip_"+str(i)))
            WingRib(_ribs[i*2+1], profil ,False,0, chord_tip, x_tip, _position, z_tip)
            ViewProviderWingRib(_ribs[i*2+1].ViewObject)

            # Add wing panel
            obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","WingPanel")
            WingSections(obj, _ribs[i*2], _ribs[i*2+1], chord_root, chord_tip, _position)
            ViewProviderWingPanel(obj.ViewObject)
           
            # add to Wing
            wing.Panels= wing.Panels + [obj]

        FreeCAD.ActiveDocument.recompute()

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('apdWing',CommandWing())
