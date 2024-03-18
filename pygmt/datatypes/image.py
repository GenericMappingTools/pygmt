"""
Wrapper for the GMT_IMAGE data type.
"""

import ctypes as ctp
from typing import ClassVar

from pygmt.datatypes.grid import _GMT_GRID_HEADER


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
    >>> data = xr.DataArray(
    ...     data, dims=["y", "x", "band"], coords={"y": y, "x": x, "band": [1, 2, 3]}
    ... )
    >>> data = data.transpose("band", "y", "x")
    >>> data = data.sortby(list(data.dims))
    >>> data.plot.imshow()
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
