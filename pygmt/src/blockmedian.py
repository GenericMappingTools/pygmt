"""
blockmedian - Block average (x,y,z) data tables by median estimation.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(I="spacing", R="region", V="verbose", f="coltypes")
@kwargs_to_strings(R="sequence")
def blockmedian(table, outfile=None, **kwargs):
    r"""
    Block average (x,y,z) data tables by median estimation.

    Reads arbitrarily located (x,y,z) triples [or optionally weighted
    quadruples (x,y,z,w)] from a table and writes to the output a median
    position and value for every non-empty block in a grid region defined by
    the ``region`` and ``spacing`` parameters.

    Full option list at :gmt-docs:`blockmedian.html`

    {aliases}

    Parameters
    ----------
    table : pandas.DataFrame or str
        Either a pandas dataframe with (x, y, z) or (longitude, latitude,
        elevation) values in the first three columns, or a file name to an
        ASCII data table.

    spacing : str
        *xinc*\[\ *unit*\][**+e**\|\ **n**]
        [/*yinc*\ [*unit*][**+e**\|\ **n**]].
        *xinc* [and optionally *yinc*] is the grid spacing.

    region : str or list
        *xmin/xmax/ymin/ymax*\[\ **+r**\][**+u**\ *unit*].
        Specify the region of interest.

    outfile : str
        Required if ``table`` is a file. The file name for the output ASCII
        file.

    {V}
    {f}

    Returns
    -------
    output : pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, z) columns if ``outfile``
          is not set
        - None if ``outfile`` is set (filtered output will be stored in file
          set by ``outfile``)
    """
    kind = data_kind(table)
    with GMTTempFile(suffix=".csv") as tmpfile:
        with Session() as lib:
            if kind == "matrix":
                if not hasattr(table, "values"):
                    raise GMTInvalidInput(f"Unrecognized data type: {type(table)}")
                file_context = lib.virtualfile_from_matrix(table.values)
            elif kind == "file":
                if outfile is None:
                    raise GMTInvalidInput("Please pass in a str to 'outfile'")
                file_context = dummy_context(table)
            else:
                raise GMTInvalidInput(f"Unrecognized data type: {type(table)}")

            with file_context as infile:
                if outfile is None:
                    outfile = tmpfile.name
                arg_str = " ".join([infile, build_arg_string(kwargs), "->" + outfile])
                lib.call_module(module="blockmedian", args=arg_str)

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            result = pd.read_csv(tmpfile.name, sep="\t", names=table.columns)
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

    return result
