"""
Histogram - Create a histogram
"""
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    A="horizontal",
    B="frame",
    C="cmap",
    G="fill",
    J="projection",
    R="region",
    W="pen",
    p="perspective",
)
@kwargs_to_strings(R="sequence", T="sequence")
def histogram(self, table, **kwargs):
    r"""
    Plots a histogram, and can read data from a file or
    list, array, or dataframe.

    Full option list at :gmt-docs:`histogram.html`

    {aliases}

    Parameters
    ----------
    table : str, list, or 1d array
        A data file name, list, or 1d numpy array. This is a required argument.
    {J}
    {R}
    {B}
    """
    with GMTTempFile() as outfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(data=table)
            with file_context as infile:
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("histogram", arg_str)
        result = outfile.read()
    return result
