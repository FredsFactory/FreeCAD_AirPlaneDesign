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

__title__="FreeCAD Arch Stairs"
__author__ = "F. Nivoix"
__url__ = "https://fredsfactory.fr"

import os,FreeCAD,FreeCADGui
from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
from pivy import coin
from FreeCAD import Vector, Base
from Draft import makeWire

import re, FreeCAD, FreeCADGui, Draft, Part, PartDesign,PartDesignGui,Sketcher,cProfile, os, string
import importAirfoilDAT



#################################################
#  This module provides tools to build a
#  wing panel
#################################################
if open.__module__ in ['__builtin__','io']:
    pythonopen = open

useDraftWire = False #True

def decodeName(name):
    "decodes encoded strings"
    try:
        decodedName = name
    except UnicodeDecodeError:
        try:
            decodedName = (name.decode("latin1"))
        except UnicodeDecodeError:
            try:
                decodedName = (name.decode("utf8"))
            except UnicodeDecodeError:
                print("AirfoilDAT: error: couldn't determine character encoding")
                decodedName = name
    return decodedName

def open(filename):
    "called when freecad opens a file"
    docname = os.path.splitext(os.path.basename(filename))[0]
    doc = FreeCAD.newDocument(docname)
    doc.Label = decodeName(docname[:-4])
    process(doc,filename)

def insert(filename,docname):
    "called when freecad imports a file"
    groupname = os.path.splitext(os.path.basename(filename))[0]
    try:
        doc=FreeCAD.getDocument(docname)
    except NameError:
        doc=FreeCAD.newDocument(docname)
    importgroup = doc.addObject("App::DocumentObjectGroup",groupname)
    importgroup.Label = decodeName(groupname)
    process(doc,filename)

def process(doc,filename,scale,posX,posY,posZ):
    # The common airfoil dat format has many flavors, This code should work with almost every dialect,
    #Regex to identify data rows and throw away unused metadata
    regex = re.compile(r'^\s*(?P<xval>(\-|\d*)\.\d+(E\-?\d+)?)\,?\s*(?P<yval>\-?\s*\d*\.\d+(E\-?\d+)?)\s*$')
    afile = pythonopen(filename,'r')
    # read the airfoil name which is always at the first line
    airfoilname = afile.readline().strip()
    coords=[]
    upside=True
    last_x=None
    # Collect the data for the upper and the lower side separately if possible
    for lin in afile:
        curdat = regex.match(lin)
        if curdat != None:
           #x = float(curdat.group("xval"))
           #y = float(curdat.group("yval"))
           x = float(curdat.group("xval"))+posX
           y = posY
           z = float(curdat.group("yval"))+posZ
           # the normal processing
           coords.append(Vector(x,y,z))
        # End of if curdat != None
    # End of for lin in file
    afile.close

    if len(coords) < 3:
        print('Did not find enough coordinates\n')
        return
    # sometimes coords are divided in upper an lower side
    # so that x-coordinate begin new from leading or trailing edge
    # check for start coordinates in the middle of list

    if coords[0:-1].count(coords[0]) > 1:
        flippoint = coords.index(coords[0],1)
        upper = coords[0:flippoint]
        lower = coords[flippoint+1:]
        lower.reverse()
        for i in lower:
            upper.append(i)
        coords = upper

    # do we use the parametric Draft Wire?
    if useDraftWire:
        obj = makeWire ( coords, True )
        #obj.label = airfoilname
    else:
        # alternate solution, uses common Part Faces
        lines = []
        first_v = None
        last_v = None
        for v in coords:
            if first_v == None:
                first_v = v
            # End of if first_v == None
            # Line between v and last_v if they're not equal
            if (last_v != None) and (last_v != v):
                lines.append(Part.makeLine(last_v, v))
            # End of if (last_v != None) and (last_v != v)
            # The new last_v
            last_v = v
        # End of for v in upper
        # close the wire if needed
        if last_v != first_v:
                lines.append(Part.makeLine(last_v, first_v))
            
        wire = Part.Wire(lines)
        face = Part.Face(wire)
        #Scale the foil
        myScale = Base.Matrix()
        myScale.scale(scale,1,scale)
        face=face.transformGeometry(myScale)
    return face
        #obj = FreeCAD.ActiveDocument.addObject('Part::Feature',airfoilname)
        #obj.Shape = face
        #oobj.Shape=Part.Shape(lines)
        #doc.recompute()
        #return line



class _WPanel:
    def __init__(self, obj):
        '''Add some custom properties to our box feature'''
        obj.addProperty("App::PropertyLength","Length","WingPanel","Length of the wing").Length=1.0
        obj.addProperty("App::PropertyLength","Width","WingPanel","Width of the wing").Width=1.0
        obj.addProperty("App::PropertyLength","Height","WingPanel", "Height of the wing").Height=1.0
        obj.addProperty("App::PropertyStringList","PanelProfil","WingPanel","Profil type").PanelProfil=[u"/Users/fredericnivoix/Library/Preferences/FreeCAD/Mod/AirPlaneDesign/wingribprofil/e207.dat"]
        obj.addProperty("App::PropertyLength","PanelLength","WingPanel","Length of the Wing").PanelLength=100.0
        obj.addProperty("App::PropertyFloatList","PanelDelta","WingPanel","Delta").PanelDelta=[0,70.0]
        obj.addProperty("App::PropertyLength","PanelWidth","WingPanel","Width of the panel").PanelWidth=300.0
        #cordre a l'emplature
        obj.addProperty("App::PropertyLength","PanelRootLength","WingPanel"," root length").PanelRootLength=300.0
        #corde au saumon
        obj.addProperty("App::PropertyLength","PanelTipLength","WingPanel"," wingtip length").PanelTipLength=200.0
        #---------
        #obj.addProperty("App::PropertyLink", "Operations", "Base", "Operations ")
        # Ordonner les champs
        #obj.OrderOutputBy = ['NumberOfPanel','Length', 'Width', 'Height','Delta']
        #ops = FreeCAD.ActiveDocument.addObject("Ribs::FeatureCompoundPython", "Ribs")
        #if ops.ViewObject:
        #    ops.ViewObject.Proxy = 0
        #    ops.ViewObject.Visibility = False 
        #obj.Operations = ops 
        obj.Proxy = self
    
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
    

    def setupRib(self, fp,number,pos,length,models=None):
        name=decodeName(fp.PanelProfil[number])
        fp.addProperty("App::PropertyLink", "Rib", "Panel", "Rib")
        #model = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", "Wing")
        #fp.Shape=process(FreeCAD.ActiveDocument.Name,name,0,pos)#0)
        
        fp.Shape=process(FreeCAD.ActiveDocument.Name,name,length,pos)
        
        #myScale = Base.Matrix()
        #myScale.scale(length,1,length)
        #fp.Shape=fp.Shape.transformGeometry(myScale)
        
    
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage(fp.PanelProfil[0])
        panelRootFace=FreeCAD.ActiveDocument.addObject("Part::Feature","PanelRootFace")
        
        panelRootFace.Shape=process(FreeCAD.ActiveDocument.Name,fp.PanelProfil[0],fp.PanelRootLength,fp.PanelDelta[0],0,0)
        
        panelTipFace=FreeCAD.ActiveDocument.addObject("Part::Feature","PanelTipFace")
        panelTipFace.Shape=process(FreeCAD.ActiveDocument.Name,fp.PanelProfil[0],fp.PanelTipLength,fp.PanelDelta[1],fp.PanelLength,0)
        #panelTipFace.translate(Base.Vector(fp.PanelLength,0,0))
        
        
        #fp=panelRootFace
        a=FreeCAD.ActiveDocument.addObject('Part::Loft','Loft') #addObject
        a.Sections=[panelRootFace, panelTipFace]
        fp=a#panelRootFace
        #FreeCAD.ActiveDocument.recompute()
       #App.getDocument('Sans_nom').ActiveObject.Sections=[App.getDocument('Sans_nom').wpanel, App.getDocument('Sans_nom').wpanel001, ]
        #name=decodeName(fp.PanelProfil[0])
        #fp.Shape=process(FreeCAD.ActiveDocument.Name,name,0,0)
        #myScale = Base.Matrix()
        #myScale.scale(fp.PanelRootLength[0],1,fp.PanelRootLength[0])
        #fp.Shape=fp.Shape.transformGeometry(myScale)
        FreeCAD.Console.PrintMessage("Recompute Python Wing feature\n")

class ViewProviderWing:
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

    #def makeWing():
    # FreeCAD.newDocument()
    # a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wpanel")
    #a=FreeCAD.ActiveDocument.addObject("Wing::FeaturePython","Wing")
    #Wing(a)
    #ViewProviderWing(a.ViewObject)
#App.ActiveDocument.recompute()
#makeWing()

class _CommandWPanel:
    "the WingPanel command definition"
    def GetResources(self):
        return {'MenuText': "Create a Panel(under dev)"}
    
    def IsActive(self):
        return not FreeCAD.ActiveDocument is None
    
    def Activated(self):
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","wpanel")
        _WPanel(a)
        ViewProviderWing(a.ViewObject)
        #FreeCADGui.addModule("AirPlaneDesign")
        #FreeCAD.ActiveDocument.commitTransaction()
        FreeCAD.ActiveDocument.recompute()

if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesingWPanel',_CommandWPanel())
