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
    >>> import numpy as np
    >>> from pygmt.clib import Session
    >>> with Session() as lib:
    ...     with lib.virtualfile_out(kind="image") as voutimg:
    ...         lib.call_module("read", ["@earth_day_01d_p", voutimg, "-Ti"])
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
    ...         x = image.x[: header.n_columns]
    ...         y = image.y[: header.n_rows]
    ...         # The data array (with paddings)
    ...         data = np.reshape(
    ...             image.data[: header.n_bands * header.mx * header.my],
    ...             (header.my, header.mx, header.n_bands),
    ...         )
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
    >>> x
    [-179.5, -178.5, ..., 178.5, 179.5]
    >>> y
    [89.5, 88.5, ..., -88.5, -89.5]
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
