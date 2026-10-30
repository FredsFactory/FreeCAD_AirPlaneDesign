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

import FreeCADGui
import FreeCAD
from FreeCAD import Vector
import Part, Draft, os
from PySide import QtGui, QtCore
import WorkingPlane
import CompoundTools.Explode
try:
    import CurvedShapes
except ImportError:
    #FreeCAD.Console.PrintError("The 'CurvedShapes' module is required. Please install or load it first.\n")
    # Create a custom popup using PySide
    msg_box = QtGui.QMessageBox()
    msg_box.setIcon(QtGui.QMessageBox.Critical)
    msg_box.setWindowTitle("Dependency Error")
    msg_box.setText("The 'CurvedShapes' module is required but not found.")
    msg_box.setInformativeText("Please install the 'CurvedShapes' module to continue.")
    msg_box.setStandardButtons(QtGui.QMessageBox.Ok)
    msg_box.exec_()
    FreeCADGui.runCommand('Std_AddonMgr', 0)
import math

import os
from airPlaneRib import WingRib, ViewProviderWingRib
from PySide import QtCore

#import airPlaneDesingCurvedArray
import CompoundTools.Explode
import CurvedShapes,CompoundTools
global epsilon
epsilon = CurvedShapes.epsilon

smWB_icons_path =  os.path.join( os.path.dirname(__file__), 'resources', 'icons')

# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)


def scaleByBoundbox(shape, boundbox, doScaleXYZ, copy=True):
        basebbox = shape.BoundBox
        #basebbox=[1.0,1.0,1.0]
        scalevec = Vector(1, 1, 1)
        if doScaleXYZ[0] and basebbox.XLength > epsilon: scalevec.x = boundbox.XLength / basebbox.XLength
        if doScaleXYZ[1] and basebbox.YLength > epsilon: scalevec.y = boundbox.YLength / basebbox.YLength
        if doScaleXYZ[2] and basebbox.ZLength > epsilon: scalevec.z = boundbox.ZLength / basebbox.ZLength

        scalevec.x=boundbox.XLength
        scalevec.y=boundbox.YLength
        scalevec.z=boundbox.ZLength

        if scalevec.x < epsilon:
            if doScaleXYZ[0]:
                scalevec.x = epsilon
            else:
                scalevec.x = 1
        if scalevec.y < epsilon:
            if doScaleXYZ[1]:
                scalevec.y = epsilon
            else:
                scalevec.y = 1
        if scalevec.z < epsilon:
            if doScaleXYZ[2]:
                scalevec.z = epsilon
            else:
                scalevec.z = 1

        _rib=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Rib00")
        print("Scale in scaleByBoundbox")
        print(scalevec)
        WingRib(_rib,"/Users/fredericnivoix/Library/Preferences/FreeCAD/Mod/AirPlaneDesign/wingribprofil/naca/naca2412.dat",False,0,scalevec.x,0,0,0,0,0,0)
        ViewProviderWingRib(_rib.ViewObject)
        _rib.Placement=shape.Placement
        #dolly = scale(shape, scalevec, basebbox.Center, copy)
        #dolly.Placement = shape.Placement

        if doScaleXYZ[0]:
            _rib.Placement.Base.x += boundbox.XMin - basebbox.XMin * scalevec.x
        if doScaleXYZ[1]:
            _rib.Placement.Base.y += boundbox.YMin - basebbox.YMin * scalevec.y
        if doScaleXYZ[2]:
            _rib.Placement.Base.z += boundbox.ZMin - basebbox.ZMin * scalevec.z

        return _rib#dolly

def scaleByBoundbox2(shape, boundbox, doScaleXYZ):
        basebbox = shape.BoundBox
        scalevec = Vector(1, 1, 1)
        x=shape.Placement.Base.x
        y=shape.Placement.Base.y
        z=shape.Placement.Base.z
        if doScaleXYZ[0] and basebbox.XLength > epsilon: scalevec.x = boundbox.XLength / basebbox.XLength
        if doScaleXYZ[1] and basebbox.YLength > epsilon: scalevec.y = boundbox.YLength / basebbox.YLength
        if doScaleXYZ[2] and basebbox.ZLength > epsilon: scalevec.z = boundbox.ZLength / basebbox.ZLength

        scalevec.x=boundbox.XLength
        scalevec.y=boundbox.YLength
        scalevec.z=boundbox.ZLength

        if scalevec.x < epsilon:
            if doScaleXYZ[0]:
                scalevec.x = epsilon
            else:
                scalevec.x = 1
        if scalevec.y < epsilon:
            if doScaleXYZ[1]:
                scalevec.y = epsilon
            else:
                scalevec.y = 1
        if scalevec.z < epsilon:
            if doScaleXYZ[2]:
                scalevec.z = epsilon
            else:
                scalevec.z = 1

        if doScaleXYZ[0]:
            x += boundbox.XMin - basebbox.XMin * scalevec.x
        if doScaleXYZ[1]:
            y += boundbox.YMin - basebbox.YMin * scalevec.y
        if doScaleXYZ[2]:
            z += boundbox.ZMin - basebbox.ZMin * scalevec.z

        return x,y,z,scalevec.x, scalevec.y, scalevec.z


def makeSurfaceSolid(ribs, solid):
    surfaces = []
    wiribs = []
    for r in ribs:
        if len(r.Shape.OuterWire) > 0:
            wiribs += r.Shape.OuterWire#Wires
        else:
            try:
                wiribs.append(Part.Wire(r.Edges))
            except:
                FreeCAD.Console.PrintError("Cannot make a wire. Creation of surface is not possible !\n")
                return

    try:
        loft = Part.makeLoft(wiribs)
        surfaces += loft.Faces
    except:
        FreeCAD.Console.PrintError("Creation of surface is not possible !\n")
        return Part.makeCompound(wiribs)

    if solid:
        face1 = makeFace(ribs[0])
        if face1:
            surfaces.append(face1)
        face2 = makeFace(ribs[len(ribs)-1])
        if face2:
            surfaces.append(face2)

        try:
            shell = Part.makeShell(surfaces)
            if face1 and face2:
                try:
                    return Part.makeSolid(shell)
                except:
                    FreeCAD.Console.PrintError("Creating solid failed !\n")
        except:
            FreeCAD.Console.PrintError("Creating shell failed !\n")

    if len(surfaces) == 1:
        return surfaces[0]
    elif len(surfaces) > 1:
        return Part.makeCompound(surfaces)

# x is in range 0 to 1. result must be in range 0 to 1.
def distribute(x, distribution, reverse = False):
    d = x   # default = 'linear'

    if distribution == 'parabolic':
        d = x*x

    if distribution == 'x³':
        d = x*x*x

    if distribution == 'sinusoidal':
        d = math.sin(x * math.pi / 2)

    if distribution == 'elliptic':
        d = math.sqrt(1 - x*x)

    if reverse:
        d = 1 - d

    return d


# Chord (mm) below which a "rib" is numerical garbage: scaleByBoundbox2
# clamps a collapsed bbox to 1e-7, and lofting over such sections raises or
# segfaults BRepFill_CompatibleWires depending on the OCCT build.
_minRibChord = 1e-3


def _teStationWindow(pathEdge, leEdge, teObj):
    """Spanwise arc-length window [lo, hi] on the panel leading edge within
    which the rib slice plane (through the LE point at that arc length,
    normal = path tangent) still crosses the trailing edge. Near a panel end
    the plane can fall entirely forward of the finite TE segment;
    boundbox_from_intersect then silently collapses the bbox onto the LE
    point (its `found` flag is shared across hull curves) and the rib gets a
    zero chord. Spacing stations inside this window prevents that.

    Returns None when no window can be derived; caller keeps its own range.

    ponytail: the window linearises the LE at its start tangent and samples
    the TE every ~1/32 of each edge, so it is exact for straight sketch
    segments and approximate for splines - leaks are caught by the
    per-rib _minRibChord guard, so exactness is not required here.
    """
    teShape = getattr(teObj, "Shape", None)
    if teShape is None or teShape.isNull() or not teShape.Edges:
        return None

    d = pathEdge.tangentAt(pathEdge.getParameterByLength(pathEdge.Length / 2.0))
    tproj = leEdge.tangentAt(leEdge.FirstParameter).dot(d)
    if abs(tproj) < 1e-6:  # chord has no extent along the path: no window
        return None
    le0 = leEdge.valueAt(leEdge.FirstParameter).dot(d)
    projs = [e.valueAt(e.FirstParameter + (e.LastParameter - e.FirstParameter) * i / 32.0).dot(d)
             for e in teShape.Edges for i in range(33)]

    lo = (min(projs) - le0) / tproj
    hi = (max(projs) - le0) / tproj
    return (lo, hi) if lo <= hi else (hi, lo)

#################################################
#
#  This module provides tools to build a wing panel
#
#################################################
if open.__module__ in ['__builtin__','io', '_io']:
    pythonopen = open

_wingRibProfilDir = os.path.join(os.path.dirname(__file__), 'wingribprofil')

class WingPanel:
    def __init__(self,
                 obj,
                 _rootRib,
                 _path,
                 _envelope,
                 _leadingedge,
                 _traillingedge,
                 _rootChord=200,
                 _tipChord=100,
                 _panelLength=100,
                 _tipTwist=0,
                 _dihedral=0,
                 axis=Vector(0.0,0.0,0.0),
                 items=5,
                 OffsetStart=0, OffsetEnd=0,
                 _distribution = 'linear',
                 _distributionReverse = False,
                 extract=False,
                 Twist=0,_ribs=[]
                 ):

        #_rootRib,_tipRib,
        '''Add some custom properties to our box feature'''
        self.obj = obj

        obj.addProperty("App::PropertyLink","Base","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Rib of the panel")).Base=_rootRib#
        obj.addProperty("App::PropertyLink","Envelope","WPRibs",QtCore.QT_TRANSLATE_NOOP("App::Property","Eveloppe of wing")).Envelope=_envelope
        obj.addProperty("App::PropertyLink","Path","WPRibs",QtCore.QT_TRANSLATE_NOOP("App::Property","Path of wing")).Path=_path

        # generated Ribs
        obj.addProperty("App::PropertyLinkList","Ribs","WPRibs",QtCore.QT_TRANSLATE_NOOP("App::Property","Ribs of the panel")).Ribs=_ribs

        # need to convert into function not attributes
        obj.addProperty("App::PropertyLength","TipChord","WPRibs",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Chord")).TipChord=_tipChord
        obj.addProperty("App::PropertyLength","RootChord","WPRibs",QtCore.QT_TRANSLATE_NOOP("App::Property","Root Chord")).RootChord=_rootChord
        obj.addProperty("App::PropertyLength","PanelLength","Design",QtCore.QT_TRANSLATE_NOOP("App::Property","Panel Length")).PanelLength=_panelLength

        # need to convert into function not attributes
        obj.addProperty("App::PropertyVector", "Axis",    "WingPanel",   "Direction axis").Axis = axis
        obj.addProperty("App::PropertyLinkList",  "Hullcurves",   "WingEdge",   "Bounding curves").Hullcurves=[_leadingedge,_traillingedge]

        # leadingEdge : bord d'attaque
        obj.addProperty("App::PropertyLinkList","Edges","WingEdges",QtCore.QT_TRANSLATE_NOOP("App::Property","Select the leading edge of the panal, line or Spline")).Edges=[]
        obj.addProperty("App::PropertyLink","LeadingEdge","WingEdges",QtCore.QT_TRANSLATE_NOOP("App::Property","Select the leading edge of the panal, line or Spline")).LeadingEdge=_leadingedge
        # trailing edge : bord de fuite
        obj.addProperty("App::PropertyLink","TrailingEdge","WingEdges",QtCore.QT_TRANSLATE_NOOP("App::Property","Select the trailing edge of the panel, line or Spline")).TrailingEdge=_traillingedge


        # twist(f) = Twist + TipTwist * f (f: 0 root -> 1 tip), right-hand
        # rotation about the rib normal (+Y; section plane is local XZ) =
        # airPlaneCavity's station axis, so negative TipTwist = washout.
        # Dihedral is unimplemented (see tutorials/wing-panel.md).
        obj.addProperty("App::PropertyAngle","TipTwist","Design",QtCore.QT_TRANSLATE_NOOP("App::Property","Tip Twist")).TipTwist=_tipTwist
        obj.addProperty("App::PropertyAngle","Dihedral","Design",QtCore.QT_TRANSLATE_NOOP("App::Property","Dihedral")).Dihedral=_dihedral
        #obj.addProperty("App::PropertyLinkList","Ribs","WingPanel",QtCore.QT_TRANSLATE_NOOP("App::Property","list of ribs")).Ribs=[]

        obj.addProperty("App::PropertyBool","Solid","Design",QtCore.QT_TRANSLATE_NOOP("App::Property","Solid")).Solid=False
        obj.addProperty("App::PropertyBool","Surface","Design",QtCore.QT_TRANSLATE_NOOP("App::Property","Surface")).Surface=False
        obj.addProperty("App::PropertyBool","Structure","Design",QtCore.QT_TRANSLATE_NOOP("App::Property","Surface")).Structure=False

        obj.addProperty("App::PropertyQuantity", "Items", "Design",   "Nr. of array items").Items = items
        obj.addProperty("App::PropertyFloat", "OffsetStart","Design",  "Offset of the first part in Axis direction").OffsetStart = OffsetStart
        obj.addProperty("App::PropertyFloat", "OffsetEnd","Design",  "Offset of the last part from the end in opposite Axis direction").OffsetEnd = OffsetEnd

        obj.addProperty("App::PropertyFloat", "Twist","Design",  "Rotate around Axis in degrees").Twist = Twist

        obj.addProperty("App::PropertyEnumeration", "Distribution", "Design",  QtCore.QT_TRANSLATE_NOOP("App::Property","Algorithm for distance between elements"))
        obj.addProperty("App::PropertyBool", "DistributionReverse", "Design",  QtCore.QT_TRANSLATE_NOOP("App::Property","Reverses direction of Distribution algorithm")).DistributionReverse = _distributionReverse
        obj.Distribution = ['linear', 'parabolic', 'x³', 'sinusoidal', 'elliptic']
        obj.Distribution = _distribution
        self.extract = extract
        self.doScaleXYZ = []
        self.doScaleXYZsum = [False, False, False]
        obj.Base.Visibility=False
        obj.Proxy = self


    def __getstate__(self):
        # FreeCAD >=1.x persists this as JSON text (json.dumps of the state).
        # Keep links/transients out: obj is a DocumentObject, and json.dumps
        # failing on the old implicit __dict__ is exactly what made pre-fix
        # saves store an EMPTY proxy state.
        return {'extract': getattr(self, 'extract', False)}

    def __setstate__(self, state):
        # Restore never runs __init__.  FreeCAD allocates the proxy with
        # __new__ and calls this with the JSON state - but NOT for documents
        # saved before this hook existed: their stored value is empty and
        # FreeCAD skips __setstate__ entirely, leaving __dict__ bare.  So
        # reset transient state here, and never assume this ran (_adopt).
        if state:
            self.__dict__.update(state)
        self.obj = None
        self.doScaleXYZ = []
        self.doScaleXYZsum = [False, False, False]

    def _adopt(self, obj):
        # re-link the feature on first use after a restore.  getattr, not
        # `self.obj is None`: an old-format restore never reached
        # __setstate__, so the proxy has NO obj attribute at all and plain
        # access raises AttributeError (the GUI crash this guard stops).
        if getattr(self, 'obj', None) is None:
            self.obj = obj

    def onChanged(self, obj, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("******* onChanged routine *********************\n"+" Change property: " + str(prop) + "\n")
        # a restored proxy may carry no attributes at all; adopt before the rib wipe
        self._adopt(obj)
        proplist = ["Base", "Hullcurves",
                    "Axis", "Items", "OffsetStart",
                    "OffsetEnd", "Twist", "TipTwist", "Surface",
                    "Solid",
                    "LeadingEdge", "TrailingEdge"
                    ,"DistributionReverse"] #,"Ribs"

        for p in proplist:
            if not hasattr(obj, p):
                return

        if prop in proplist:
             # No count check: the old "update" branch kept ribs at their old
             # stations (its updateRib calls were dead), so every tracked
             # change wipes and rebuilds. Plain recomputes still reach the
             # re-skin path through execute()'s update forcing.
             print("Need to delete and recreate all Ribs")
             if len(obj.Ribs)>0 : self.deleteAllRib(obj)
             self.execute(obj,False)


    def createLeadingEdge(self, obj):
        print("Create LeadingEdge:")

        leadingEdge = FreeCAD.activeDocument().addObject('Sketcher::SketchObject','LeadingEdge')

        leadingEdge.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0.000000,0.000000,0.000000,1.000000))
        leadingEdge.addGeometry(Part.LineSegment(FreeCAD.Vector(-410.985718,84.541397,0),FreeCAD.Vector(-375.014648,308.281403,0)),False)

        #-----------------------START------------------------------------------
        # Code from CurvedShapes workbench adapted for Airplanedesign.
        #__author__ = "Christian Bergmann"
        #__license__ = "LGPL 2.1"
        #
        #----------------------------------------------------------------------
    def createRib(self, obj,chord, posvec,direction, rotaxis, angle, twist=0.0):
        FreeCAD.Console.PrintMessage("------------ createRib ------------\n")
        if _minRibChord > chord:
            # a collapsed section poisons lofts/cavity downstream - refuse at source
            FreeCAD.Console.PrintWarning(
                "  Rib skipped : computed chord %.3g mm is below the %.3g mm"
                " minimum - check the hull curves and offsets.\n"
                % (chord, _minRibChord))
            return None
        _rib=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Rib")
        #calcul du facteur d'échelle de la nervure
        #x,y,z,scalex,scaley,scalez=scaleByBoundbox2(obj.Base.Shape, bbox, self.doScaleXYZsum )
        #(obj,_profil,_nacagene,_nacaNbrPoint,_chord,_x,_y,_z,_xrot,_yrot,_zrot,_thickness=0,_useSpline = True,_finite_TE = False,_splitSpline = False)
        #(self, obj,_profil,_nacagene,_nacaNbrPoint,_chord,_x,_y,_z,_xrot,_yrot,_zrot,_rot=0,_thickness=0,_useSpline = True,_finite_TE = False,_splitSpline = False)

        #FreeCAD.Console.PrintMessage("------------ createRib.posvec:"+str(posvec)+ " ------------\n")
        #FreeCAD.Console.PrintMessage("------------ createRib.rotaxis:"+str(rotaxis)+ " ------------\n")
        #FreeCAD.Console.PrintMessage("------------ createRib.angle"+str(angle)+ " ------------\n")
        #FreeCAD.Console.PrintMessage("------------ createRib.scalex"+str(scalex)+ " ------------\n")
        #FreeCAD.Console.PrintMessage("------------ createRib.scaley"+str(scaley)+ " ------------\n")
        #FreeCAD.Console.PrintMessage("------------ createRib.scalez"+str(scalez)+ " ------------\n")

        if obj.Base.NacaProfil=="" :
            WingRib(_rib,
                    obj.Base.RibProfil,
                    "",
                    obj.Base.NacaNbrPoint,
                    chord,
                    posvec.x,posvec.y,posvec.z,
                    rotaxis.x, rotaxis.y,rotaxis.z,#obj.Base.Placement.Rotation.Axis.x,obj.Base.Placement.Rotation.Axis.y, obj.Base.Placement.Rotation.Axis.z,
                    angle,#math.degrees(obj.Base.Placement.Rotation.Angle),
                    0,
                    obj.Base.useSpline,
                    obj.Base.finite_TE,
                    obj.Base.splitSpline)

        else :
            WingRib(_rib,obj.Base.NacaProfil or obj.Base.RibProfil,
                    True,
                    obj.Base.NacaNbrPoint,
                    chord,
                    posvec.x,posvec.y,posvec.z,
                    rotaxis.x, rotaxis.y,rotaxis.z,#obj.Base.Placement.Rotation.Axis.x,obj.Base.Placement.Rotation.Axis.y, obj.Base.Placement.Rotation.Axis.z,
                    angle,#math.degrees(obj.Base.Placement.Rotation.Angle),
                    0,
                    obj.Base.useSpline,
                    obj.Base.finite_TE,
                    obj.Base.splitSpline)
            #obj.addProperty("App::PropertyString","NacaProfil","NacaProfil",QtCore.QT_TRANSLATE_NOOP("App::Property","Naca Profil")).NacaProfil=""

        if abs(twist) > 1e-9:
            # rib-plane rotation: about local +Y (section plane is local XZ),
            # right-multiplied after the alignment rotation, hinged at the LE.
            # Placement only; Coordinates keeps the untwisted unit chord.
            _rib.Placement = FreeCAD.Placement(
                _rib.Placement.Base,
                _rib.Placement.Rotation.multiply(
                    FreeCAD.Rotation(Vector(0, 1, 0), twist)))

        if _rib.ViewObject:   # headless (freecadcmd): cosmetic provider only
            ViewProviderWingRib(_rib.ViewObject)
        return _rib

    def deleteAllRib(self, obj):
        #print("Delete a rib")
        for rib in obj.Ribs :
          FreeCAD.ActiveDocument.removeObject(rib.Label)

    def wingpshape(self, obj) :
        # Only loft over sections OCCT survives: null/empty/sub-micron shapes
        # and coincident duplicates (legacy ribs stacked by the old plen
        # clamp) make makeSurfaceSolid's Part.makeLoft raise or segfault
        # BRepFill_CompatibleWires. Warn, skip, loft the rest - this also
        # self-heals documents saved with such ribs (update path).
        a=[]
        skipped=[]
        lastCenter=None
        for i in obj.Ribs :
            s = i.Shape
            if s.isNull() or len(s.Edges) == 0 or s.BoundBox.DiagonalLength < _minRibChord:
                skipped.append(i.Label)
                continue
            center = s.BoundBox.Center
            if lastCenter is not None and (center - lastCenter).Length < 1e-6:
                skipped.append(i.Label + " (duplicate position)")
                continue
            lastCenter = center
            a.append(s)
        if skipped:
            FreeCAD.Console.PrintWarning(
                "  " + str(obj.Label) + " : skin skipped " + str(len(skipped))
                + " degenerate rib(s): " + ", ".join(skipped)
                + " - check their Chord and the trailing-edge coverage.\n")
        if len(a) < 2:
            FreeCAD.Console.PrintWarning(
                "  " + str(obj.Label) + " : skin not built - fewer than 2 valid ribs remain.\n")
            return
        obj.Shape = CurvedShapes.makeSurfaceSolid(a, False)



    def makeRibs(self, obj, update):
        # obj.LeadingEdge, obj.traillingedge, obj.Path, obj.Hullcurves=[obj.leadingedge,obj.traillingedge]
        ribs = []
        if update==True :
            FreeCAD.Console.PrintMessage("MakeRibs update ------------------------------------\n")
            ribs=obj.Ribs
        else :
            FreeCAD.Console.PrintMessage("MakeRibs create ------------------------------------\n")
            FreeCAD.Console.PrintMessage("  Number of Hullcurves  : "+str(len(obj.Hullcurves))+ "\n")

            #--------------CurvesPathArray code--------------------------
            curvebox = FreeCAD.BoundBox(float("-inf"), float("-inf"), float("-inf"), float("inf"), float("inf"), float("inf"))
            for n in range(0, len(obj.Hullcurves)):
                cbbx = obj.Hullcurves[n].Shape.BoundBox
                if self.doScaleXYZ[n][0]:
                    if cbbx.XMin > curvebox.XMin: curvebox.XMin = cbbx.XMin
                    if cbbx.XMax < curvebox.XMax: curvebox.XMax = cbbx.XMax
                if self.doScaleXYZ[n][1]:
                    if cbbx.YMin > curvebox.YMin: curvebox.YMin = cbbx.YMin
                    if cbbx.YMax < curvebox.YMax: curvebox.YMax = cbbx.YMax
                if self.doScaleXYZ[n][2]:
                    if cbbx.ZMin > curvebox.ZMin: curvebox.ZMin = cbbx.ZMin
                    if cbbx.ZMax < curvebox.ZMax: curvebox.ZMax = cbbx.ZMax


                if len(obj.Hullcurves) > 0:
                    if curvebox.XMin == float("-inf"):
                        curvebox.XMin = obj.Hullcurves[0].Shape.BoundBox.XMin
                if curvebox.XMax == float("inf"):
                    curvebox.XMax = obj.Hullcurves[0].Shape.BoundBox.XMax
                if curvebox.YMin == float("-inf"):
                    curvebox.YMin = obj.Hullcurves[0].Shape.BoundBox.YMin
                if curvebox.YMax == float("inf"):
                    curvebox.YMax = obj.Hullcurves[0].Shape.BoundBox.YMax
                if curvebox.ZMin == float("-inf"):
                    curvebox.ZMin = obj.Hullcurves[0].Shape.BoundBox.ZMin
                if curvebox.ZMax == float("inf"):
                    curvebox.ZMax = obj.Hullcurves[0].Shape.BoundBox.ZMax

            edges = Part.__sortEdges__(obj.Path.Shape.Edges)
            leadingedge_edges = Part.__sortEdges__(obj.LeadingEdge.Shape.Edges) #leadingedge_edges=Part.sortEdges(obj.LeadingEdge.Shape.Edges)  # deprecated !

            FreeCAD.Console.PrintMessage("  Len of edges  : "+str(len(edges))+ "\n")
            FreeCAD.Console.PrintMessage("  Items         : "+str(int(obj.Items))+ "\n")

            maxlen=obj.LeadingEdge.Shape.Length

            # Space the stations over the span where the rib slice plane
            # actually crosses the trailing edge, trimmed by the user's
            # OffsetStart/OffsetEnd (see _teStationWindow). A station past
            # that window collapses to a zero chord.
            pmin = obj.OffsetStart
            pmax = maxlen - obj.OffsetEnd
            if edges:
                win = _teStationWindow(edges[0], leadingedge_edges[0], obj.TrailingEdge)
                if win is not None:
                    wlo, whi = max(win[0], 0.0), min(win[1], maxlen)
                    lo, hi = max(pmin, wlo), min(pmax, whi)
                    if hi - lo > epsilon:
                        pmin, pmax = lo, hi
                    elif whi - wlo > epsilon:
                        pmin, pmax = wlo, whi
                        FreeCAD.Console.PrintWarning(
                            "  " + str(obj.Label) + " : OffsetStart/OffsetEnd trim away the whole"
                            " span the trailing edge covers; stations re-spread over"
                            " [%.2f, %.2f].\n" % (wlo, whi))
                    # degenerate window: keep the offsets, every rib then
                    # trips the per-rib chord-skip warning below.

            # A plen past the positioning edge is clamped onto the edge end,
            # stacking ribs on one point - Part.makeLoft then dies on the
            # duplicate profiles. Spread the stations over the edge that
            # positions them instead.
            if edges and edges[0].Length < pmax:
                if edges[0].Length < pmax - epsilon:
                    FreeCAD.Console.PrintWarning(
                        "  " + str(obj.Label) + " : path sketch segment is shorter than the panel,"
                        " last rib moves inboard to its end at %.2f mm.\n" % edges[0].Length)
                pmax = edges[0].Length
                pmin = min(pmin, pmax)

            for n in range(0, int(obj.Items)):
                FreeCAD.Console.PrintMessage("  Rib number                 : --- "+str(n)+ " ---\n")
                plen = pmin
                if obj.Items > 1:
                    plen += (pmax - pmin) * n / (float(obj.Items) - 1)

                for edge in edges:
                    if plen > edge.Length:
                        plen = edge.Length
                    if plen > edge.Length:
                        print("  plen > edge.Length:")
                        #plen -= edge.Length
                    else:
                        param = edge.getParameterByLength(plen)
                        direction = edge.tangentAt(param) # path direction
                        posvec = edge.valueAt(param) #on path
                        posvec_path=edge.valueAt(param)

                        directionleadingedge = leadingedge_edges[0].tangentAt(param) # leadinedge direction
                        param_leadingedge = leadingedge_edges[0].getParameterByLength(plen)
                        posvec_leadingedge = leadingedge_edges[0].valueAt(param_leadingedge)

                        normal = CurvedShapes.getNormal(obj.Base) # get the rib normal
                        rotaxis = normal.cross(direction)

                        angle = math.degrees(normal.getAngle(direction))

                        planEdge=Part.makePlane(edge.Length,edge.Length,FreeCAD.Vector(0, 0, 0),direction).Faces[0]
                        FreeCAD.Console.PrintMessage("      planEdge             : "+str(planEdge)+ "\n")
                        uv = planEdge.Surface.parameter(posvec_path)
                        normaledge=planEdge.normalAt(uv[0], uv[1])
                        FreeCAD.Console.PrintMessage("  normaledge                 : --- "+str(normaledge)+ " ---\n")

                        planLeadingedge=Part.makePlane(leadingedge_edges[0].Length,leadingedge_edges[0].Length,FreeCAD.Vector(0, 0, 0),directionleadingedge)
                        FreeCAD.Console.PrintMessage("      planLeadingedge             : "+str(planLeadingedge)+ "\n")
                        uv = planLeadingedge.Surface.parameter(posvec_leadingedge)
                        normaLeadingedge=planLeadingedge.normalAt(uv[0], uv[1])
                        FreeCAD.Console.PrintMessage("  normaLeadingedge                 c: --- "+str(normaLeadingedge)+ " ---\n")

                        #l=Part.Line(FreeCAD.Vector(posvec_path),normaledge)
                        ##ll=Part.Line(FreeCAD.Vector(posvec_leadingedge),normaLeadingedge)

                        #point=l.intersect(normaLeadingedge)

                        #p=App.Vector(1,1,1)
                        #posvec_path.projectToPlane(App.Vector(0,0,0),App.Vector(1,0,1))
                        #point =normaLeadingedge.cross() #
                        point=FreeCAD.Vector(posvec_leadingedge.x,
                                             posvec_leadingedge.y,
                                             posvec_path.z)#math.sqrt(posvec.x*posvec.x+posvec.y*posvec.y))#posvec_path.projectToPlane(planLeadingedge)

                        #point=planLeadingedge.projectPoint.(FreeCAD.Vector(posvec_path))
                        FreeCAD.Console.PrintMessage("      Intercsection                 : --- "+str(point)+ " ---\n")
                        #normalleadingedge=leadingedge_edges[0].normalAt(param_leadingedge)
                        #A=DraftGeomUtils.findIntersection(normaledge,normalleadingedge)
                        #posvecrib=FreeCAD.Vector(posvec_leadingedge.x, posvec_leadingedge.y,posvec_path.z)
                        #posvecrib=FreeCAD.Vector(posvec_path.x, posvec_path.y,posvec_path.z)
                        posvecrib=FreeCAD.Vector(point.x, point.y,point.z)

                        if len(obj.Ribs) < obj.Items :

                              FreeCAD.Console.PrintMessage("      Rib normal             : "+str(normal)+ "\n")
                              FreeCAD.Console.PrintMessage("      Path Plen              : "+str(plen)+ "\n")
                              FreeCAD.Console.PrintMessage("      Path Param             : "+str(param)+ "\n")
                              FreeCAD.Console.PrintMessage("      Path Position          : "+str(posvec)+ "\n")
                              FreeCAD.Console.PrintMessage("      Path Direction         : "+str(direction)+ "\n")
                              FreeCAD.Console.PrintMessage("      Path doScaleXYZ        : "+str(self.doScaleXYZ)+ "\n")
                              FreeCAD.Console.PrintMessage("      LeadingEdge doScaleXYZ : "+str(self.doScaleXYZ)+ "\n")
                              FreeCAD.Console.PrintMessage("      Leading position       : "+str(posvec_leadingedge)+ "\n")
                              FreeCAD.Console.PrintMessage("      Path position          : "+str(posvec_path)+ "\n")
                              FreeCAD.Console.PrintMessage("      Rib Angle              : "+str(angle)+ "\n")
                              FreeCAD.Console.PrintMessage("      Rotaxis                : "+str(rotaxis )+ "\n")
                              FreeCAD.Console.PrintMessage("      Rotaxis.Length         : "+str(rotaxis.Length )+ "\n")
                              #plane = Part.Plane(posvecrib, direction)
                              #Part.show(plane)
                              #bbox = CurvedShapes.boundbox_from_intersect(obj.Hullcurves, posvecrib, direction, self.doScaleXYZ,False)

                              bbox = CurvedShapes.boundbox_from_intersect(obj.Hullcurves, posvec_leadingedge, direction, self.doScaleXYZ,False)
                              if  bbox:
                                    x,y,z,scalex,scaley,scalez=scaleByBoundbox2(obj.Base.Shape, bbox, self.doScaleXYZsum )
                                    if scalex < _minRibChord:
                                        # bbox collapsed onto one hull curve:
                                        # this plane missed the other (usually
                                        # the TE). Skip instead of lofting a
                                        # 1e-7 section.
                                        FreeCAD.Console.PrintWarning(
                                            "      Skipping rib "+str(n)+" of "+str(obj.Label)
                                            +" : chord "+str(scalex)+" mm at plen="
                                            +str(round(plen, 2))+" - the slice plane crossed the"
                                            " leading edge but not the trailing edge. Lengthen or"
                                            " shift the trailing-edge segment.\n")
                                        continue
                                    FreeCAD.Console.PrintMessage("      scalex"+str(scalex)+ " \n")
                                    FreeCAD.Console.PrintMessage("      scaley"+str(scaley)+ " \n")
                                    FreeCAD.Console.PrintMessage("      scalez"+str(scalez)+ " \n")
                                    chord=scalex
                                    # f = span fraction inside the actual rib
                                    # window [pmin,pmax], so offsets/TE-trim
                                    # do not skew the twist ramp
                                    fspan = (plen - pmin) / (pmax - pmin) if pmax > pmin else 0.0
                                    twist = float(obj.Twist) + float(obj.TipTwist) * fspan
                                    rib = self.createRib(obj,chord ,posvecrib, direction, rotaxis, angle, twist)# posvec_leadingedge
                                    if rib :
                                       FreeCAD.Console.PrintMessage("      Rib.Label         : "+str(rib.Label )+ "\n")
                                       ribs.append(rib)
                              else :
                                    FreeCAD.Console.PrintWarning(
                                        "      Rib "+str(n)+" of "+str(obj.Label)+" skipped : the"
                                        " slice plane at plen="+str(round(plen, 2))
                                        +" missed the hull curves entirely.\n")

        if len(ribs)>1 :
           FreeCAD.Console.PrintMessage("     Number of rib created : "+str(len(ribs))+"\n")
           # the ribs are still Touched (null Shape) and recompute() inside
           # execute() trips the recursion guard: build the shapes directly.
           # generateNaca ignores positional args, so carry the Placement.
           for _rib in ribs:
               if _rib.Shape.isNull():
                   from airPlaneAirFoilNaca import generateNaca
                   _face, _coords = generateNaca(
                       _rib.NacaProfil, _rib.NacaNbrPoint, _rib.finite_TE,
                       True, float(_rib.Chord), 0, 0, 0, 0, 0, 0, 0,
                       _rib.useSpline, _rib.splitSpline)
                   _face.Placement = _rib.Placement
                   _rib.Coordinates = _coords
                   _rib.Shape = _face
           # wingpshape lofts obj.Ribs: fresh ribs must be linked before the
           # loft or it sees an empty schedule and refuses
           if update==False :
               obj.Ribs=ribs
           self.wingpshape(obj)

        print("------------End of makeRibs function------------" )

    def execute(self, prop, update=True):
        print("wingPanel : Execute function")

        FreeCAD.Console.PrintMessage("  update  : "+str(update)+ "\n")

        # restored proxies never ran __init__ (nor, for old-format docs, __setstate__)
        self._adopt(prop)
        if not(self.obj.Ribs) :
            update=False
        else :
            update=True

        if prop.Base and prop.Axis == Vector(0.0,0.0,0.0):
            prop.Axis = CurvedShapes.getNormal(prop.Base)
            return

        self.doScaleXYZ = []
        self.doScaleXYZsum = [False, False, False]
        sumbbox = None   # empty Hullcurves left this unbound for `if sumbbox`
        # Pour le bord d'attaque et le bord de fuite calcul de la BoundBox
        for h in prop.Hullcurves:

            bbox = h.Shape.BoundBox

            if h == prop.Hullcurves[0]:
                sumbbox = bbox
            else:
                sumbbox.add(bbox)
            print(sumbbox)
            doScale = [False, False, False]

            #Détermine les axes où il est nécessaire de faire une mise à l'échelle.
            if bbox.XLength > epsilon:
                doScale[0] = True

            if bbox.YLength > epsilon:
                doScale[1] = True

            if bbox.ZLength > epsilon:
                doScale[2] = True

            self.doScaleXYZ.append(doScale)

        if sumbbox:
            if sumbbox.XLength > epsilon:
                self.doScaleXYZsum[0] = True

            if sumbbox.YLength > epsilon:
                self.doScaleXYZsum[1] = True

            if sumbbox.ZLength > epsilon:
                self.doScaleXYZsum[2] = True

        if prop.Items > 0  and len(prop.Hullcurves) > 0: #and prop.RootRib and hasattr(prop.RootRib, "Shape")
            self.makeRibs(prop,update)
            return

#--------------------------END---------------------------------------
# Code from CurvedShapes workbench adapted for Airplanedesign.
#__author__ = "Christian Bergmann"
#__license__ = "LGPL 2.1"
#
#-----------------------------------------------------------------


class ViewProviderPanel:
    def __init__(self, vobj):
        vobj.Proxy = self
        self.Object = vobj.Object

    def getIcon(self):
        return os.path.join(smWB_icons_path,'panel.xpm')

    def attach(self, vobj):
        self.Object = vobj.Object
        self.onChanged(vobj,"Base")

    def claimChildren(self):
        return [self.Object.Base]+[self.Object.Path]+[self.Object.LeadingEdge]+[self.Object.TrailingEdge]+self.Object.Ribs#+[self.Object.TipRib] + [self.Object.RootRib]

    def onDelete(self, feature, subelements):
        return True

    def onChanged(self, fp, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def dumps(self):
        return None

    def loads(self, state):
        return None

class CommandWPanel:
    "the WingPanel command definition"
    def GetResources(self):
        iconpath = os.path.join(smWB_icons_path,'panel.png')
        return {'Pixmap': iconpath, 'MenuText': QtCore.QT_TRANSLATE_NOOP("Create_a_wing_Panel","Create/Add a wing panel, select a panl and clic")}

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        b=[]
        selection = FreeCADGui.Selection.getSelectionEx()
        if selection :
           if len(selection)==4:
              base = FreeCAD.ActiveDocument.getObject((selection[0].ObjectName))
              b=base.WingPanels
              _rootRib=FreeCAD.ActiveDocument.getObject((selection[1].ObjectName))
              _path=FreeCAD.ActiveDocument.getObject((selection[2].ObjectName))
              base.WingEdges.append(_path)
              _envelope=FreeCAD.ActiveDocument.getObject((selection[3].ObjectName))
              base.WingEdges.append(_envelope)
              _leadingedge=FreeCAD.ActiveDocument.getObject((selection[3].ObjectName))# A netoyer en doublon
              wingsketch=FreeCAD.ActiveDocument.getObject((selection[3].ObjectName))
              # Separate leadInEdge & trailingEdge
              edges=Part.sortEdges(wingsketch.Shape.Edges) # Separate, #edges=Part.sortEdges(wingsketch.Shape.Edges) # deprecated ?
              paths=Part.__sortEdges__(_path.Shape.Edges)
              leadInEdges=edges[0]  #id the leading edge
              trailingEdges=edges[1]#id the trailing edge
              FreeCAD.Console.PrintMessage("Edges number : "+str(len(edges))+ "\n")
              if len(edges)!=2 :
                  FreeCAD.Console.PrintMessage("Edges must be 2 and not "+str(len(edges))+ "\n")
                  return

              nbOfPanels=len(leadInEdges)
              FreeCAD.Console.PrintMessage("-------------------- Wing Panel --------------------"+ "\n")
              FreeCAD.Console.PrintMessage("  Rib :"+str(_rootRib.Label)+ "\n")
              FreeCAD.Console.PrintMessage("  Wing :"+str(base.Label)+ "\n")
              FreeCAD.Console.PrintMessage("  Path :"+str(_path.Label)+ "\n")
              FreeCAD.Console.PrintMessage("  envelope :"+str(_envelope.Label)+ "\n")
              FreeCAD.Console.PrintMessage("  envelope placement:"+str(_envelope.Placement)+ "\n")
              FreeCAD.Console.PrintMessage("  Number of Panels :"+str(nbOfPanels)+ "\n")

              pmin=0
              pmax=0
              for i in range(0,nbOfPanels): # for each panel
                  pmin=0 #pmax
                  pmax=leadInEdges[i].Length
                  param = leadInEdges[i].getParameterByLength(pmin)
                  param2 = leadInEdges[i].getParameterByLength(pmax)
                  direction = leadInEdges[i].tangentAt(param)
                  posvec = leadInEdges[i].valueAt(param)
                  posvec2 = leadInEdges[i].valueAt(param2)

                  #normal = CurvedShapes.getNormal(obj.Base)
                  #rotaxis = normal.cross(direction)
                  #angle = math.degrees(normal.getAngle(direction))
                  bbox=leadInEdges[i].BoundBox
                  bbox2=trailingEdges[i].BoundBox

                  FreeCAD.Console.PrintMessage("  Panel n° "+str(i)+ " ------------------------\n")
                  FreeCAD.Console.PrintMessage("  leadInEdges id        :"+str(leadInEdges[i])+ "\n")
                  FreeCAD.Console.PrintMessage("  leadInEdges Length    :"+str(leadInEdges[i].Length)+ "\n")
                  FreeCAD.Console.PrintMessage("  trailingEdges id      :"+str(trailingEdges[i])+ "\n")
                  FreeCAD.Console.PrintMessage("  trailingEdges Length  :"+str(trailingEdges[i].Length)+ "\n")
                  FreeCAD.Console.PrintMessage("  direction             :"+str(direction)+ "\n")
                  FreeCAD.Console.PrintMessage("     pmin               : "+str(pmin)+ "\n")
                  FreeCAD.Console.PrintMessage("     Param              : "+str(param)+ "\n")
                  FreeCAD.Console.PrintMessage("     Position           : "+str(posvec)+ "\n")
                  FreeCAD.Console.PrintMessage("     Position2          : "+str(posvec2)+ "\n")
                  FreeCAD.Console.PrintMessage("     BoundBox leadInEdges   : "+str(bbox)+ "\n")
                  FreeCAD.Console.PrintMessage("     BoundBox trailingEdges   : "+str(bbox2)+ "\n")


                  FreeCADGui.activateWorkbench("DraftWorkbench")
                  plane = WorkingPlane.plane()
                  FreeCAD.DraftWorkingPlane = plane


                  #workplane = WorkingPlane.plane()
                  workplane = FreeCAD.DraftWorkingPlane
                  v1 = FreeCAD.Vector(0, 1, 0).normalize()#paths[i].tangentAt(param).normalize()
                  v2 = FreeCAD.Vector(0, 0, 1).normalize()
                  #workplane.alignToPointAndAxis(v1, v2, 0)

                  #FreeCAD.DraftWorkingPlane.alignToPointAndAxis(v1, v2, 0)
                  #FreeCADGui.Snapper.toggleGrid()

                  FreeCAD.Console.PrintMessage("     V1   : "+str(v1)+ "\n")
                  FreeCAD.Console.PrintMessage("     V2   : "+str(v2)+ "\n")

                 # workplane.alignToPointAndAxis( v1, v2, 0)
                  #FreeCADGui.Snapper.toggleGrid()
                  FreeCADGui.activeDocument().activeView().setCameraOrientation(_path.Placement.Rotation)

                  #paths[i].

                  FreeCAD.Console.PrintMessage("     pathline   : "+str(paths[i])+ "\n")
                  #pathline=Part.Line(paths[i].Geometry)

                  myObj0=Draft.makeSketch(paths[i], autoconstraints=True)
                  #myObj1=Part.Line(paths[i].Content)
                  myObj0.Label="path"+str(i)

                  vec=_envelope.Placement.Rotation
                  FreeCADGui.activeDocument().activeView().setCameraOrientation(vec)#(0,0,0,1))
                  myObj1=Draft.makeSketch(leadInEdges[i], 	name = "leadInEdges"+str(i), autoconstraints=True)
                  #myObj1=Part.Line()
                  myObj1.Label="leadInEdges"+str(i)

                  FreeCADGui.activeDocument().activeView().setCameraOrientation(vec)
                  myObj2=Draft.makeSketch(trailingEdges[i], autoconstraints=True)
                  myObj2.Label="trailingEdge"+str(i)

                  obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","WingPanel"+str(i))

                  WingPanel(obj,_rootRib,myObj0,_envelope,myObj1,myObj2,200,100,100,0,0)
                  #WingPanel(obj,_rootRib,_path,_envelope,myObj1,myObj2,200,100,100,0,0)
                  #WingPanel(obj,_rootRib,_path,_envelope,leadInEdges[i],trailingEdges[i],200,100,100,0,0)

                  #WingPanel(obj,_rootRib,_path,leadInEdges[i],trailingEdges[i],200,100,100,0,0)
                  ViewProviderPanel(obj.ViewObject)
                  b.append(obj)
                  FreeCAD.ActiveDocument.recompute()
           else :
              #---------------------création des nervures temporaires
              #_rootRib=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibRoot_")
              #WingRib(_rootRib,"/Users/fredericnivoix/Library/Preferences/FreeCAD/Mod/AirPlaneDesign/wingribprofil/naca/naca2412.dat",False,0,200,0,0,0,0,0,0)
              #ViewProviderWingRib(_rootRib.ViewObject)

              #_tipRib=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RibTip_")
              #WingRib(_tipRib,"/Users/fredericnivoix/Library/Preferences/FreeCAD/Mod/AirPlaneDesign/wingribprofil/naca/naca2412.dat",False,0,200,0,500,0,0,0,0)
              #ViewProviderWingRib(_tipRib.ViewObject)

              #----------

              obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","WingPanel")
              WingPanel(obj,None,None, None,None,None,200,100,100,0,0)
              ViewProviderPanel(obj.ViewObject)

        if selection : #selection==None :
           try :
               #b=base.WingPanels
               #b.append(obj)
               base.WingPanels=b
           except :
               print("The selection is not a wing")
        FreeCAD.Gui.activeDocument().activeView().viewAxonometric()
        FreeCAD.Gui.SendMsgToActiveView("ViewFit")


if FreeCAD.GuiUp:
    #register the FreeCAD command
    FreeCADGui.addCommand('airPlaneDesignWingPanel',CommandWPanel())
