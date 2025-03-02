"""
Read a file into an appropriate object.
"""

from collections.abc import Mapping, Sequence
from pathlib import PurePath
from typing import Any, Literal

import pandas as pd
import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, is_nonstr_iter
from pygmt.src.which import which


def read(
    file: str | PurePath,
    kind: Literal["dataset", "grid", "image"],
    region: Sequence[float] | str | None = None,
    header: int | None = None,
    column_names: pd.Index | None = None,
    dtype: type | Mapping[Any, type] | None = None,
    index_col: str | int | None = None,
) -> pd.DataFrame | xr.DataArray:
    """
    Read a dataset, grid, or image from a file and return the appropriate object.

    The returned object is a :class:`pandas.DataFrame` for datasets, and
    :class:`xarray.DataArray` for grids and images.

    For datasets, keyword arguments ``column_names``, ``header``, ``dtype``, and
    ``index_col`` are supported.

    Parameters
    ----------
    file
        The file name to read.
    kind
        The kind of data to read. Valid values are ``"dataset"``, ``"grid"``, and
        ``"image"``.
    region
        The region of interest. Only data within this region will be read.
    column_names
        A list of column names.
    header
        Row number containing column names. ``header=None`` means not to parse the
        column names from table header. Ignored if the row number is larger than the
        number of headers in the table.
    dtype
        Data type. Can be a single type for all columns or a dictionary mapping
        column names to types.
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
    if kind not in {"dataset", "grid", "image"}:
        msg = f"Invalid kind {kind}: must be one of 'dataset', 'grid', or 'image'."
        raise ValueError(msg)

    if kind != "dataset" and any(
        v is not None for v in [column_names, header, dtype, index_col]
    ):
        msg = (
            "Only the 'dataset' kind supports the 'column_names', 'header', "
            "'dtype', and 'index_col' arguments."
        )
        raise ValueError(msg)

    kwdict = {
        "R": "/".join(f"{v}" for v in region) if is_nonstr_iter(region) else region,  # type: ignore[union-attr]
        "T": {"dataset": "d", "grid": "g", "image": "i"}[kind],
    }

    with Session() as lib:
        with lib.virtualfile_out(kind=kind) as voutfile:
            lib.call_module("read", args=[file, voutfile, *build_arg_list(kwdict)])

        match kind:
            case "dataset":
                return lib.virtualfile_to_dataset(
                    vfname=voutfile,
                    column_names=column_names,
                    header=header,
                    dtype=dtype,
                    index_col=index_col,
                )
            case "grid" | "image":
                raster = lib.virtualfile_to_raster(vfname=voutfile, kind=kind)
                # Add "source" encoding
                source = which(fname=file)
                raster.encoding["source"] = (
                    source[0] if isinstance(source, list) else source
                )
                _ = raster.gmt  # Load GMTDataArray accessor information
                return raster
