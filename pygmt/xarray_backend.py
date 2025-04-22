"""
An xarray backend for reading raster grid/image files using the 'gmt' engine.
"""

import os
from pathlib import Path
from typing import Literal

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list
from pygmt.src.which import which
from xarray.backends import BackendEntrypoint


class GMTBackendEntrypoint(BackendEntrypoint):
    """
    Xarray backend to read raster grid/image files using 'gmt' engine.

    Internally, GMT uses the NetCDF C library to read NetCDF files, and GDAL for GeoTIFF
    and other raster formats.

    When using :py:func:`xarray.open_dataarray` or :py:func:`xarray.load_dataarray` with
    ``engine="gmt"``, pass the ``decode_kind`` parameter that can be either:

    - ``"grid"`` - for reading single-band raster grids
    - ``"image"`` - for reading multi-band raster images

    Examples
    --------
    Read a single-band NetCDF file using ``decode_kind="grid"``

    >>> import pygmt
    >>> import xarray as xr
    >>>
    >>> da_grid = xr.open_dataarray(
    ...     "@static_earth_relief.nc", engine="gmt", decode_kind="grid"
    ... )
    >>> da_grid
    <xarray.DataArray 'z' (lat: 14, lon: 8)> Size: 448B
    [112 values with dtype=float32]
    Coordinates:
      * lat      (lat) float64 112B -23.5 -22.5 -21.5 -20.5 ... -12.5 -11.5 -10.5
      * lon      (lon) float64 64B -54.5 -53.5 -52.5 -51.5 -50.5 -49.5 -48.5 -47.5
    Attributes:
        Conventions:   CF-1.7
        title:         Produced by grdcut
        history:       grdcut @earth_relief_01d_p -R-55/-47/-24/-10 -Gstatic_eart...
        description:   Reduced by Gaussian Cartesian filtering (111.2 km fullwidt...
        actual_range:  [190. 981.]
        long_name:     elevation (m)

    Read a multi-band GeoTIFF file using ``decode_kind="image"``

    >>> da_image = xr.open_dataarray(
    ...     "@earth_night_01d", engine="gmt", decode_kind="image"
    ... )
    >>> da_image
    <xarray.DataArray 'z' (band: 3, y: 180, x: 360)> Size: 194kB
    [194400 values with dtype=uint8]
    Coordinates:
      * y        (y) float64 1kB 89.5 88.5 87.5 86.5 ... -86.5 -87.5 -88.5 -89.5
      * x        (x) float64 3kB -179.5 -178.5 -177.5 -176.5 ... 177.5 178.5 179.5
      * band     (band) uint8 3B 1 2 3
    Attributes:
        long_name:  z
    """

    description = "Open raster (.grd, .nc or .tif) files in Xarray via GMT."
    open_dataset_parameters = ("filename_or_obj", "decode_kind")
    url = "https://github.com/GenericMappingTools/pygmt"

    def open_dataset(  # type: ignore[override]
        self,
        filename_or_obj: str | os.PathLike,
        *,
        drop_variables=None,  # noqa: ARG002
        decode_kind: Literal["grid", "image"],
        # other backend specific keyword arguments
        # `chunks` and `cache` DO NOT go here, they are handled by xarray
    ) -> xr.Dataset:
        """
        Backend open_dataset method used by Xarray in :py:func:`~xarray.open_dataset`.
        """
        if decode_kind not in {"grid", "image"}:
            msg = f"Invalid raster kind: '{decode_kind}'. Valid values are 'grid' or 'image'."
            raise GMTInvalidInput(msg)

        with Session() as lib:
            with lib.virtualfile_out(kind=decode_kind) as voutfile:
                kwdict = {"T": {"grid": "g", "image": "i"}[decode_kind]}
                lib.call_module(
                    module="read",
                    args=[filename_or_obj, voutfile, *build_arg_list(kwdict)],
                )

                raster: xr.DataArray = lib.virtualfile_to_raster(
                    vfname=voutfile, kind=decode_kind
                )
                # Add "source" encoding
                source = which(fname=filename_or_obj)
                raster.encoding["source"] = (
                    source[0] if isinstance(source, list) else source
                )
                _ = raster.gmt  # Load GMTDataArray accessor information
                return raster.to_dataset()

    def guess_can_open(self, filename_or_obj) -> bool:
        """
        Try to guess whether we can read this file.

        This allows files ending in '.grd', '.nc', or '.tif(f)' to be automatically
        opened by xarray.
        """
        try:
            ext = Path(filename_or_obj).suffix
        except TypeError:
            return False
        return ext in {".grd", ".nc", ".tif", ".tiff"}
