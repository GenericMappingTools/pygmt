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

    Examples
    --------
    >>> import numpy as np
    >>> from pygmt import which
    >>> from pygmt.clib import Session
    >>> cubefile = which("@cube.nc", download="c")
    >>> with Session() as lib:
    ...     with lib.virtualfile_out(kind="cube") as voutcube:
    ...         lib.call_module("read", [cubefile, voutcube, "-Tu", "-Vd"])
    ...         # Read the cube from the virtual file
    ...         cube = lib.read_virtualfile(vfname=voutcube, kind="cube").contents
    ...         # The cube header
    ...         header = cube.header.contents
    ...         # Access the header properties
    ...         print(header.n_rows, header.n_columns, header.registration)
    ...         print(header.wesn[:], header.inc[:])
    ...         print(header.z_scale_factor, header.z_add_offset)
    ...         print(header.x_units, header.y_units, header.z_units)
    ...         print(header.nm, header.size, header.complex_mode)
    ...         print(header.type, header.n_bands, header.mx, header.my)
    ...         print(header.pad[:])
    ...         print(header.mem_layout, header.xy_off)
    ...         # Cube-specific attributes.
    ...         print(cube.mode, cube.z_range[:], cube.z_inc, cube.name, cube.units)
    ...         # The x, y, and z coordinates
    ...         x = cube.x[: header.n_columns]
    ...         y = cube.y[: header.n_rows]
    ...         z = cube.z[: header.n_bands]
    ...         # The data array (with paddings)
    ...         data = np.reshape(
    ...             cube.data[: header.n_bands * header.mx * header.my],
    ...             (header.my, header.mx, header.n_bands),
    ...         )
    ...         # The data array (without paddings)
    ...         pad = header.pad[:]
    ...         data = data[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1], :]
    11 11 0
    [0.0, 10.0, 0.0, 10.0] [1.0, 1.0]
    1.0 0.0
    b'x' b'y' b'cube'
    121 226 0
    18 4 15 15
    [2, 2, 2, 2]
    b'' 0.0
    0 [1.0, 5.0] 0.0 b'' b'z'
    >>> x
    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    >>> y
    [10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0]
    >>> z
    [1.0, 2.0, 3.0, 5.0]
    >>> data.shape
    (11, 11, 4)
    >>> #data.min(), data.max()  # The min/max are wrong. Upstream bug?
    >>> #(-29.399999618530273, 169.39999389648438)
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
