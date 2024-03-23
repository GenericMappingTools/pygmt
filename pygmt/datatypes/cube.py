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


class _GMT_CUBE(ctp.Structure):  # noqa: N801
    """
    GMT cube data structure for 3D data.
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
        # GMT_CUBE_IS_STACK if input dataset was a list of 2-D grids rather than a
        # single cube
        ("mode", ctp.c_uint),
        # Minimum/max z values (complements header->wesn[4])
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

    def to_dataarray(self):
        """
        Convert the GMT_CUBE to an xarray.DataArray.

        Returns
        -------
            xarray.DataArray: The data array representation of the GMT_CUBE.
        """
        # The grid header
        header = self.header.contents

        name = "cube"
        # Dimensions and attributes
        dims = header.dims
        dim_attrs = header.dim_attrs

        # Patch for the 3rd dimension
        dims.append("z")
        z_attrs = {"actual_range": np.array(self.z_range[:]), "axis": "Z"}
        long_name, units = _parse_nameunits(self.units.decode())
        if long_name:
            z_attrs["long_name"] = long_name
        if units:
            z_attrs["units"] = units
        dim_attrs.append(z_attrs)

        # The coordinates, given as a tuple of the form (dims, data, attrs)
        coords = [
            (dims[0], self.y[: header.n_rows], dim_attrs[0]),
            (dims[1], self.x[: header.n_columns], dim_attrs[1]),
            # header->n_bands is used for the number of layers for 3-D cubes
            (dims[2], self.z[: header.n_bands], dim_attrs[1]),
        ]

        # The data array without paddings
        pad = header.pad[:]
        data = np.reshape(
            self.data[: header.mx * header.my * header.n_bands],
            (header.my, header.mx, header.n_bands),
        )[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1], :]

        # Create the xarray.DataArray object
        grid = xr.DataArray(data, coords=coords, name=name, attrs=header.dataA_attrs)
        return grid
