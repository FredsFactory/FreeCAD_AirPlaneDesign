#################################################
#
# Airfoil creation - Aircraft
# 
# Copyright (c) F. Nivoix - 2019 - V0.1
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

__title__="FreeCAD Airplane Design"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"


import FreeCAD, FreeCADGui, Part, os
from FreeCAD import Units
from PySide import QtCore
from PySide import QtGui
#from airPlaneRib import WingRib, ViewProviderWingRib
#from airPlaneWingUI import WingEditorPanel
#from FreeCAD import Vector
#import Part, Draft 
#from importlib import reload
#import math
#from airPlaneWPanel import WingPanel 

smWB_icons_path =  os.path.join( os.path.dirname(__file__), 'resources', 'icons')

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)

#################################################
#  This module provides tools to build a
#  wing panel
#################################################
if open.__module__ in ['__builtin__','io']:
    pythonopen = open

_wingRibProfilDir=FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/wingribprofil'

class Wing:
    def __init__(self, obj, _wPanels):
         # _parent,_NberOfPanel,_panelInput,_rootChord,_tipChord,_panelLength,_tipTwist,_dihedral):
        '''Add some custom properties to our box feature'''
        self.obj = obj
        obj.Proxy = self
        
        obj.addProperty("App::PropertyLinkList","WingPanels","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","panel")).WingPanels=_wPanels
        obj.addProperty("App::PropertyLength","WingLength","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","Panel Length"))
        obj.addProperty("App::PropertyLength","WingRootChoord","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","Wing Tip Choord"))        
        obj.addProperty("App::PropertyLength","WingTipChoord","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","Wing Tip Choord")) 
        obj.addProperty("App::PropertyBool","Solid","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","Solid")).Solid=True # 
        obj.addProperty("App::PropertyBool","Surface","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","Surface")).Surface=False
        obj.addProperty("App::PropertyBool","Structure","Wing",QtCore.QT_TRANSLATE_NOOP("App::Property","Surface")).Structure=False        
        #FreeCAD.ActiveDocument.recompute()

    def getWingLength(self, obj):
        wlength=Units.Quantity(0.0,1)  # create a quantity Length 0.0 mm
        for panel in obj.WingPanels :
            wlength=wlength+(panel.PanelLength)   
        obj.WingLength= wlength
 
    def getRootChoord(self, obj):
        # return the Root Choord of the Wing 
        print(obj.WingPanels[0].RootRib)
        obj.WingRootChoord=obj.WingPanels[0].RootRib
         
    def getTipChoord(self, obj):
        # return the Tip Choord of the Wing 
        for panel in obj.WingPanels :
            tipRib=panel.TipRib 
        obj.WingTipChoord=tipRib
        
    def onChanged(self, obj, prop):
        '''Do something when a property has changed'''        
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        
    def execute(self, obj):
        '''Do something when doing a recomputation, this method is mandatory'''
        panelShape=[]
        for panel in obj.WingPanels :
            panelShape.append(panel.Shape)
        if obj.WingPanels :
         obj.Shape=Part.makeCompound(panelShape)
        self.getWingLength(obj)
        #self.getRootChoord(obj)
        #self.getTipChoord(obj)
        
        FreeCAD.Console.PrintMessage("Recompute Python Wing feature\n")
    
class WingTaskPanel: 
    '''A TaskPanel for the Rib'''
    def __init__(self,vobj): 
        self.obj = vobj
        path_to_ui = FreeCAD.getUserAppDataDir()+ 'Mod/AirPlaneDesign/resources/airPlaneWpanelTask.ui'  
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        self.update(vobj)

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)

    def update(self,vobj):
        'fills the dialog with wing properties'
        self.form.name.setText(vobj.Object.Label)
        self.form.wingLength.setValue(vobj.Object.WingLength)
        self.form.wingRootChoord.setValue(vobj.Object.WingRootChoord)
        
        initPanelTable = [
             ["1","Eppler207",_wingRibProfilDir+u"/naca/naca2412.dat","250","222","122","0","0","0.0","-54.","0","0","22"],
             ["2","Eppler207",_wingRibProfilDir+u"/naca/naca2412.dat","222","196","35.","0","0","-54","-54","0","54","0"],
             ["3","Eppler205",_wingRibProfilDir+u"/naca/naca2412.dat","196","146","456","0","0","-54","12","0","0","81"],
             ["4","Eppler205",_wingRibProfilDir+u"/naca/naca2412.dat","146","100","10","0","0.","12","12","12","0","0"],
             ["5","Eppler205",_wingRibProfilDir+u"/naca/naca2412.dat","100","100","10","0","0.","12","12","0","0","0"]
                         ]
        #self.form.PanelTable.setRowCount(0)
        for row_number,row_data in enumerate(initPanelTable):
            self.form.trapezeList.insertRow(row_number)
            for col_number, data in enumerate(row_data):
               self.form.trapezeList.setItem(row_number,col_number,QtGui.QTableWidgetItem(str(data)))#,QtGui.QTableWidgetItem(str(data)))
               
    def addLine(self):
        initPanelTable = [
             ["-","-","","","","","","",""],]
        for row_number,row_data in enumerate(initPanelTable):
            self.form.trapezeList.insertRow(row_number)
            for col_number, data in enumerate(row_data):
               self.form.trapezeList.setItem(row_number,col_number,QtGui.QTableWidgetItem(str(data)))#,QtGui.QTableWidgetItem(str(data)))   
                          
    def delLine(self):
        self.form.trapezeList.removeRow(self.form.PanelTable.currentRow())
    
    def accept(self):
        '''Update properties of wing'''
        print("accept")

    def retranslateUi(self, TaskPanel):
        #TaskPanel.setWindowTitle(QtGui.QApplication.translate("draft", "Faces", None))
        self.addButton.setText(QtGui.QApplication.translate("draft", "Update", None))
        self.form.tpzControllerAdd.clicked.connect(self.addLine)
        self.form.tpzControllerDelete.clicked.connect(self.delLine)

class ViewProviderWing:
    def __init__(self, vobj):
        vobj.Proxy = self
        self.Object = vobj.Object
        
    def getIcon(self):    
        return os.path.join(smWB_icons_path,'wing2.xpm')

    def attach(self, vobj):
        self.Object = vobj.Object
        self.onChanged(vobj,"Base")

    def claimChildren(self):
        return self.Object.WingPanels
        
    def onDelete(self, feature, subelements):
        return True
    
    def onChanged(self, fp, prop):
        pass
        
    def __getstate__(self):
        return None
 
    def __setstate__(self,state):
        return None
    
    def setEdit(self,vobj,mode):       
        taskd = WingTaskPanel(vobj)
        FreeCADGui.Control.showDialog(taskd)
        return True

class CommandWing:
    "the Wing command definition"
    def GetResources(self):
        iconpath = os.path.join(smWB_icons_path,'wing2.png')
        return {'Pixmap': iconpath, 'MenuText': QtCore.QT_TRANSLATE_NOOP("Create_a_wing","Create/Add a wing to plane, select a plane and clic")}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):
        print("-----------------Wing-----------------")     
        selection = FreeCADGui.Selection.getSelectionEx()
        if selection :
           base = FreeCAD.ActiveDocument.getObject((selection[0].ObjectName))

        _wPanels=[]
          
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Wing")
        Wing(obj,_wPanels)
        ViewProviderWing(obj.ViewObject)
        #FreeCAD.ActiveDocument.recompute()
        b=[]
        if selection : #selection==None :
           if not base.Wings :
              base.Wings=obj
           else : 
              b=base.Wings
              b.append(obj)
              base.Wings=b
              
        if selection :  #selection ==None:   
           if not base.Group :
              base.Group=obj
           else : 
              b=base.Group
              b.append(obj)
              base.Group=b
           
        FreeCAD.ActiveDocument.recompute()      
        FreeCAD.Gui.activeDocument().activeView().viewAxonometric()
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")

 
if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignWing',CommandWing())
