"""
An xarray backend for reading raster grid/image files using the 'gmt' engine.
"""

from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list
from pygmt.src.which import which
from xarray.backends import BackendEntrypoint


class GMTBackendEntrypoint(BackendEntrypoint):
    """
    Xarray backend to read raster grid/image files using 'gmt' engine.

    Internally, GMT uses the netCDF C library to read netCDF files, and GDAL for GeoTIFF
    and other raster formats. See :gmt-docs:`reference/features.html#grid-file-format`
    for more details about supported formats. This GMT engine can also read
    :gmt-docs:`GMT remote datasets <datasets/remote-data.html>` (file names starting
    with an `@`) directly, and pre-loads :class:`pygmt.GMTDataArrayAccessor` properties
    (in the '.gmt' accessor) for easy access to GMT-specific metadata and features.

    When using :py:func:`xarray.open_dataarray` or :py:func:`xarray.load_dataarray` with
    ``engine="gmt"``, the ``raster_kind`` parameter is required and can be either:

    - ``"grid"``: for reading single-band raster grids
    - ``"image"``: for reading multi-band raster images

    Examples
    --------
    Read a single-band netCDF file using ``raster_kind="grid"``

    >>> import pygmt
    >>> import xarray as xr
    >>>
    >>> da_grid = xr.open_dataarray(
    ...     "@static_earth_relief.nc", engine="gmt", raster_kind="grid"
    ... )
    >>> da_grid  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    <xarray.DataArray 'z' (lat: 14, lon: 8)>...
    [112 values with dtype=float32]
    Coordinates:
      * lat      (lat) float64... -23.5 -22.5 -21.5 -20.5 ... -12.5 -11.5 -10.5
      * lon      (lon) float64... -54.5 -53.5 -52.5 -51.5 -50.5 -49.5 -48.5 -47.5
    Attributes:...
        Conventions:   CF-1.7
        title:         Produced by grdcut
        history:       grdcut @earth_relief_01d_p -R-55/-47/-24/-10 -Gstatic_eart...
        description:   Reduced by Gaussian Cartesian filtering (111.2 km fullwidt...
        actual_range:  [190. 981.]
        long_name:     elevation (m)

    Read a multi-band GeoTIFF file using ``raster_kind="image"``

    >>> da_image = xr.open_dataarray(
    ...     "@earth_night_01d", engine="gmt", raster_kind="image"
    ... )
    >>> da_image  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    <xarray.DataArray 'z' (band: 3, y: 180, x: 360)>...
    [194400 values with dtype=uint8]
    Coordinates:
      * y        (y) float64... 89.5 88.5 87.5 86.5 ... -86.5 -87.5 -88.5 -89.5
      * x        (x) float64... -179.5 -178.5 -177.5 -176.5 ... 177.5 178.5 179.5
      * band     (band) uint8... 1 2 3
    Attributes:...
        long_name:  z
    """

    description = "Open raster (.grd, .nc or .tif) files in Xarray via GMT."
    open_dataset_parameters = ("filename_or_obj", "raster_kind")
    url = "https://pygmt.org/dev/api/generated/pygmt.GMTBackendEntrypoint.html"

    def open_dataset(  # type: ignore[override]
        self,
        filename_or_obj: PathLike,
        *,
        drop_variables=None,  # noqa: ARG002
        raster_kind: Literal["grid", "image"],
        # other backend specific keyword arguments
        # `chunks` and `cache` DO NOT go here, they are handled by xarray
    ) -> xr.Dataset:
        """
        Backend open_dataset method used by Xarray in :py:func:`~xarray.open_dataset`.

        Parameters
        ----------
        filename_or_obj
            File path to a netCDF (.nc), GeoTIFF (.tif) or other grid/image file format
            that can be read by GMT via the netCDF or GDAL C libraries. See also
            :gmt-docs:`reference/features.html#grid-file-format`.
        raster_kind
            Whether to read the file as a "grid" (single-band) or "image" (multi-band).
        """
        if raster_kind not in {"grid", "image"}:
            msg = f"Invalid raster kind: '{raster_kind}'. Valid values are 'grid' or 'image'."
            raise GMTInvalidInput(msg)

        with Session() as lib:
            with lib.virtualfile_out(kind=raster_kind) as voutfile:
                kwdict = {"T": {"grid": "g", "image": "i"}[raster_kind]}
                lib.call_module(
                    module="read",
                    args=[filename_or_obj, voutfile, *build_arg_list(kwdict)],
                )

                raster: xr.DataArray = lib.virtualfile_to_raster(
                    vfname=voutfile, kind=raster_kind
                )
                # Add "source" encoding
                source = which(fname=filename_or_obj)
                raster.encoding["source"] = (
                    source[0] if isinstance(source, list) else source
                )
                _ = raster.gmt  # Load GMTDataArray accessor information
                return raster.to_dataset()
