"""
grdvolume - Calculate grid volume and area constrained by a contour.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    C="plane",
    Cr="outside_volume",
    D="slice",
    R="region",
    S="unit",
    V="verbose",
)
@kwargs_to_strings(C="sequence", R="sequence")
def grdvolume(grid, output_type="pandas", outfile=None, **kwargs):
    r"""
     Determine the volume between the surface of a grid and a plane.

     Read a 2-D grid file and calculate the volume contained below the surface
     and above the plane specified by the given contour (or zero if not given)
     and return the contour, area, volume, and maximum mean height
     (volume/area). Alternatively, a range of contours can be specified to
     return the volume and area inside the contour for all contour values.
     Using **-T**, the contour that produced the maximum mean height
     (or maximum curvature of heights vs contour value) is returned as well.

     {aliases}

     Parameters
     ----------
     grid : str or xarray.DataArray
         The file name of the input grid or the grid loaded as a DataArray.
         This is the only required parameter.
     output_type : str
         Determine the format the xyz data will be returned in [Default is
         ``pandas``]:
             - ``numpy`` - :class:`numpy.ndarray`
             - ``pandas``-  :class:`pandas.DataFrame`
             - ``file`` - ASCII file (requires ``outfile``)
     outfile : str
         The file name for the output ASCII file.
     {R}
     {V}

     Returns
     -------
    ret : pandas.DataFrame or numpy.ndarray or None
         Return type depends on ``outfile`` and ``output_type``:
         - None if ``outfile`` is set (output will be stored in file set by
           ``outfile``)
         - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile``
            is not set (depends on ``output_type`` [Default is
           :class:`pandas.DataFrame`])

    """
    if output_type not in ["numpy", "pandas", "file"]:
        raise GMTInvalidInput(
            """Must specify format as either numpy, pandas, or file."""
        )
    if output_type == "file" and outfile is None:
        raise GMTInvalidInput("""Must specify outfile for ASCII output.""")

    with GMTTempFile() as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if outfile is None:
                    outfile = tmpfile.name
                arg_str = " ".join([infile, build_arg_string(kwargs), "->" + outfile])
                lib.call_module("grdvolume", arg_str)

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            result = pd.read_csv(tmpfile.name, sep="\t", header=None, comment=">")
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

        if output_type == "numpy":
            result = result.to_numpy()
    return result
