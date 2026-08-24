"""
Wrapper for the GMT_CUBE data type.
"""

import ctypes as ctp
from typing import ClassVar

import numpy as np
import xarray as xr
from pygmt.datatypes.header import (
    _GMT_GRID_HEADER,
    GMT_GRID_UNIT_LEN80,
    GMT_GRID_VARNAME_LEN80,
    _parse_nameunits,
    gmt_grdfloat,
)


class _GMT_CUBE(ctp.Structure):  # ruff: ignore[invalid-class-name]
    """
    GMT cube data structure for 3-D data.

    The GMT_CUBE structure is a extension of the GMT_GRID structure to handle 3-D data
    cubes. It requires a 2-D grid header and extended parameters for the 3rd dimension.

    ``header->n_bands`` is used for the number of layers in 3-D cubes.

    The ``data`` array is a stack of 2-D padded layers, i.e., layer ``k`` starts at
    offset ``k * header.size``. Note that ``header.size`` is the allocated length of one
    padded layer, which can exceed ``header.my * header.mx``.

    Examples
    --------
    >>> import numpy as np
    >>> from pygmt import which
    >>> from pygmt.clib import Session
    >>> from pygmt.datatypes import _GMT_CUBE
    >>> cubefile = which("@cube.nc", download="c")
    >>> with Session() as lib:
    ...     with lib.virtualfile_out(kind="cube") as voutcube:
    ...         lib.call_module("read", [cubefile, voutcube, "-Tu"])
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
    ...         x = np.ctypeslib.as_array(cube.x, shape=(header.n_columns,)).copy()
    ...         y = np.ctypeslib.as_array(cube.y, shape=(header.n_rows,)).copy()
    ...         z = np.ctypeslib.as_array(cube.z, shape=(header.n_bands,)).copy()
    ...         # The data array (one padded layer per row)
    ...         data = np.ctypeslib.as_array(
    ...             cube.data, shape=(header.n_bands, header.size)
    ...         ).copy()
    ...         # Reshape the layers to 2-D and strip the paddings
    ...         pad = header.pad[:]
    ...         data = data[:, : header.my * header.mx].reshape(
    ...             header.n_bands, header.my, header.mx
    ...         )
    ...         data = data[:, pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1]]
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
    array([ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10.])
    >>> y
    array([10.,  9.,  8.,  7.,  6.,  5.,  4.,  3.,  2.,  1.,  0.])
    >>> z
    array([1., 2., 3., 5.])
    >>> data.shape
    (4, 11, 11)
    >>> print(data.min(), data.max())
    0.0 140.0
    >>> # GMT stores rows north-first, so row 0 is y=10 and the last row is y=0.
    >>> print(data[0, :, :])
    [[  0.  10.  20.  30.  40.  50.  60.  70.  80.  90. 100.]
     [  0.   9.  18.  27.  36.  45.  54.  63.  72.  81.  90.]
     [  0.   8.  16.  24.  32.  40.  48.  56.  64.  72.  80.]
     [  0.   7.  14.  21.  28.  35.  42.  49.  56.  63.  70.]
     [  0.   6.  12.  18.  24.  30.  36.  42.  48.  54.  60.]
     [  0.   5.  10.  15.  20.  25.  30.  35.  40.  45.  50.]
     [  0.   4.   8.  12.  16.  20.  24.  28.  32.  36.  40.]
     [  0.   3.   6.   9.  12.  15.  18.  21.  24.  27.  30.]
     [  0.   2.   4.   6.   8.  10.  12.  14.  16.  18.  20.]
     [  0.   1.   2.   3.   4.   5.   6.   7.   8.   9.  10.]
     [  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]]
    >>> # The northernmost row of every layer. The four layers are the same X*Y grid
    >>> # scaled by 1.0, 1.1, 1.2, and 1.4, respectively.
    >>> print(data[:, 0, :])
    [[  0.  10.  20.  30.  40.  50.  60.  70.  80.  90. 100.]
     [  0.  11.  22.  33.  44.  55.  66.  77.  88.  99. 110.]
     [  0.  12.  24.  36.  48.  60.  72.  84.  96. 108. 120.]
     [  0.  14.  28.  42.  56.  70.  84.  98. 112. 126. 140.]]
    >>> # Verify that layer k equals scale[k] * outer(y, x) for every element.
    >>> scale = [1.0, 1.1, 1.2, 1.4]
    >>> expected = np.array([s * np.outer(y, x) for s in scale], dtype=np.float32)
    >>> np.allclose(data, expected)
    True
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

    def _parse_dimension(self) -> tuple[str, dict]:
        """
        Get the name and attributes of the 3rd dimension.

        Unlike the x/y dimensions, the 3rd dimension is described by the cube itself
        rather than by the 2-D grid header. ``self.units`` holds the dimension's
        "long_name [units]" string, and ``self.z_range`` its actual range.
        """
        attrs: dict = {}
        long_name, units = _parse_nameunits(self.units.decode())
        if long_name:
            attrs["long_name"] = long_name
        if units:
            attrs["units"] = units
        attrs["axis"] = "Z"
        attrs["actual_range"] = np.array(self.z_range[:])
        return "z", attrs

    def to_xarray(self) -> xr.DataArray:
        """
        Convert a _GMT_CUBE object to a :class:`xarray.DataArray` object.

        Returns
        -------
        dataarray
            A 3-D :class:`xr.DataArray` object with dimensions ordered as
            (3rd dimension, y, x).

        Examples
        --------
        >>> import numpy as np
        >>> from pygmt import which
        >>> from pygmt.clib import Session
        >>> cubefile = which("@cube.nc", download="c")
        >>> with Session() as lib:
        ...     with lib.virtualfile_out(kind="cube") as voutcube:
        ...         lib.call_module("read", [cubefile, voutcube, "-Tu"])
        ...         # Read the cube from the virtual file
        ...         cube = lib.read_virtualfile(voutcube, kind="cube")
        ...         # Convert to xarray.DataArray and use it later
        ...         da = cube.contents.to_xarray()
        >>> da.name, da.dims, da.shape
        ('z', ('z', 'y', 'x'), (4, 11, 11))
        >>> da.coords["z"]
        <xarray.DataArray 'z' (z: 4)> Size: 32B
        array([1., 2., 3., 5.])
        Coordinates:
          * z        (z) float64 32B 1.0 2.0 3.0 5.0
        Attributes:
            long_name:     z
            axis:          Z
            actual_range:  [1. 5.]
        >>> # The four layers are the same X*Y grid scaled by 1.0, 1.1, 1.2, and 1.4.
        >>> # Verify that layer k equals scale[k] * outer(y, x) for every element.
        >>> scale = [1.0, 1.1, 1.2, 1.4]
        >>> expected = [s * np.outer(da.y, da.x) for s in scale]
        >>> np.allclose(da.values, expected)
        True
        >>> # Cross-check against loading the same file directly with xarray.
        >>> import xarray as xr
        >>> direct = xr.open_dataset(cubefile)["cube"]
        >>> da.dims == direct.dims
        True
        >>> np.allclose(da.coords["x"], direct.coords["x"])
        True
        >>> np.allclose(da.coords["y"], direct.coords["y"])
        True
        >>> np.allclose(da.coords["z"], direct.coords["z"])
        True
        >>> np.allclose(da.values, direct.values)
        True
        >>> da.gmt.registration, da.gmt.gtype
        (<GridRegistration.GRIDLINE: 0>, <GridType.CARTESIAN: 0>)
        """
        header = self.header.contents

        # The y/x dimensions come from the 2-D grid header; the 3rd one from the cube.
        dims, dim_attrs = header.dims, header.dim_attrs
        zdim, zdim_attrs = self._parse_dimension()

        # The coordinates, given as a tuple of the form (dims, data, attrs)
        x = np.ctypeslib.as_array(self.x, shape=(header.n_columns,)).copy()
        y = np.ctypeslib.as_array(self.y, shape=(header.n_rows,)).copy()
        z = np.ctypeslib.as_array(self.z, shape=(header.n_bands,)).copy()
        coords = [
            (zdim, z, zdim_attrs),
            (dims[0], y, dim_attrs[0]),
            (dims[1], x, dim_attrs[1]),
        ]

        # The data array. The cube is a stack of 2-D padded layers, i.e., layer k
        # starts at offset k * header.size, which can exceed header.my * header.mx.
        data = np.ctypeslib.as_array(
            self.data, shape=(header.n_bands, header.size)
        ).copy()
        pad = header.pad[:]
        data = data[:, : header.my * header.mx].reshape(
            header.n_bands, header.my, header.mx
        )
        data = data[:, pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1]]

        # Create the xarray.DataArray object
        cube = xr.DataArray(
            data, coords=coords, name=header.name, attrs=header.data_attrs
        )

        # Flip the coordinates and data if necessary so that coordinates are ascending.
        # `cube.sortby(list(cube.dims))` sometimes causes crashes.
        # The solution comes from https://github.com/pydata/xarray/discussions/6695.
        for dim in cube.dims:
            if cube[dim].size > 1 and cube[dim][0] > cube[dim][1]:
                cube = cube.isel({dim: slice(None, None, -1)})

        # Set GMT accessors.
        # Must put at the end, otherwise info gets lost after certain grid operations.
        cube.gmt.registration = header.registration
        cube.gmt.gtype = header.gtype
        return cube
