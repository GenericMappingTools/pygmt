"""
An xarray backend for reading grid files using the 'gmtread' engine.
"""

from pathlib import Path

import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import build_arg_list
from xarray.backends import BackendEntrypoint


class GMTReadBackendEntrypoint(BackendEntrypoint):
    """
    Xarray backend to read grid files using 'gmtread' engine.

    Relies on the libgdal-netcdf driver used by GMT C.
    """

    description = "Use .nc files in Xarray"
    open_dataset_parameters = ("filename_or_obj",)
    url = "https://github.com/GenericMappingTools/pygmt"

    def open_dataset(
        self,
        filename_or_obj: str,
        *,
        drop_variables=None,  # noqa: ARG002
        # other backend specific keyword arguments
        # `chunks` and `cache` DO NOT go here, they are handled by xarray
    ) -> xr.Dataset:
        """
        Backend open_dataset method used by Xarray in :py:func:`~xarray.open_dataset`.
        """
        with Session() as lib:
            with lib.virtualfile_out(kind="grid") as voutfile:
                lib.call_module(
                    module="read",
                    args=[filename_or_obj, voutfile, *build_arg_list({"T": "g"})],
                )

                raster: xr.DataArray = lib.virtualfile_to_raster(
                    vfname=voutfile, kind="grid"
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
        return ext in {".nc"}
