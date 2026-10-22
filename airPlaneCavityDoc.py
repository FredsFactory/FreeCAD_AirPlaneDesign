#################################################
#
# Cavity void creation - Aircraft (document builder)
#
# Copyright (c) RedxHerring - 2026 - V0.1
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

"""Qt-free builder between the GUI panel and the airPlaneCavity core.

buildSchedule() turns the panel's wing parameters into the per-station
schedule the core consumes; buildCavityShapes() turns a params dict into
(outer, void, shell) shapes.  Importable under freecadcmd - no PySide,
no FreeCADGui, ever (tests/testCavitySchedule.py pins that).
"""
__title__ = "FreeCAD airPlaneCavityDoc"
__author__ = "RedxHerring"
__url__ = "https://fredsfactory.fr"

import FreeCAD
import Part

import airPlaneCavity
from airPlaneAirFoilNaca import generateNacaCoords


def buildSchedule(number, rootChordMm, taper, spanMm, tipTwistDeg, tipSweepMm,
                  nOuter=40):
    """
    Three-station root->tip schedule for airPlaneCavity.makeCavityVoid().

    Chords: root, (1+taper)/2*root (linear taper midpoint), taper*root.
    y, twist and sweep are distributed linearly 0 -> half -> full across
    the three stations.  spanMm is the ROOT->TIP distance of this
    half-wing model (y = 0 .. spanMm); tipSweepMm is the leading-edge
    offset of the tip, negative = forward sweep.

    Each placement Base IS the station's quarter-chord point (the core's
    section-plane origin) and its Rotation is the twist about +y.
    """
    coords = generateNacaCoords(number, nOuter, False, True,
                                1, 0, 0, 0, 0, 0, 0)
    midChord = 0.5 * rootChordMm * (1.0 + taper)
    stations = [(0.0, rootChordMm, 0.0, 0.0),
                (0.5 * spanMm, midChord, 0.5 * tipTwistDeg, 0.5 * tipSweepMm),
                (spanMm, taper * rootChordMm, tipTwistDeg, tipSweepMm)]
    return [(coords, chord,
             FreeCAD.Placement(FreeCAD.Vector(sweep, y, 0.0),
                               FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0),
                                                twist)))
            for y, chord, twist, sweep in stations]


def planformAreaMm2(rootChordMm, taper, spanMm):
    """Trapezoid planform area (mm^2) of the half-wing; with the linear
    midpoint chord this is exact for the lofted schedule."""
    return 0.5 * (rootChordMm + taper * rootChordMm) * spanMm


def buildCavityShapes(params):
    """
    params dict -> (outer, void, shell) shapes.

    Keys: number, rootChord, span, taper, tipTwist, tipSweep, wall, nPts.
    The GUI panel's params() is the production producer; tests build the
    dict by hand.  Raises the core's plain ValueErrors (bad wall swallows
    the section, nPts too small) - the caller decides how to surface them.
    """
    schedule = buildSchedule(params["number"], params["rootChord"],
                             params["taper"], params["span"],
                             params["tipTwist"], params["tipSweep"])
    wires = []
    for coords, chord, pl in schedule:
        pts = [pl.multVec(FreeCAD.Vector((p.x - 0.25) * chord, 0.0,
                                         p.z * chord))
               for p in coords]
        if pts[0].sub(pts[-1]).Length < 1e-9:
            pts.pop()
        wires.append(Part.makePolygon(pts + [pts[0]]))
    outer = Part.makeLoft(wires, True, False)
    void = airPlaneCavity.makeCavityVoid(schedule, params["wall"],
                                         params["nPts"])
    return outer, void, outer.cut(void)


# ---------------------------------------------------------------------------
# Phase B: cavity an EXISTING APD wing/panel (selection path).
#
# Detection is TypeId + property-presence duck-typing ONLY - proxies do not
# survive document reload, properties do.  airPlaneRib / airPlaneWPanel /
# airPlaneSWPanel are deliberately NOT imported (they drag in PySide/numpy);
# the rib contract probed here is the property set airPlaneRib.py:59-72
# creates: Coordinates (unit-chord section points from the LEADING EDGE -
# generateNacaCoords ignores its scale/pos args, and the shipped .dat
# profiles are unit chord), Chord (mm), RibProfil/NacaProfil.
# ---------------------------------------------------------------------------

def _isRibObj(obj):
    """Duck-type: an APD WingRib carries Coordinates + Chord."""
    return (obj is not None and hasattr(obj, "Coordinates")
            and hasattr(obj, "Chord"))


def classifySelection(obj):
    """
    (kind, why) for a selected document object; kind in
    {"wing", "panel", "rib", "other"}.  "why" is always non-empty and is
    the refusal text for the non-cavityable kinds.
    """
    if obj is not None and obj.isDerivedFrom("Part::FeaturePython"):
        if hasattr(obj, "WingPanels"):
            return ("wing", "APD wing carrying %d WingPanel(s)"
                    % len(obj.WingPanels))
        root = getattr(obj, "RootRib", None)
        tip = getattr(obj, "TipRib", None)
        if _isRibObj(root) and _isRibObj(tip):
            return ("panel", "wizard wing panel with RootRib/TipRib "
                    "schedule")
        ribs = getattr(obj, "Ribs", None)
        if ribs and len(ribs) >= 2 and all(_isRibObj(r) for r in ribs):
            return ("panel", "curved wing panel with a %d-rib schedule"
                    % len(ribs))
        if _isRibObj(obj) and (hasattr(obj, "RibProfil")
                               or hasattr(obj, "NacaProfil")):
            return ("rib", "a single rib is a section, not a volume to "
                    "shell - select the wing panel or wing it belongs to")
    return ("other", "no APD rib schedule on '%s' (%s): this command "
            "shells APD wings/panels whose ribs store the section "
            "schedule; an arbitrary imported solid has no recoverable "
            "schedule" % (getattr(obj, "Label", obj),
                          getattr(obj, "TypeId", type(obj).__name__)))


def stationFromRib(rib):
    """
    Rib document object -> (coords, chord, placement) core station.

    THE conversion: a rib's Placement origin is the LEADING EDGE, the core
    wants the QUARTER-CHORD origin:
        base' = base + rot.multVec(Vector(0.25 * chord, 0, 0))
    Coordinates pass through unchanged (unit chord from the LE, matching
    the core's coords convention) - but the unit-chord invariant is
    CHECKED first (see below), so a rib populated with mm-scaled or
    truncated Coordinates raises instead of silently mis-scaling.
    Pinned by tests/testCavityDoc.py.
    """
    coords = list(rib.Coordinates)
    chord = float(rib.Chord)
    if not coords:
        raise ValueError("rib '%s' has no section Coordinates (recompute "
                         "it or check its airfoil source)" % rib.Label)
    if chord <= 0.0:
        raise ValueError("rib '%s' has non-positive Chord %.3f mm"
                         % (rib.Label, chord))
    # unit-chord invariant: BOTH producers of rib Coordinates -
    # generateNacaCoords (x in [0,1] by construction) and readpointsonfile
    # (its filter forces -0.01 < x < 1.01) - yield x-extent ~1.0 with
    # x >= -0.01.  mm-scaled Coordinates span ~chord in mm (hundreds to
    # thousands) and truncated fragments span a fraction, so the band is
    # deliberately loose and order-of-magnitude based: reject only extent
    # outside [0.5, 1.5] or x below -0.01 (mirrors readpointsonfile's
    # tolerance; the x-max bound is implied by extent <= 1.5 and x >=
    # -0.01).  Camber, thickness and TE rounding past 1.0 never trip it.
    xs = [v.x for v in coords]
    xMin = min(xs)
    extent = max(xs) - xMin
    if not (0.5 <= extent <= 1.5) or xMin < -0.01:
        raise ValueError(
            "rib '%s': section Coordinates must be chord-normalised (unit "
            "chord from the leading edge, x in [0,1]); got x-extent %.3f "
            "(x from %.3f to %.3f) - check this rib's airfoil source"
            % (rib.Label, extent, xMin, max(xs)))
    pl = rib.Placement
    base = pl.Base + pl.Rotation.multVec(FreeCAD.Vector(0.25 * chord,
                                                        0.0, 0.0))
    return coords, chord, FreeCAD.Placement(base, pl.Rotation)


def panelSchedule(panel):
    """
    Panel document object -> root->tip schedule for makeCavityVoid().

    Wizard WingSPanel: 2 stations (RootRib, TipRib).  Curved WingPanel:
    one station per entry, in Ribs-list order.  Raises a named ValueError
    when no schedule is recoverable.
    """
    root = getattr(panel, "RootRib", None)
    tip = getattr(panel, "TipRib", None)
    if _isRibObj(root) and _isRibObj(tip):
        return [stationFromRib(root), stationFromRib(tip)]
    ribs = getattr(panel, "Ribs", None)
    if ribs:
        if len(ribs) < 2:
            raise ValueError("panel '%s' has only %d rib(s); a loft needs "
                             "at least 2 stations" % (panel.Label,
                                                      len(ribs)))
        missing = [r.Label for r in ribs if not _isRibObj(r)]
        if missing:
            raise ValueError("panel '%s' Ribs list entries without a rib "
                             "schedule: %s" % (panel.Label,
                                               ", ".join(missing)))
        return [stationFromRib(r) for r in ribs]
    raise ValueError("no recoverable rib schedule on '%s' (%s): expected "
                     "RootRib/TipRib or a Ribs list"
                     % (panel.Label, panel.TypeId))


def addCavityObjects(doc, outer, void, shell, label_prefix=None):
    """
    Create the three cavity Part::Features with the canonical lifecycle
    defaults; returns them in order (HollowShell, CavityVoid, OuterSkin).

    Lifecycle rationale (the ONE place to read it): HollowShell alone IS
    the part - outer.cut(void) keeps the full outer surface; CavityVoid is
    kept but hidden for later reuse as a CFD fluid domain; OuterSkin is
    created hidden, not deleted - undo/transaction stays clean and
    un-hiding it is an instant x-ray.

    label_prefix qualifies the labels for multi-panel builds (e.g.
    "HollowShell (WingPanel001)") so per-panel objects stay distinguishable;
    None keeps the plain demo labels.  ViewObject writes are guarded so
    this stays headless-safe.
    """
    suffix = " (%s)" % label_prefix if label_prefix else ""
    created = []
    for name, label, shape, visible, color, transp in (
            ("Shell", "HollowShell" + suffix, shell, True,
             (0.20, 0.50, 0.90), 0),
            ("CavityVoid", "CavityVoid" + suffix, void, False,
             (1.00, 0.20, 0.20), 0),
            ("Skin", "OuterSkin" + suffix, outer, False,
             (0.80, 0.80, 0.80), 70)):
        obj = doc.addObject("Part::Feature", name)
        obj.Label = label
        obj.Shape = shape
        obj.Visibility = visible
        if obj.ViewObject:  # headless-safe
            obj.ViewObject.ShapeColor = color
            obj.ViewObject.Transparency = transp
        created.append(obj)
    return created


def addCavityToPanel(doc, panel, wall, nPts=41):
    """
    Cut a cavity void out of panel.Shape and add HollowShell / CavityVoid /
    OuterSkin Part::Feature objects (labels qualified with the panel's
    Label, so multi-panel wings stay readable).  The parametric panel
    itself is NOT modified or deleted.  Same lifecycle defaults as the demo
    path (see addCavityObjects).  Returns the created objects.

    STALE ON EDIT: the created objects are STATIC Part::Features while
    WingSPanel.execute rewrites the panel Shape on every recompute - after
    editing a panel's chord/twist/profile, delete the three objects and
    re-run the command to recreate the cavity.

    Coords: the void is built from the ribs' document-level Placements and
    cut against panel.Shape (which carries the panel's own Placement) -
    correct for APD's flat object structure, where the panel loft is built
    from the rib wires in that same frame (airPlaneSWPanel.execute).
    """
    schedule = panelSchedule(panel)
    void = airPlaneCavity.makeCavityVoid(schedule, wall, nPts)
    outer = panel.Shape
    if outer.isNull():
        raise ValueError("panel '%s' has no shape (recompute it first)"
                         % panel.Label)
    shell = outer.cut(void)
    return addCavityObjects(doc, outer, void, shell,
                            label_prefix=panel.Label)


# wizard "Cavity wall" table cell (mm implicit, like the sibling columns)
# -> cavity decision (Phase C).  Lives here (Qt-free) so the wing wizard
# and tests/testCavityWizard.py share one implementation; the dialog itself
# only reads the cell text.
_SOLID_CELLS = ("", "n/a", "na", "-", "none")


def parseCavityCell(txt):
    """
    Cell text -> None (SOLID panel, the default) or a wall thickness in mm.

    Empty / N/A / na / - / none (case-insensitive) -> None.  A number > 0
    -> float.  Anything else (garbage, zero, negative) raises ValueError so
    the wizard can warn-and-continue: invalid text leaves the panel solid,
    it never aborts the build and never cavities a panel by accident.
    """
    t = (txt or "").strip().lower()
    if t in _SOLID_CELLS:
        return None
    try:
        wall = float(t)
    except ValueError:
        raise ValueError("invalid cavity wall %r: enter a number > 0 (mm) "
                         "or N/A for a solid panel" % txt)
    if wall <= 0.0:
        raise ValueError("invalid cavity wall %.3g mm: must be > 0 (or N/A "
                         "for a solid panel)" % wall)
    return wall
