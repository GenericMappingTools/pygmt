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
    >>> from pygmt.clib import Session
    >>> import numpy as np
    >>> import xarray as xr
    >>> import rioxarray

    >>> with Session() as lib:
    ...     with lib.virtualfile_out(kind="image") as voutimg:
    ...         lib.call_module("read", f"@earth_day_01d {voutimg} -Ti")
    ...         ds = lib.read_virtualfile(vfname=voutimg, kind="image").contents
    ...         header = ds.header.contents
    ...         pad = header.pad[:]
    ...         print(ds.type, header.n_bands, header.n_rows, header.n_columns)
    ...         print(header.pad[:])
    ...         data = np.reshape(
    ...             ds.data[: header.n_bands * header.mx * header.my],
    ...             (header.my, header.mx, header.n_bands),
    ...         )
    ...         data = data[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1], :]
    ...         x = ds.x[: header.n_columns]
    ...         y = ds.y[: header.n_rows]
    >>> da = xr.DataArray(
    ...     data=data,
    ...     dims=["y", "x", "band"],
    ...     coords={"y": y, "x": x, "band": [1, 2, 3]},
    ... )
    >>> da = da.transpose("band", "y", "x")
    >>> da = da.sortby(list(data.dims))
    >>> da.plot.imshow()
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

    def to_dataarray(self) -> xr.DataArray:
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
        ...         da = image.contents.to_dataarray()
        >>> da  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        <xarray.DataArray 'z' (band: 3, y: 180, x: 360)> Size: 2MB
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
                [189, 191, 191, ..., 191, 191, 189]]])
        Coordinates:
          * x        (x) float64 3kB -179.5 -178.5 -177.5 -176.5 ... 177.5 178.5 179.5
          * y        (y) float64 1kB 89.5 88.5 87.5 86.5 ... -86.5 -87.5 -88.5 -89.5
          * band     (band) uint8 3B 0 1 2
        Attributes:
            title:
            history:
            description:
            long_name:     z
            actual_range:  [ 1.79769313e+308 -1.79769313e+308]

        >>> da.coords["x"]  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        <xarray.DataArray 'x' (x: 360)> Size: 3kB
        array([-179.5, -178.5, -177.5, ...,  177.5,  178.5,  179.5])
        Coordinates:
          * x        (x) float64 3kB -179.5 -178.5 -177.5 -176.5 ... 177.5 178.5 179.5

        >>> da.coords["y"]  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        <xarray.DataArray 'y' (y: 180)> Size: 1kB
        array([ 89.5,  88.5,  87.5,  86.5,  85.5,  84.5,  83.5,  82.5,  81.5,  80.5,
                79.5,  78.5,  77.5,  76.5,  75.5,  74.5,  73.5,  72.5,  71.5,  70.5,
                69.5,  68.5,  67.5,  66.5,  65.5,  64.5,  63.5,  62.5,  61.5,  60.5,
                ...
                -0.5,  -1.5,  -2.5,  -3.5,  -4.5,  -5.5,  -6.5,  -7.5,  -8.5,  -9.5,
                ...
               -60.5, -61.5, -62.5, -63.5, -64.5, -65.5, -66.5, -67.5, -68.5, -69.5,
               -70.5, -71.5, -72.5, -73.5, -74.5, -75.5, -76.5, -77.5, -78.5, -79.5,
               -80.5, -81.5, -82.5, -83.5, -84.5, -85.5, -86.5, -87.5, -88.5, -89.5])
        Coordinates:
          * y        (y) float64 1kB 89.5 88.5 87.5 86.5 ... -86.5 -87.5 -88.5 -89.5

        >>> da.gmt.registration, da.gmt.gtype
        (1, 0)
        """

        # Get image header
        header: _GMT_GRID_HEADER = self.header.contents

        # Get DataArray without padding
        pad = header.pad[:]
        data: np.ndarray = np.reshape(
            a=self.data[: header.n_bands * header.mx * header.my],
            newshape=(header.my, header.mx, header.n_bands),
        )[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1], :]

        # Get x and y coordinates
        coords: dict[str, list | np.ndarray] = {
            "x": self.x[: header.n_columns],
            "y": self.y[: header.n_rows],
            "band": np.array([0, 1, 2], dtype=np.uint8),
        }

        # Create the xarray.DataArray object
        image = xr.DataArray(
            data=data,
            coords=coords,
            dims=("y", "x", "band"),
            name=header.name,
            attrs=header.data_attrs,
        ).transpose("band", "y", "x")

        # Set GMT accessors.
        # Must put at the end, otherwise info gets lost after certain image operations.
        image.gmt.registration = header.registration
        image.gmt.gtype = header.gtype
        return image
