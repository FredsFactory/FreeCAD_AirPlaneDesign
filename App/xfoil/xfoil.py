# -*- coding: utf-8 -*-
#   Copyright (c) 2019 D. de Vries
#
#   This file is part of XFoil.
#
#   XFoil is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   XFoil is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with XFoil.  If not, see <https://www.gnu.org/licenses/>.
import numpy as np
import ctypes
import os
import glob

from ctypes import c_bool, c_int, c_float, byref, POINTER, cdll
from shutil import copy2
from tempfile import NamedTemporaryFile

from .model import Airfoil

here = os.path.abspath(os.path.dirname(__file__))
lib_path = glob.glob(os.path.join(here, 'libxfoil.*'))[0]
lib_ext = lib_path[lib_path.rfind('.'):]

fptr = POINTER(c_float)
bptr = POINTER(c_bool)


class XFoil(object):
    """Interface to the XFoil Fortran routines.

    Attributes
    ----------
    airfoil
    Re
    M
    xtr
    n_crit
    max_iter
    """

    def __init__(self):
        super().__init__()
        tmp = NamedTemporaryFile(mode='wb', delete=False, suffix=lib_ext)
        tmp.close()
        self._lib_path = tmp.name
        copy2(lib_path, self._lib_path)
        self._lib = cdll.LoadLibrary(self._lib_path)
        self._lib.init()
        self._airfoil = None

        self._lib.get_print.restype = c_bool
        self._lib.get_reynolds.restype = c_float
        self._lib.get_mach.restype = c_float
        self._lib.get_n_crit.restype = c_float

    def __del__(self):
        handle = self._lib._handle
        del self._lib
        try:
            ctypes.windll.kernel32.FreeLibrary(handle)
        except AttributeError:
            pass
        finally:
            os.remove(self._lib_path)

    @property
    def print(self):
        """bool: True if console output should be shown."""
        return self._lib.get_print()

    @print.setter
    def print(self, value):
        self._lib.set_print(byref(c_bool(value)))

    @property
    def airfoil(self):
        """Airfoil: Instance of the Airfoil class."""
        n = self._lib.get_n_coords()
        x = np.asfortranarray(np.zeros(n), dtype=c_float)
        y = np.asfortranarray(np.zeros(n), dtype=c_float)
        self._lib.get_airfoil(x.ctypes.data_as(fptr), y.ctypes.data_as(fptr), byref(c_int(n)))
        return Airfoil(x.astype(float), y.astype(float))

    @airfoil.setter
    def airfoil(self, airfoil):
        self._airfoil = airfoil
        self._lib.set_airfoil(
            np.asfortranarray(airfoil.x.flatten(), dtype=c_float).ctypes.data_as(fptr),
            np.asfortranarray(airfoil.y.flatten(), dtype=c_float).ctypes.data_as(fptr),
            byref(c_int(airfoil.n_coords))
        )

    @property
    def Re(self):
        """float: Reynolds number."""
        return float(self._lib.get_reynolds())

    @Re.setter
    def Re(self, value):
        self._lib.set_reynolds(byref(c_float(value)))

    @property
    def M(self):
        """float: Mach number."""
        return float(self._lib.get_mach())

    @M.setter
    def M(self, value):
        self._lib.set_mach(byref(c_float(value)))

    @property
    def xtr(self):
        """tuple(float, float): Top and bottom flow trip x/c locations."""
        xtr_top = c_float()
        xtr_bot = c_float()
        self._lib.get_xtr(byref(xtr_top), byref(xtr_bot))
        return float(xtr_top), float(xtr_bot)

    @xtr.setter
    def xtr(self, value):
        self._lib.set_xtr(byref(c_float(value[0])), byref(c_float(value[1])))

    @property
    def n_crit(self):
        """float: Critical amplification ratio."""
        return float(self._lib.get_n_crit())

    @n_crit.setter
    def n_crit(self, value):
        self._lib.set_n_crit(byref(c_float(value)))

    @property
    def max_iter(self):
        """int: Maximum number of iterations."""
        return int(self._lib.get_max_iter())

    @max_iter.setter
    def max_iter(self, max_iter):
        self._lib.set_max_iter(byref(c_int(max_iter)))

    def naca(self, specifier):
        """Set a NACA 4 or 5 series airfoil.

        Parameters
        ----------
        specifier : string
            A NACA 4 or 5 series identifier, such as '2412'.
        """
        self._lib.set_naca(byref(c_int(int(specifier))))

    def reset_bls(self):
        """Reset the boundary layers to be reinitialized on the next analysis."""
        self._lib.reset_bls()

    def repanel(self, n_nodes=160, cv_par=1, cte_ratio=0.15, ctr_ratio=0.2, xt_ref=(1, 1), xb_ref=(1, 1)):
        """Re-panel airfoil.

        Parameters
        ----------
        n_nodes : int
            Number of panel nodes
        cv_par : float
            Panel bunching parameter
        cte_ratio : float
            TE/LE panel density ratio
        ctr_ratio : float
            Refined-area/LE panel density ratio
        xt_ref : tuple of two floats
            Top side refined area x/c limits
        xb_ref : tuple of two floats
            Bottom side refined area x/c limits
        """
        self._lib.repanel(byref(c_int(n_nodes)), byref(c_float(cv_par)),
                          byref(c_float(cte_ratio)), byref(c_float(ctr_ratio)),
                          byref(c_float(xt_ref[0])), byref(c_float(xt_ref[1])),
                          byref(c_float(xb_ref[0])), byref(c_float(xb_ref[1])))

    def filter(self, factor=0.2):
        """Filter surface speed distribution using modified Hanning filter.

        Parameters
        ----------
        factor : float
            Filter parameter. If set to 1, the standard, full Hanning filter is applied. Default is 0.2.
        """
        self._lib.filter(byref(c_float(factor)))

    def a(self, a):
        """Analyze airfoil at a fixed angle of attack.

        Parameters
        ----------
        a : float
            Angle of attack in degrees

        Returns
        -------
        cl, cd, cm, cp : float
            Corresponding values of the lift, drag, moment, and minimum pressure coefficients.
        """
        cl = c_float()
        cd = c_float()
        cm = c_float()
        cp = c_float()
        conv = c_bool()

        self._lib.alfa(byref(c_float(a)), byref(cl), byref(cd), byref(cm), byref(cp), byref(conv))

        return (cl.value, cd.value, cm.value, cp.value) if conv else (np.nan, np.nan, np.nan, np.nan)

    def cl(self, cl):
        """"Analyze airfoil at a fixed lift coefficient.

        Parameters
        ----------
        cl : float
            Lift coefficient

        Returns
        -------
        a, cd, cm, cp : float
            Corresponding values of the angle of attack, drag, moment, and minimum pressure coefficients.
        """
        a = c_float()
        cd = c_float()
        cm = c_float()
        cp = c_float()
        conv = c_bool()

        self._lib.cl(byref(c_float(cl)), byref(a), byref(cd), byref(cm), byref(cp), byref(conv))

        return (a.value, cd.value, cm.value, cp.value) if conv else (np.nan, np.nan, np.nan, np.nan)

    def aseq(self, a_start, a_end, a_step):
        """Analyze airfoil at a sequence of angles of attack.

        The analysis is done for the angles of attack given by range(a_start, a_end, a_step).

        Parameters
        ----------
        a_start, a_end, a_step : float
            Start, end, and increment angles for the range.

        Returns
        -------
        a, cl, cd, cm, co : np.ndarray
            Lists of angles of attack and their corresponding lift, drag, moment, and minimum pressure coefficients.
        """
        n = abs(int((a_end - a_start) / a_step))

        a = np.zeros(n, dtype=c_float)
        cl = np.zeros(n, dtype=c_float)
        cd = np.zeros(n, dtype=c_float)
        cm = np.zeros(n, dtype=c_float)
        cp = np.zeros(n, dtype=c_float)
        conv = np.zeros(n, dtype=c_bool)

        self._lib.aseq(byref(c_float(a_start)), byref(c_float(a_end)), byref(c_int(n)),
                       a.ctypes.data_as(fptr), cl.ctypes.data_as(fptr),
                       cd.ctypes.data_as(fptr), cm.ctypes.data_as(fptr),
                       cp.ctypes.data_as(fptr), conv.ctypes.data_as(bptr))

        isnan = np.logical_not(conv)
        a[isnan] = np.nan
        cl[isnan] = np.nan
        cd[isnan] = np.nan
        cm[isnan] = np.nan
        cp[isnan] = np.nan
        return a.astype(float), cl.astype(float), cd.astype(float), cm.astype(float), cp.astype(float)

    def cseq(self, cl_start, cl_end, cl_step):
        """Analyze airfoil at a sequence of lift coefficients.

        The analysis is done for the lift coefficients given by range(cl_start, cl_end, cl_step).

        Parameters
        ----------
        cl_start, cl_end, cl_step : float
            Start, end, and increment lift coefficients for the range.

        Returns
        -------
        a, cl, cd, cm, co : np.ndarray
            Lists of angles of attack and their corresponding lift, drag, moment, and minimum pressure coefficients.
        """
        n = abs(int((cl_end - cl_start) / cl_step))

        a = np.zeros(n, dtype=c_float)
        cl = np.zeros(n, dtype=c_float)
        cd = np.zeros(n, dtype=c_float)
        cm = np.zeros(n, dtype=c_float)
        cp = np.zeros(n, dtype=c_float)
        conv = np.zeros(n, dtype=c_bool)

        self._lib.cseq(byref(c_float(cl_start)), byref(c_float(cl_end)), byref(c_int(n)),
                       a.ctypes.data_as(fptr), cl.ctypes.data_as(fptr),
                       cd.ctypes.data_as(fptr), cm.ctypes.data_as(fptr),
                       cp.ctypes.data_as(fptr), conv.ctypes.data_as(bptr))

        isnan = np.logical_not(conv)
        a[isnan] = np.nan
        cl[isnan] = np.nan
        cd[isnan] = np.nan
        cm[isnan] = np.nan
        cp[isnan] = np.nan
        return a.astype(float), cl.astype(float), cd.astype(float), cm.astype(float), cp.astype(float)

    def get_cp_distribution(self):
        """Get the Cp distribution from the last converged point.

        Returns
        -------
        x : np.array
            X-coordinates
        cp : np.ndarray
            Pressure coefficients at the corresponding x-coordinates
        """
        n = self._lib.get_n_cp()
        x = np.zeros(n, dtype=c_float)
        cp = np.zeros(n, dtype=c_float)

        self._lib.get_cp(x.ctypes.data_as(fptr), cp.ctypes.data_as(fptr), byref(c_int(n)))
        return x.astype(float), cp.astype(float)
