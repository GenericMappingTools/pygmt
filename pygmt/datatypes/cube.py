"""
Wrapper for the GMT_CUBE data type.
"""

import ctypes as ctp
from typing import ClassVar

from pygmt.datatypes.header import (
    _GMT_GRID_HEADER,
    GMT_GRID_UNIT_LEN80,
    GMT_GRID_VARNAME_LEN80,
    gmt_grdfloat,
)


class _GMT_CUBE(ctp.Structure):  # noqa: N801
    """
    GMT cube data structure for 3-D data.

    The GMT_CUBE structure is a extension of the GMT_GRID structure to handle 3-D data
    cubes. It requires a 2-D grid header and extended parameters for the 3rd dimension.

    header->n_bands is used for the number of layers in 3-D cubes.
    """

    _fields_: ClassVar = [
        # Pointer to full GMT 2-D header for a layer (common to all layers)
        ("header", ctp.POINTER(_GMT_GRID_HEADER)),
        # Pointer to the gmt_grdfloat 3-D cube - a stack of 2-D padded grids
        ("data", ctp.POINTER(gmt_grdfloat)),
        # Vector of x coordinates common to all layers
        ("x", ctp.POINTER(ctp.c_double)),
        # Vector of y coordinates common to all layers
        ("y", ctp.POINTER(ctp.c_double)),
        # Low-level information for GMT use only
        ("hidden", ctp.c_void_p),
        # mode=GMT_CUBE_IS_STACK means the input dataset was a list of 2-D grids, rather
        # than a single cube.
        ("mode", ctp.c_uint),
        # Minimum/maximum z values (complements header->wesn[4])
        ("z_range", ctp.c_double * 2),
        # z increment (complements inc[2]) (0 if variable z spacing)
        ("z_inc", ctp.c_double),
        # Array of z values (complements x, y)
        ("z", ctp.POINTER(ctp.c_double)),
        # Name of the 3-D variable, if read from file (or empty if just one)
        ("name", ctp.c_char * GMT_GRID_VARNAME_LEN80),
        # Units in 3rd direction (complements x_units, y_units, z_units)
        ("units", ctp.c_char * GMT_GRID_UNIT_LEN80),
    ]
