"""
Enumerations for PyGMT.
"""

from enum import IntEnum


class GridID(IntEnum):
    """
    Enum for the GMT grid format ID.

    These enums are defined in 'gmt_grdio.h'.
    """

    UNKNOWN = 0  #: Unkown grid format
    BF = 1  #: GMT native, C-binary format (32-bit float)
    BS = 2  #: GMT native, C-binary format (16-bit integer)
    RB = 3  #: SUN rasterfile format (8-bit standard)
    BB = 4  #: GMT native, C-binary format (8-bit integer)
    BM = 5  #: GMT native, C-binary format (bit-mask)
    SF = 6  #: Golden Software Surfer format 6 (32-bit float)
    CB = 7  #: GMT netCDF format (8-bit integer, depreciated)
    CS = 8  #: GMT netCDF format (16-bit integer, depreciated)
    CI = 9  #: GMT netCDF format (32-bit integer, depreciated)
    CF = 10  #: GMT netCDF format (32-bit float, depreciated)
    CD = 11  #: GMT netCDF format (64-bit float, depreciated)
    RF = 12  #: GEODAS grid format GRD98 (NGDC)
    BI = 13  #: GMT native, C-binary format (32-bit integer)
    BD = 14  #: GMT native, C-binary format (64-bit float)
    NB = 15  #: GMT netCDF format (8-bit integer)
    NS = 16  #: GMT netCDF format (16-bit integer)
    NI = 17  #: GMT netCDF format (32-bit integer)
    NF = 18  #: GMT netCDF format (32-bit float)
    ND = 19  #: GMT netCDF format (64-bit float)
    SD = 20  #: Golden Software Surfer format 7 (64-bit float, read-only)
    AF = 21  #: Atlantic Geoscience Center format AGC (32-bit float)
    GD = 22  #: Import through GDAL
    EI = 23  #: ESRI Arc/Info ASCII Grid Interchange format (ASCII integer)
    EF = 24  #: ESRI Arc/Info ASCII Grid Interchange format (ASCII float)
