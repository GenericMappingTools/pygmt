"""
Wrapper for the GMT_GRID data type.
"""

import ctypes as ctp
from typing import ClassVar

import numpy as np
import xarray as xr

# from pygmt.clib.session import Session

# # Lengths of grid header variables
# with Session() as lib:
#     GMT_GRID_UNIT_LEN80 = lib["GMT_GRID_UNIT_LEN80"]
#     GMT_GRID_TITLE_LEN80 = lib["GMT_GRID_TITLE_LEN80"]
#     GMT_GRID_COMMAND_LEN320 = lib["GMT_GRID_COMMAND_LEN320"]
#     GMT_GRID_REMARK_LEN160 = lib["GMT_GRID_REMARK_LEN160"]
# Ideally we should be able to get the lengths of grid header variables
# from GMT shared library, but it cause cyclic import error.
# So we hardcode the values here.
GMT_GRID_UNIT_LEN80 = 80
GMT_GRID_TITLE_LEN80 = 80
GMT_GRID_COMMAND_LEN320 = 320
GMT_GRID_REMARK_LEN160 = 160

# GMT uses single-precision for grids by default, but can be built to use
# double-precision. Currently, only single-precision is supported.
gmt_grdfloat = ctp.c_float


class _GMT_GRID_HEADER(ctp.Structure):  # noqa: N801
    """
    Structure for GMT grid header.

    See
    https://docs.generic-mapping-tools.org/dev/devdocs/api.html#gmt-grid
    for definition.
    """

    _fields_: ClassVar = [
        # items stored in grids
        ("n_columns", ctp.c_uint32),  # number of columns
        ("n_rows", ctp.c_uint32),  # number of rows
        ("registration", ctp.c_uint32),  # grid registration (0 or 1)
        ("wesn", ctp.c_double * 4),  # minimum/maximum x and y coordinates
        ("z_min", ctp.c_double),  # minimum z value
        ("z_max", ctp.c_double),  # maximum z value
        ("inc", ctp.c_double * 2),  # x and y increments
        ("z_scale_factor", ctp.c_double),  # grid values must be multiplied by this
        ("z_add_offset", ctp.c_double),  # after scaling, add this
        ("x_units", ctp.c_char * GMT_GRID_UNIT_LEN80),  # units in x-direction
        ("y_units", ctp.c_char * GMT_GRID_UNIT_LEN80),  # units in y-direction
        ("z_units", ctp.c_char * GMT_GRID_UNIT_LEN80),  # grid value units
        ("title", ctp.c_char * GMT_GRID_TITLE_LEN80),  # name of data set
        ("command", ctp.c_char * GMT_GRID_COMMAND_LEN320),  # name of generating command
        ("remark", ctp.c_char * GMT_GRID_REMARK_LEN160),  # comments for this data set
        # items used internally by GMT
        # number of data points (n_columns * n_rows) [padding is excluded]
        ("nm", ctp.c_size_t),
        # actual number of items (not bytes) required to hold this grid (mx * my)
        ("size", ctp.c_size_t),
        ("bits", ctp.c_uint),  # bits per data value
        # complex grid
        # 0 for normal
        # GMT_GRID_IS_COMPLEX_REAL = real part of complex grid
        # GMT_GRID_IS_COMPLEX_IMAG = imag part of complex grid
        ("complex_mode", ctp.c_uint),
        ("type", ctp.c_uint),  # grid format
        ("n_bands", ctp.c_uint),  # number of bands [1]
        ("mx", ctp.c_uint),  # actual x-dimension in memory, allowing for padding
        ("my", ctp.c_uint),  # actual y-dimension in memory, allowing for padding
        ("pad", ctp.c_uint * 4),  # padding on west, east, south, north sides [2,2,2,2]
        # Three or four char codes T|B R|C S|R|S (grd) or B|L|P + A|a (img)
        # describing array layout in mem and interleaving
        ("mem_layout", ctp.c_char * 4),
        ("nan_value", gmt_grdfloat),  # missing value as stored in grid file
        ("xy_off", ctp.c_double),  # 0.0 for gridline grid and 0.5 for pixel grid
        ("ProjRefPROJ4", ctp.c_char_p),  # referencing system string in PROJ.4 format
        ("ProjRefWKT", ctp.c_char_p),  # referencing system string in WKT format
        ("ProjRefEPSG", ctp.c_int),  # referencing system EPSG code
        ("hidden", ctp.c_void_p),  # lower-level information for GMT use only
    ]


class _GMT_GRID(ctp.Structure):  # noqa: N801
    """
    Structure for GMT grid.

    See https://docs.generic-mapping-tools.org/dev/devdocs/api.html#gmt-grid
    for definition.

    Examples
    --------

    Here is an example showing how to access the data and metadata in a GMT_GRID object.

    >>> with Session() as lib:
    ...     # create a virtual file for output
    ...     with lib.virtualfile_out(kind="grid") as vfile:
    ...         # read in a grid file and output to the virtual file
    ...         lib.call_module("read", f"@static_earth_relief.nc {vfile} -Tg")
    ...         # read the data in the virtual file
    ...         # and cast the data into a pointer to _GMT_GRID
    ...         grid_pointer = ctp.cast(
    ...             lib.read_virtualfile(vfile), ctp.POINTER(GMT_GRID)
    ...         )
    ...         # get the contents of the grid and header
    ...         grid = grid_pointer.contents  # a GMT_GRID object
    ...         header = grid.header.contents  # a GMT_GRID_HEADER object
    ...         # access the header properties
    ...         print(header.n_rows, header.n_columns, header.registration)
    ...         print(header.wesn[:], header.z_min, header.z_max, header.inc[:])
    ...         print(header.z_scale_factor, header.z_add_offset)
    ...         print(header.x_units, header.y_units, header.z_units)
    ...         print(header.title)
    ...         print(header.command)
    ...         print(header.remark)
    ...         print(header.nm, header.type, header.n_bands)
    ...         print(header.mx, header.my)
    ...         print(header.pad[:])
    ...         print(header.mem_layout, header.nan_value, header.xy_off)
    ...         # access the x, y arrays
    ...         print(grid.x[: header.n_columns])
    ...         print(grid.y[: header.n_rows])
    ...         # access the data array (with paddings)
    ...         pad = header.pad[:]
    ...         data = np.reshape(
    ...             grid.data[: header.mx * header.my], (header.my, header.mx)
    ...         )[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1]]
    ...         print(data)
    14 8 1
    [-55.0, -47.0, -24.0, -10.0] 190.0 981.0 [1.0, 1.0]
    1.0 0.0
    b'longitude [degrees_east]' b'latitude [degrees_north]' b'elevation (m)'
    b'Produced by grdcut'
    b'grdcut @earth_relief_01d_p -R-55/-47/-24/-10 -Gstatic_earth_relief.nc'
    b'Reduced by Gaussian Cartesian filtering (111.2 km fullwidth) from ...'
    112 18 1
    12 18
    [2, 2, 2, 2]
    b'' nan 0.5
    [-54.5, -53.5, -52.5, -51.5, -50.5, -49.5, -48.5, -47.5]
    [-10.5, -11.5, -12.5, -13.5, -14.5, -15.5, ..., -22.5, -23.5]
    [[347.5 331.5 309.  282.  190.  208.  299.5 348. ]
    [349.  313.  325.5 247.  191.  225.  260.  452.5]
    [345.5 320.  335.  292.  207.5 247.  325.  346.5]
    [450.5 395.5 366.  248.  250.  354.5 550.  797.5]
    [494.5 488.5 357.  254.5 286.  484.5 653.5 930. ]
    [601.  526.5 535.  299.  398.5 645.  797.5 964. ]
    [308.  595.5 555.5 556.  580.  770.  927.  920. ]
    [521.5 682.5 796.  886.  571.5 638.5 739.5 881.5]
    [310.  521.5 757.  570.5 538.5 524.  686.5 794. ]
    [561.5 539.  446.5 481.5 439.5 553.  726.5 981. ]
    [557.  435.  385.5 345.5 413.5 496.  519.5 833.5]
    [373.  367.5 349.  352.5 419.5 428.  570.  667.5]
    [383.  284.5 344.5 394.  491.  556.5 578.5 618.5]
    [347.5 344.5 386.  640.5 617.  579.  646.5 671. ]]
    """

    _fields_: ClassVar = [
        ("header", ctp.POINTER(_GMT_GRID_HEADER)),  # pointer to grid header
        ("data", ctp.POINTER(gmt_grdfloat)),  # pointer to grid data
        ("x", ctp.POINTER(ctp.c_double)),  # pointer to x coordinate vector
        ("y", ctp.POINTER(ctp.c_double)),  # pointer to y coordinate vector
        ("hidden", ctp.c_void_p),  # low-level information for GMT use only
    ]

    def to_dataarray(self):
        """
        Convert a GMT_GRID object to a xarray.DataArray object.
        """
        header = self.header.contents
        pad = header.pad[:]
        x = self.x[: header.n_columns]
        y = self.y[: header.n_rows]
        data = np.array(self.data[: header.mx * header.my]).reshape(
            (header.my, header.mx)
        )[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1]]
        if x[0] > x[1]:
            x = list(reversed(x))
            data = np.fliplr(data)
        if y[0] > y[1]:
            y = list(reversed(y))
            data = np.flipud(data)
        grid = xr.DataArray(data, coords=[y, x], dims=["lat", "lon"])
        grid.name = "z"
        grid.gmt.registration = header.registration
        # Determine the gtype property based on x and y units.
        # This is a temporary workaround and may not work for all cases.
        if (
            header.x_units == b"longitude [degrees_east]"
            and header.y_units == b"latitude [degrees_north]"
        ):
            grid.gmt.gtype = 1
        else:
            grid.gmt.gtype = 0
        return grid
