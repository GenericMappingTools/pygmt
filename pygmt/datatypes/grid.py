"""
Wrapper for the GMT_GRID data type and the GMT_GRID_HEADER data structure.
"""

import ctypes as ctp
from typing import ClassVar

import numpy as np
import xarray as xr

# Constants for lengths of grid header variables.
#
# Note: Ideally we should be able to get these constants from the GMT shared library
# using the ``lib["GMT_GRID_UNIT_LEN80"]`` syntax, but it causes cyclic import error.
# So we have to hardcode the values here.
GMT_GRID_UNIT_LEN80 = 80
GMT_GRID_TITLE_LEN80 = 80
GMT_GRID_COMMAND_LEN320 = 320
GMT_GRID_REMARK_LEN160 = 160

# GMT uses single-precision for grids by default, but can be built to use
# double-precision. Currently, only single-precision is supported.
gmt_grdfloat = ctp.c_float


class _GMT_GRID_HEADER(ctp.Structure):  # noqa: N801
    """
    GMT grid header structure for metadata about the grid.

    The class is used in the `GMT_GRID`/`GMT_IMAGE`/`GMT_CUBE` data structure. See the
    GMT source code gmt_resources.h for the original C structure definitions.
    """

    _fields_: ClassVar = [
        # Number of columns
        ("n_columns", ctp.c_uint32),
        # Number of rows
        ("n_rows", ctp.c_uint32),
        # Grid registration, 0 for gridline and 1 for pixel
        ("registration", ctp.c_uint32),
        # Minimum/maximum x and y coordinates
        ("wesn", ctp.c_double * 4),
        # Minimum z value
        ("z_min", ctp.c_double),
        # Maximum z value
        ("z_max", ctp.c_double),
        # x and y increments
        ("inc", ctp.c_double * 2),
        # Grid values must be multiplied by this factor
        ("z_scale_factor", ctp.c_double),
        # After scaling, add this offset
        ("z_add_offset", ctp.c_double),
        # Units in x-directions, in the form "long_name [units]"
        ("x_units", ctp.c_char * GMT_GRID_UNIT_LEN80),
        # Units in y-direction, in the form "long_name [units]"
        ("y_units", ctp.c_char * GMT_GRID_UNIT_LEN80),
        # Grid value units, in the form "long_name [units]"
        ("z_units", ctp.c_char * GMT_GRID_UNIT_LEN80),
        # Name of data set
        ("title", ctp.c_char * GMT_GRID_TITLE_LEN80),
        # Name of generating command
        ("command", ctp.c_char * GMT_GRID_COMMAND_LEN320),
        # Comments for this data set
        ("remark", ctp.c_char * GMT_GRID_REMARK_LEN160),
        # Below are items used internally by GMT
        # Number of data points (n_columns * n_rows) [paddings are excluded]
        ("nm", ctp.c_size_t),
        # Actual number of items (not bytes) required to hold this grid (mx * my),
        # per band (for images)
        ("size", ctp.c_size_t),
        # Bits per data value (e.g., 32 for ints/floats; 8 for bytes).
        # Only used for ERSI ArcInfo ASCII Exchange grids.
        ("bits", ctp.c_uint),
        # For complex grid.
        # 0 for normal
        # GMT_GRID_IS_COMPLEX_REAL = real part of complex grid
        # GMT_GRID_IS_COMPLEX_IMAG = imag part of complex grid
        ("complex_mode", ctp.c_uint),
        # Grid format
        ("type", ctp.c_uint),
        # Number of bands [1]. Used with GMT_IMAGE containers
        ("n_bands", ctp.c_uint),
        # Actual x-dimension in memory. mx = n_columns + pad[0] + pad[1]
        ("mx", ctp.c_uint),
        # Actual y-dimension in memory. my = n_rows + pad[2] + pad[3]
        ("my", ctp.c_uint),
        # Paddings on west, east, south, north sides [2,2,2,2]
        ("pad", ctp.c_uint * 4),
        # Three or four char codes T|B R|C S|R|S (grd) or B|L|P + A|a (img)
        # describing array layout in mem and interleaving
        ("mem_layout", ctp.c_char * 4),
        # Missing value as stored in grid file
        ("nan_value", gmt_grdfloat),
        # 0.0 for gridline grids and 0.5 for pixel grids
        ("xy_off", ctp.c_double),
        # Referencing system string in PROJ.4 format
        ("ProjRefPROJ4", ctp.c_char_p),
        # Referencing system string in WKT format
        ("ProjRefWKT", ctp.c_char_p),
        # Referencing system EPSG code
        ("ProjRefEPSG", ctp.c_int),
        # Lower-level information for GMT use only
        ("hidden", ctp.c_void_p),
    ]


def _parse_nameunits(nameunits: str) -> tuple[str, str | None]:
    """
    Get long_name and units attributes from x_units/y_units/z_units in grid header.

    In GMT grid header, the x_units/y_units/z_units are strings in the form of
    ``long_name [units]``, in which both ``long_name`` and ``units`` and standard
    netCDF attributes defined by CF conventions. The ``[units]`` part is optional.

    This function parses the x_units/y_units/z_units string and get the ``long_name``
    and ``units`` attributes.

    Parameters
    ----------
    nameunits
        The x_units/y_units/z_units string in grid header.

    Returns
    -------
    (long_name, units)
        Tuple of netCDF attributes 'long_name' and 'units'. 'units' may be None.

    Examples
    --------
    >>> _parse_nameunits("longitude [degrees_east]")
    ('longitude', 'degrees_east')
    >>> _parse_nameunits("latitude [degrees_north]")
    ('latitude', 'degrees_north')
    >>> _parse_nameunits("x")
    ('x', None)
    >>> _parse_nameunits("y")
    ('y', None)
    >>>
    """
    parts = nameunits.split("[")
    long_name = parts[0].strip()
    units = parts[1].strip("]").strip() if len(parts) > 1 else None
    return long_name, units


def _parse_header(header: _GMT_GRID_HEADER) -> tuple[tuple, dict, int, int]:
    """
    Get dimension names, attributes and grid type from the grid header.

    For a 2D grid, the dimension names are set to "x", "y", and "z" by default.
    The attributes for each dimension are parsed from the grid header following
    GMT conventions.

    The last dimension is special and is the data variable name, and the attributes
    for this dimension are global attributes for the grid.

    The grid is assumed to be Cartesian by default. If the x and y units are
    "degrees_east" and "degrees_north", respectively, then the grid is assumed to be
    geographic.

    Parameters
    ----------
    header
        The grid header structure.

    Returns
    -------
    dims : tuple
        The dimension names with the last dimension for the data variable.
    attrs : dict
        The attributes for each dimension.
    registration : int
        The grid registration. 0 for gridline and 1 for pixel.
    gtype : int
        The grid type. 0 for Cartesian grid and 1 for geographic grid.
    """
    # Default dimension names. The last dimension is for the data.
    dims = ("x", "y", "z")
    nameunits = (header.x_units, header.y_units, header.z_units)

    # Dictionary for dimension attributes with the dimension name as the key.
    attrs: dict = {dim: {} for dim in dims}
    # Dictionary for mapping the default dimension names to the actual names.
    newdims = {dim: dim for dim in dims}
    # Loop over dimensions and get the dimension name and attribute from header
    for dim, nameunit in zip(dims, nameunits, strict=False):
        # The long_name and units attributes.
        long_name, units = _parse_nameunits(nameunit.decode())
        if long_name:
            attrs[dim]["long_name"] = long_name
        if units:
            attrs[dim]["units"] = units

        # "degrees_east"/"degrees_north" are the units for geographic coordinates
        # following CF-conventions
        if units == "degrees_east":
            attrs[dim]["standard_name"] = "longitude"
            newdims[dim] = "lon"
        elif units == "degrees_north":
            attrs[dim]["standard_name"] = "latitude"
            newdims[dim] = "lat"

        # Axis attribute are "X"/"Y"/"Z"/"T" for horizontal/vertical/time axis.
        # The codes here may not work for 3-D grids.
        if dim == dims[-1]:  # The last dimension is the data.
            attrs[dim]["actual_range"] = np.array([header.z_min, header.z_max])
        else:
            attrs[dim]["axis"] = dim.upper()
            idx = dims.index(dim) * 2
            attrs[dim]["actual_range"] = np.array(header.wesn[idx : idx + 2])

    # Cartesian or Geographic grid
    gtype = 0
    if (
        attrs[dims[0]].get("standard_name") == "longitude"
        and attrs[dims[1]].get("standard_name") == "latitude"
    ):
        gtype = 1
    # Registration
    registration = header.registration

    # Update the attributes dictionary with new dimension names as keys
    attrs = {newdims[dim]: attrs[dim] for dim in dims}
    # Update the dimension names
    dims = tuple(newdims[dim] for dim in dims)
    return dims, attrs, registration, gtype


class _GMT_GRID(ctp.Structure):  # noqa: N801
    """
    GMT grid structure for holding a grid and its header.

    The class is only meant for internal use and is not exposed to users. See the GMT
    source code gmt_resources.h for the original C structure definitions.

    Examples
    --------
    >>> from pygmt.clib import Session
    >>> with Session() as lib:
    ...     with lib.virtualfile_out(kind="grid") as voutgrd:
    ...         lib.call_module("read", f"@static_earth_relief.nc {voutgrd} -Tg")
    ...         # Read the grid from the virtual file
    ...         grid = lib.read_virtualfile(voutgrd, kind="grid").contents
    ...         # The grid header
    ...         header = grid.header.contents
    ...         # Access the header properties
    ...         print(header.n_rows, header.n_columns, header.registration)
    ...         print(header.wesn[:], header.z_min, header.z_max, header.inc[:])
    ...         print(header.z_scale_factor, header.z_add_offset)
    ...         print(header.x_units, header.y_units, header.z_units)
    ...         print(header.title)
    ...         print(header.command)
    ...         print(header.remark)
    ...         print(header.nm, header.size, header.complex_mode)
    ...         print(header.type, header.n_bands, header.mx, header.my)
    ...         print(header.pad[:])
    ...         print(header.mem_layout, header.nan_value, header.xy_off)
    ...         # The x and y coordinates
    ...         print(grid.x[: header.n_columns])
    ...         print(grid.y[: header.n_rows])
    ...         # The data array (with paddings)
    ...         data = np.reshape(
    ...             grid.data[: header.mx * header.my], (header.my, header.mx)
    ...         )
    ...         # The data array (without paddings)
    ...         pad = header.pad[:]
    ...         data = data[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1]]
    ...         print(data)
    14 8 1
    [-55.0, -47.0, -24.0, -10.0] 190.0 981.0 [1.0, 1.0]
    1.0 0.0
    b'longitude [degrees_east]' b'latitude [degrees_north]' b'elevation (m)'
    b'Produced by grdcut'
    b'grdcut @earth_relief_01d_p -R-55/-47/-24/-10 -Gstatic_earth_relief.nc'
    b'Reduced by Gaussian Cartesian filtering (111.2 km fullwidth) from ...'
    112 216 0
    18 1 12 18
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
        # Pointer to full GMT header for grid
        ("header", ctp.POINTER(_GMT_GRID_HEADER)),
        # Pointer to grid data
        ("data", ctp.POINTER(gmt_grdfloat)),
        # Pointer to x coordinate vector
        ("x", ctp.POINTER(ctp.c_double)),
        # Pointer to y coordinate vector
        ("y", ctp.POINTER(ctp.c_double)),
        # Low-level information for GMT use only
        ("hidden", ctp.c_void_p),
    ]

    def to_dataarray(self) -> xr.DataArray:
        """
        Convert a _GMT_GRID object to a :class:`xarray.DataArray` object.

        Returns
        -------
        dataarray
            A :class:`xr.DataArray` object.

        Examples
        --------
        >>> from pygmt.clib import Session
        >>> with Session() as lib:
        ...     with lib.virtualfile_out(kind="grid") as voutgrd:
        ...         lib.call_module("read", f"@static_earth_relief.nc {voutgrd} -Tg")
        ...         # Read the grid from the virtual file
        ...         grid = lib.read_virtualfile(voutgrd, kind="grid")
        ...         # Convert to xarray.DataArray and use it later
        ...         da = grid.contents.to_dataarray()
        >>> da  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        <xarray.DataArray 'z' (lat: 14, lon: 8)>...
        array([[347.5, 344.5, 386. , 640.5, 617. , 579. , 646.5, 671. ],
               [383. , 284.5, 344.5, 394. , 491. , 556.5, 578.5, 618.5],
               [373. , 367.5, 349. , 352.5, 419.5, 428. , 570. , 667.5],
               [557. , 435. , 385.5, 345.5, 413.5, 496. , 519.5, 833.5],
               [561.5, 539. , 446.5, 481.5, 439.5, 553. , 726.5, 981. ],
               [310. , 521.5, 757. , 570.5, 538.5, 524. , 686.5, 794. ],
               [521.5, 682.5, 796. , 886. , 571.5, 638.5, 739.5, 881.5],
               [308. , 595.5, 555.5, 556. , 580. , 770. , 927. , 920. ],
               [601. , 526.5, 535. , 299. , 398.5, 645. , 797.5, 964. ],
               [494.5, 488.5, 357. , 254.5, 286. , 484.5, 653.5, 930. ],
               [450.5, 395.5, 366. , 248. , 250. , 354.5, 550. , 797.5],
               [345.5, 320. , 335. , 292. , 207.5, 247. , 325. , 346.5],
               [349. , 313. , 325.5, 247. , 191. , 225. , 260. , 452.5],
               [347.5, 331.5, 309. , 282. , 190. , 208. , 299.5, 348. ]])
        Coordinates:
          * lon      (lon) float64... -54.5 -53.5 -52.5 -51.5 -50.5 -49.5 -48.5 -47.5
          * lat      (lat) float64... -23.5 -22.5 -21.5 -20.5 ... -12.5 -11.5 -10.5
        Attributes:
            long_name:     elevation (m)
            actual_range:  [190. 981.]
        >>> da.coords["lon"]  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        <xarray.DataArray 'lon' (lon: 8)>...
        array([-54.5, -53.5, -52.5, -51.5, -50.5, -49.5, -48.5, -47.5])
        Coordinates:
          * lon      (lon) float64... -54.5 -53.5 -52.5 -51.5 -50.5 -49.5 -48.5 -47.5
        Attributes:
            long_name:      longitude
            units:          degrees_east
            standard_name:  longitude
            axis:           X
            actual_range:   [-55. -47.]
        >>> da.coords["lat"]  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        <xarray.DataArray 'lat' (lat: 14)>...
        array([-23.5, -22.5, -21.5, -20.5, -19.5, -18.5, -17.5, -16.5, -15.5, -14.5,
            -13.5, -12.5, -11.5, -10.5])
        Coordinates:
          * lat      (lat) float64... -23.5 -22.5 -21.5 -20.5 ... -12.5 -11.5 -10.5
        Attributes:
            long_name:      latitude
            units:          degrees_north
            standard_name:  latitude
            axis:           Y
            actual_range:   [-24. -10.]
        >>> da.gmt.registration, da.gmt.gtype
        (1, 1)
        """
        # The grid header
        header = self.header.contents

        # The dimension names, attributes and grid registration and type
        dims, attrs, registration, gtype = _parse_header(header)

        # The x and y coordinates
        coords = {dims[0]: self.x[: header.n_columns], dims[1]: self.y[: header.n_rows]}

        # The data array without paddings
        pad = header.pad[:]
        data = np.reshape(self.data[: header.mx * header.my], (header.my, header.mx))[
            pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1]
        ]

        # Create the xarray.DataArray object
        grid = xr.DataArray(
            data, coords=coords, dims=dims[1::-1], name=dims[-1], attrs=attrs[dims[-1]]
        )
        # Assign coordinate attributes
        for dim in grid.dims:
            grid[dim].attrs.update(attrs[dim])

        # Flip the coordinates and data if necessary so that coordinates are ascending.
        # `grid.sortby(list(grid.dims))` sometimes causes crashes.
        # The solution comes from https://github.com/pydata/xarray/discussions/6695.
        for dim in grid.dims:
            if grid[dim][0] > grid[dim][1]:
                grid = grid.isel({dim: slice(None, None, -1)})

        # Set the gmt accesssor.
        # Must put at the end. The information get lost after specific grid operation.
        grid.gmt.registration = registration
        grid.gmt.gtype = gtype
        return grid
