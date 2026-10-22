#################################################
#
# Cavity void creation - Aircraft
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

"""
Headless cavity-wall offset for lofted wings.

offsetProfileCoords() is pure math: it takes a closed ordered section (the
exact output of generateNacaCoords, or plain (x, z) chord-normalised tuples
from a .dat import) and returns the inward normal offset chains of the inner
(cavity) profile.  offsetSectionWire() wraps one station in Part,
makeCavityVoid() lofts a root->tip schedule into the cavity void solid.

No FreeCADGui, no PySide, no side effects at import - the module is usable
from freecadcmd scripts and the workbench alike, with no registration.

Why the inner wire is THREE edges (upper spline, lower spline, blunt trailing
edge line) and never one periodic spline through the nose U-turn: that
interpolant rings into the wall (measured 2-40 mm) and it is the wire type
OCC integrates wrongly.  Why the wall is MEASURED and not assumed: the spline
interpolant cuts toward the skin by an amount that depends on the point set,
so offsetSectionWire() asks the exact geometry for the deficit and adds it
back, bounded.
"""

__title__="FreeCAD airPlaneCavity"
__author__ = "RedxHerring"
__url__ = "https://fredsfactory.fr"


import FreeCAD,Part

from math import cos
from math import hypot
from math import pi


def _profilePoints(coords):
    """
    Normalise a closed ordered section to plain (x, z) chord-fraction pairs.

    Accepts the output of generateNacaCoords (FreeCAD.Vector(x, 0, z)) or
    plain (x, z) tuples in the same convention: trailing edge first, upper
    surface to the nose, lower surface back to the trailing edge.  A
    duplicated closing point (coords[0] == coords[-1] at a sharp trailing
    edge, what generateNacaCoords produces) is dropped: the offset walks the
    loop with modular neighbours and a seam duplicate would zero one tangent.
    """
    pts = []
    for p in coords:
        if hasattr(p, "x"):
            pts.append((float(p.x), float(p.z)))
        else:
            pts.append((float(p[0]), float(p[1])))
    if len(pts) > 1 and abs(pts[0][0] - pts[-1][0]) < 1e-12 \
            and abs(pts[0][1] - pts[-1][1]) < 1e-12:
        pts.pop()
    if len(pts) < 4:
        raise ValueError("section has %d points, too few to offset" % len(pts))
    return pts


def _signedArea(pts):
    """
    Shoelace area of the closed (u, v) loop: positive counter-clockwise.
    The winding is MEASURED, never assumed - a .dat import may come either way.
    """
    area = 0.0
    n = len(pts)
    for i in range(n):
        u0, v0 = pts[i]
        u1, v1 = pts[(i + 1) % n]
        area += u0 * v1 - u1 * v0
    return 0.5 * area


def _cosResample(pts, n):
    """
    Arc-length resample of an open polyline with COSINE point density
    (endpoints kept): spacing is fine at both ends of the chain and coarse in
    the middle.  Applied per surface, that concentrates points at the nose
    crown and at the tail - the two high-curvature ends of the inner profile.
    Deterministic, stdlib.
    """
    seg = [hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
           for i in range(len(pts) - 1)]
    total = sum(seg) or 1.0
    out, acc, i = [pts[0]], 0.0, 0
    for k in range(1, n):
        target = total * 0.5 * (1.0 - cos(pi * k / (n - 1)))
        while i < len(seg) - 1 and acc + seg[i] < target:
            acc += seg[i]
            i += 1
        f = 0.0 if seg[i] == 0.0 else (target - acc) / seg[i]
        out.append((pts[i][0] + f * (pts[i + 1][0] - pts[i][0]),
                    pts[i][1] + f * (pts[i + 1][1] - pts[i][1])))
    return out


def _popCrossed(up, low):
    """
    Drop tail points where the two offset chains cross each other.

    Near a sharp trailing edge the wedge angle is shallow, so an inward normal
    offset pushes the chains through each other (upper below lower) and a
    naive offset self-intersects there.  Both chains run tail->nose and are
    trimmed in lockstep from index 0 while the upper head sits at or below
    the lower head; the caller closes the opening with one blunt inner
    trailing-edge segment.

    The rule is chain-vs-chain (not camber-line-vs-chain as in the NACA-only
    ancestor), so camber needs no special case.  It is exact for STATION-PAIRED
    surface sets: both chains derive from the SAME closed loop, so for the
    usual section convention (both surfaces sampled from one chordwise station
    distribution - the NACA generator and typical .dat files) index i of one
    and index i of the other are the two surfaces of one station, and the
    comparison is station-paired by construction - symmetric for a symmetric
    section, with no interpolation to fight the non-monotonic normal-offset
    hook at the seam.  An import whose surfaces are NOT station-paired (e.g.
    one surface sampled far coarser than the other) can leave a stranded head
    inside the wedge; it then fails LOUDLY - the measured-gap loop of
    offsetSectionWire() raises ValueError rather than shipping a thin wall.
    """
    if len(up) > 1 and len(low) > 1 and up[0][1] <= low[0][1]:
        up.pop(0)  # the sharp-TE seam point sits on the chord between the two
                   # chains and is a station of its own: popped alone, else
                   # every later pair is off by one surface point
    while len(up) > 1 and len(low) > 1 and up[0][1] <= low[0][1]:
        up.pop(0)
        low.pop(0)


def offsetProfileCoords(coords, chord, wall, nPts=41):
    """
    Cavity-wall inward normal offset of a closed section - pure math, no Part.

    coords  closed ordered chord-normalised section: the exact output of
            generateNacaCoords, or plain (x, z) tuples in the same convention
            (trailing edge first, upper surface to the nose, lower surface
            back to the trailing edge).
    chord   millimetres.  wall  the normal offset in millimetres - a
            proportional thickness reduction is NOT a wall, its gap collapses
            to ~0 at the nose and tail.
    nPts    resample points per surface (cosine spacing, dense at both
            high-curvature ends).

    Returns (upper, lower) as (u, v) millimetre pairs in the section plane
    with the quarter-chord point as origin: upper runs trailing edge -> nose,
    lower runs nose -> trailing edge, and lower[0] is upper[-1] (the nose
    point is shared, which is what closes the caller's wire).  Tail points
    where the two offset chains cross are popped; the blunt inner trailing
    edge is left open for the caller (see offsetSectionWire).

    Raises ValueError if the wall swallows the section or nPts is too small
    to resample a surface.
    """
    if nPts < 4:
        raise ValueError("nPts %d too small to resample a surface" % nPts)
    pts = _profilePoints(coords)
    if _signedArea(pts) < 0.0:
        pts.reverse()  # clockwise input: the inward normal sign is chosen
                       # from the measured winding, never assumed
    # A flipped import reversed back is CCW but trailing-edge-LAST; rotate so
    # the loop starts at the aftmost point, restoring the trailing-edge-first
    # convention the surface split and the station pairing rely on.  For a
    # canonical section this is the identity (ties pick the first, upper TE).
    start = max(range(len(pts)), key=lambda i: pts[i][0])
    pts = pts[start:] + pts[:start]
    n = len(pts)
    nose = min(range(n), key=lambda i: pts[i][0])
    mm = [((xi - 0.25) * chord, zeta * chord) for xi, zeta in pts]
    up, low = [], []
    for i in range(n):
        tu = mm[(i + 1) % n][0] - mm[i - 1][0]
        tv = mm[(i + 1) % n][1] - mm[i - 1][1]
        ln = hypot(tu, tv) or 1.0
        # inward normal of the counter-clockwise loop = (-tv, tu)
        pnt = (mm[i][0] - wall * tv / ln, mm[i][1] + wall * tu / ln)
        (up if i <= nose else low).append(pnt)
    low = [up[-1]] + low  # share the nose point
    lowR = low[::-1]      # both chains tail->nose for the pop rule
    _popCrossed(up, lowR)
    low = lowR[::-1]
    if len(up) < 2 or len(low) < 2:
        raise ValueError("wall %.0f mm swallows the section - the inner "
                         "profile collapses to %d/%d points, no cavity is "
                         "possible at this wall thickness"
                         % (wall, len(up), len(low)))
    return _cosResample(up, nPts), _cosResample(low, nPts)


def _to3d(uv, placement):
    """Section-plane (u, v) mm -> 3D point (chord along +x, thickness along
    +z, quarter-chord origin), mapped by placement when given."""
    p = FreeCAD.Vector(uv[0], 0.0, uv[1])
    return placement.multVec(p) if placement is not None else p


def _outerWire(pts, chord, placement):
    """
    Reference outer wire of a station: closed polygon through the profile
    points.  Deliberately NOT a periodic single-edge B-spline - that wire type
    is what OCC integrates wrongly.  The polygon is the raw truth of the
    input schedule, which is what the wall measurement must answer to.
    """
    mm = [((xi - 0.25) * chord, zeta * chord) for xi, zeta in pts]
    pts3 = [_to3d(p, placement) for p in mm]
    return Part.makePolygon(pts3 + [pts3[0]])


def offsetSectionWire(coords, chord, wall, placement=None, nPts=41):
    """
    One cavity station as a closed 3-EDGE Part.Wire: upper-surface spline,
    lower-surface spline, blunt inner trailing-edge line.  Never a single
    periodic spline through the nose U-turn (see the module docstring).

    placement maps the section plane (chord along +x, thickness along +z,
    quarter-chord origin) into 3D; None keeps the wire in the x-z plane.

    The wall is BUILT MEASURED, not assumed: the spline interpolant cuts
    toward the outer profile by an amount that depends on the point set, so
    the wire is built at `wall`, the gap outerWire.distToShape(innerWire) is
    asked how far the interpolant actually cut, and the deficit is added back
    (plus a 0.05 mm convergence nudge), at most 3 passes.  These anchors are
    the measured ones from the source project - do not tighten them toward
    epsilon.

    Raises ValueError if the wall swallows the section, or if the measured
    gap stays below the wall after 3 passes.
    """
    pts = _profilePoints(coords)
    outer = _outerWire(pts, chord, placement)
    built = wall
    gap = 0.0
    for _ in range(3):
        up, low = offsetProfileCoords(coords, chord, built, nPts)
        splineUp = Part.BSplineCurve()
        splineUp.interpolate([_to3d(p, placement) for p in up])
        splineLow = Part.BSplineCurve()
        splineLow.interpolate([_to3d(p, placement) for p in low])
        wire = Part.Wire([splineUp.toShape(), splineLow.toShape(),
                          Part.makeLine(_to3d(low[-1], placement),
                                        _to3d(up[0], placement))])
        gap = outer.distToShape(wire)[0]
        if gap >= wall:
            return wire
        built += wall - gap + 0.05
    raise ValueError("station wall %.0f mm not reached after 3 measured "
                     "passes: gap %.2f mm (built at %.2f mm)"
                     % (wall, gap, built))


def makeCavityVoid(schedule, wall, nPts=41):
    """
    Loft the cargo cavity void solid.

    schedule  [(coords, chord, placement), ...] root -> tip; coords as in
              offsetProfileCoords, chord in millimetres, placement carries the
              spanwise position and the twist about the (baked) quarter-chord
              origin.
    wall, nPts  see offsetProfileCoords.

    Returns Part.makeLoft(wires, True, False) - the cavity void solid, ready
    to cut from the wing envelope.  Every station wire has the identical
    3-edge structure, which is what makes the loft succeed.
    """
    wires = [offsetSectionWire(coords, chord, wall, placement, nPts)
             for coords, chord, placement in schedule]
    return Part.makeLoft(wires, True, False)
