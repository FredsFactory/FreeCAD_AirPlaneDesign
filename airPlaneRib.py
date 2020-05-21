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

__title__="FreeCAD airPlaneRib"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"


import FreeCAD,FreeCADGui,os,math

from PySide import QtCore
from PySide import QtGui
from airPlaneAirFoil import process
from airPlaneDesignProfilUI import SelectObjectUI
from airPlaneAirFoilNaca import generateNaca

import numpy as np


from App.xfoil.xfoil import XFoil
from App.xfoil.model import Airfoil

from App.xfoil.test import naca0012

import freecad.plot.Plot as Plot


FreeCADGui.addLanguagePath(":/translations")
smWB_icons_path =  os.path.join( os.path.dirname(__file__), 'resources', 'icons')

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)


class WingRib:
    def __init__(self, obj,_profil,_nacagene,_nacaNbrPoint,_chord,_x,_y,_z,_xrot,_yrot,_zrot,_rot=0,_thickness=0,_useSpline = True,_finite_TE = False,_splitSpline = False):
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
        obj.addProperty("App::PropertyBool","splitSpline","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","split spline in lower and upper side")).splitSpline=_splitSpline
        obj.addProperty("App::PropertyLength","Chord","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Chord")).Chord=_chord
        obj.addProperty("App::PropertyLength","Thickness","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Thickness")).Thickness=_thickness
        obj.addProperty("App::PropertyLength","wingkey","Rib",QtCore.QT_TRANSLATE_NOOP("App::Property","Wing Key"))

        obj.Placement=FreeCAD.Placement(FreeCAD.Vector(_x,_y,_z), FreeCAD.Rotation(FreeCAD.Vector(_xrot,_yrot,_zrot),_rot))#, FreeCAD.Vector(0,0,0))

        # List Geomtry to edit list of points
        obj.addProperty("App::PropertyVectorList","Coordinates","Rib","Vector list that defines the airfoil's geometry").Coordinates=[]

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        if (str(prop) == "RibProfil") and (fp.PropertiesList.__contains__("Coordinates")):
            print("Rib onChanged:")
            fp.Coordinates=[]
        if (str(prop)=="wingkey"):
            print("Clef d'aile")

    def execute(self, fp):
        #   Do something when doing a recomputation, this method is mandatory
        #print("--------  Rib execute  --------")

        if fp.NacaProfil =="" :
            face, fp.Coordinates=process(fp.RibProfil,
                                         fp.Chord,
                                         fp.Placement.Base.x,fp.Placement.Base.y,fp.Placement.Base.z,
                                         fp.Placement.Rotation.Axis.x,fp.Placement.Rotation.Axis.y,fp.Placement.Rotation.Axis.z,
                                         math.degrees(fp.Placement.Rotation.Angle),
                                         fp.useSpline,fp.splitSpline,fp.Coordinates)
        else :
            face, fp.Coordinates=generateNaca(fp.NacaProfil, fp.NacaNbrPoint, fp.finite_TE,True,
                                    fp.Chord,fp.Placement.Base.x,fp.Placement.Base.y,fp.Placement.Base.z,
                                    fp.Placement.Rotation.Axis.x,fp.Placement.Rotation.Axis.y,fp.Placement.Rotation.Axis.z,
                                    math.degrees(fp.Placement.Rotation.Angle),
                                    fp.useSpline,fp.splitSpline)
        #FreeCAD.Console.PrintMessage("After Rib generation\n")
        #Xfoil
        fp.Placement=FreeCAD.Placement(FreeCAD.Vector(fp.Placement.Base.x,fp.Placement.Base.y,fp.Placement.Base.z), FreeCAD.Rotation(FreeCAD.Vector(fp.Placement.Rotation.Axis.x,fp.Placement.Rotation.Axis.y,fp.Placement.Rotation.Axis.z),math.degrees(fp.Placement.Rotation.Angle)))#, FreeCAD.Vector(0,0,0))
        if fp.Thickness != 0 :
            fp.Shape = face.extrude(FreeCAD.Vector(0,fp.Thickness,0))
        else:
            #fp.Shape = Part.Face(Part.Wire(fp.Coordinates))
            fp.Shape = face
        #fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(fp.Placement.Rotation.Axis.x,fp.Placement.Rotation.Axis.y,fp.Placement.Rotation.Axis.z),fp.Placement.Rotation.Angle))


class RibTaskPanel:
    '''A TaskPanel for the Rib'''
    def __init__(self,vobj):
        self.obj = vobj
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/ribTaskPanel.ui'
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        self.update(vobj)
        self.form.xfoilSimulation.clicked.connect(self.xfoilSimulation)

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)

    def updateGraphicsViewRib(self):
        #coords=_coords
        fp=self.obj.Object
        coords=fp.Coordinates

        for row_number,row_data in enumerate(coords):
            self.form.profilTable.insertRow(row_number)
            for col_number, data in enumerate(row_data):
               self.form.profilTable.setItem(row_number,col_number,QtGui.QTableWidgetItem(str(data)))

        scale=self.form.chord.value()*2
        scene=QtGui.QGraphicsScene()
        self.form.ribView.setScene(scene)

        points=[]
        first_v = None
        last_v = None
        for v in coords:
                 if first_v is None:
                     first_v = v
            # End of if first_v is None
            # Line between v and last_v if they're not equal
                 if (last_v != None) and (last_v != v):
                     points.append(QtCore.QPointF(last_v.x*scale,-last_v.z*scale ))
                     points.append(QtCore.QPointF(v.x*scale,-v.z*scale ))
            # End of if (last_v != None) and (last_v != v)
            # The new last_v
                 last_v = v

        # End of for v in upper
        # close the wire if needed
        if last_v != first_v:
                     points.append(QtCore.QPointF(last_v.x*scale,-last_v.z*scale ))
                     points.append(QtCore.QPointF(first_v.x*scale,-first_v.z*scale ))
        item=QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(points))
        item.setPen(QtGui.QPen(QtCore.Qt.blue))
        scene.addItem(item)
        self.form.ribView.setFocus()
        self.form.ribView.show()
        return


    def update(self,vobj):
        'fills the dialog with rib properties'

        self.form.thickness.setValue(vobj.Object.Thickness)
        self.form.chord.setValue(vobj.Object.Chord)
        self.form.kingOfLines.setChecked(vobj.Object.useSpline)

        self.form.fileName.setText(vobj.Object.RibProfil)

        self.form.NACANumber.setText(vobj.Object.NacaProfil)
        self.form.nacaNbrPoint.setValue(vobj.Object.NacaNbrPoint)
        self.form.finite_TE.setChecked(vobj.Object.finite_TE)

        for row_number,row_data in enumerate(vobj.Object.Coordinates):
            self.form.profilTable.insertRow(row_number)
            for col_number, data in enumerate(row_data):
               self.form.profilTable.setItem(row_number,col_number,QtGui.QTableWidgetItem(str(data)))
        self.updateGraphicsViewRib()

    def accept(self):
        '''Update properties of Rib'''
        print("Update properties of Rib")
        fp=self.obj.Object
        fp.Thickness=self.form.thickness.value()
        fp.Chord=self.form.chord.value()
        fp.useSpline=self.form.kingOfLines.isChecked()

        print("-bug-------------------------------")
        fp.RibProfil=self.form.fileName.text()
        print(self.form.fileName.text())
        print("-bug-------------------------------")

        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def xfoilSimulation(self):
        #naca0012 = Airfoil(x=np.array(),y=np.array)
        xx=[]
        yy=[]
        for vect in self.obj.Object.Coordinates:
            xx.append(vect[0])
            yy.append(vect[2])

        xf = XFoil()
        xf.airfoil  = Airfoil(np.array(xx),np.array(yy))#naca0012#

        xf.max_iter = 40
        # Cl=Cz coefficients de portance
        # Cd =Cx coefficients de trainée
        # Cm coefficients de moment
        for i in [100000,200000,500000]:
            xf.Re = i#1000000
            #a, cl, cd, cm, cp = xf.aseq(-20, 20, 0.5)#xf.cseq(-0.5, 0.5, 0.05)#

            cl, cd, cm, cp=xf.a(0)

            print("a")
            #print(a)
            print("cl")
            print(cl)
        # trainée / portance
            #Plot.plot(cm,a)
            #Plot.plot(cl,a)
            #Plot.plot(cd,a)
            Plot.plot(cl,cd)
            #Plot.plot(xx,yy)


            #Plot.plot(xx,yy)
            #Plot.plot(a,cm)

        #Plot.plot(a,cl)
       # Plot.plot(a,cd)
       # Plot.plot(a,cm)
       # Plot.plot(a,cp)
        #Plot.plot(a,cm)
        #Plot.plot(a,cd)
        #Plot.plot(a,cl)
       # print(a)
        print(cl)
        print("Profil")
        print(naca0012)

    def retranslateUi(self, TaskPanel):
        #TaskPanel.setWindowTitle(QtGui.QApplication.translate("draft", "Faces", None))
        self.addButton.setText(QtGui.QApplication.translate("draft", "Update", None))


class ViewProviderWingRib:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self

    def getDefaultDisplayMode(self):
        '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
        return "Flat Lines"

    def getIcon(self):
        '''Return the icon in XPM format which will appear in the tree view. This method is\
            optional and if not defined a default icon is shown.'''
        return os.path.join(smWB_icons_path,'rib.xpm')

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
        taskd = RibTaskPanel(vobj)
        FreeCADGui.Control.showDialog(taskd)
        return True

class CommandWingRib:
    "the WingPanel command definition"
    def GetResources(self):
        iconpath = os.path.join(smWB_icons_path,'rib.svg')
        return {'Pixmap': iconpath, 'MenuText': QtCore.QT_TRANSLATE_NOOP("Create_a_Rib","Create a Rib")}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        editor = SelectObjectUI()
        editor.setupUi()
        r = editor.form.exec_()
        if r:
            if editor.form.NACANumber.text()=="" :
                b=editor.filePath
                a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wrib")
                WingRib(a,b,False,0,editor.form.chord.value(),0,0,0,1,0,0,0,editor.form.thickness.value(),editor.form.useSpline.isChecked(),_splitSpline=editor.form.splitSpline.isChecked())
                ViewProviderWingRib(a.ViewObject)
            else :
                b=editor.form.NACANumber
                a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wrib")
                WingRib(a,b.text(),True,int(editor.form.nacaNbrPoint.value()),editor.form.chord.value(),0,0,0,1,0,0,0,editor.form.thickness.value(),editor.form.useSpline.isChecked(),editor.form.finite_TE.isChecked(),editor.form.splitSpline.isChecked())
                ViewProviderWingRib(a.ViewObject)
            FreeCAD.ActiveDocument.recompute()
        else :
            FreeCAD.Console.PrintMessage("Rib creation canceled")

if FreeCAD.GuiUp:
    #Register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignWRib',CommandWingRib())
