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


class Airfoil(object):
    """Airfoil

    Attributes
    ----------
    n_coords
    x
    y
    """

    def __init__(self, x, y):
        super().__init__()
        self.coords = np.ndarray((0, 2))
        self.x = x
        self.y = y

    @property
    def n_coords(self):
        """int: Number of coordinates which define the airfoil surface."""
        return self.coords.shape[0]

    @property
    def x(self):
        """np.ndarray: List of x-coordinates of the airfoil surface."""
        return self.coords[:, 0]

    @x.setter
    def x(self, value):
        v = value.flatten()
        self.coords = np.resize(self.coords, (v.size, 2))
        self.coords[:, 0] = v[:]

    @property
    def y(self):
        """np.ndarray: List of y-coordinates of the airfoil surface."""
        return self.coords[:, 1]

    @y.setter
    def y(self, value):
        v = value.flatten()
        self.coords = np.resize(self.coords, (v.size, 2))
        self.coords[:, 1] = v[:]
