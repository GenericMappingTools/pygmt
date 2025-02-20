"""
Wrapper for the GMT_IMAGE data type.
"""

import ctypes as ctp
from typing import ClassVar

import numpy as np
import xarray as xr
from pygmt.datatypes.header import _GMT_GRID_HEADER


class _GMT_IMAGE(ctp.Structure):  # noqa: N801
    """
    GMT image data structure.

    Examples
    --------
    >>> import numpy as np
    >>> from pygmt.clib import Session
    >>> with Session() as lib:
    ...     with lib.virtualfile_out(kind="image") as voutimg:
    ...         lib.call_module("read", ["@earth_day_01d", voutimg, "-Ti"])
    ...         # Read the image from the virtual file
    ...         image = lib.read_virtualfile(vfname=voutimg, kind="image").contents
    ...         # The image header
    ...         header = image.header.contents
    ...         # Access the header properties
    ...         print(header.n_rows, header.n_columns, header.registration)
    ...         print(header.wesn[:], header.inc[:])
    ...         print(header.z_scale_factor, header.z_add_offset)
    ...         print(header.x_units, header.y_units, header.z_units)
    ...         print(header.title)
    ...         print(header.command)
    ...         print(header.remark)
    ...         print(header.nm, header.size, header.complex_mode)
    ...         print(header.type, header.n_bands, header.mx, header.my)
    ...         print(header.pad[:])
    ...         print(header.mem_layout, header.xy_off)
    ...         # Image-specific attributes.
    ...         print(image.type, image.n_indexed_colors)
    ...         # The x and y coordinates
    ...         x = np.ctypeslib.as_array(image.x, shape=(header.n_columns,)).copy()
    ...         y = np.ctypeslib.as_array(image.y, shape=(header.n_rows,)).copy()
    ...         # The data array (with paddings)
    ...         data = np.ctypeslib.as_array(
    ...             image.data, shape=(header.my, header.mx, header.n_bands)
    ...         ).copy()
    ...         # The data array (without paddings)
    ...         pad = header.pad[:]
    ...         data = data[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1], :]
    180 360 1
    [-180.0, 180.0, -90.0, 90.0] [1.0, 1.0]
    1.0 0.0
    b'x' b'y' b'z'
    b''
    b''
    b''
    64800 66976 0
    0 3 364 184
    [2, 2, 2, 2]
    b'BRPa' 0.5
    1 0
    >>> x  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    array([-179.5, -178.5, ..., 178.5, 179.5])
    >>> y  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    array([ 89.5,  88.5, ..., -88.5, -89.5])
    >>> data.dtype
    dtype('uint8')
    >>> data.shape
    (180, 360, 3)
    >>> data.min(), data.max()
    (10, 255)
    """

    _fields_: ClassVar = [
        # Data type, e.g. GMT_FLOAT
        ("type", ctp.c_int),
        # Array with color lookup values
        ("colormap", ctp.POINTER(ctp.c_int)),
        # Number of colors in a paletted image
        ("n_indexed_colors", ctp.c_int),
        # Pointer to full GMT header for the image
        ("header", ctp.POINTER(_GMT_GRID_HEADER)),
        # Pointer to actual image
        ("data", ctp.POINTER(ctp.c_ubyte)),
        # Pointer to an optional transparency layer stored in a separate variable
        ("alpha", ctp.POINTER(ctp.c_ubyte)),
        # Color interpolation
        ("color_interp", ctp.c_char_p),
        # Pointer to the x-coordinate vector
        ("x", ctp.POINTER(ctp.c_double)),
        # Pointer to the y-coordinate vector
        ("y", ctp.POINTER(ctp.c_double)),
        # Book-keeping variables "hidden" from the API
        ("hidden", ctp.c_void_p),
    ]

    def to_xarray(self) -> xr.DataArray:
        """
        Convert a _GMT_IMAGE object to an :class:`xarray.DataArray` object.

        Returns
        -------
        dataarray
            A :class:`xarray.DataArray` object.

        Examples
        --------
        >>> from pygmt.clib import Session
        >>> with Session() as lib:
        ...     with lib.virtualfile_out(kind="image") as voutimg:
        ...         lib.call_module("read", ["@earth_day_01d", voutimg, "-Ti"])
        ...         # Read the image from the virtual file
        ...         image = lib.read_virtualfile(voutimg, kind="image")
        ...         # Convert to xarray.DataArray and use it later
        ...         da = image.contents.to_xarray()
        >>> da  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        <xarray.DataArray 'z' (band: 3, y: 180, x: 360)>...
        array([[[ 10,  10,  10, ...,  10,  10,  10],
                [ 10,  10,  10, ...,  10,  10,  10],
                [ 10,  10,  10, ...,  10,  10,  10],
                ...,
                [192, 193, 193, ..., 193, 192, 191],
                [204, 206, 206, ..., 205, 206, 204],
                [208, 210, 210, ..., 210, 210, 208]],
        <BLANKLINE>
               [[ 10,  10,  10, ...,  10,  10,  10],
                [ 10,  10,  10, ...,  10,  10,  10],
                [ 10,  10,  10, ...,  10,  10,  10],
                ...,
                [186, 187, 188, ..., 187, 186, 185],
                [196, 198, 198, ..., 197, 197, 196],
                [199, 201, 201, ..., 201, 202, 199]],
        <BLANKLINE>
               [[ 51,  51,  51, ...,  51,  51,  51],
                [ 51,  51,  51, ...,  51,  51,  51],
                [ 51,  51,  51, ...,  51,  51,  51],
                ...,
                [177, 179, 179, ..., 178, 177, 177],
                [185, 187, 187, ..., 187, 186, 185],
                [189, 191, 191, ..., 191, 191, 189]]], dtype=uint8)
        Coordinates:
          * y        (y) float64... 89.5 88.5 87.5 86.5 ... -86.5 -87.5 -88.5 -89.5
          * x        (x) float64... -179.5 -178.5 -177.5 -176.5 ... 177.5 178.5 179.5
          * band     (band) uint8... 1 2 3
        Attributes:
            long_name:     z

        >>> da.coords["x"]  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        <xarray.DataArray 'x' (x: 360)>...
        array([-179.5, -178.5, -177.5, ...,  177.5,  178.5,  179.5])
        Coordinates:
          * x        (x) float64... -179.5 -178.5 -177.5 -176.5 ... 177.5 178.5 179.5
        Attributes:
            long_name:     x
            axis:          X
            actual_range:  [-180.  180.]
        >>> da.coords["y"]  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        <xarray.DataArray 'y' (y: 180)>...
        array([ 89.5,  88.5,  87.5,  86.5,  ...,   -87.5, -88.5, -89.5])
        Coordinates:
          * y        (y) float64... 89.5 88.5 87.5 86.5 ... -86.5 -87.5 -88.5 -89.5
        Attributes:
            long_name:     y
            axis:          Y
            actual_range:  [-90.  90.]
        >>> da.gmt.registration, da.gmt.gtype
        (<GridRegistration.PIXEL: 1>, <GridType.GEOGRAPHIC: 1>)
        """
        # The image header
        header = self.header.contents

        if header.n_bands != 3:
            msg = (
                f"The raster image has {header.n_bands} band(s). "
                "Currently only 3-band images are supported. "
                "Please consider submitting a feature request to us. "
            )
            raise NotImplementedError(msg)

        # Get dimensions and their attributes from the header.
        dims, dim_attrs = header.dims, header.dim_attrs
        # The coordinates, given as a tuple of the form (dims, data, attrs)
        x = np.ctypeslib.as_array(self.x, shape=(header.n_columns,)).copy()
        y = np.ctypeslib.as_array(self.y, shape=(header.n_rows,)).copy()
        coords = [
            (dims[0], y, dim_attrs[0]),
            (dims[1], x, dim_attrs[1]),
            ("band", np.array([1, 2, 3], dtype=np.uint8), None),
        ]

        # Get DataArray without padding
        data = np.ctypeslib.as_array(
            self.data, shape=(header.my, header.mx, header.n_bands)
        ).copy()
        pad = header.pad[:]
        data = data[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1], :]

        # Create the xarray.DataArray object
        image = xr.DataArray(
            data=data,
            coords=coords,
            name=header.name,
            attrs=header.data_attrs,
        ).transpose("band", dims[0], dims[1])

        # Set GMT accessors.
        # Must put at the end, otherwise info gets lost after certain image operations.
        image.gmt.registration = header.registration
        image.gmt.gtype = header.gtype
        return image
