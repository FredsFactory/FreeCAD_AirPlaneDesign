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
# Modificaiotn by F. Nivoix to integrate
# in Airplane workbench 2019 -
# V0.1, V0.2 & V0.3
#***************************************************************************

import FreeCAD,FreeCADGui,Part,re
FreeCADGui.addLanguagePath(":/translations")

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)



#################################################
#  This module provides tools to build a
#  wing panel
#################################################
if open.__module__ in ['__builtin__','io']:
    pythonopen = open

def readpointsonfile(filename):
    # The common airfoil dat format has many flavors, This code should work with almost every dialect,
    # Regex to identify data rows and throw away unused metadata
    regex = re.compile(r'^\s*(?P<xval>(\-|\d*)\.\d+(E\-?\d+)?)\,?\s*(?P<yval>\-?\s*\d*\.\d+(E\-?\d+)?)\s*$')
    afile = pythonopen(filename,'r')
    coords=[]
    # Collect the data for the upper and the lower side separately if possible
    for lin in afile:
        curdat = regex.match(lin)
        if curdat != None:
            x = float(curdat.group("xval"))
            y = 0#posY
            z = float(curdat.group("yval"))
            #ignore points out of range, small tolerance for x value and arbitrary limit for y value, this is necesary because Lednicer
            #format airfoil files include a line indicating the number of coordinates in the same format of the coordinates.
            if (x < 1.01) and (z < 1) and (x > -0.01) and (z > -1):
                coords.append(FreeCAD.Vector(x,y,z))
            else:
                FreeCAD.Console.PrintWarning("Ignoring coordinates out of range -0.01<x<1.01 and/or -1<z<1. If this is a Lednicer format airfoil file there is nothing to worrya about.")
        # End of if curdat != None
    # End of for lin in file
    afile.close

    if len(coords) < 3:
        FreeCAD.Console.PrintError('Did not find enough coordinates\n')
        return
    # sometimes coords are divided in upper an lower side
    # so that x-coordinate begin new from leading or trailing edge
    # check for start coordinates in the middle of list

    if coords[0:-1].count(coords[0]) > 1:
        flippoint = coords.index(coords[0],1)
        coords[:flippoint+1]=coords[flippoint-1::-1]

    return coords

def process(filename,scale,posX,posY,posZ,rotX,rotY,rotZ,useSpline,splitSpline,coords=[]):
    if len(coords) == 0 :
        coords = readpointsonfile(filename)
    # do we use a BSpline?
    if useSpline:
        if splitSpline: #do we split between upper and lower side?
            if coords.__contains__(FreeCAD.Vector(0,0,0)): # lgtm[py/modification-of-default-value]
                flippoint = coords.index(FreeCAD.Vector(0,0,0))
            else:
                lenghtList=[v.Length for v in coords]
                flippoint = lenghtList.index(min(lenghtList))
            splineLower = Part.BSplineCurve()
            splineUpper = Part.BSplineCurve()
            splineUpper.interpolate(coords[:flippoint+1])
            splineLower.interpolate(coords[flippoint:])
            if coords[0] != coords[-1]:
                wire = Part.Wire([splineUpper.toShape(),splineLower.toShape(),Part.makeLine(coords[0],coords[-1])])
            else:
                wire = Part.Wire([splineUpper.toShape(),splineLower.toShape()])
        else:
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
            if first_v is None:
                first_v = v
            # End of if first_v is None
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
    face = face.scale(scale) #Scale the foil
    return face, coords
