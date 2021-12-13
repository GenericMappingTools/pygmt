"""
binstats - Bin spatial data and determine statistics per bin
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
    C="compute",
    E="empty",
    G="outgrid",
    I="spacing",
    N="normalize",
    R="region",
    S="spacing",
    T="tiling",
    V="verbose",
    W="weight",
    a="colname",
    b="binary",
    h="header",
    i="incols",
    r="registration",
)
@kwargs_to_strings(I="sequence", R="sequence", i="sequence_comma")
def binstats(data, **kwargs):
    r"""
    Bin spatial data and determine statistics per bin.

    Reads arbitrarily located (x,y[,z][,w]) points
    (2-4 columns) from standard input [or *table*] and for each
    node in the specified grid layout determines which points are
    within the given radius.  These point are then used in the
    calculation of the specified statistic. The results may be
    presented as is or may be normalized by the circle area to
    perhaps give density estimates.  Alternatively, select
    hexagonal tiling instead or a rectangular grid layout.

    Full option list at :gmt-docs:`gmtbinstats.html`

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in data with L, M, C[L,M], S[L,M] values by
        providing a file name to an ASCII data table, a 2D
        {table-classes}.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {I}
    {R}
    {V}
    {b}
    {h}
    {i}
    {r}
    {x}

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
            file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with file_context as infile:
                if "G" not in kwargs:  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("gmtbinstats", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
