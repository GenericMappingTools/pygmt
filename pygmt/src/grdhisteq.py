"""
grdhisteq - Perform histogram equalization for a grid.
"""

import pandas as pd
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


@fmt_docstring
@use_alias(
    C="divisions",
    G="outgrid",
    R="region",
    N="gaussian",
    Q="quadratic",
    V="verbose",
    h="header",
)
@kwargs_to_strings(R="sequence")
def grdhisteq(grid, **kwargs):
    r"""
    Perform histogram equalization for a grid.

    Two common use cases of :meth:`pygmt.grdhisteq` are to find data values that
    divide a grid into patches of equal area or to write a grid with statistics
    based on some kind of cumulative distribution function.

    Histogram equalization provides a way to highlight data that has most
    values clustered in a small portion of the dynamic range, such as a grid
    of flat topography with a mountain in the middle. Ordinary gray shading of
    this grid (using :meth:`pygmt.Figure.grdimage` or
    :meth:`pygmt.Figure.grdview`) with a linear mapping from topography to
    graytone will result in most of the image being very dark gray, with the
    mountain being almost white. :meth:`pygmt.grdhisteq` can provide a list of
    data values that divide the data range into divisions which have an equal
    area in the image [Default is 16 if ``divisions`` is not set]. The
    :class:`pandas.DataFrame` or ASCII file output can be used to make a
    colormap with :meth:`pygmt.makecpt` and an image with
    :meth:`pygmt.Figure.grdimage` that has all levels of gray occuring equally.

    :meth:`pygmt.grdhisteq` also provides a way to write a grid with statistics based
    on a cumulative distribution function. In this application, the ``outgrid``
    has relative highs and lows in the same (x,y) locations as the ``grid``,
    but the values are changed to reflect their place in the cumulative
    distribution.

    Full option list at :gmt-docs:`grdhisteq.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in. Requires ``Gaussian`` to be set.
    outfile : str or None
        The name of the output ASCII file to store the results of the
        histogram equalization in. Not allowed if ``outgrid`` is used.
    divisions : int
        Set the number of divisions of the data range.

    {R}
    {V}
    {h}

    Returns
    -------
    ret: pandas.DataFrame or xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - pandas.DataFrame if ``outgrid`` is None (default)
        - xarray.DataArray if ``outgrid`` is True
        - None if ``outgrid`` is a str (grid output is stored in ``outgrid``)
        - None if ``outfile`` is a str (file output is stored in ``outfile``)

    See Also
    -------
    :meth:`pygmt.grd2cpt`
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs:  # table output if outgrid is unset
                    kwargs.update({">": tmpfile.name})
                else:  # NetCDF or xarray.DataArray output if outgrid is set
                    if (
                        kwargs["G"] is True
                    ):  # xarray.DataArray output if outgrid is True
                        kwargs.update({"G": tmpfile.name})
                    outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdhisteq", arg_str)

        try:
            result = load_dataarray(outgrid) if outgrid == tmpfile.name else None
        except UnboundLocalError:  # if outgrid unset, return pd.DataFrame
            result = pd.read_csv(tmpfile.name, sep="\t", header=None)

    return result
