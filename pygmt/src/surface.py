"""
surface - Grids table data using adjustable tension continuous curvature
splines.
"""
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    check_data_input_order,
    deprecate_parameter,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


@fmt_docstring
@deprecate_parameter("outfile", "outgrid", "v0.5.0", remove_version="v0.7.0")
@check_data_input_order("v0.5.0", remove_version="v0.7.0")
@use_alias(
    I="spacing",
    R="region",
    G="outgrid",
    V="verbose",
    a="aspatial",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    h="header",
    i="incols",
    r="registration",
    w="wrap",
)
@kwargs_to_strings(I="sequence", R="sequence")
def surface(data=None, x=None, y=None, z=None, **kwargs):
    r"""
    Grids table data using adjustable tension continuous curvature splines.

    Surface reads randomly-spaced (x,y,z) triples and produces gridded values
    z(x,y) by solving:

    .. math::    (1 - t)\nabla^2(z)+t\nabla(z) = 0

    where :math:`t` is a tension factor between 0 and 1, and :math:`\nabla`
    indicates the Laplacian operator.

    Takes a matrix, xyz triples, or a file name as input.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`surface.html`

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2D
        {table-classes}.
    x/y/z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.

    {I}

    {R}

    outgrid : str
        Optional. The file name for the output netcdf file with extension .nc
        to store the grid in.

    {V}
    {a}
    {b}
    {d}
    {e}
    {f}
    {h}
    {i}
    {r}
    {w}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray`: if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            # Choose how data will be passed into the module
            file_context = lib.virtualfile_from_data(
                check_kind="vector", data=data, x=x, y=y, z=z, required_z=True
            )
            with file_context as infile:
                if "G" not in kwargs:  # if outgrid is unset, output to tmpfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module(module="surface", args=arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
