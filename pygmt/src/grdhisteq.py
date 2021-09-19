"""
grdhisteq - Perform histogram equalization for a grid.
"""

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

    Allows the user to find the data values which divide a given grid file into
    patches of equal area. One common use of **grdhisteq** is in a kind of
    histogram equalization of an image. In this application, the user might
    have a grid of flat topography with a mountain in the middle. Ordinary gray
    shading of this file (using :meth:`pygmt.Figure.grdimage` or
    :meth:`pygmt.Figure.grdview`) with a linear mapping from topography to
    graytone will result in most of the image being very dark gray, with the
    mountain being almost white. One could use **grdhisteq** to write to a
    :class:`pandas.DataFrame` or ASCII file with a list of those data values
    which divide the range of the data into *n_cells* segments, each of which
    has an equal area in the image. Using **awk** or :meth:`pygmt.makecpt` one
    can take this output and build a CPT; using the CPT with
    :meth:`pygmt.Figure.grdimage` will result in an image with all levels of
    gray occurring equally. Alternatively, see :meth:`pygmt.grd2cpt`.

    The second common use of **grdhisteq** is in writing a grid with statistics
    based on some kind of cumulative distribution function. In this
    application, the output has relative highs and lows in the same (x,y)
    locations as the input file, but the values are changed to reflect their
    place in some cumulative distribution. One example would be to find the
    lowest 10% of the data: Take a grid, run **grdhisteq** and make a grid
    using *n_cells* = 10, and then contour the result to trace the 1 contour.
    This will enclose the lowest 10% of the data, regardless of their original
    values. Another example is in equalizing the output of
    :meth:`pygmt.grdgradient`. For shading purposes it is desired that the data
    have a smooth distribution, such as a Gaussian. If you run **grdhisteq** on
    output from :meth:`pygmt.grdgradient` and make a grid file output with the
    Gaussian option, you will have a grid whose values are distributed
    according to a Gaussian distribution with zero mean and unit variance. The
    locations of these values will correspond to the locations of the input;
    that is, the most negative output value will be in the (x,y) location of
    the most negative input value, and so on.

    Full option list at :gmt-docs:`grdhisteq.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    divisions : int or bool
        The number of divisions of data range to make [Default is 16].

    {R}
    {V}
    {h}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdhisteq", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result
