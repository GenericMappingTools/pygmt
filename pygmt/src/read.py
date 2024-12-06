"""
Read data from files
"""

from typing import Literal

import pandas as pd
import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.src.which import which


@fmt_docstring
@use_alias(R="region")
@kwargs_to_strings(R="sequence")
def read(
    file: str,
    kind: Literal["dataset", "grid", "image"],
    **kwargs,
) -> pd.DataFrame | xr.DataArray:
    """
    Read a dataset, grid, or image from a file and return the appropriate object.

    For datasets, it returns a :class:`pandas.DataFrame`. For grids and images, it
    returns a :class:`xarray.DataArray`.

    Parameters
    ----------
    file
        The file name to read.
    kind
        The kind of data to read. Valid values are ``"dataset"``, ``"grid"``, and
        ``"image"``.
    {region}

        For datasets, the following keyword arguments are supported:

    column_names
        A list of column names.
    header
        Row number containing column names. ``header=None`` means not to parse the
        column names from table header. Ignored if the row number is larger than the
        number of headers in the table.
    dtype
        Data type. Can be a single type for all columns or a dictionary mapping column
        names to types.
    index_col
        Column to set as index.

    Returns
    -------
    data
        Return type depends on the ``kind`` argument:

        - ``"dataset"``: :class:`pandas.DataFrame`
        - ``"grid"`` or ``"image"``: :class:`xarray.DataArray`


    Examples
    --------
    Read a dataset into a :class:`pandas.DataFrame` object:

    >>> from pygmt import read
    >>> df = read("@hotspots.txt", kind="dataset")
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    Read a grid into an :class:`xarray.DataArray` object:

    >>> dataarray = read("@earth_relief_01d", kind="grid")
    >>> type(dataarray)
    <class 'xarray.core.dataarray.DataArray'>
    """
    kwdict = {
        "R": kwargs.get("R"),
        "T": {"dataset": "d", "grid": "g", "image": "i"}[kind],
    }

    with Session() as lib:
        with lib.virtualfile_out(kind=kind) as voutfile:
            lib.call_module("read", args=[file, voutfile, *build_arg_list(kwdict)])

        match kind:
            case "dataset":
                return lib.virtualfile_to_dataset(vfname=voutfile, **kwargs)
            case "grid" | "image":
                raster = lib.virtualfile_to_raster(vfname=voutfile, kind=kind)
                # Add "source" encoding
                source = which(fname=file)
                raster.encoding["source"] = (
                    source if isinstance(source, str) else source[0]
                )
                _ = raster.gmt  # Load GMTDataArray accessor information
                return raster
