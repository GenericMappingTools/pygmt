"""
Enumerations for PyGMT.
"""

from enum import IntEnum


class GridID(IntEnum):
    """
    Enum for the GMT grid format ID.

    These enums are defined in 'gmt_grdio.h'.
    """

    GMT_GRD_UNKNOWN_FMT = 0  # If grid format cannot be auto-detected
    GMT_GRID_IS_BF = 1  # GMT native, C-binary format (32-bit float)
    GMT_GRID_IS_BS = 2  # GMT native, C-binary format (16-bit integer)
    GMT_GRID_IS_RB = 3  # SUN rasterfile format (8-bit standard)
    GMT_GRID_IS_BB = 4  # GMT native, C-binary format (8-bit integer)
    GMT_GRID_IS_BM = 5  # GMT native, C-binary format (bit-mask)
    GMT_GRID_IS_SF = 6  # Golden Software Surfer format 6 (32-bit float)
    GMT_GRID_IS_CB = 7  # GMT netCDF format (8-bit integer, depreciated)
    GMT_GRID_IS_CS = 8  # GMT netCDF format (16-bit integer, depreciated)
    GMT_GRID_IS_CI = 9  # GMT netCDF format (32-bit integer, depreciated)
    GMT_GRID_IS_CF = 10  # GMT netCDF format (32-bit float, depreciated)
    GMT_GRID_IS_CD = 11  # GMT netCDF format (64-bit float, depreciated)
    GMT_GRID_IS_RF = 12  # GEODAS grid format GRD98 (NGDC)
    GMT_GRID_IS_BI = 13  # GMT native, C-binary format (32-bit integer)
    GMT_GRID_IS_BD = 14  # GMT native, C-binary format (64-bit float)
    GMT_GRID_IS_NB = 15  # GMT netCDF format (8-bit integer)
    GMT_GRID_IS_NS = 16  # GMT netCDF format (16-bit integer)
    GMT_GRID_IS_NI = 17  # GMT netCDF format (32-bit integer)
    GMT_GRID_IS_NF = 18  # GMT netCDF format (32-bit float)
    GMT_GRID_IS_ND = 19  # GMT netCDF format (64-bit float)
    GMT_GRID_IS_SD = 20  # Golden Software Surfer format 7 (64-bit float, read-only)
    GMT_GRID_IS_AF = 21  # Atlantic Geoscience Center format AGC (32-bit float)
    GMT_GRID_IS_GD = 22  # Import through GDAL
    GMT_GRID_IS_EI = 23  # ESRI Arc/Info ASCII Grid Interchange format (ASCII integer)
    GMT_GRID_IS_EF = 24  # ESRI Arc/Info ASCII Grid Interchange format (ASCII float)
