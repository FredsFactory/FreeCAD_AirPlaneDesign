# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   AirPlaneDesign workbench                                              *
#*     For more details see InitGui.py and the LICENCE text file.          *
#*                                                                         *
#*   Module : apdLibShapes.py                                              *
#*   Routines to generate aero shapes from *.dat files, NACA, Lyon,        *
#*     Hoerner, Duhamel                                                    *
#*                                                                         *
#*   History :                                                             *
#*     2021-10-05 : add Heiko and Gorissen code (modifications Nivoix)     * 
#      2021-07-28 : Initial release Claude GUTH (nacelle shapes)                           *
#*                                                                         *
#***************************************************************************


__title__  = "airPlaneDesign Workbench - construction de formes fuselées"
__author__ = "Dirk GORISSEN, Claude GUTH, Jakob HEIKO"

import FreeCAD
import FreeCADGui
from FreeCAD import Base
import Draft
import DraftTools
import Part
import math
from math import cos, sin
from math import atan
from math import pi
from math import pow
from math import sqrt
import re
import apdWBCommon as wb

if open.__module__ in ['__builtin__','io']:
    pythonopen = open

#***************************************************************************
#*                                                                         *
#*   These routines to generate ribs from *.dat files                      *
#*                                                                         *
#*   Author : Heiko Jakob <heiko.jakob@gediegos.de>  Copyright (c) 2010    *
#*   Modification by F. Nivoix to integrate in airPlaneDesign workbench    *
#*                                                                         *
#*   Created :  2010                                                       *
#*   Modified : 2019  airPlaneDesign WB integration                        *
#*                                                                         *
#***************************************************************************

def readPointsOnFile(filename):
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
                wb.consoleMsg("Ignoring coordinates out of range -0.01<x<1.01 and/or -1<z<1. If this is a Lednicer format airfoil this is normal.", "W")
        # End of if curdat != None
    # End of for lin in file
    afile.close

    if len(coords) < 3:
        wb.consoleMsg('Did not find enough coordinates\n', "E")
        return
    # sometimes coords are divided in upper an lower side
    # so that x-coordinate begin new from leading or trailing edge
    # check for start coordinates in the middle of list

    if coords[0:-1].count(coords[0]) > 1:
        flippoint = coords.index(coords[0],1)
        coords[:flippoint+1]=coords[flippoint-1::-1]

    return coords

def getCoordsFromDat(filename,scale,posX,posY,posZ,rotX,rotY,rotZ,rot,useSpline,splitSpline,coords=[]):
    if len(coords) == 0 :
        coords = readPointsOnFile(filename)
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

    #face = Part.Face(wire).scale(scale) #Scale the foil, # issue31 doesn't work with v0.18
    face = Part.Face(wire)
    myScale = Base.Matrix() # issue31
    myScale.scale(scale,scale,scale)# issue31
    face=face.transformGeometry(myScale)# issue31

    face.Placement.Rotation.Axis.x=rotX
    face.Placement.Rotation.Axis.y=rotY
    face.Placement.Rotation.Axis.z=rotZ
    face.Placement.Rotation.Angle=rot

    #face.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(rotX,rotY,rotZ),rot))
    #face.rotate([0,0,0],FreeCAD.Vector(rotX, rotY, rotZ),rot)


    return face, coords


#***************************************************************************
#*                                                                         *
#*   These routines to generate generate 4 and 5 digit NACA profiles       *
#*   The parameters in the numerical code can be entered into equations    *
#*    to precisely generate the cross-section of the airfoil               *
#*    and calculate its properties.                                        *
#*   https://en.wikipedia.org/wiki/NACA_airfoil                            *
#*                                                                         *
#*   Author : Dirk Gorissen <dgorissen@gmail.com>  Copyright (c) 2011      *
#*                                                                         *
#*   Created :  2011                                                       *
#*   Modified : 2019  airPlaneDesign WB integration                        *
#*                                                                         *
#***************************************************************************

def linspace(start,stop,np):
    """
    Emulate Matlab linspace
    """
    return [start+(stop-start)*i/(np-1) for i in range(np)]

def interpolate(xa,ya,queryPoints):
    """
    A cubic spline interpolation on a given set of points (x,y)
    Recalculates everything on every call which is far from efficient but does the job for now
    should eventually be replaced by an external helper class
    """

    # PreCompute() from Paint Mono which in turn adapted:
    # NUMERICAL RECIPES IN C: THE ART OF SCIENTIFIC COMPUTING
    # ISBN 0-521-43108-5, page 113, section 3.3.
    # http://paint-mono.googlecode.com/svn/trunk/src/PdnLib/SplineInterpolator.cs

    #number of points
    n = len(xa)
    u, y2 = [0]*n, [0]*n

    for i in range(1,n-1):

        # This is the decomposition loop of the tridiagonal algorithm.
        # y2 and u are used for temporary storage of the decomposed factors.

        wx = xa[i + 1] - xa[i - 1]
        sig = (xa[i] - xa[i - 1]) / wx
        p = sig * y2[i - 1] + 2.0

        y2[i] = (sig - 1.0) / p

        ddydx = (ya[i + 1] - ya[i]) / (xa[i + 1] - xa[i]) - (ya[i] - ya[i - 1]) / (xa[i] - xa[i - 1])

        u[i] = (6.0 * ddydx / wx - sig * u[i - 1]) / p


    y2[n - 1] = 0

    # This is the backsubstitution loop of the tridiagonal algorithm
    #((int i = n - 2; i >= 0; --i):
    for i in range(n-2,-1,-1):
        y2[i] = y2[i] * y2[i + 1] + u[i]

    # interpolate() adapted from Paint Mono which in turn adapted:
    # NUMERICAL RECIPES IN C: THE ART OF SCIENTIFIC COMPUTING
    # ISBN 0-521-43108-5, page 113, section 3.3.
    # http://paint-mono.googlecode.com/svn/trunk/src/PdnLib/SplineInterpolator.cs

    results = [0]*n

    #loop over all query points
    for i in range(len(queryPoints)):
        # bisection. This is optimal if sequential calls to this
        # routine are at random values of x. If sequential calls
        # are in order, and closely spaced, one would do better
        # to store previous values of klo and khi and test if

        klo = 0
        khi = n - 1

        while (khi - klo > 1):
            k = (khi + klo) >> 1
            if (xa[k] > queryPoints[i]):
                khi = k
            else:
                klo = k

        h = xa[khi] - xa[klo]
        a = (xa[khi] - queryPoints[i]) / h
        b = (queryPoints[i] - xa[klo]) / h

        # Cubic spline polynomial is now evaluated.
        results[i] = a * ya[klo] + b * ya[khi] + ((a * a * a - a) * y2[klo] + (b * b * b - b) * y2[khi]) * (h * h) / 6.0

    return results

def naca4(number, n, finite_TE = False, half_cosine_spacing = False):
    """
    Returns 2*n+1 points in [0 1] for the given 4 digit NACA number string
    """

    m = float(number[0])/100.0
    p = float(number[1])/10.0
    t = float(number[2:])/100.0

    a0 = +0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = +0.2843

    if finite_TE:
        a4 = -0.1015 # For finite thick TE
    else:
        a4 = -0.1036 # For zero thick TE

    if half_cosine_spacing:
        beta = linspace(0.0,pi,n+1)
        x = [(0.5*(1.0-cos(xx))) for xx in beta]  # Half cosine based spacing
    else:
        x = linspace(0.0,1.0,n+1)

    yt = [5*t*(a0*sqrt(xx)+a1*xx+a2*pow(xx,2)+a3*pow(xx,3)+a4*pow(xx,4)) for xx in x]

    xc1 = [xx for xx in x if xx <= p]
    xc2 = [xx for xx in x if xx > p]

    if p == 0:
        xu = x
        yu = yt

        xl = x
        yl = [-xx for xx in yt]

        #xc = xc1 + xc2
        #zc = [0]*len(xc)
    else:
        yc1 = [m/pow(p,2)*xx*(2*p-xx) for xx in xc1]
        yc2 = [m/pow(1-p,2)*(1-2*p+xx)*(1-xx) for xx in xc2]
        zc = yc1 + yc2

        dyc1_dx = [m/pow(p,2)*(2*p-2*xx) for xx in xc1]
        dyc2_dx = [m/pow(1-p,2)*(2*p-2*xx) for xx in xc2]
        dyc_dx = dyc1_dx + dyc2_dx

        theta = [atan(xx) for xx in dyc_dx]

        xu = [xx - yy * sin(zz) for xx,yy,zz in zip(x,yt,theta)]
        yu = [xx + yy * cos(zz) for xx,yy,zz in zip(zc,yt,theta)]

        xl = [xx + yy * sin(zz) for xx,yy,zz in zip(x,yt,theta)]
        yl = [xx - yy * cos(zz) for xx,yy,zz in zip(zc,yt,theta)]

    X = xu[::-1] + xl[1:]
    Z = yu[::-1] + yl[1:]
    # AiplaneDesign modification - start
    coords=[]
    for i in range(len(X)) :
        coords.append(FreeCAD.Vector(X[i],0,Z[i]))
    return coords

   # AiplaneDesign modification - end

def naca5(number, n, finite_TE = False, half_cosine_spacing = False):
    """
    Returns 2*n+1 points in [0 1] for the given 5 digit NACA number string
    """


    naca1 = int(number[0])
    naca23 = int(number[1:3])
    naca45 = int(number[3:])

    cld = naca1*(3.0/2.0)/10.0
    p = 0.5*naca23/100.0
    t = naca45/100.0

    a0 = +0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = +0.2843

    if finite_TE:
        a4 = -0.1015 # For finite thickness trailing edge
    else:
        a4 = -0.1036  # For zero thickness trailing edge

    if half_cosine_spacing:
        beta = linspace(0.0,pi,n+1)
        x = [(0.5*(1.0-cos(x))) for x in beta]  # Half cosine based spacing
    else:
        x = linspace(0.0,1.0,n+1)

    yt = [5*t*(a0*sqrt(xx)+a1*xx+a2*pow(xx,2)+a3*pow(xx,3)+a4*pow(xx,4)) for xx in x]

    P = [0.05,0.1,0.15,0.2,0.25]
    M = [0.0580,0.1260,0.2025,0.2900,0.3910]
    K = [361.4,51.64,15.957,6.643,3.230]

    m = interpolate(P,M,[p])[0]
    k1 = interpolate(M,K,[m])[0]

    xc1 = [xx for xx in x if xx <= p]
    xc2 = [xx for xx in x if xx > p]
    #xc = xc1 + xc2

    if p == 0:
        xu = x
        yu = yt

        xl = x
        yl = [-x for x in yt]

        #zc = [0]*len(xc)
    else:
        yc1 = [k1/6.0*(pow(xx,3)-3*m*pow(xx,2)+ pow(m,2)*(3-m)*xx) for xx in xc1]
        yc2 = [k1/6.0*pow(m,3)*(1-xx) for xx in xc2]
        zc  = [cld/0.3 * xx for xx in yc1 + yc2]

        dyc1_dx = [cld/0.3*(1.0/6.0)*k1*(3*pow(xx,2)-6*m*xx+pow(m,2)*(3-m)) for xx in xc1]
        dyc2_dx = [cld/0.3*(1.0/6.0)*k1*pow(m,3)]*len(xc2)

        dyc_dx = dyc1_dx + dyc2_dx
        theta = [atan(xx) for xx in dyc_dx]

        xu = [xx - yy * sin(zz) for xx,yy,zz in zip(x,yt,theta)]
        yu = [xx + yy * cos(zz) for xx,yy,zz in zip(zc,yt,theta)]

        xl = [xx + yy * sin(zz) for xx,yy,zz in zip(x,yt,theta)]
        yl = [xx - yy * cos(zz) for xx,yy,zz in zip(zc,yt,theta)]

    X = xu[::-1] + xl[1:]
    Z = yu[::-1] + yl[1:]

    # AiplaneDesign modification - start
    coords=[]
    for i in range(len(X)) :
        coords.append(FreeCAD.Vector(X[i],0,Z[i]))
    return coords

   # AiplaneDesign modification - end


#***************************************************************************
#* Main NACA generate routines                                             *
#***************************************************************************
def generateNacaCoords(number, n, finite_TE, half_cosine_spacing,scale,posX,posY,posZ,rotX,rotY,rotZ,):
    coords=[]
    if len(number)==4:
        coords=naca4(number, n, finite_TE, half_cosine_spacing)
    elif len(number)==5:
        coords=naca5(number, n, finite_TE, half_cosine_spacing)
    else:
        raise ValueError("Invalid NACA number")
    return coords

def generateNaca(number, n=240, finite_TE = False, half_cosine_spacing = True,scale=1,posX=0,posY=0,posZ=0,rotX=0,rotY=0,rotZ=0,rot=0,useSpline=True,splitSpline=False):
    coords=generateNacaCoords(number, n, finite_TE , half_cosine_spacing ,scale,posX,posY,posZ,rotX,rotY,rotZ)
    if useSpline:
        if splitSpline:
            splineLower = Part.BSplineCurve()
            splineUpper = Part.BSplineCurve()
            splineUpper.interpolate(coords[:len(coords)//2+1])
            splineLower.interpolate(coords[len(coords)//2:])
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

    face = Part.Face(wire).scale(scale) #Scale the foil
    #face.Placement.Rotation.Axis.x=rotX
    #face.Placement.Rotation.Axis.y=rotY
    #face.Placement.Rotation.Axis.z=rotZ
    #face.Placement.Rotation.Angle=rot

    return face, coords



#***************************************************************************
#*                                                                         *
#*   These routines to generate nacelles                                   *
#*   https://fr.wikipedia.org/wiki/Corps_de_moindre_tra%C3%AEn%C3%A9e.     *
#*   Nota : coordinates and faces in xy plane.                             *
#*                                                                         *
#*   Author :   Claude GUTH                                                *
#*   Created :  2021-07-28                                                 *
#*                                                                         *
#***************************************************************************

def getLyonCoords(longueur, diametre, nbPoints=100):
  """
  :param longueur:          longueur (selon axe x) de la forme
  :param diametre:          diamètre de la forme
  :param nbPoints:          nb de points calculés
  :return: les coordonnées d'ordonnées positives d'une fome Lyon modèle A
  """
  # parametres intermédiaires de calcul
  ky = diametre*1.11326

  # points de la forme
  cLyon = [FreeCAD.Vector(0, 0, 0)]
  kx = 1 / float(nbPoints-1)
  for i in range(1, nbPoints):
    xRel= kx * float(i) 
    xRel2= xRel * xRel
    xRel3= xRel2 * xRel
    xRel4= xRel3 * xRel
    yPos = ky * math.sqrt(xRel - xRel2 - xRel3 + xRel4)
    cLyon.append(FreeCAD.Vector(xRel * longueur, yPos, 0))
  return cLyon

def getHoernerCoords(longueur, diametre, xRelEpaisseurMax, nbPoints=100):
  """
  :param longueur:          longueur (selon axe x) de la forme
  :param diametre:          diamètre de la forme
  :param xRelEpaisseurMax:  abscisse relative (0..1) pour l'épaisseur max
  :param nbPoints:          nb de points calculés
  :return: les coordonnées d'ordonnées positives d'une FEC
  """
  # parametres intermédiaires de calcul
  xeMax = xRelEpaisseurMax*longueur
  yeMax = 0.5*diametre
  pi_2 =  math.pi/2

  # points de la forme
  cFEC = [FreeCAD.Vector(0, 0, 0)]
  kl = longueur / float(nbPoints-1)
  for i in range(1, nbPoints):
    xPos = kl * float(i)
    if xPos < xeMax:
      yPos = yeMax * math.sqrt(2*xPos*xeMax - xPos*xPos) / xeMax
    else:
      yPos = yeMax * math.cos(pi_2*(xeMax-xPos)/(longueur-xeMax))
    cFEC.append(FreeCAD.Vector(xPos, yPos, 0))
  return cFEC

def getDuhamelCoords(longueur, diametre, nbPoints=100):
  """
  :param longueur:          longueur (selon axe x) de la forme
  :param diametre:          diamètre de la forme
  :param nbPoints:          nb de points calculés
  :return: les coordonnées d'ordonnées positives d'une forme Duhamel simplifiée
  """
  # parametres intermédiaires de calcul
  ky = diametre*1.3

  # points de la forme
  cLyon = [FreeCAD.Vector(0, 0, 0)]
  kx = 1 / float(nbPoints-1)
  for i in range(1, nbPoints):
    xRel= kx * float(i) 
    yPos = ky * (1 - xRel) * math.sqrt(xRel)
    cLyon.append(FreeCAD.Vector(xRel * longueur, yPos, 0))
  return cLyon

def getNACACoords(longueur, diametre, nbPoints=100):
  """
  :param longueur:          longueur (selon axe x) de la forme
  :param diametre:          diamètre de la forme
  :param nbPoints:          nb de points calculés
  :return: les coordonnées d'ordonnées positives d'une fome NACA 4 chiffres 
  """
  # parametres intermédiaires de calcul
  a0= 0.2969
  a1= -0.126
  a2= -0.3516
  a3= 0.2843
  a4= -0.1036
  ky = 5*diametre*diametre/longueur

  # points de la forme
  cNaca = [FreeCAD.Vector(0, 0, 0)]
  kx = 1 / float(nbPoints-1)
  for i in range(1, nbPoints):
    xRel= kx * float(i) 
    xRel2= xRel * xRel
    xRel3= xRel2 * xRel
    xRel4= xRel3 * xRel
    yPos = ky * (a0*math.sqrt(xRel) + a1*xRel + a2*xRel2 + a3*xRel3 + a4*xRel4)
    cNaca.append(FreeCAD.Vector(xRel * longueur, yPos, 0))
  return cNaca


