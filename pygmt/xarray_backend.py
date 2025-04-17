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

    Relies on the libgdal-netcdf driver used by GMT C for NetCDF files, and libgdal for
    GeoTIFF files.
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
        Backend open_dataset method used by Xarray in :py:func:`~xarray.open_dataset`.
        """
        try:
            ext = Path(filename_or_obj).suffix
        except TypeError:
            return False
        return ext in {".grd", ".nc", ".tif", ".tiff"}
