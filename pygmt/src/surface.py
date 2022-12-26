"""
surface - Grids table data using adjustable tension continuous curvature
splines.
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

__doctest_skip__ = ["surface"]


@fmt_docstring
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

    Surface reads randomly-spaced (x, y, z) triplets and produces gridded
    values z(x,y) by solving:

    .. math::    (1 - t)\nabla^2(z)+t\nabla(z) = 0

    where :math:`t` is a tension factor between 0 and 1, and :math:`\nabla`
    indicates the Laplacian operator.

    Takes a matrix, (x, y, z) triplets, or a file name as input.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`surface.html`

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    x/y/z : 1-D arrays
        Arrays of x and y coordinates and values z of the data points.

    {spacing}

    {region}

    outgrid : str
        Optional. The file name for the output netcdf file with extension .nc
        to store the grid in.

    {verbose}
    {aspatial}
    {binary}
    {nodata}
    {find}
    {coltypes}
    {header}
    {incols}
    {registration}
    {wrap}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray`: if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load a sample table of topography
    >>> topography = pygmt.datasets.load_sample_data(
    ...     name="notre_dame_topography"
    ... )
    >>> # Perform gridding of topography data
    >>> grid = pygmt.surface(data=topography, spacing=1, region=[0, 4, 0, 8])
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            # Choose how data will be passed into the module
            file_context = lib.virtualfile_from_data(
                check_kind="vector", data=data, x=x, y=y, z=z, required_z=True
            )
            with file_context as infile:
                if (outgrid := kwargs.get("G")) is None:
                    kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
                lib.call_module(
                    module="surface", args=build_arg_string(kwargs, infile=infile)
                )

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
