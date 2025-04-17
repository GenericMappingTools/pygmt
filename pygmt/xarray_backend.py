"""
An xarray backend for reading raster grid/image files using the 'gmtread' engine.
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
from xarray.backends.common import AbstractDataStore
from xarray.core.types import ReadBuffer


class GMTReadBackendEntrypoint(BackendEntrypoint):
    """
    Xarray backend to read raster grid/image files using 'gmtread' engine.

    Relies on the libgdal-netcdf driver used by GMT C for NetCDF files, and libgdal for
    GeoTIFF files.
    """

    description = "Open .nc and .tif files in Xarray via GMT read."
    open_dataset_parameters = ("filename_or_obj", "kind")
    url = "https://github.com/GenericMappingTools/pygmt"

    def open_dataset(
        self,
        filename_or_obj: str | os.PathLike | ReadBuffer | AbstractDataStore,
        *,
        drop_variables=None,  # noqa: ARG002
        kind: Literal["grid", "image"],
        # other backend specific keyword arguments
        # `chunks` and `cache` DO NOT go here, they are handled by xarray
    ) -> xr.Dataset:
        """
        Backend open_dataset method used by Xarray in :py:func:`~xarray.open_dataset`.
        """
        if kind not in {"grid", "image"}:
            msg = f"Invalid raster kind: '{kind}'. Valid values are 'grid' or 'image'."
            raise GMTInvalidInput(msg)

        with Session() as lib:
            with lib.virtualfile_out(kind=kind) as voutfile:
                kwdict = {"T": {"grid": "g", "image": "i"}[kind]}
                lib.call_module(
                    module="read",
                    args=[filename_or_obj, voutfile, *build_arg_list(kwdict)],
                )

                raster: xr.DataArray = lib.virtualfile_to_raster(
                    vfname=voutfile, kind=kind
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
        Backend open_dataset method used by Xarray in :py:func:`~xarray.open_dataset`.
        """
        try:
            ext = Path(filename_or_obj).suffix
        except TypeError:
            return False
        return ext in {".nc", ".tif"}
