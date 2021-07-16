"""
grd2xyz - Convert grid to data table
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
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def grd2xyz(grid, output_type="d", outfile=None, **kwargs):
    r"""
    Convert grid to data table.

    Read a grid and output xyz-triplets as a numpy array,
    pandas DataFrame, string, or ASCII [or binary] file.

    Full option list at :gmt-docs:`grd2xyz.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
        This is the only required parameter.
    output_type : str
        Determine the format the xyz data will be returned in:
            **a**: numpy array
            **d**: pandas DataFrame [Default option]
            **s**: string
    outfile : str
        The file name for the output ASCII file.
    {R}
    {V}

    Returns
    -------
    data : pandas.DataFrame or numpy.array or str
        The xyz triplet data in a pandas DataFrame, numpy array, or string.
    """
    if output_type not in ["a", "d", "s"]:
        raise GMTInvalidInput("""Must specify format as either a, d, or s.""")
    if output_type == "s" and outfile is None:
        raise GMTInvalidInput("""Must specify outfile for ASCII output.""")

    with GMTTempFile() as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if outfile is None:
                    outfile = tmpfile.name
                arg_str = " ".join([infile, build_arg_string(kwargs), "->" + outfile])
                lib.call_module("grd2xyz", arg_str)

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            result = pd.read_csv(tmpfile.name, sep="\t", header=None, comment=">")
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

        if output_type == "a":
            result = result.to_numpy()
    return result
