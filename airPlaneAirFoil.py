# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2010 Heiko Jakob <heiko.jakob@gediegos.de>        *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************
# Modificaiotn by F. Nivoix to integrate in Airplane workbench 2019 - V0.1
#
#***************************************************************************

import os,FreeCAD,FreeCADGui
from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
from pivy import coin
from FreeCAD import Vector, Base

import re, FreeCAD, FreeCADGui, Part, PartDesign,PartDesignGui,Sketcher,cProfile, os, string
#################################################
#  This module provides tools to build a
#  wing panel
#################################################
if open.__module__ in ['__builtin__','io']:
    pythonopen = open

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

def process(doc,filename,scale,posX,posY,posZ,rotX,rotY,rotZ, useSpline = True):
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
           x = float(curdat.group("xval"))#+posX
           y = 0#posY
           z = float(curdat.group("yval"))#+posZ
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

    # do we use a BSpline?
    if useSpline:
        spline = Part.BSplineCurve()
        spline.interpolate(coords)
        if coords[0] != coords[-1]:
            wire = Part.Wire([spline.toShape(),Part.makeLine(coords[0],coords[-1])])
        else:
            wire = Part.Wire(spline.toShape())
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

#move(face, FreeCAD.Vector(posX, posY, posZ))
    face.Placement=FreeCAD.Placement(FreeCAD.Vector(1,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,0),posX))
    face.Placement=FreeCAD.Placement(FreeCAD.Vector(0,1,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,0),posY))
    face.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,1),FreeCAD.Rotation(FreeCAD.Vector(0,0,0),posZ))
    face.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),rotX))
    face.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),rotY))
    face.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),rotZ))

#face.Placement(App.Vector(0,1,0),App.Rotation(App.Vector(0,0,0),posY))
#face.Placement(App.Vector(0,0,1),App.Rotation(App.Vector(0,0,0),posZ))

    return face
