"""
grd2xyz - Convert grid to data table
"""
import numpy as np
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
def grd2xyz(grid, output_type="d", **kwargs):
    r"""
    Create xyz tables from grid files.

    Read a binary 2-D grid files and write out
    xyz-triplets in ASCII [or binary] format to a standard output.

    Full option list at :gmt-docs:`grd2xyz.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
        This is the only required parameter.
    output_type : str
        Determine the format the xyz data will be returned in:
            **a**: numpy array [Default option]
            **d**: pandas DataFrame
            **s**: string

    {R}
    {V}

    Returns
    -------
    info : str
        A string with information about the grid.
    """
    with GMTTempFile() as outfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                arg_str = " ".join(
                    [infile, build_arg_string(kwargs), "->" + outfile.name]
                )
                lib.call_module("grd2xyz", arg_str)
        result = outfile.read()
    if output_type == "s":
        return result
    data_list = []
    for string_entry in result.strip().split("\n"):
        float_entry = []
        string_list = string_entry.strip().split()
        for i in string_list:
            float_entry.append(float(i))
        data_list.append(float_entry)
    data_array = np.array(data_list)
    if output_type == "a":
        result = data_array
    elif output_type == "d":
        result = pd.DataFrame(data_array)
    else:
        raise GMTInvalidInput("""Must specify format as either a, d, or s.""")
    return result
