"""
surface - Grids table data using adjustable tension continuous curvature
splines.
"""
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    data_kind,
    deprecate_parameter,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


@fmt_docstring
@deprecate_parameter("outfile", "outgrid", "v0.5.0", remove_version="v0.7.0")
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
    s="skiprows",
)
@kwargs_to_strings(R="sequence")
def surface(x=None, y=None, z=None, data=None, **kwargs):
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
    x/y/z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.
    data : str or 2d array
        Either a data file name or a 2d numpy array with the tabular data.

    {I}

    region : str or list
        *xmin/xmax/ymin/ymax*\[**+r**][**+u**\ *unit*].
        Specify the region of interest.

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
    {s}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray`: if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    kind = data_kind(data, x, y, z)
    if kind == "vectors" and z is None:
        raise GMTInvalidInput("Must provide z with x and y.")

    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            if kind == "file":
                file_context = dummy_context(data)
            elif kind == "matrix":
                file_context = lib.virtualfile_from_matrix(data)
            elif kind == "vectors":
                file_context = lib.virtualfile_from_vectors(x, y, z)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(data)))
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tmpfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module(module="surface", args=arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
