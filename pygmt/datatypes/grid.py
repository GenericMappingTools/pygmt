"""
Wrapper for the GMT_GRID data type.
"""

import ctypes as ctp
from typing import ClassVar

import numpy as np
import xarray as xr
from pygmt.datatypes.header import _GMT_GRID_HEADER, gmt_grdfloat


class _GMT_GRID(ctp.Structure):  # noqa: N801
    """
    GMT grid structure for holding a grid and its header.

    This class is only meant for internal use and is not exposed to users. See the GMT
    source code gmt_resources.h for the original C structure definitions.

    Examples
    --------
    >>> from pygmt.clib import Session
    >>> with Session() as lib:
    ...     with lib.virtualfile_out(kind="grid") as voutgrd:
    ...         lib.call_module("read", ["@static_earth_relief.nc", voutgrd, "-Tg"])
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
        ...         lib.call_module("read", ["@static_earth_relief.nc", voutgrd, "-Tg"])
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
          * lat      (lat) float64... -23.5 -22.5 -21.5 -20.5 ... -12.5 -11.5 -10.5
          * lon      (lon) float64... -54.5 -53.5 -52.5 -51.5 -50.5 -49.5 -48.5 -47.5
        Attributes:
            Conventions:   CF-1.7
            title:         Produced by grdcut
            history:       grdcut @earth_relief_01d_p -R-55/-47/-24/-10 -Gstatic_ea...
            description:   Reduced by Gaussian Cartesian filtering (111.2 km fullwi...
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

        # Get dimensions and their attributes from the header.
        dims, dim_attrs = header.dims, header.dim_attrs
        # The coordinates, given as a tuple of the form (dims, data, attrs)
        coords = [
            (dims[0], self.y[: header.n_rows], dim_attrs[0]),
            (dims[1], self.x[: header.n_columns], dim_attrs[1]),
        ]

        # The data array without paddings
        pad = header.pad[:]
        data = np.reshape(self.data[: header.mx * header.my], (header.my, header.mx))[
            pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1]
        ]

        # Create the xarray.DataArray object
        grid = xr.DataArray(
            data, coords=coords, name=header.name, attrs=header.data_attrs
        )

        # Flip the coordinates and data if necessary so that coordinates are ascending.
        # `grid.sortby(list(grid.dims))` sometimes causes crashes.
        # The solution comes from https://github.com/pydata/xarray/discussions/6695.
        for dim in grid.dims:
            if grid[dim][0] > grid[dim][1]:
                grid = grid.isel({dim: slice(None, None, -1)})

        # Set GMT accessors.
        # Must put at the end, otherwise info gets lost after certain grid operations.
        grid.gmt.registration = header.registration
        grid.gmt.gtype = header.gtype
        return grid
