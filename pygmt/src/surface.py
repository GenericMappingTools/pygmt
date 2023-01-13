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
    C="convergence",
    I="spacing",
    L="limit",
    R="region",
    G="outgrid",
    M="max_radius",
    T="tension",
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
    convergence: float
        Optional. Convergence limit. Iteration is assumed to have converged when the maximum 
        absolute change in any grid value is less than convergence_limit. 
        (Units same as data z units). Alternatively, give limit in percentage 
        of rms deviation by appending %. [Default is scaled to  of the 
        root-mean-square deviation of the data from a best-fit (least-squares) plane.]. 
        This is the final convergence limit at the desired grid spacing; 
        for intermediate (coarser) grids the effective convergence limit 
        is divided by the grid spacing multiplier.
    max_radius: str
        Optional. After solving for the surface, apply a mask so that nodes farther than 
        max_radius away from a data constraint are set to NaN [no masking]. 
        Append a distance unit (see Units) if needed. One can also select the nodes to mask by 
        using the n_cells**c**\ form. Here n_cells means the number of cells around the node 
        controlled by a data point. As an example **0c**\ means that only the cell where the point 
        lies is filled, **1c**\ keeps one cell beyond that 
        (i.e. makes a 3x3 square neighborhood), and so on.
    limit: float 
        
    tension: float or str
        [**b**\|\ **i**]
        Optional. These must be between 0 and 1. 
        Tension may be used in the interior solution (above equation, 
        where it suppresses spurious oscillations) and in the boundary conditions 
        (where it tends to flatten the solution approaching the edges). 
        Add **i**\ tension to set interior tension, and **b**\ tension to set boundary tension.
        If you do not prepend **i**\ or **b**\, both will be set to the same value.
        [Default = 0 for both gives minimum curvature solution.]
    

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
