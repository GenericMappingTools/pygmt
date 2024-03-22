"""
Wrapper for the GMT_GRID data type and the GMT_GRID_HEADER data structure.
"""

import ctypes as ctp
from typing import ClassVar

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


class _GMT_GRID(ctp.Structure):  # noqa: N801
    pass
