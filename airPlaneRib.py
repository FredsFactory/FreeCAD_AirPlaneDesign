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


import FreeCAD,FreeCADGui

from PySide import QtCore
from PySide import QtGui
from airPlaneAirFoil import process,decodeName
from airPlaneDesingProfilUI import SelectObjectUI
from airPlaneAirFoilNaca import generateNaca

FreeCADGui.addLanguagePath(":/translations")

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)


class WingRib:
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
        if fp.NacaProfil =="" :
             FreeCAD.Console.PrintMessage("Create Rib Start\n")
             name=decodeName(fp.RibProfil)
             FreeCAD.Console.PrintMessage(name)
              # process(doc,filename,
              #         scale,
              #         posX,posY,posZ,
              #         rotX,rotY,rotZ,
              #         thickness,
              #         useSpline = False,coords=[]):
             fp.Shape,fp.Coordinates=process(FreeCAD.ActiveDocument.Name,fp.RibProfil,
                                   fp.Chord,
                                   fp.Placement.Base.x,fp.Placement.Base.y,fp.Placement.Base.z,
                                   fp.xrot,fp.yrot,fp.zrot,
                                   0,
                                   fp.useSpline,fp.Coordinates)
        else :
             fp.Shape,fp.Coordinates=generateNaca(fp.NacaProfil, fp.NacaNbrPoint, fp.finite_TE, True,fp.Chord,fp.Placement.Base.x,fp.Placement.Base.y,fp.Placement.Base.z,fp.xrot,fp.yrot,fp.zrot,fp.useSpline,fp.Coordinates)

        if fp.Thickness != 0 :
            fp.Shape = fp.Shape.extrude(FreeCAD.Base.Vector(0,fp.Thickness,0))

        FreeCAD.Console.PrintMessage("Create Rib End\n")


class RibTaskPanel: 
    '''A TaskPanel for the Rib'''
    def __init__(self,vobj): 
        print("init RibTaskPanel")
        self.obj = vobj
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/ribTaskPanel.ui'  
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        self.update(vobj)

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
        print("accept")
        fp=self.obj.Object
        fp.Thickness=self.form.thickness.value()
        fp.Chord=self.form.chord.value()
        fp.useSpline=self.form.kingOfLines.isChecked()
        
        
        
        
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def retranslateUi(self, TaskPanel):
        #TaskPanel.setWindowTitle(QtGui.QApplication.translate("draft", "Faces", None))
        #self.addButton.setText(QtGui.QApplication.translate("draft", "Update", None))
        print("")


class ViewProviderWingRib:
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
        #print("setEdit start")
        taskd = RibTaskPanel(vobj)
        #taskd.obj = vobj.Object
        #taskd.update()
        #self.Object.ViewObject.Visibility=False
        #self.Object.baseObject[0].ViewObject.Visibility=True
        FreeCADGui.Control.showDialog(taskd)
        return True


class CommandWingRib:
    "the WingPanel command definition"
    def GetResources(self):
        return {'MenuText': "Create a Rib"}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):
        editor = SelectObjectUI()
        editor.setupUi()
        r = editor.form.exec_()
        if r:
            #r=1 => OK
            #print("corde : /n")
            #print (editor.form.NACANumber.text())

            if editor.form.NACANumber.text()=="" :
                b=editor.profilSelectedFilePath()
                a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wrib")
                WingRib(a,b,False,0,editor.form.chord.value(),0,0,0,0,0,0,editor.form.thickness.value(),editor.form.kingOfLines.isChecked())
                ViewProviderWingRib(a.ViewObject)
            else :
                print("Naca : ")
                print( editor.form.NACANumber)
                b=editor.form.NACANumber
                a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wrib")
                WingRib(a,b.text(),True,int(editor.form.nacaNbrPoint.value()),editor.form.chord.value(),0,0,0,0,0,0,editor.form.thickness.value(),editor.form.kingOfLines.isChecked(),editor.form.finite_TE.isChecked())
                ViewProviderWingRib(a.ViewObject)
            FreeCAD.ActiveDocument.recompute()
        else :
            print("Canceled")

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesingWRib',CommandWingRib())
